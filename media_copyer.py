#!/usr/bin/env python3
"""
Media Copyer - Organize media files by date into structured directories
"""

import os
import sys
import shutil
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple
import subprocess
import json

try:
    from PIL import Image
    from PIL.ExifTags import TAGS
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

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
    
    photo_extensions = {'.jpg', '.jpeg', '.arw', '.png', '.tiff', '.tif', '.heic', '.cr2', '.nef', '.dng'}
    video_extensions = {'.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv', '.webm', '.m4v'}
    
    if ext in photo_extensions:
        return 'photo'
    elif ext in video_extensions:
        return 'video'
    
    return None

def get_device_name(file_path: str, file_type: str) -> str:
    """Extract device name from file metadata or filename"""
    device_name = "Unknown"
    
    if file_type == 'photo':
        # Try to get camera make/model from EXIF
        device_name = get_device_from_exif(str(file_path))
    elif file_type == 'video':
        # Try to get device info from video metadata
        device_name = get_device_from_video(str(file_path))
    
    # If no device found from metadata, try filename patterns
    if device_name == "Unknown":
        device_name = get_device_from_filename(str(file_path))
    
    return device_name

def get_device_from_exif(file_path: str) -> str:
    """Extract camera make from EXIF data"""
    if not PIL_AVAILABLE:
        return "Unknown"
    
    try:
        with Image.open(file_path) as image:
            exif_data = image._getexif()
            if exif_data:
                make = None
                model = None
                
                for tag, value in exif_data.items():
                    tag_name = TAGS.get(tag, tag)
                    if tag_name == 'Make':
                        make = value.strip()
                    elif tag_name == 'Model':
                        model = value.strip()
                
                if make:
                    # Normalize common camera brands
                    make_lower = make.lower()
                    if 'canon' in make_lower:
                        return 'Canon'
                    elif 'nikon' in make_lower:
                        return 'Nikon'
                    elif 'sony' in make_lower:
                        return 'Sony'
                    elif 'fujifilm' in make_lower or 'fuji' in make_lower:
                        return 'Fujifilm'
                    elif 'olympus' in make_lower:
                        return 'Olympus'
                    elif 'panasonic' in make_lower:
                        return 'Panasonic'
                    elif 'leica' in make_lower:
                        return 'Leica'
                    elif 'apple' in make_lower:
                        return 'iPhone'
                    elif 'dji' in make_lower:
                        return 'DJI'
                    else:
                        return make
                        
    except Exception as e:
        pass
    
    return "Unknown"

def get_device_from_video(file_path: str) -> str:
    """Extract device info from video metadata"""
    try:
        cmd = [
            'ffprobe', '-v', 'quiet', '-print_format', 'json',
            '-show_format', '-show_streams', file_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            return "Unknown"
            
        metadata = json.loads(result.stdout)
        
        # Check format tags first
        if 'format' in metadata and 'tags' in metadata['format']:
            tags = metadata['format']['tags']
            
            # Look for device/camera info in various tag names
            device_tags = ['make', 'model', 'camera_make', 'camera_model', 'com.apple.quicktime.make', 'com.apple.quicktime.model']
            
            for tag in device_tags:
                if tag in tags:
                    device_info = tags[tag].strip()
                    device_lower = device_info.lower()
                    
                    if 'dji' in device_lower:
                        return 'DJI'
                    elif 'sony' in device_lower:
                        return 'Sony'
                    elif 'canon' in device_lower:
                        return 'Canon'
                    elif 'panasonic' in device_lower:
                        return 'Panasonic'
                    elif 'gopro' in device_lower:
                        return 'GoPro'
                    elif 'apple' in device_lower or 'iphone' in device_lower:
                        return 'iPhone'
                    elif device_info and device_info != "Unknown":
                        return device_info
        
        # Check stream tags
        if 'streams' in metadata:
            for stream in metadata['streams']:
                if 'tags' in stream:
                    tags = stream['tags']
                    for tag in ['handler_name', 'encoder']:
                        if tag in tags:
                            handler = tags[tag].lower()
                            if 'dji' in handler:
                                return 'DJI'
                            elif 'gopro' in handler:
                                return 'GoPro'
                                
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, json.JSONDecodeError, FileNotFoundError):
        pass
    
    return "Unknown"

def get_device_from_filename(file_path: str) -> str:
    """Try to determine device from filename patterns"""
    filename = Path(file_path).name.upper()
    
    # Common filename patterns
    if filename.startswith('DJI_'):
        return 'DJI'
    elif filename.startswith('GOPR') or filename.startswith('GP'):
        return 'GoPro'
    elif filename.startswith('DSC') or filename.startswith('IMG'):
        # These are common but not device-specific
        pass
    elif 'PANO' in filename:
        # Could be DJI panorama
        return 'DJI'
    
    return "Unknown"

def generate_unique_filename(target_path: Path) -> Path:
    """Generate a unique filename if file already exists"""
    if not target_path.exists():
        return target_path
    
    base_name = target_path.stem
    extension = target_path.suffix
    parent = target_path.parent
    
    counter = 1
    while True:
        new_name = f"{base_name}_{counter}{extension}"
        new_path = parent / new_name
        if not new_path.exists():
            return new_path
        counter += 1

def scan_directory(source_dir: Path) -> list:
    """Recursively scan directory for media files"""
    media_files = []
    
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            file_path = Path(root) / file
            file_type = get_file_type(str(file_path))
            
            if file_type:
                media_files.append((file_path, file_type))
    
    return media_files

def organize_files(source_dir: Path, dest_dir: Path, move_mode: bool = False, dry_run: bool = False, by_device: bool = False):
    """Main function to organize media files"""
    
    print(f"Scanning source directory: {source_dir}")
    media_files = scan_directory(source_dir)
    
    if not media_files:
        print("No media files found!")
        return
    
    print(f"Found {len(media_files)} media files")
    
    stats = {
        'photos': 0,
        'videos': 0,
        'errors': 0,
        'devices': set()
    }
    
    for file_path, file_type in media_files:
        try:
            # Get file creation date
            file_date = get_file_date(str(file_path), file_type)
            
            # Create target directory structure
            year = file_date.strftime('%Y')
            
            if by_device:
                # Get device name for organization
                device_name = get_device_name(str(file_path), file_type)
                stats['devices'].add(device_name)
                
                # Organize by device: /Movies/2025/DJI or /Movies/2025/Sony
                target_dir = dest_dir / year / device_name
                print(f"Device detected: {device_name} for {file_path.name}")
            else:
                # Original organization by type and date
                date_str = file_date.strftime('%Y-%m-%d')
                
                if file_type == 'photo':
                    target_dir = dest_dir / 'Picture' / year / date_str
                else:  # video
                    target_dir = dest_dir / 'Video' / year / date_str
            
            if file_type == 'photo':
                stats['photos'] += 1
            else:
                stats['videos'] += 1
            
            # Create target directory if it doesn't exist
            if not dry_run:
                target_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate unique target filename
            target_path = target_dir / file_path.name
            if not dry_run:
                target_path = generate_unique_filename(target_path)
            
            print(f"{file_path} -> {target_path}")
            
            if not dry_run:
                if move_mode:
                    shutil.move(str(file_path), str(target_path))
                    print(f"  Moved: {file_path.name}")
                else:
                    shutil.copy2(str(file_path), str(target_path))
                    print(f"  Copied: {file_path.name}")
            
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            stats['errors'] += 1
    
    # Print statistics
    print("\n" + "="*50)
    print("PROCESSING COMPLETE")
    print("="*50)
    print(f"Photos processed: {stats['photos']}")
    print(f"Videos processed: {stats['videos']}")
    print(f"Errors: {stats['errors']}")
    print(f"Total files: {stats['photos'] + stats['videos']}")
    
    if by_device:
        print(f"Devices detected: {', '.join(sorted(stats['devices']))}")
    
    if dry_run:
        print("\n(This was a dry run - no files were actually moved/copied)")

def main():
    parser = argparse.ArgumentParser(description='Organize media files by date into structured directories')
    parser.add_argument('source', help='Source directory containing media files')
    parser.add_argument('destination', help='Destination directory for organized files')
    parser.add_argument('--move', action='store_true', 
                       help='Move files instead of copying (default: copy)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be done without actually moving/copying files')
    parser.add_argument('--by-device', action='store_true',
                       help='Organize files by device (camera/drone) instead of type and date')
    
    args = parser.parse_args()
    
    source_dir = Path(args.source)
    dest_dir = Path(args.destination)
    
    # Validate source directory
    if not source_dir.exists():
        print(f"Error: Source directory '{source_dir}' does not exist!")
        sys.exit(1)
    
    if not source_dir.is_dir():
        print(f"Error: '{source_dir}' is not a directory!")
        sys.exit(1)
    
    # Create destination directory if it doesn't exist
    if not args.dry_run:
        dest_dir.mkdir(parents=True, exist_ok=True)
    
    print("Media Copyer - Organizing your media files")
    print("="*50)
    print(f"Source: {source_dir}")
    print(f"Destination: {dest_dir}")
    print(f"Mode: {'Move' if args.move else 'Copy'}")
    print(f"Organization: {'By Device' if args.by_device else 'By Type and Date'}")
    
    if not PIL_AVAILABLE:
        print("Warning: PIL not available, EXIF reading disabled")
    
    try:
        subprocess.run(['ffprobe', '-version'], capture_output=True, check=True)
    except (subprocess.SubprocessError, FileNotFoundError):
        print("Warning: ffprobe not available, video metadata reading disabled")
    
    print("="*50)
    
    organize_files(source_dir, dest_dir, args.move, args.dry_run, args.by_device)

if __name__ == "__main__":
    main()
