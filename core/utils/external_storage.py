#!/usr/bin/env python3
"""
External storage device detection utilities for MediaCopyer
"""

import os
import platform
from pathlib import Path
from typing import List


def get_external_storage_devices() -> List[str]:
    """
    Detect all external storage devices (USB drives, SD cards, external HDDs, etc.)
    
    Returns:
        List of paths to external storage devices
    """
    external_devices = []
    system = platform.system()
    
    if system == 'Darwin':  # macOS
        external_devices = _get_macos_external_devices()
    elif system == 'Linux':
        external_devices = _get_linux_external_devices()
    elif system == 'Windows':
        external_devices = _get_windows_external_devices()
    
    # Filter out invalid or inaccessible paths
    valid_devices = []
    for device in external_devices:
        try:
            if os.path.exists(device) and os.path.isdir(device) and os.access(device, os.R_OK):
                valid_devices.append(device)
        except (OSError, PermissionError):
            continue
    
    return valid_devices


def _get_macos_external_devices() -> List[str]:
    """Get external storage devices on macOS"""
    devices = []
    volumes_path = Path('/Volumes')
    
    if not volumes_path.exists():
        return devices
    
    try:
        # List all volumes except Macintosh HD and system volumes
        for volume in volumes_path.iterdir():
            if not volume.is_dir():
                continue
            
            volume_name = volume.name
            
            # Skip system volumes
            if volume_name in ['Macintosh HD', 'Preboot', 'Recovery', 'VM', 'Update']:
                continue
            
            # Skip hidden volumes
            if volume_name.startswith('.'):
                continue
            
            # Add valid external volume
            devices.append(str(volume))
    
    except (OSError, PermissionError):
        pass
    
    return devices


def _get_linux_external_devices() -> List[str]:
    """Get external storage devices on Linux"""
    devices = []
    
    # Common mount points for external devices
    mount_points = [
        '/media',
        '/mnt',
        '/run/media'
    ]
    
    for mount_base in mount_points:
        mount_path = Path(mount_base)
        if not mount_path.exists():
            continue
        
        try:
            # For /media and /run/media, check user subdirectories
            if mount_base in ['/media', '/run/media']:
                for user_dir in mount_path.iterdir():
                    if user_dir.is_dir():
                        for device in user_dir.iterdir():
                            if device.is_dir() and not device.name.startswith('.'):
                                devices.append(str(device))
            else:
                # For /mnt, directly check subdirectories
                for device in mount_path.iterdir():
                    if device.is_dir() and not device.name.startswith('.'):
                        devices.append(str(device))
        
        except (OSError, PermissionError):
            continue
    
    return devices


def _get_windows_external_devices() -> List[str]:
    """Get external storage devices on Windows"""
    devices = []
    
    try:
        import string
        import ctypes
        
        # Get all drive letters
        drives = []
        bitmask = ctypes.windll.kernel32.GetLogicalDrives()
        for letter in string.ascii_uppercase:
            if bitmask & 1:
                drives.append(f"{letter}:")
            bitmask >>= 1
        
        # Check each drive to see if it's removable
        for drive in drives:
            drive_path = f"{drive}\\"
            try:
                drive_type = ctypes.windll.kernel32.GetDriveTypeW(drive_path)
                # DRIVE_REMOVABLE = 2, DRIVE_FIXED = 3 (we want removable)
                # But also include DRIVE_FIXED as it could be external HDD
                if drive_type in [2, 3]:
                    # Skip C: drive (usually system drive)
                    if drive.upper() != 'C:':
                        devices.append(drive_path)
            except Exception:
                continue
    
    except ImportError:
        # If ctypes is not available, just return empty list
        pass
    
    return devices


def is_external_storage(path: str) -> bool:
    """
    Check if a given path is on an external storage device
    
    Args:
        path: Path to check
        
    Returns:
        True if path is on external storage, False otherwise
    """
    if not path:
        return False
    
    external_devices = get_external_storage_devices()
    path_obj = Path(path).resolve()
    
    for device in external_devices:
        device_obj = Path(device).resolve()
        try:
            # Check if path is under this device
            path_obj.relative_to(device_obj)
            return True
        except ValueError:
            continue
    
    return False


def get_device_info(device_path: str) -> dict:
    """
    Get information about an external storage device
    
    Args:
        device_path: Path to the device
        
    Returns:
        Dictionary with device information (name, size, free space, etc.)
    """
    info = {
        'path': device_path,
        'name': Path(device_path).name,
        'exists': False,
        'readable': False,
        'total_size': 0,
        'free_space': 0,
        'used_space': 0
    }
    
    try:
        if os.path.exists(device_path):
            info['exists'] = True
            
            if os.access(device_path, os.R_OK):
                info['readable'] = True
            
            # Get disk usage statistics
            stat = os.statvfs(device_path) if hasattr(os, 'statvfs') else None
            if stat:
                info['total_size'] = stat.f_blocks * stat.f_frsize
                info['free_space'] = stat.f_bavail * stat.f_frsize
                info['used_space'] = info['total_size'] - info['free_space']
    
    except (OSError, PermissionError):
        pass
    
    return info
