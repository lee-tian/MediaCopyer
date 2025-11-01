#!/usr/bin/env python3
"""
File processor module that handles the actual file processing logic
"""

import threading
from pathlib import Path
from tkinter import messagebox
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

from core import organize_media_files, validate_directory, scan_directory
from core.utils import (
    calculate_multiple_directories_size, 
    format_size_summary, 
    compare_directories_size,
    estimate_required_space,
    check_available_space,
    calculate_copy_operation_analysis
)
from .i18n import i18n, _, I18nMixin


class FileProcessor:
    """Handles the file processing operations in a separate thread"""
    
    def __init__(self, progress_display, log_display):
        self.progress_display = progress_display
        self.log_display = log_display
        self.is_processing = False
        self.cancel_requested = False
        self.processing_thread = None
        self.progress_lock = threading.Lock()
        self.log_lock = threading.Lock()
        self.stats_lock = threading.Lock()
        self.global_progress = {'current': 0, 'total': 0}
    
    def cancel_processing(self):
        """Cancel the current processing operation"""
        if self.is_processing and self.processing_thread:
            self.cancel_requested = True
            self.log_display.add_log(_("canceling_operation"))
            self.log_display.update_display()
    
    def start_processing(self, source_dirs, dest_dirs, move_mode, dry_run, md5_check, organization_mode):
        """Start the file processing in a separate thread"""
        if self.is_processing:
            return
        
        # Validate inputs
        if not source_dirs or len(source_dirs) == 0:
            messagebox.showerror(_("error"), _("please_select_source_dir"))
            return
        
        if not dest_dirs or len(dest_dirs) == 0:
            messagebox.showerror(_("error"), _("please_select_dest_dir"))
            return
        
        # Validate all source directories
        source_paths = []
        for source_dir in source_dirs:
            if source_dir.strip():  # Only process non-empty directories
                source_path = Path(source_dir)
                if not validate_directory(str(source_path), must_exist=True):
                    messagebox.showerror(_("error"), _("source_dir_invalid").format(source_path))
                    return
                source_paths.append(source_path)
        
        if not source_paths:
            messagebox.showerror(_("error"), _("please_select_source_dir"))
            return
        
        # Validate all destination directories
        dest_paths = []
        for dest_dir in dest_dirs:
            if dest_dir.strip():  # Only process non-empty directories
                dest_paths.append(Path(dest_dir))
        
        if not dest_paths:
            messagebox.showerror(_("error"), _("please_select_dest_dir"))
            return
        
        # Start processing in a separate thread
        self.is_processing = True
        self.cancel_requested = False
        self.progress_display.start_progress()
        
        self.processing_thread = threading.Thread(
            target=self._process_files,
            args=(source_paths, dest_paths, move_mode, dry_run, md5_check, organization_mode)
        )
        self.processing_thread.daemon = True
        self.processing_thread.start()
    
    def _safe_log(self, message):
        """Thread-safe logging"""
        with self.log_lock:
            self.log_display.add_log(message)
            self.log_display.update_display()
    
    def _update_global_progress(self, current_increment=0):
        """Thread-safe progress update"""
        with self.progress_lock:
            self.global_progress['current'] += current_increment
            self.progress_display.set_progress(
                self.global_progress['current'], 
                self.global_progress['total']
            )
    
    def _process_single_source_to_dest(self, source_path, dest_path, source_index, dest_index, 
                                     total_sources, total_dests, move_mode, dry_run, 
                                     md5_check, organization_mode):
        """Process a single source directory to a single destination directory"""
        try:
            # Check if cancel was requested
            if self.cancel_requested:
                return {'success': False, 'stats': None, 'message': 'Cancelled'}
            
            self._safe_log(_("parallel_start_processing").format(source_index + 1, total_sources, dest_index + 1, total_dests))
            self._safe_log(_("parallel_source_dir").format(source_path))
            self._safe_log(_("parallel_dest_dir").format(dest_path))
            
            # Get file count for this source directory
            source_files = scan_directory(source_path)
            if not source_files:
                self._safe_log(_("parallel_no_media_files").format(source_index + 1))
                return {'success': True, 'stats': {'photos': 0, 'videos': 0, 'errors': 0, 'processed': 0}, 'message': 'No files'}
            
            # Define callback functions for this source-destination pair
            def progress_callback(current, total, filename):
                """Callback function for progress updates"""
                # Check for cancel request in callback
                if self.cancel_requested:
                    return False  # Signal to core library to stop processing
                
                # Update progress (increment by 1 for each file processed)
                self._update_global_progress(1)
                
                with self.progress_lock:
                    self.progress_display.set_status(_("parallel_progress_status").format(source_index + 1, dest_index + 1, filename))
                
                self._safe_log(_("parallel_processing_file").format(filename))
                return True  # Continue processing
            
            # Call the main organize function from core library for this source-destination pair
            stats = organize_media_files(
                source_dir=source_path,
                dest_dir=dest_path,
                move_mode=move_mode,  # Each thread handles move independently
                dry_run=dry_run,
                verify_md5=md5_check,
                organization_mode=organization_mode,
                progress_callback=progress_callback
            )
            
            # Log individual operation results
            self._safe_log(_("parallel_source_dest_complete").format(source_index + 1, dest_index + 1))
            self._safe_log(_("parallel_photos").format(stats['photos']))
            self._safe_log(_("parallel_videos").format(stats['videos']))
            self._safe_log(_("parallel_duplicates").format(stats.get('duplicates', 0)))
            self._safe_log(_("parallel_errors").format(stats['errors']))
            self._safe_log(_("parallel_total").format(stats['processed']))
            
            return {'success': True, 'stats': stats, 'message': 'Success'}
            
        except Exception as e:
            error_msg = _("parallel_processing_error").format(source_index + 1, dest_index + 1, e)
            self._safe_log(error_msg)
            # Get the file count for this specific source directory for error counting
            try:
                source_files = scan_directory(source_path)
                error_stats = {'photos': 0, 'videos': 0, 'duplicates': 0, 'errors': len(source_files), 'processed': 0}
            except:
                error_stats = {'photos': 0, 'videos': 0, 'duplicates': 0, 'errors': 1, 'processed': 0}
            return {'success': False, 'stats': error_stats, 'message': str(e)}

    def _process_files(self, source_paths, dest_paths, move_mode, dry_run, md5_check, organization_mode):
        """Process the media files using parallel processing"""
        try:
            self.progress_display.set_status(_("processing_files"))
            self._safe_log(_("start_processing_media"))
            
            # Log all source directories
            self._safe_log(_("source_dir_count").format(len(source_paths)))
            for i, source_path in enumerate(source_paths, 1):
                self._safe_log(_("source_dir_number").format(i, source_path))
            
            # Log all destination directories
            self._safe_log(_("dest_dir_count").format(len(dest_paths)))
            for i, dest_path in enumerate(dest_paths, 1):
                self._safe_log(_("dest_dir_number").format(i, dest_path))
            
            self._safe_log(_("mode_info").format(_("move_mode_text") if move_mode else _("copy_mode_text")))
            if dry_run:
                self._safe_log(_("dry_run_info"))
            
            # Calculate and display source directory sizes
            self._safe_log("="*60)
            self._safe_log(_("source_size_analysis"))
            self._safe_log("="*60)
            
            source_size_infos = calculate_multiple_directories_size(source_paths, include_all_files=False)
            total_source_media_files = 0
            total_source_media_size = 0
            
            for i, size_info in enumerate(source_size_infos, 1):
                self._safe_log(f"\n" + _("source_dir_info").format(i, size_info.path))
                self._safe_log(_("total_files").format(size_info.total_files))
                self._safe_log(_("photos_info").format(size_info.photos, size_info.photo_size / (1024*1024)))
                self._safe_log(_("videos_info").format(size_info.videos, size_info.video_size / (1024*1024)))
                self._safe_log(_("media_files_total").format(size_info.media_files, size_info.media_size / (1024*1024)))
                
                total_source_media_files += size_info.media_files
                total_source_media_size += size_info.media_size
            
            self._safe_log(f"\n" + _("all_sources_summary"))
            self._safe_log(_("total_media_files").format(total_source_media_files))
            self._safe_log(_("total_media_size").format(total_source_media_size / (1024*1024)))
            
            # Estimate required space
            required_space = estimate_required_space(source_size_infos, len(dest_paths), move_mode)
            mode_text = _("move_mode_text_short") if move_mode else _("copy_mode_text_short")
            self._safe_log(_("estimated_space_needed").format(required_space / (1024*1024), mode_text, len(dest_paths)))
            
            # Check available space for each destination
            self._safe_log(f"\n" + _("dest_space_check"))
            space_warnings = []
            for i, dest_path in enumerate(dest_paths, 1):
                try:
                    has_space, available_bytes = check_available_space(dest_path, required_space // len(dest_paths))
                    available_mb = available_bytes / (1024*1024)
                    required_mb = (required_space // len(dest_paths)) / (1024*1024)
                    
                    status = _("space_status_sufficient") if has_space else _("space_status_insufficient")
                    self._safe_log(_("dest_space_info").format(i, available_mb, required_mb, status))
                    
                    if not has_space:
                        space_warnings.append(_("dest_dir_number").format(i, _("space_status_insufficient")))
                except Exception as e:
                    self._safe_log(_("dest_space_check_failed").format(i, e))
            
            if space_warnings and not dry_run:
                self._safe_log(f"\n" + _("space_warning").format('; '.join(space_warnings)))
            
            # Capture destination directory sizes before operation (for enhanced analysis)
            if not dry_run:
                self._safe_log(f"\n" + "📊 " + _("dest_size_analysis") + " (Before Operation)")
                self._dest_before_infos = calculate_multiple_directories_size(dest_paths, include_all_files=False)
                
                for i, size_info in enumerate(self._dest_before_infos, 1):
                    self._safe_log(_("dest_dir_info").format(i, size_info.path))
                    self._safe_log(_("media_files_total").format(size_info.media_files, size_info.media_size / (1024*1024)))
            
            self._safe_log("="*60)
            self._safe_log(_("start_parallel_processing"))
            self._safe_log("="*60)
            
            # Scan all source directories to get total file count
            all_media_files = []
            source_file_counts = {}
            for source_path in source_paths:
                media_files = scan_directory(source_path)
                all_media_files.extend(media_files)
                source_file_counts[source_path] = len(media_files)
            
            if not all_media_files:
                self._safe_log(_("no_media_files_found"))
                return
            
            self._safe_log(_("found_files_count").format(len(all_media_files)))
            
            # Initialize global progress tracking
            total_operations = len(dest_paths) * len(source_paths)
            total_files_to_process = len(all_media_files) * len(dest_paths)
            
            with self.progress_lock:
                self.global_progress = {'current': 0, 'total': total_files_to_process}
            
            # Initialize combined statistics
            combined_stats = {
                'photos': 0,
                'videos': 0,
                'duplicates': 0,
                'errors': 0,
                'processed': 0
            }
            
            # Process each destination directory
            for dest_index, dest_path in enumerate(dest_paths):
                # Check if cancel was requested
                if self.cancel_requested:
                    self._safe_log(_("operation_canceled"))
                    self.progress_display.set_status(_("operation_canceled"))
                    return
                
                self._safe_log(f"\n{'='*30}")
                self._safe_log(_("processing_dest_header").format(dest_index + 1, len(dest_paths), dest_path))
                self._safe_log(f"{'='*30}")
                
                # Create a list of tasks for parallel processing
                tasks = []
                for source_index, source_path in enumerate(source_paths):
                    tasks.append((source_path, dest_path, source_index, dest_index, 
                                len(source_paths), len(dest_paths), move_mode, dry_run, 
                                md5_check, organization_mode))
                
                # Use ThreadPoolExecutor for parallel processing
                # Limit concurrent threads to avoid overwhelming the system
                max_workers = min(len(source_paths), 4)  # Max 4 concurrent operations
                self._safe_log(_("parallel_using_threads").format(max_workers, len(source_paths)))
                
                with ThreadPoolExecutor(max_workers=max_workers) as executor:
                    # Submit all tasks
                    future_to_task = {
                        executor.submit(self._process_single_source_to_dest, *task): task 
                        for task in tasks
                    }
                    
                    # Process completed tasks
                    for future in as_completed(future_to_task):
                        # Check if cancel was requested
                        if self.cancel_requested:
                            self._safe_log(_("operation_canceled"))
                            self.progress_display.set_status(_("operation_canceled"))
                            # Cancel remaining futures
                            for f in future_to_task:
                                f.cancel()
                            return
                        
                        task = future_to_task[future]
                        try:
                            result = future.result()
                            if result['stats']:
                                # Add to combined statistics (thread-safe)
                                with self.stats_lock:
                                    combined_stats['photos'] += result['stats']['photos']
                                    combined_stats['videos'] += result['stats']['videos']
                                    combined_stats['duplicates'] += result['stats'].get('duplicates', 0)
                                    combined_stats['errors'] += result['stats']['errors']
                                    combined_stats['processed'] += result['stats']['processed']
                        except Exception as e:
                            source_path, dest_path, source_index, dest_index = task[:4]
                            self._safe_log(_("parallel_task_exception").format(source_index + 1, dest_index + 1, e))
                            with self.stats_lock:
                                combined_stats['errors'] += source_file_counts.get(source_path, 1)
            
            # Print combined statistics
            self._safe_log("\n" + "="*60)
            self._safe_log(_("parallel_all_complete"))
            self._safe_log("="*60)
            self._safe_log(_("total_photos").format(combined_stats['photos']))
            self._safe_log(_("total_videos").format(combined_stats['videos']))
            self._safe_log(_("total_duplicates").format(combined_stats['duplicates']))
            self._safe_log(_("total_errors").format(combined_stats['errors']))
            self._safe_log(_("total_processed").format(combined_stats['processed']))
            
            # Calculate and display destination directory sizes (only if not dry run)
            if not dry_run:
                self._safe_log("\n" + "="*60)
                self._safe_log(_("dest_size_analysis"))
                self._safe_log("="*60)
                
                dest_size_infos = calculate_multiple_directories_size(dest_paths, include_all_files=False)
                total_dest_media_files = 0
                total_dest_media_size = 0
                
                for i, size_info in enumerate(dest_size_infos, 1):
                    self._safe_log(f"\n" + _("dest_dir_info").format(i, size_info.path))
                    self._safe_log(_("total_files").format(size_info.total_files))
                    self._safe_log(_("photos_info").format(size_info.photos, size_info.photo_size / (1024*1024)))
                    self._safe_log(_("videos_info").format(size_info.videos, size_info.video_size / (1024*1024)))
                    self._safe_log(_("media_files_total").format(size_info.media_files, size_info.media_size / (1024*1024)))
                    
                    total_dest_media_files += size_info.media_files
                    total_dest_media_size += size_info.media_size
                
                self._safe_log(f"\n" + _("all_dests_summary"))
                self._safe_log(_("total_media_files").format(total_dest_media_files))
                self._safe_log(_("total_media_size").format(total_dest_media_size / (1024*1024)))
                
                # Enhanced copy operation analysis
                if source_size_infos and hasattr(self, '_dest_before_infos') and dest_size_infos:
                    analysis = calculate_copy_operation_analysis(
                        source_size_infos, 
                        self._dest_before_infos, 
                        dest_size_infos, 
                        combined_stats, 
                        move_mode
                    )
                    
                    # Display enhanced analysis
                    self._safe_log(f"\n" + _("copy_operation_summary"))
                    self._safe_log(_("files_copied_this_time").format(analysis['operation']['files_copied']))
                    self._safe_log(_("size_copied_this_time").format(analysis['operation']['size_copied_formatted']))
                    self._safe_log(_("dest_increase_files").format(analysis['operation']['actual_files_increase']))
                    self._safe_log(_("dest_increase_size").format(analysis['operation']['actual_size_increase_formatted']))
                    
                    self._safe_log(f"\n" + _("dest_before_after"))
                    self._safe_log(_("dest_before").format(
                        analysis['destination_before']['files'], 
                        analysis['destination_before']['size_formatted']
                    ))
                    self._safe_log(_("dest_after").format(
                        analysis['destination_after']['files'], 
                        analysis['destination_after']['size_formatted']
                    ))
                    self._safe_log(_("net_increase").format(
                        analysis['operation']['actual_files_increase'],
                        analysis['operation']['actual_size_increase_formatted']
                    ))
                    
                    self._safe_log(f"\n" + _("copy_match_analysis"))
                    if analysis['operation']['files_match']:
                        self._safe_log(_("copy_files_match"))
                    else:
                        self._safe_log(_("copy_files_mismatch").format(
                            analysis['operation']['files_copied'],
                            analysis['operation']['actual_files_increase'],
                            analysis['operation']['files_difference']
                        ))
                    
                    if analysis['operation']['size_match']:
                        self._safe_log(_("copy_size_match"))
                    else:
                        self._safe_log(_("copy_size_mismatch").format(
                            analysis['operation']['size_copied_formatted'],
                            analysis['operation']['actual_size_increase_formatted'],
                            analysis['operation']['size_difference_formatted']
                        ))
                
                # Traditional comparison for backward compatibility
                if source_size_infos and dest_size_infos:
                    comparison = compare_directories_size(source_size_infos, dest_size_infos)
                    
                    self._safe_log(f"\n" + _("size_comparison"))
                    self._safe_log(_("source_comparison").format(comparison['source']['media_files'], comparison['source']['media_size_formatted']))
                    self._safe_log(_("dest_comparison").format(comparison['destination']['media_files'], comparison['destination']['media_size_formatted']))
                    
                    if move_mode:
                        # For move mode, files should be the same count
                        if comparison['difference']['media_files'] == 0:
                            self._safe_log(_("files_match_move"))
                        else:
                            self._safe_log(_("files_mismatch").format(comparison['difference']['media_files']))
                    else:
                        # For copy mode, destination should have more files (copies to multiple destinations)
                        expected_files = comparison['source']['media_files'] * len(dest_paths)
                        if comparison['destination']['media_files'] == expected_files:
                            self._safe_log(_("files_copy_complete").format(len(dest_paths)))
                        else:
                            actual_ratio = comparison['destination']['media_files'] / comparison['source']['media_files'] if comparison['source']['media_files'] > 0 else 0
                            self._safe_log(_("copy_ratio").format(actual_ratio, len(dest_paths)))
            
            if dry_run:
                self._safe_log("\n" + _("dry_run_notice"))
            
            self.progress_display.set_status(_("processing_complete"))
            
                # Skip messagebox in test environment to avoid GUI issues
            try:
                if combined_stats['errors'] == 0:
                    messagebox.showinfo(_("complete"), _("parallel_success_message").format(combined_stats['processed'], len(dest_paths)))
                else:
                    messagebox.showwarning(_("complete"), _("parallel_warning_message").format(combined_stats['processed'], combined_stats['errors']))
            except Exception:
                # Skip messagebox if GUI is not available (e.g., in tests)
                self._safe_log(_("processing_complete_log").format(combined_stats['processed'], combined_stats['errors']))
        
        except Exception as e:
            self._safe_log(_("serious_error").format(e))
            messagebox.showerror(_("error"), _("error_occurred").format(e))
        
        finally:
            # Reset UI state
            self.is_processing = False
            self.progress_display.stop_progress()
            if not hasattr(self, '_processing_complete'):
                self.progress_display.reset_progress()
