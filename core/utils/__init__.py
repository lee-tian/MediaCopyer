"""
Core utilities package

This package provides utility functions for file operations, string handling,
and system checks for the MediaCopyer application.
"""

# Import filesystem utilities
from .filesystem import (
    validate_directory,
    get_directory_size,
    check_available_space,
    is_hidden_file,
    count_files_in_directory,
    ensure_directory_exists,
    get_relative_path,
    create_directory_structure
)

# Import string utilities
from .string_utils import (
    format_file_size,
    safe_filename
)

# System and dependency checks
import sys


def check_dependencies() -> dict:
    """
    Check if required dependencies are available
    
    Returns:
        Dictionary with dependency status
    """
    dependencies = {
        'PIL': False,
        'exifread': False,
        'python_version': False
    }
    
    # Check Python version
    if sys.version_info >= (3, 7):
        dependencies['python_version'] = True
    
    # Check PIL/Pillow
    try:
        from PIL import Image
        dependencies['PIL'] = True
    except ImportError:
        pass
    
    # Check exifread
    try:
        import exifread
        dependencies['exifread'] = True
    except ImportError:
        pass
    
    return dependencies


# Make all functions available at package level
__all__ = [
    # Filesystem utilities
    'validate_directory',
    'get_directory_size', 
    'check_available_space',
    'is_hidden_file',
    'count_files_in_directory',
    'ensure_directory_exists',
    'get_relative_path',
    'create_directory_structure',
    # String utilities
    'format_file_size',
    'safe_filename',
    # System checks
    'check_dependencies'
]
