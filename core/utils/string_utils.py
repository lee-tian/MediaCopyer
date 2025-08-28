"""
String and filename related utility functions
"""

import os
from datetime import datetime


def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"

    size_names = ["B", "KB", "MB", "GB", "TB"]
    size_index = 0
    size = float(size_bytes)

    while size >= 1024 and size_index < len(size_names) - 1:
        size /= 1024
        size_index += 1

    if size_index == 0:
        return f"{int(size)} {size_names[size_index]}"
    else:
        return f"{size:.1f} {size_names[size_index]}"


def safe_filename(filename: str, replacement: str = '_') -> str:
    """
    Make a filename safe for the current operating system

    Args:
        filename: Original filename
        replacement: Character to replace invalid characters with

    Returns:
        Safe filename
    """
    # Characters that are invalid on Windows/macOS/Linux
    invalid_chars = '<>:"/\\|?*'

    # Replace invalid characters
    safe_name = filename
    for char in invalid_chars:
        safe_name = safe_name.replace(char, replacement)

    # Remove leading/trailing spaces and dots
    safe_name = safe_name.strip(' .')

    # Ensure filename isn't empty
    if not safe_name:
        safe_name = 'untitled'

    # Limit length to avoid filesystem issues
    if len(safe_name) > 255:
        name, ext = os.path.splitext(safe_name)
        max_name_len = 255 - len(ext)
        safe_name = name[:max_name_len] + ext

    return safe_name


def format_date_path(file_date: datetime) -> str:
    """
    Format a date into a directory path structure (YYYY/MM/DD format)
    
    Args:
        file_date: datetime object to format
        
    Returns:
        String path in format "YYYY/MM/DD"
    """
    return f"{file_date.year:04d}/{file_date.month:02d}/{file_date.day:02d}"


def sanitize_filename(filename: str, replacement: str = '_') -> str:
    """
    Alias for safe_filename for backward compatibility
    
    Args:
        filename: Original filename
        replacement: Character to replace invalid characters with
        
    Returns:
        Safe filename
    """
    return safe_filename(filename, replacement)
