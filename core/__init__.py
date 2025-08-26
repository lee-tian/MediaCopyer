"""
MediaCopyer Core Library

A modular media file organization system that can organize photos and videos
by date or device type with support for metadata extraction.
"""

# Import key functions from each module for easy access
from .metadata import get_file_type, get_file_date, get_creation_date_from_exif, get_creation_date_from_video
from .device import get_device_name, get_device_from_exif, get_device_from_video, get_device_from_filename
from .organizer import (
    scan_directory, 
    generate_unique_filename, 
    get_target_directory,
    organize_file, 
    organize_media_files
)
from .utils import (
    validate_directory,
    format_file_size,
    get_directory_size,
    check_available_space,
    is_hidden_file,
    safe_filename,
    count_files_in_directory,
    ensure_directory_exists,
    get_relative_path
)

# Version info
__version__ = "2.0.0"
__author__ = "MediaCopyer"
__description__ = "Modular media file organization system"

# Supported file extensions (from metadata module)
PHOTO_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.webp', '.heic', '.heif', '.raw', '.cr2', '.nef', '.arw', '.dng'}
VIDEO_EXTENSIONS = {'.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv', '.webm', '.m4v', '.mpg', '.mpeg', '.3gp', '.mts', '.m2ts'}

# Export main interface functions
__all__ = [
    # Metadata functions
    'get_file_type',
    'get_file_date', 
    'get_creation_date_from_exif',
    'get_creation_date_from_video',
    
    # Device detection functions
    'get_device_name',
    'get_device_from_exif',
    'get_device_from_video', 
    'get_device_from_filename',
    
    # Organization functions
    'scan_directory',
    'generate_unique_filename',
    'get_target_directory', 
    'organize_file',
    'organize_media_files',
    
    # Utility functions
    'validate_directory',
    'format_file_size',
    'get_directory_size',
    'check_available_space',
    'is_hidden_file',
    'safe_filename',
    'count_files_in_directory',
    'ensure_directory_exists',
    'get_relative_path',
    
    # Constants
    'PHOTO_EXTENSIONS',
    'VIDEO_EXTENSIONS'
]
