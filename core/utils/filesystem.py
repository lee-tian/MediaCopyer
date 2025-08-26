"""
File system related utility functions
"""

import os
from pathlib import Path
from typing import Optional


def validate_directory(path: str, must_exist: bool = False) -> bool:
    """Validate if a path is a valid directory"""
    try:
        path_obj = Path(path)

        if must_exist:
            return path_obj.exists() and path_obj.is_dir()
        else:
            # Check if path is valid and can be created
            if path_obj.exists():
                return path_obj.is_dir()
            else:
                # Try to create parent directories to test validity
                try:
                    path_obj.mkdir(parents=True, exist_ok=True)
                    return True
                except (OSError, PermissionError):
                    return False
    except (OSError, ValueError):
        return False


def get_directory_size(directory: Path) -> int:
    """Calculate total size of a directory in bytes"""
    total_size = 0

    try:
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    total_size += os.path.getsize(filepath)
                except (OSError, FileNotFoundError):
                    pass  # Skip files that can't be accessed
    except (OSError, PermissionError):
        pass

    return total_size


def check_available_space(directory: Path, required_bytes: int = 0) -> tuple[bool, int]:
    """
    Check if there's enough available space in the target directory

    Returns:
        tuple: (has_enough_space, available_bytes)
    """
    try:
        stat = os.statvfs(directory)
        available_bytes = stat.f_bavail * stat.f_frsize
        has_enough = available_bytes >= required_bytes
        return has_enough, available_bytes
    except (OSError, AttributeError):
        # On Windows or if statvfs is not available
        try:
            import shutil
            total, used, free = shutil.disk_usage(directory)
            has_enough = free >= required_bytes
            return has_enough, free
        except (OSError, ImportError):
            # Fallback - assume there's space
            return True, 0


def is_hidden_file(file_path: Path) -> bool:
    """Check if a file or directory is hidden"""
    name = file_path.name

    # Files starting with . are hidden on Unix systems
    if name.startswith('.'):
        return True

    # On Windows, check for hidden attribute
    if os.name == 'nt':
        try:
            import stat
            attrs = os.stat(file_path).st_file_attributes
            return attrs & stat.FILE_ATTRIBUTE_HIDDEN
        except (ImportError, OSError, AttributeError):
            pass

    return False


def count_files_in_directory(directory: Path, extensions: set = None) -> int:
    """
    Count files in a directory, optionally filtered by extensions

    Args:
        directory: Directory to count files in
        extensions: Set of file extensions to count (e.g., {'.jpg', '.png'})

    Returns:
        Number of files found
    """
    count = 0

    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if extensions:
                    file_ext = Path(file).suffix.lower()
                    if file_ext in extensions:
                        count += 1
                else:
                    count += 1
    except (OSError, PermissionError):
        pass

    return count


def ensure_directory_exists(directory: Path) -> bool:
    """
    Ensure a directory exists, creating it if necessary

    Returns:
        True if directory exists or was created successfully
    """
    try:
        directory.mkdir(parents=True, exist_ok=True)
        return True
    except (OSError, PermissionError):
        return False


def get_relative_path(file_path: Path, base_path: Path) -> Optional[Path]:
    """
    Get relative path from base_path to file_path

    Returns:
        Relative path or None if not possible
    """
    try:
        return file_path.relative_to(base_path)
    except ValueError:
        # file_path is not relative to base_path
        return None


def create_directory_structure(base_path: Path, structure: dict) -> bool:
    """
    Create a directory structure based on a nested dictionary

    Args:
        base_path: Base directory to create structure in
        structure: Dictionary describing directory structure

    Returns:
        True if successful, False otherwise
    """
    try:
        for name, subdirs in structure.items():
            dir_path = base_path / name
            if not ensure_directory_exists(dir_path):
                return False

            if isinstance(subdirs, dict):
                if not create_directory_structure(dir_path, subdirs):
                    return False

        return True
    except Exception:
        return False
