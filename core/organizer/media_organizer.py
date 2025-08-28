"""
Main media organizer class that coordinates all operations
"""

from pathlib import Path
from typing import Dict, List, Tuple, Callable, Optional
import logging

from .scanner import scan_directory, scan_all_files
from .file_operations import safe_copy, safe_move, handle_duplicate
from .hash_utils import verify_file_integrity
from ..metadata import get_file_date, get_file_type
from ..utils import format_date_path, sanitize_filename, ensure_directory_exists


class MediaOrganizer:
    """Main class for organizing media files"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def organize_files(self, source_dir: str, target_dir: str, 
                      organize_by: str = 'date', 
                      copy_mode: bool = True,
                      duplicate_action: str = 'skip',
                      verify_integrity: bool = True,
                      progress_callback: Optional[Callable] = None) -> Dict:
        """
        Organize media files from source to target directory
        
        Args:
            source_dir: Source directory path
            target_dir: Target directory path
            organize_by: Organization method ('date', 'type', etc.)
            copy_mode: True for copy, False for move
            duplicate_action: 'skip', 'overwrite', or 'rename'
            verify_integrity: Whether to verify file integrity
            progress_callback: Callback function for progress updates
        
        Returns:
            Dictionary with operation results
        """
        source_path = Path(source_dir)
        target_path = Path(target_dir)
        
        if not source_path.exists():
            raise ValueError(f"Source directory does not exist: {source_dir}")
        
        # Create target directory structure
        ensure_directory_exists(target_path)
        
        # Scan for files - use different scanner based on organization method
        if organize_by == 'extension':
            media_files = scan_all_files(source_path)
        else:
            media_files = scan_directory(source_path)
        
        results = {
            'total_files': len(media_files),
            'processed_files': 0,
            'failed_files': 0,
            'skipped_files': 0,
            'errors': []
        }
        
        for file_path, file_type in media_files:
            try:
                # Determine target path based on organization method
                if organize_by == 'date':
                    target_file_path = self._get_date_based_path(
                        file_path, target_path, file_type
                    )
                elif organize_by == 'extension':
                    target_file_path = self._get_extension_based_path(
                        file_path, target_path, file_type
                    )
                else:
                    target_file_path = self._get_type_based_path(
                        file_path, target_path, file_type
                    )
                
                # Handle duplicates
                final_target_path = handle_duplicate(
                    file_path, target_file_path, duplicate_action
                )
                
                if final_target_path is None:
                    results['skipped_files'] += 1
                    continue
                
                # Perform file operation
                operation_func = safe_move if not copy_mode else safe_copy
                success = operation_func(
                    file_path, final_target_path, 
                    verify_integrity, progress_callback
                )
                
                if success:
                    results['processed_files'] += 1
                else:
                    results['failed_files'] += 1
                    results['errors'].append(f"Failed to process: {file_path}")
                    
            except Exception as e:
                results['failed_files'] += 1
                results['errors'].append(f"Error processing {file_path}: {e}")
                self.logger.error(f"Error processing {file_path}: {e}")
        
        return results
    
    def _get_date_based_path(self, file_path: Path, target_dir: Path, 
                           file_type: str) -> Path:
        """Generate date-based target path"""
        try:
            file_date = get_file_date(str(file_path), file_type)
            date_path = format_date_path(file_date)
            safe_filename = sanitize_filename(file_path.name)
            return target_dir / date_path / safe_filename
        except Exception:
            # Fallback to modification date or 'unknown' folder
            try:
                mod_time = file_path.stat().st_mtime
                from datetime import datetime
                file_date = datetime.fromtimestamp(mod_time)
                date_path = format_date_path(file_date)
                safe_filename = sanitize_filename(file_path.name)
                return target_dir / date_path / safe_filename
            except Exception:
                safe_filename = sanitize_filename(file_path.name)
                return target_dir / 'unknown' / safe_filename
    
    def _get_type_based_path(self, file_path: Path, target_dir: Path, 
                           file_type: str) -> Path:
        """Generate type-based target path"""
        safe_filename = sanitize_filename(file_path.name)
        return target_dir / file_type / safe_filename
    
    def _get_extension_based_path(self, file_path: Path, target_dir: Path, 
                                 file_type: str) -> Path:
        """Generate extension-based target path organized by file extension"""
        extension = file_path.suffix.lower()
        if extension.startswith('.'):
            extension = extension[1:]  # Remove the dot
        
        # Handle files without extensions
        if not extension:
            extension = 'no_extension'
        
        safe_filename = sanitize_filename(file_path.name)
        # Organize directly by extension without media type classification
        return target_dir / extension / safe_filename
