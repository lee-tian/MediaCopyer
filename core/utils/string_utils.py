"""
String and filename related utility functions
"""

import os


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
