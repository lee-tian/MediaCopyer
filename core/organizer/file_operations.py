"""
File copy and move operations
"""

import shutil
from pathlib import Path
from typing import Callable, Optional

from .hash_utils import verify_file_integrity


def safe_copy(source_path: Path, target_path: Path, 
              verify_integrity: bool = True,
              progress_callback: Optional[Callable] = None) -> bool:
    """Safely copy file with optional integrity verification"""
    try:
        # Create target directory if it doesn't exist
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Copy file
        shutil.copy2(source_path, target_path)
        
        # Verify integrity if requested
        if verify_integrity:
            if not verify_file_integrity(source_path, target_path):
                # Clean up failed copy
                try:
                    target_path.unlink()
                except Exception:
                    pass
                return False
        
        if progress_callback:
            progress_callback(source_path, target_path)
        
        return True
        
    except Exception as e:
        # Clean up partial copy on error
        try:
            if target_path.exists():
                target_path.unlink()
        except Exception:
            pass
        return False


def safe_move(source_path: Path, target_path: Path,
              verify_integrity: bool = True,
              progress_callback: Optional[Callable] = None) -> bool:
    """Safely move file with optional integrity verification"""
    try:
        # First try to copy
        if safe_copy(source_path, target_path, verify_integrity, progress_callback):
            # If copy succeeded, remove original
            source_path.unlink()
            return True
        return False
    except Exception:
        return False


def handle_duplicate(source_path: Path, target_path: Path, duplicate_action: str) -> Optional[Path]:
    """Handle duplicate files based on action"""
    if not target_path.exists():
        return target_path
    
    if duplicate_action == 'skip':
        return None
    elif duplicate_action == 'overwrite':
        return target_path
    elif duplicate_action == 'rename':
        # Generate unique filename
        counter = 1
        stem = target_path.stem
        suffix = target_path.suffix
        parent = target_path.parent
        
        while True:
            new_name = f"{stem}_{counter:03d}{suffix}"
            new_path = parent / new_name
            if not new_path.exists():
                return new_path
            counter += 1
    
    return target_path
