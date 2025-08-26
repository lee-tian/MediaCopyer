"""
Core file organization functionality for MediaCopyer
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Optional

from ..metadata import get_file_type, get_file_date
from ..device import get_device_name


def scan_directory(source_dir: Path) -> List[Tuple[Path, str]]:
    """Recursively scan directory for media files"""
    media_files = []
    
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            file_path = Path(root) / file
            file_type = get_file_type(str(file_path))
            
            if file_type:
                media_files.append((file_path, file_type))
    
    return media_files


def generate_unique_filename(target_path: Path) -> Path:
    """Generate a unique filename if file already exists"""
    if not target_path.exists():
        return target_path
    
    base_name = target_path.stem
    extension = target_path.suffix
    parent = target_path.parent
    
    counter = 1
    while True:
        new_name = f"{base_name}_{counter}{extension}"
        new_path = parent / new_name
        if not new_path.exists():
            return new_path
        counter += 1


def get_target_directory(dest_path: Path, file_path: Path, file_type: str, 
                        file_date: datetime, by_device: bool = False) -> Path:
    """Determine target directory structure based on organization mode"""
    year = file_date.strftime('%Y')
    
    if by_device:
        # Get device name for organization
        device_name = get_device_name(str(file_path), file_type)
        # Organize by device: /Movies/2025/DJI or /Movies/2025/Sony
        target_dir = dest_path / year / device_name
    else:
        # Original organization by type and date
        date_str = file_date.strftime('%Y-%m-%d')
        
        if file_type == 'photo':
            target_dir = dest_path / 'Picture' / year / date_str
        else:  # video
            target_dir = dest_path / 'Video' / year / date_str
    
    return target_dir


def organize_file(file_path: Path, file_type: str, dest_path: Path, 
                 move_mode: bool = False, dry_run: bool = False, 
                 by_device: bool = False) -> dict:
    """
    Organize a single media file.
    
    Returns:
        dict: Result with 'success', 'message', 'target_path', 'device_name' (if applicable)
    """
    try:
        # Get file creation date
        file_date = get_file_date(str(file_path), file_type)
        
        # Create target directory structure
        target_dir = get_target_directory(dest_path, file_path, file_type, file_date, by_device)
        
        # Get device name if organizing by device
        device_name = None
        if by_device:
            device_name = get_device_name(str(file_path), file_type)
        
        # Create target directory if it doesn't exist
        if not dry_run:
            target_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate unique target filename
        target_path = target_dir / file_path.name
        if not dry_run:
            target_path = generate_unique_filename(target_path)
        
        # Perform the file operation
        if not dry_run:
            if move_mode:
                shutil.move(str(file_path), str(target_path))
                operation = "moved"
            else:
                shutil.copy2(str(file_path), str(target_path))
                operation = "copied"
        else:
            operation = f"{'move' if move_mode else 'copy'} (dry run)"
        
        return {
            'success': True,
            'message': f"Successfully {operation}: {file_path.name}",
            'target_path': target_path,
            'device_name': device_name,
            'operation': operation
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f"Error processing {file_path}: {e}",
            'target_path': None,
            'device_name': None,
            'operation': None
        }


def organize_media_files(source_dir: Path, dest_dir: Path, move_mode: bool = False,
                        dry_run: bool = False, by_device: bool = False,
                        progress_callback=None) -> dict:
    """
    Organize all media files from source to destination directory.
    
    Args:
        source_dir: Source directory to scan
        dest_dir: Destination directory for organized files
        move_mode: Move files instead of copying
        dry_run: Preview mode, don't actually move/copy files
        by_device: Organize by device instead of by type/date
        progress_callback: Callback function for progress updates
        
    Returns:
        dict: Statistics and results
    """
    # Scan for media files
    media_files = scan_directory(source_dir)
    
    if not media_files:
        return {
            'total_files': 0,
            'processed': 0,
            'photos': 0,
            'videos': 0,
            'errors': 0,
            'devices': set(),
            'results': []
        }
    
    stats = {
        'total_files': len(media_files),
        'processed': 0,
        'photos': 0,
        'videos': 0,
        'errors': 0,
        'devices': set(),
        'results': []
    }
    
    for i, (file_path, file_type) in enumerate(media_files):
        # Update progress if callback provided
        if progress_callback:
            progress_callback(i + 1, len(media_files), file_path.name)
        
        # Organize the file
        result = organize_file(file_path, file_type, dest_dir, move_mode, dry_run, by_device)
        stats['results'].append(result)
        
        # Update statistics
        if result['success']:
            stats['processed'] += 1
            if file_type == 'photo':
                stats['photos'] += 1
            else:
                stats['videos'] += 1
            
            if result['device_name']:
                stats['devices'].add(result['device_name'])
        else:
            stats['errors'] += 1
    
    return stats
