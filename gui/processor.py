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
            
            self._safe_log(f"[并行] 开始处理: 源 {source_index + 1}/{total_sources} -> 目标 {dest_index + 1}/{total_dests}")
            self._safe_log(f"[并行] 源目录: {source_path}")
            self._safe_log(f"[并行] 目标目录: {dest_path}")
            
            # Get file count for this source directory
            source_files = scan_directory(source_path)
            if not source_files:
                self._safe_log(f"[并行] 源目录 {source_index + 1} 中没有找到媒体文件")
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
                    self.progress_display.set_status(f"[并行] 源{source_index + 1}->目标{dest_index + 1}: {filename}")
                
                self._safe_log(f"[并行] 处理文件: {filename}")
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
            self._safe_log(f"[并行] 源 {source_index + 1} -> 目标 {dest_index + 1} 完成:")
            self._safe_log(f"[并行]   照片: {stats['photos']}")
            self._safe_log(f"[并行]   视频: {stats['videos']}")
            self._safe_log(f"[并行]   错误: {stats['errors']}")
            self._safe_log(f"[并行]   总计: {stats['processed']}")
            
            return {'success': True, 'stats': stats, 'message': 'Success'}
            
        except Exception as e:
            error_msg = f"[并行] 源 {source_index + 1} -> 目标 {dest_index + 1} 处理错误: {e}"
            self._safe_log(error_msg)
            # Get the file count for this specific source directory for error counting
            try:
                source_files = scan_directory(source_path)
                error_stats = {'photos': 0, 'videos': 0, 'errors': len(source_files), 'processed': 0}
            except:
                error_stats = {'photos': 0, 'videos': 0, 'errors': 1, 'processed': 0}
            return {'success': False, 'stats': error_stats, 'message': str(e)}

    def _process_files(self, source_paths, dest_paths, move_mode, dry_run, md5_check, organization_mode):
        """Process the media files using parallel processing"""
        try:
            self.progress_display.set_status(_("processing_files"))
            self._safe_log(_("start_processing_media"))
            
            # Log all source directories
            self._safe_log(f"源目录数量: {len(source_paths)}")
            for i, source_path in enumerate(source_paths, 1):
                self._safe_log(f"源目录 {i}: {source_path}")
            
            # Log all destination directories
            self._safe_log(f"目标目录数量: {len(dest_paths)}")
            for i, dest_path in enumerate(dest_paths, 1):
                self._safe_log(f"目标目录 {i}: {dest_path}")
            
            self._safe_log(_("mode_info").format(_("move_mode_text") if move_mode else _("copy_mode_text")))
            if dry_run:
                self._safe_log(_("dry_run_info"))
            self._safe_log("="*50)
            self._safe_log("启用并行处理模式 - 多个源目录将同时复制")
            self._safe_log("="*50)
            
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
                self._safe_log(f"处理目标目录 {dest_index + 1}/{len(dest_paths)}: {dest_path}")
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
                self._safe_log(f"使用 {max_workers} 个并行线程处理 {len(source_paths)} 个源目录")
                
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
                                    combined_stats['errors'] += result['stats']['errors']
                                    combined_stats['processed'] += result['stats']['processed']
                        except Exception as e:
                            source_path, dest_path, source_index, dest_index = task[:4]
                            self._safe_log(f"[并行] 任务执行异常: 源 {source_index + 1} -> 目标 {dest_index + 1}: {e}")
                            with self.stats_lock:
                                combined_stats['errors'] += source_file_counts.get(source_path, 1)
            
            # Print combined statistics
            self._safe_log("\n" + "="*50)
            self._safe_log("所有目标处理完成 (并行模式)")
            self._safe_log("="*50)
            self._safe_log(f"总照片数: {combined_stats['photos']}")
            self._safe_log(f"总视频数: {combined_stats['videos']}")
            self._safe_log(f"总错误数: {combined_stats['errors']}")
            self._safe_log(f"总处理数: {combined_stats['processed']}")
            
            if dry_run:
                self._safe_log("\n" + _("dry_run_notice"))
            
            self.progress_display.set_status(_("processing_complete"))
            
            if combined_stats['errors'] == 0:
                messagebox.showinfo(_("complete"), f"成功并行处理 {combined_stats['processed']} 个文件到 {len(dest_paths)} 个目标目录")
            else:
                messagebox.showwarning(_("complete"), f"并行处理了 {combined_stats['processed']} 个文件，但有 {combined_stats['errors']} 个错误")
        
        except Exception as e:
            self._safe_log(_("serious_error").format(e))
            messagebox.showerror(_("error"), _("error_occurred").format(e))
        
        finally:
            # Reset UI state
            self.is_processing = False
            self.progress_display.stop_progress()
            if not hasattr(self, '_processing_complete'):
                self.progress_display.reset_progress()
