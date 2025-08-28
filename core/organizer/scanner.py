"""
Directory scanning functionality
"""

import os
from pathlib import Path
from typing import List, Tuple

from ..metadata import get_file_type


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


def scan_all_files(source_dir: Path) -> List[Tuple[Path, str]]:
    """Recursively scan directory for all files (for extension-based organization)"""
    all_files = []
    
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            file_path = Path(root) / file
            # For extension-based organization, we use the extension as the type
            extension = file_path.suffix.lower()
            if extension:  # Only include files with extensions
                all_files.append((file_path, extension))
    
    return all_files
