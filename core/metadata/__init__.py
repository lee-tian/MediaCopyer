"""
Core metadata extraction functionality for MediaCopyer
"""

import os
import subprocess
import json
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    from PIL import Image
    from PIL.ExifTags import TAGS
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


# File extension constants
PHOTO_EXTENSIONS = {
    # Standard image formats
    '.jpg', '.jpeg', '.png', '.tiff', '.tif', '.heic', '.heif', '.gif', '.bmp', '.webp',
    
    # Canon RAW formats
    '.cr2', '.cr3', '.crw',
    
    # Nikon RAW formats
    '.nef', '.nrw',
    
    # Sony RAW formats
    '.arw', '.srf', '.sr2',
    
    # Fuji RAW formats
    '.raf',
    
    # Leica RAW formats
    '.dng', '.rwl', '.raw',
    
    # Olympus RAW formats
    '.orf',
    
    # Panasonic RAW formats
    '.rw2', '.raw',
    
    # Pentax RAW formats
    '.pef', '.ptx',
    
    # Sigma RAW formats
    '.x3f',
    
    # Hasselblad RAW formats
    '.3fr', '.fff',
    
    # Phase One RAW formats
    '.iiq',
    
    # Mamiya RAW formats
    '.mef',
    
    # Kodak RAW formats
    '.dcr', '.kdc',
    
    # Minolta RAW formats
    '.mrw',
    
    # Casio RAW formats
    '.bay',
    
    # Epson RAW formats
    '.erf'
}

VIDEO_EXTENSIONS = {'.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv', '.webm', '.m4v', '.mpg', '.mpeg', '.3gp', '.mts', '.m2ts'}


def get_creation_date_from_exif(file_path: str) -> Optional[datetime]:
    """Extract creation date from image EXIF data"""
    if not PIL_AVAILABLE:
        return None
    
    try:
        with Image.open(file_path) as image:
            exif_data = image._getexif()
            if exif_data:
                for tag, value in exif_data.items():
                    tag_name = TAGS.get(tag, tag)
                    if tag_name == 'DateTimeOriginal' or tag_name == 'DateTime':
                        return datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
    except Exception as e:
        print(f"Warning: Could not read EXIF from {file_path}: {e}")
    
    return None


def get_creation_date_from_video(file_path: str) -> Optional[datetime]:
    """Extract creation date from video metadata using ffprobe"""
    try:
        # Use ffprobe to get metadata
        cmd = [
            'ffprobe', '-v', 'quiet', '-print_format', 'json',
            '-show_format', '-show_streams', file_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            return None
            
        metadata = json.loads(result.stdout)
        
        # Check format tags first
        if 'format' in metadata and 'tags' in metadata['format']:
            tags = metadata['format']['tags']
            
            # Try different tag names
            for date_tag in ['creation_time', 'date', 'DATE', 'com.apple.quicktime.creationdate']:
                if date_tag in tags:
                    date_str = tags[date_tag]
                    try:
                        # Handle different date formats
                        if 'T' in date_str:
                            # ISO format
                            return datetime.fromisoformat(date_str.replace('Z', '+00:00')).replace(tzinfo=None)
                        else:
                            # Try other formats
                            return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                    except ValueError:
                        continue
        
        # Check stream tags
        if 'streams' in metadata:
            for stream in metadata['streams']:
                if 'tags' in stream:
                    tags = stream['tags']
                    for date_tag in ['creation_time', 'date', 'DATE']:
                        if date_tag in tags:
                            date_str = tags[date_tag]
                            try:
                                if 'T' in date_str:
                                    return datetime.fromisoformat(date_str.replace('Z', '+00:00')).replace(tzinfo=None)
                                else:
                                    return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                            except ValueError:
                                continue
                                
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, json.JSONDecodeError, FileNotFoundError):
        pass
    
    return None


def get_file_date(file_path: str, file_type: str) -> datetime:
    """Get the creation date of a file, trying metadata first, then file mtime"""
    
    if file_type == 'photo':
        # Try EXIF first for photos
        date = get_creation_date_from_exif(file_path)
        if date:
            return date
    elif file_type == 'video':
        # Try video metadata first
        date = get_creation_date_from_video(file_path)
        if date:
            return date
    
    # Fallback to file modification time
    mtime = os.path.getmtime(file_path)
    return datetime.fromtimestamp(mtime)


def get_file_type(file_path: str) -> Optional[str]:
    """Determine if file is a photo or video based on extension"""
    ext = Path(file_path).suffix.lower()
    
    if ext in PHOTO_EXTENSIONS:
        return 'photo'
    elif ext in VIDEO_EXTENSIONS:
        return 'video'
    
    return None


def is_pil_available() -> bool:
    """Check if PIL/Pillow is available"""
    return PIL_AVAILABLE


def check_ffprobe_available() -> bool:
    """Check if ffprobe is available"""
    try:
        subprocess.run(['ffprobe', '-version'], capture_output=True, check=True)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False
