"""
Core device detection functionality for MediaCopyer
"""

import subprocess
import json
from pathlib import Path
from typing import Optional

try:
    from PIL import Image
    from PIL.ExifTags import TAGS
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


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
                
                # If no make found, try to identify from model
                if model and not make:
                    model_lower = model.lower()
                    if any(x in model_lower for x in ['a7', 'a9', 'fx', 'rx', 'zv', 'alpha', 'cybershot']):
                        return 'Sony'
                        
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
    elif filename.startswith('DSC'):
        # Sony cameras commonly use DSC prefix
        return 'Sony'
    elif 'PANO' in filename:
        # Could be DJI panorama
        return 'DJI'
    # Sony camera filename patterns
    elif any(filename.startswith(prefix) for prefix in ['_DSC', 'SONY', 'ILCE', 'ILCA', 'FX', 'RX']):
        return 'Sony'
    # More Sony video patterns
    elif any(pattern in filename for pattern in ['C0001', 'C0002', 'C0003', 'C0004', 'C0005']):
        # Sony video files often have C#### pattern
        return 'Sony'
    elif filename.startswith('IMG'):
        # IMG is too generic, keep as unknown for now
        pass
    
    return "Unknown"
