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


def _should_skip_file(filename: str) -> bool:
    """Check if a file should be skipped (system files, hidden files, etc.)"""
    # Skip hidden files (starting with .)
    if filename.startswith('.'):
        return True
    
    # Skip macOS resource fork files (starting with ._)
    if filename.startswith('._'):
        return True
    
    # Skip other common system files
    system_files = {
        'Thumbs.db',      # Windows thumbnails
        'Desktop.ini',    # Windows folder settings
        '.DS_Store',      # macOS folder settings
        '__MACOSX',       # macOS archive metadata
        'desktop.ini',    # Windows (case variation)
    }
    
    if filename in system_files:
        return True
    
    return False


def _cleanup_empty_directories(base_path: Path) -> int:
    """Remove empty directories recursively, returns count of removed directories"""
    removed_count = 0
    
    try:
        # Walk through directories bottom-up to handle nested empty directories
        for root, dirs, files in os.walk(base_path, topdown=False):
            root_path = Path(root)
            
            # Skip the base directory itself
            if root_path == base_path:
                continue
                
            try:
                # Check if directory is empty (no files and no subdirectories)
                if not files and not dirs:
                    root_path.rmdir()
                    removed_count += 1
                    # Import here to avoid circular imports
                    try:
                        from gui.i18n import _
                        print(_("removed_empty_directory").format(root_path))
                    except ImportError:
                        print(f"Removed empty directory: {root_path}")
            except OSError:
                # Directory not empty or permission error, skip
                pass
                
    except Exception as e:
        try:
            from gui.i18n import _
            print(_("warning_empty_dir_cleanup").format(e))
        except ImportError:
            print(f"Warning: Error during empty directory cleanup: {e}")
    
    return removed_count


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
            # Skip system files and hidden files
            if _should_skip_file(file):
                continue
                
            file_path = Path(root) / file
            file_type = get_file_type(str(file_path))
            
            if file_type:
                media_files.append((file_path, file_type))
    
    return media_files


def scan_all_files(source_dir: Path) -> List[Tuple[Path, str]]:
    """Recursively scan directory for all files (for extension-based organization)"""
    all_files = []
    
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            file_path = Path(root) / file
            # Skip hidden files and system files
            if not _should_skip_file(file):
                file_type = get_file_type(str(file_path))
                # For extension mode, we still track if it's a known media type
                # but include all files
                if not file_type:
                    file_type = 'other'  # Mark as other file type
                all_files.append((file_path, file_type))
    
    return all_files


def is_duplicate_file(source_path: Path, target_path: Path) -> bool:
    """Check if source file is a duplicate of target file by comparing MD5 hashes"""
    if not target_path.exists():
        return False
    
    try:
        # Compare file sizes first (quick check)
        if source_path.stat().st_size != target_path.stat().st_size:
            return False
        
        # Compare MD5 hashes
        source_md5 = calculate_md5(source_path)
        target_md5 = calculate_md5(target_path)
        return source_md5 == target_md5
    except Exception:
        return False


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
                        file_date: datetime, organization_mode: str = "date", 
                        is_duplicate: bool = False) -> Path:
    """Determine target directory structure based on organization mode"""
    year = file_date.strftime('%Y')
    date_str = file_date.strftime('%Y-%m-%d')
    
    if organization_mode == "extension":
        # Mode 4: Extension-based organization
        extension = file_path.suffix.lower()
        if not extension:
            extension = 'no_extension'
        else:
            extension = extension[1:]  # Remove the dot
        target_dir = dest_path / extension.upper()
    else:
        # For other modes, determine base type directory
        if file_type == 'photo':
            base_dir = dest_path / 'Picture'
        elif file_type == 'video':
            base_dir = dest_path / 'Video'
        else:  # other file type
            base_dir = dest_path / 'Other'
        
        if organization_mode == "date":
            # Mode 1: Video/2025-07-25
            target_dir = base_dir / date_str
        elif organization_mode == "device":
            # Mode 2: Video/DJI
            device_name = get_device_name(str(file_path), file_type)
            target_dir = base_dir / device_name
        elif organization_mode == "date_device":
            # Mode 3: Video/2025-07-25/DJI
            device_name = get_device_name(str(file_path), file_type)
            target_dir = base_dir / date_str / device_name
        else:
            # Default to date mode if unknown mode
            target_dir = base_dir / date_str
    
    # If this is a duplicate file, move it to duplicate folder
    if is_duplicate:
        # Create duplicate folder structure: Picture/duplicate, Video/duplicate
        if file_type == 'photo':
            duplicate_base = dest_path / 'Picture' / 'duplicate'
        elif file_type == 'video':
            duplicate_base = dest_path / 'Video' / 'duplicate'
        else:
            duplicate_base = dest_path / 'Other' / 'duplicate'
        
        # Keep the same sub-organization within duplicate folder
        if organization_mode == "extension":
            extension = file_path.suffix.lower()
            if not extension:
                extension = 'no_extension'
            else:
                extension = extension[1:]  # Remove the dot
            target_dir = duplicate_base / extension.upper()
        elif organization_mode == "date":
            target_dir = duplicate_base / date_str
        elif organization_mode == "device":
            device_name = get_device_name(str(file_path), file_type)
            target_dir = duplicate_base / device_name
        elif organization_mode == "date_device":
            device_name = get_device_name(str(file_path), file_type)
            target_dir = duplicate_base / date_str / device_name
        else:
            target_dir = duplicate_base / date_str
    
    return target_dir


def organize_file(file_path: Path, file_type: str, dest_path: Path, 
                 move_mode: bool = False, dry_run: bool = False, 
                 organization_mode: str = "date", verify_md5: bool = False,
                 ignore_duplicates: bool = False) -> dict:
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
        ignore_duplicates: Whether to skip duplicate files instead of organizing them
    
    Returns:
        dict: Result with 'success', 'message', 'target_path', 'device_name' (if applicable), 'is_duplicate'
    """
    try:
        # Get file creation date
        file_date = get_file_date(str(file_path), file_type)
        
        # First, check if this file already exists in the normal location
        normal_target_dir = get_target_directory(dest_path, file_path, file_type, file_date, organization_mode, is_duplicate=False)
        normal_target_path = normal_target_dir / file_path.name
        
        is_duplicate = False
        if normal_target_path.exists() and is_duplicate_file(file_path, normal_target_path):
            is_duplicate = True
            
            # If ignore_duplicates is enabled, skip this file
            if ignore_duplicates:
                return {
                    'success': True,
                    'message': f"Skipped duplicate file: {file_path.name}",
                    'target_path': None,
                    'device_name': None,
                    'operation': "skipped (duplicate)",
                    'is_duplicate': True
                }
        
        # Create target directory structure (normal or duplicate)
        target_dir = get_target_directory(dest_path, file_path, file_type, file_date, organization_mode, is_duplicate=is_duplicate)
        
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
        operation_type = "duplicate " if is_duplicate else ""
        if not dry_run:
            if move_mode:
                shutil.move(str(file_path), str(target_path))
                operation = f"{operation_type}moved"
            else:
                shutil.copy2(str(file_path), str(target_path))
                operation = f"{operation_type}copied"
                
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
                            'operation': None,
                            'is_duplicate': is_duplicate
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
                        'operation': None,
                        'is_duplicate': is_duplicate
                    }
        else:
            operation = f"{operation_type}{'move' if move_mode else 'copy'} (dry run)"
            if verify_md5 and not move_mode:
                operation += " with MD5 verification"
        
        duplicate_message = " (duplicate detected)" if is_duplicate else ""
        return {
            'success': True,
            'message': f"Successfully {operation}: {file_path.name}{duplicate_message}",
            'target_path': target_path,
            'device_name': device_name,
            'operation': operation,
            'is_duplicate': is_duplicate
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f"Error processing {file_path}: {e}",
            'target_path': None,
            'device_name': None,
            'operation': None,
            'is_duplicate': False
        }


def organize_media_files(source_dir: Path, dest_dir: Path, move_mode: bool = False,
                        dry_run: bool = False, organization_mode: str = "date",
                        verify_md5: bool = False, ignore_duplicates: bool = False,
                        progress_callback=None) -> dict:
    """
    Organize all media files from source to destination directory.
    
    Args:
        source_dir: Source directory to scan
        dest_dir: Destination directory for organized files
        move_mode: Move files instead of copying
        dry_run: Preview mode, don't actually move/copy files
        organization_mode: Organization mode ('date', 'device', 'date_device', 'extension')
        verify_md5: Whether to verify file integrity using MD5 checksums
        ignore_duplicates: Whether to skip duplicate files instead of organizing them
        progress_callback: Callback function for progress updates
        
    Returns:
        dict: Statistics and results
    """
    # Scan for files based on organization mode
    if organization_mode == "extension":
        # For extension mode, scan all files
        files_to_process = scan_all_files(source_dir)
    else:
        # For other modes, scan only media files
        files_to_process = scan_directory(source_dir)
    
    if not files_to_process:
        return {
            'total_files': 0,
            'processed': 0,
            'photos': 0,
            'videos': 0,
            'other': 0,
            'errors': 0,
            'devices': set(),
            'results': []
        }
    
    stats = {
        'total_files': len(files_to_process),
        'processed': 0,
        'photos': 0,
        'videos': 0,
        'other': 0,
        'duplicates': 0,
        'skipped': 0,
        'errors': 0,
        'devices': set(),
        'results': []
    }
    
    for i, (file_path, file_type) in enumerate(files_to_process):
        # Update progress if callback provided
        if progress_callback:
            # Check if callback returns False (cancel requested)
            if progress_callback(i + 1, len(files_to_process), file_path.name) is False:
                # Cancel requested, break out of loop
                break
        
        # Organize the file
        result = organize_file(file_path, file_type, dest_dir, move_mode, dry_run, organization_mode, verify_md5, ignore_duplicates)
        stats['results'].append(result)
        
        # Update statistics
        if result['success']:
            # Check if file was skipped due to ignore_duplicates
            if result.get('operation') == "skipped (duplicate)":
                stats['skipped'] += 1
                stats['duplicates'] += 1
            else:
                stats['processed'] += 1
                if file_type == 'photo':
                    stats['photos'] += 1
                elif file_type == 'video':
                    stats['videos'] += 1
                else:
                    stats['other'] += 1
                
                # Track duplicates that were still processed (moved to duplicate folder)
                if result.get('is_duplicate', False):
                    stats['duplicates'] += 1
                
                if result['device_name']:
                    stats['devices'].add(result['device_name'])
        else:
            stats['errors'] += 1
    
    # Clean up empty directories after processing (only if not dry run)
    if not dry_run and stats['processed'] > 0:
        removed_dirs = _cleanup_empty_directories(dest_dir)
        if removed_dirs > 0:
            try:
                from gui.i18n import _
                print(_("cleaned_up_empty_directories").format(removed_dirs))
            except ImportError:
                print(f"Cleaned up {removed_dirs} empty directories")
    
    return stats
