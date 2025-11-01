"""
File size calculation and statistics utilities
"""

import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from ..metadata import get_file_type


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


class DirectorySizeInfo:
    """Class to hold directory size information"""
    
    def __init__(self, path: Path):
        self.path = path
        self.total_files = 0
        self.total_size = 0
        self.media_files = 0
        self.media_size = 0
        self.photos = 0
        self.videos = 0
        self.other_files = 0
        self.photo_size = 0
        self.video_size = 0
        self.other_size = 0
        self.file_details = []  # List of (file_path, size, file_type)
    
    def add_file(self, file_path: Path, size: int, file_type: str = None):
        """Add a file to the statistics"""
        self.total_files += 1
        self.total_size += size
        
        if file_type is None:
            file_type = get_file_type(str(file_path))
        
        self.file_details.append((file_path, size, file_type))
        
        if file_type == 'photo':
            self.photos += 1
            self.photo_size += size
            self.media_files += 1
            self.media_size += size
        elif file_type == 'video':
            self.videos += 1
            self.video_size += size
            self.media_files += 1
            self.media_size += size
        else:
            self.other_files += 1
            self.other_size += size
    
    def get_summary(self) -> Dict:
        """Get summary statistics"""
        return {
            'path': str(self.path),
            'total_files': self.total_files,
            'total_size': self.total_size,
            'media_files': self.media_files,
            'media_size': self.media_size,
            'photos': self.photos,
            'videos': self.videos,
            'other_files': self.other_files,
            'photo_size': self.photo_size,
            'video_size': self.video_size,
            'other_size': self.other_size
        }


def calculate_directory_size_detailed(directory: Path, include_all_files: bool = False) -> DirectorySizeInfo:
    """
    Calculate detailed size information for a directory
    
    Args:
        directory: Directory to analyze
        include_all_files: If True, include all files; if False, only media files
    
    Returns:
        DirectorySizeInfo object with detailed statistics
    """
    size_info = DirectorySizeInfo(directory)
    
    try:
        for root, dirs, files in os.walk(directory):
            for filename in files:
                file_path = Path(root) / filename
                
                # Skip hidden files and system files
                if _should_skip_file(filename):
                    continue
                
                try:
                    file_size = file_path.stat().st_size
                    file_type = get_file_type(str(file_path))
                    
                    # If include_all_files is False, only count media files
                    if not include_all_files and not file_type:
                        continue
                    
                    size_info.add_file(file_path, file_size, file_type)
                    
                except (OSError, FileNotFoundError):
                    # Skip files that can't be accessed
                    continue
                    
    except (OSError, PermissionError):
        # Skip directories that can't be accessed
        pass
    
    return size_info


def calculate_multiple_directories_size(directories: List[Path], include_all_files: bool = False) -> List[DirectorySizeInfo]:
    """
    Calculate size information for multiple directories
    
    Args:
        directories: List of directories to analyze
        include_all_files: If True, include all files; if False, only media files
    
    Returns:
        List of DirectorySizeInfo objects
    """
    results = []
    
    for directory in directories:
        if directory.exists() and directory.is_dir():
            size_info = calculate_directory_size_detailed(directory, include_all_files)
            results.append(size_info)
    
    return results


def format_size_summary(size_info: DirectorySizeInfo) -> str:
    """
    Format size information into a readable string
    
    Args:
        size_info: DirectorySizeInfo object
    
    Returns:
        Formatted string with size information
    """
    from .string_utils import format_file_size
    
    summary = f"目录: {size_info.path}\n"
    summary += f"  总文件数: {size_info.total_files}\n"
    summary += f"  总大小: {format_file_size(size_info.total_size)}\n"
    
    if size_info.media_files > 0:
        summary += f"  媒体文件: {size_info.media_files} ({format_file_size(size_info.media_size)})\n"
        if size_info.photos > 0:
            summary += f"    照片: {size_info.photos} ({format_file_size(size_info.photo_size)})\n"
        if size_info.videos > 0:
            summary += f"    视频: {size_info.videos} ({format_file_size(size_info.video_size)})\n"
    
    if size_info.other_files > 0:
        summary += f"  其他文件: {size_info.other_files} ({format_file_size(size_info.other_size)})\n"
    
    return summary


def compare_directories_size(source_infos: List[DirectorySizeInfo], 
                           dest_infos: List[DirectorySizeInfo]) -> Dict:
    """
    Compare source and destination directory sizes
    
    Args:
        source_infos: List of source directory size information
        dest_infos: List of destination directory size information
    
    Returns:
        Dictionary with comparison results
    """
    from .string_utils import format_file_size
    
    # Calculate totals
    total_source_files = sum(info.total_files for info in source_infos)
    total_source_size = sum(info.total_size for info in source_infos)
    total_source_media = sum(info.media_files for info in source_infos)
    total_source_media_size = sum(info.media_size for info in source_infos)
    
    total_dest_files = sum(info.total_files for info in dest_infos)
    total_dest_size = sum(info.total_size for info in dest_infos)
    total_dest_media = sum(info.media_files for info in dest_infos)
    total_dest_media_size = sum(info.media_size for info in dest_infos)
    
    return {
        'source': {
            'directories': len(source_infos),
            'total_files': total_source_files,
            'total_size': total_source_size,
            'total_size_formatted': format_file_size(total_source_size),
            'media_files': total_source_media,
            'media_size': total_source_media_size,
            'media_size_formatted': format_file_size(total_source_media_size)
        },
        'destination': {
            'directories': len(dest_infos),
            'total_files': total_dest_files,
            'total_size': total_dest_size,
            'total_size_formatted': format_file_size(total_dest_size),
            'media_files': total_dest_media,
            'media_size': total_dest_media_size,
            'media_size_formatted': format_file_size(total_dest_media_size)
        },
        'difference': {
            'files': total_dest_files - total_source_files,
            'size': total_dest_size - total_source_size,
            'size_formatted': format_file_size(abs(total_dest_size - total_source_size)),
            'media_files': total_dest_media - total_source_media,
            'media_size': total_dest_media_size - total_source_media_size,
            'media_size_formatted': format_file_size(abs(total_dest_media_size - total_source_media_size))
        }
    }


def estimate_required_space(source_infos: List[DirectorySizeInfo], 
                          num_destinations: int, 
                          move_mode: bool = False) -> int:
    """
    Estimate required space for the operation
    
    Args:
        source_infos: List of source directory size information
        num_destinations: Number of destination directories
        move_mode: Whether files will be moved (not copied)
    
    Returns:
        Estimated required space in bytes
    """
    total_media_size = sum(info.media_size for info in source_infos)
    
    if move_mode:
        # For move operations, we only need space for one copy
        return total_media_size
    else:
        # For copy operations, we need space for each destination
        return total_media_size * num_destinations