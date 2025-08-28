#!/usr/bin/env python3
"""
File processor module that handles the actual file processing logic
"""

import threading
from pathlib import Path
from tkinter import messagebox

from core import organize_media_files, validate_directory, scan_directory
from .i18n import i18n, _, I18nMixin


class FileProcessor(I18nMixin):
    """Handles the file processing operations in a separate thread"""
    
    def __init__(self, progress_display, log_display):
        self.progress_display = progress_display
        self.log_display = log_display
        self.is_processing = False
        self.cancel_requested = False
        self.processing_thread = None
    
    def cancel_processing(self):
        """Cancel the current processing operation"""
        if self.is_processing and self.processing_thread:
            self.cancel_requested = True
            self.log_display.add_message(_("canceling_operation"))
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
    
    def _process_files(self, source_paths, dest_paths, move_mode, dry_run, md5_check, organization_mode):
        """Process the media files using the core library"""
        try:
            self.progress_display.set_status(_("processing_files"))
            self.log_display.add_message(_("start_processing_media"))
            
            # Log all source directories
            self.log_display.add_message(f"源目录数量: {len(source_paths)}")
            for i, source_path in enumerate(source_paths, 1):
                self.log_display.add_message(f"源目录 {i}: {source_path}")
            
            # Log all destination directories
            self.log_display.add_message(f"目标目录数量: {len(dest_paths)}")
            for i, dest_path in enumerate(dest_paths, 1):
                self.log_display.add_message(f"目标目录 {i}: {dest_path}")
            
            self.log_display.add_message(_("mode_info").format(_("move_mode_text") if move_mode else _("copy_mode_text")))
            if dry_run:
                self.log_display.add_message(_("dry_run_info"))
            self.log_display.add_message("="*50)
            self.log_display.update_display()
            
            # Scan all source directories to get total file count
            all_media_files = []
            for source_path in source_paths:
                media_files = scan_directory(source_path)
                all_media_files.extend(media_files)
            
            if not all_media_files:
                self.log_display.add_message(_("no_media_files_found"))
                return
            
            self.log_display.add_message(_("found_files_count").format(len(all_media_files)))
            self.log_display.update_display()
            
            # Initialize combined statistics
            combined_stats = {
                'photos': 0,
                'videos': 0,
                'errors': 0,
                'processed': 0
            }
            
            total_operations = len(dest_paths) * len(source_paths)
            current_operation = 0
            
            # Process each destination directory
            for dest_index, dest_path in enumerate(dest_paths):
                # Check if cancel was requested
                if self.cancel_requested:
                    self.log_display.add_message(_("operation_canceled"))
                    self.progress_display.set_status(_("operation_canceled"))
                    return
                
                self.log_display.add_message(f"\n{'='*30}")
                self.log_display.add_message(f"处理目标目录 {dest_index + 1}/{len(dest_paths)}: {dest_path}")
                self.log_display.add_message(f"{'='*30}")
                self.log_display.update_display()
                
                # Process each source directory for this destination
                for source_index, source_path in enumerate(source_paths):
                    # Check if cancel was requested
                    if self.cancel_requested:
                        self.log_display.add_message(_("operation_canceled"))
                        self.progress_display.set_status(_("operation_canceled"))
                        return
                    
                    self.log_display.add_message(f"源目录 {source_index + 1}/{len(source_paths)}: {source_path}")
                    self.log_display.update_display()
                    
                    # Define callback functions for this source-destination pair
                    def progress_callback(current, total, filename):
                        """Callback function for progress updates"""
                        # Check for cancel request in callback
                        if self.cancel_requested:
                            return False  # Signal to core library to stop processing
                        
                        # Calculate overall progress across all operations
                        overall_current = (current_operation * len(all_media_files)) + current
                        overall_total = total_operations * len(all_media_files)
                        
                        self.progress_display.set_progress(overall_current, overall_total)
                        self.progress_display.set_status(f"目标 {dest_index + 1}/{len(dest_paths)}, 源 {source_index + 1}/{len(source_paths)}: {filename}")
                        self.log_display.add_message(_("processing_file").format(filename))
                        self.log_display.update_display()
                        return True  # Continue processing
                    
                    def log_callback(message):
                        """Callback function for log messages"""
                        self.log_display.add_message(message)
                        self.log_display.update_display()
                    
                    try:
                        # Call the main organize function from core library for this source-destination pair
                        stats = organize_media_files(
                            source_dir=source_path,
                            dest_dir=dest_path,
                            move_mode=move_mode and dest_index == (len(dest_paths) - 1) and source_index == (len(source_paths) - 1),  # Only move on last source and destination
                            dry_run=dry_run,
                            verify_md5=md5_check,
                            organization_mode=organization_mode,
                            progress_callback=progress_callback
                        )
                        
                        # Add to combined statistics
                        combined_stats['photos'] += stats['photos']
                        combined_stats['videos'] += stats['videos']
                        combined_stats['errors'] += stats['errors']
                        combined_stats['processed'] += stats['processed']
                        
                        # Log individual operation results
                        self.log_display.add_message(f"源 {source_index + 1} -> 目标 {dest_index + 1} 完成:")
                        self.log_display.add_message(f"  照片: {stats['photos']}")
                        self.log_display.add_message(f"  视频: {stats['videos']}")
                        self.log_display.add_message(f"  错误: {stats['errors']}")
                        self.log_display.add_message(f"  总计: {stats['processed']}")
                        
                    except Exception as e:
                        self.log_display.add_message(f"源 {source_index + 1} -> 目标 {dest_index + 1} 处理错误: {e}")
                        # Get the file count for this specific source directory
                        source_files = scan_directory(source_path)
                        combined_stats['errors'] += len(source_files)  # Count all files as errors for this operation
                    
                    current_operation += 1
            
            # Print combined statistics
            self.log_display.add_message("\n" + "="*50)
            self.log_display.add_message("所有目标处理完成")
            self.log_display.add_message("="*50)
            self.log_display.add_message(f"总照片数: {combined_stats['photos']}")
            self.log_display.add_message(f"总视频数: {combined_stats['videos']}")
            self.log_display.add_message(f"总错误数: {combined_stats['errors']}")
            self.log_display.add_message(f"总处理数: {combined_stats['processed']}")
            
            if dry_run:
                self.log_display.add_message("\n" + _("dry_run_notice"))
            
            self.progress_display.set_status(_("processing_complete"))
            
            if combined_stats['errors'] == 0:
                messagebox.showinfo(_("complete"), f"成功处理 {combined_stats['processed']} 个文件到 {len(dest_paths)} 个目标目录")
            else:
                messagebox.showwarning(_("complete"), f"处理了 {combined_stats['processed']} 个文件，但有 {combined_stats['errors']} 个错误")
        
        except Exception as e:
            self.log_display.add_message(_("serious_error").format(e))
            messagebox.showerror(_("error"), _("error_occurred").format(e))
        
        finally:
            # Reset UI state
            self.is_processing = False
            self.progress_display.stop_progress()
            if not hasattr(self, '_processing_complete'):
                self.progress_display.reset_progress()
