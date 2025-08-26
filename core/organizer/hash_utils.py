"""
File hash calculation and verification utilities
"""

import hashlib
from pathlib import Path


def calculate_md5(file_path: Path) -> str:
    """Calculate MD5 hash of a file"""
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        raise Exception(f"Failed to calculate MD5 for {file_path}: {e}")


def verify_file_integrity(source_path: Path, target_path: Path) -> bool:
    """Verify file integrity by comparing MD5 hashes"""
    try:
        source_md5 = calculate_md5(source_path)
        target_md5 = calculate_md5(target_path)
        return source_md5 == target_md5
    except Exception:
        return False
