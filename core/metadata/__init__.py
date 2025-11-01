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

try:
    import exifread
    EXIFREAD_AVAILABLE = True
except ImportError:
    EXIFREAD_AVAILABLE = False


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


def get_creation_date_from_exiftool(file_path: str) -> Optional[datetime]:
    """Extract creation date using exiftool as fallback"""
    try:
        cmd = ['exiftool', '-DateTimeOriginal', '-DateTime', '-CreateDate', '-j', file_path]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            if data and len(data) > 0:
                file_data = data[0]
                
                # Try different date fields
                date_fields = ['DateTimeOriginal', 'DateTime', 'CreateDate']
                for field in date_fields:
                    if field in file_data:
                        date_str = file_data[field]
                        try:
                            return datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
                        except ValueError:
                            continue
                            
    except (subprocess.SubprocessError, json.JSONDecodeError, FileNotFoundError):
        pass
    
    return None


def get_creation_date_from_exif_raw(file_path: str) -> Optional[datetime]:
    """Extract creation date from RAW image files using exifread"""
    # Skip system files to avoid unnecessary warnings
    filename = Path(file_path).name
    if filename.startswith('._') or filename.startswith('.'):
        return None
        
    if not EXIFREAD_AVAILABLE:
        # Try exiftool as fallback if exifread not available
        return get_creation_date_from_exiftool(file_path)
    
    try:
        with open(file_path, 'rb') as f:
            # Process file without stopping early to get more tags
            tags = exifread.process_file(f, details=False)
            
            if not tags:
                # Only show warnings for actual image files, not system files
                if not filename.startswith('._'):
                    print(f"Warning: No EXIF tags found in {file_path} with exifread, trying exiftool...")
                return get_creation_date_from_exiftool(file_path)
            
            # Try different date tags in order of preference
            date_tags = [
                'EXIF DateTimeOriginal',
                'EXIF DateTime', 
                'Image DateTime',
                'EXIF DateTimeDigitized'
            ]
            
            for tag_name in date_tags:
                if tag_name in tags:
                    date_str = str(tags[tag_name]).strip()
                    try:
                        return datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
                    except ValueError as ve:
                        if not filename.startswith('._'):
                            print(f"Warning: Could not parse date '{date_str}' from tag {tag_name}: {ve}")
                        continue
            
            # If no date found with exifread, try exiftool
            if not filename.startswith('._'):
                print(f"No date found in EXIF tags with exifread, trying exiftool for {filename}")
            return get_creation_date_from_exiftool(file_path)
                        
    except Exception as e:
        # Only show warnings for actual image files, not system files
        if not filename.startswith('._'):
            print(f"Warning: Could not read EXIF from RAW file {file_path} with exifread: {e}")
            print(f"Trying exiftool as fallback...")
        return get_creation_date_from_exiftool(file_path)
    
    return None


def get_creation_date_from_exif(file_path: str) -> Optional[datetime]:
    """Extract creation date from image EXIF data"""
    # Skip system files to avoid unnecessary warnings
    filename = Path(file_path).name
    if filename.startswith('._') or filename.startswith('.'):
        return None
    
    # Check if this is a RAW file that PIL can't handle
    ext = Path(file_path).suffix.lower()
    raw_extensions = {'.arw', '.cr2', '.cr3', '.nef', '.nrw', '.raf', '.orf', '.rw2', '.pef', '.x3f', '.3fr', '.iiq', '.mef', '.dcr', '.mrw', '.bay', '.erf'}
    
    if ext in raw_extensions:
        # Use exifread for RAW files
        return get_creation_date_from_exif_raw(file_path)
    
    # Use PIL for standard formats
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
        # Only show warnings for actual image files, not system files
        if not filename.startswith('._'):
            print(f"Warning: PIL could not read EXIF from {file_path}: {e}")
            if EXIFREAD_AVAILABLE:
                print(f"Trying exifread as fallback for {file_path}")
                return get_creation_date_from_exif_raw(file_path)
    
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


def is_exifread_available() -> bool:
    """Check if exifread is available"""
    return EXIFREAD_AVAILABLE


def check_ffprobe_available() -> bool:
    """Check if ffprobe is available"""
    try:
        subprocess.run(['ffprobe', '-version'], capture_output=True, check=True)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False


def check_exiftool_available() -> bool:
    """Check if exiftool is available"""
    try:
        subprocess.run(['exiftool', '-ver'], capture_output=True, check=True)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False
