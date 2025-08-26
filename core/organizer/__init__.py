"""
Core file organization functionality for MediaCopyer
"""

import os
import shutil
import hashlib
from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Optional

from ..metadata import get_file_type, get_file_date
from ..device import get_device_name


def calculate_md5(file_path: Path) -> str:
    """Calculate MD5 hash of a file"""
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        raise Exception(f"Failed to calculate MD5 for {file_path}: {e}")


def verify_file_integrity(source_path: Path, target_path: Path) -> bool:
    """Verify file integrity by comparing MD5 hashes"""
    try:
        source_md5 = calculate_md5(source_path)
        target_md5 = calculate_md5(target_path)
        return source_md5 == target_md5
    except Exception:
        return False


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
                        file_date: datetime, organization_mode: str = "date") -> Path:
    """Determine target directory structure based on organization mode"""
    year = file_date.strftime('%Y')
    date_str = file_date.strftime('%Y-%m-%d')
    
    # Determine base type directory
    if file_type == 'photo':
        base_dir = dest_path / 'Picture'
    else:  # video
        base_dir = dest_path / 'Video'
    
    if organization_mode == "date":
        # Mode 1: Video/2025/2025-07-25
        target_dir = base_dir / year / date_str
    elif organization_mode == "device":
        # Mode 2: Video/2025/DJI
        device_name = get_device_name(str(file_path), file_type)
        target_dir = base_dir / year / device_name
    elif organization_mode == "date_device":
        # Mode 3: Video/2025/2025-07-25/DJI
        device_name = get_device_name(str(file_path), file_type)
        target_dir = base_dir / year / date_str / device_name
    else:
        # Default to date mode if unknown mode
        target_dir = base_dir / year / date_str
    
    return target_dir


def organize_file(file_path: Path, file_type: str, dest_path: Path, 
                 move_mode: bool = False, dry_run: bool = False, 
                 organization_mode: str = "date", verify_md5: bool = False) -> dict:
    """
    Organize a single media file.
    
    Args:
        file_path: Path to the source file
        file_type: Type of file ('photo' or 'video')
        dest_path: Destination base directory
        move_mode: Move files instead of copying
        dry_run: Preview mode, don't actually move/copy files
        organization_mode: Organization mode ('date', 'device', 'date_device')
        verify_md5: Whether to verify file integrity using MD5 checksums
    
    Returns:
        dict: Result with 'success', 'message', 'target_path', 'device_name' (if applicable)
    """
    try:
        # Get file creation date
        file_date = get_file_date(str(file_path), file_type)
        
        # Create target directory structure
        target_dir = get_target_directory(dest_path, file_path, file_type, file_date, organization_mode)
        
        # Get device name if organizing by device
        device_name = None
        if organization_mode in ["device", "date_device"]:
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
                
            # Verify MD5 if requested and not in move mode
            if verify_md5 and not move_mode:
                try:
                    if not verify_file_integrity(file_path, target_path):
                        # MD5 verification failed, remove the copied file
                        if target_path.exists():
                            target_path.unlink()
                        return {
                            'success': False,
                            'message': f"MD5 verification failed for {file_path.name}",
                            'target_path': None,
                            'device_name': device_name,
                            'operation': None
                        }
                    else:
                        operation += " (MD5 verified)"
                except Exception as e:
                    # MD5 verification error, remove the copied file
                    if target_path.exists():
                        target_path.unlink()
                    return {
                        'success': False,
                        'message': f"MD5 verification error for {file_path.name}: {e}",
                        'target_path': None,
                        'device_name': device_name,
                        'operation': None
                    }
        else:
            operation = f"{'move' if move_mode else 'copy'} (dry run)"
            if verify_md5 and not move_mode:
                operation += " with MD5 verification"
        
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
                        dry_run: bool = False, organization_mode: str = "date",
                        verify_md5: bool = False, progress_callback=None) -> dict:
    """
    Organize all media files from source to destination directory.
    
    Args:
        source_dir: Source directory to scan
        dest_dir: Destination directory for organized files
        move_mode: Move files instead of copying
        dry_run: Preview mode, don't actually move/copy files
        organization_mode: Organization mode ('date', 'device', 'date_device')
        verify_md5: Whether to verify file integrity using MD5 checksums
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
        result = organize_file(file_path, file_type, dest_dir, move_mode, dry_run, organization_mode, verify_md5)
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
