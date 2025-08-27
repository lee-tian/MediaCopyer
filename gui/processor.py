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
    
    def __init__(self, progress_display, log_display, button_panel):
        self.progress_display = progress_display
        self.log_display = log_display
        self.button_panel = button_panel
        self.is_processing = False
        self.cancel_requested = False
        self.processing_thread = None
    
    def cancel_processing(self):
        """Cancel the current processing operation"""
        if self.is_processing and self.processing_thread:
            self.cancel_requested = True
            self.log_display.add_message(_("canceling_operation"))
            self.log_display.update_display()
    
    def start_processing(self, source_dir, dest_dirs, move_mode, dry_run, md5_check, organization_mode):
        """Start the file processing in a separate thread"""
        if self.is_processing:
            return
        
        # Validate inputs
        if not source_dir:
            messagebox.showerror(_("error"), _("please_select_source_dir"))
            return
        
        if not dest_dirs or len(dest_dirs) == 0:
            messagebox.showerror(_("error"), _("please_select_dest_dir"))
            return
        
        source_path = Path(source_dir)
        if not validate_directory(str(source_path), must_exist=True):
            messagebox.showerror(_("error"), _("source_dir_invalid").format(source_path))
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
        # 立即切换到取消模式
        self.button_panel.set_processing_mode(True)
        self.progress_display.start_progress()
        
        self.processing_thread = threading.Thread(
            target=self._process_files,
            args=(source_path, dest_paths, move_mode, dry_run, md5_check, organization_mode)
        )
        self.processing_thread.daemon = True
        self.processing_thread.start()
    
    def _process_files(self, source_path, dest_paths, move_mode, dry_run, md5_check, organization_mode):
        """Process the media files using the core library"""
        try:
            self.progress_display.set_status(_("processing_files"))
            self.log_display.add_message(_("start_processing_media"))
            self.log_display.add_message(_("source_directory").format(source_path))
            
            # Log all destination directories
            self.log_display.add_message(f"目标目录数量: {len(dest_paths)}")
            for i, dest_path in enumerate(dest_paths, 1):
                self.log_display.add_message(f"目标目录 {i}: {dest_path}")
            
            self.log_display.add_message(_("mode_info").format(_("move_mode_text") if move_mode else _("copy_mode_text")))
            if dry_run:
                self.log_display.add_message(_("dry_run_info"))
            self.log_display.add_message("="*50)
            self.log_display.update_display()
            
            # Quick scan to show file count
            media_files = scan_directory(source_path)
            if not media_files:
                self.log_display.add_message(_("no_media_files_found"))
                return
            
            self.log_display.add_message(_("found_files_count").format(len(media_files)))
            self.log_display.update_display()
            
            # Initialize combined statistics
            combined_stats = {
                'photos': 0,
                'videos': 0,
                'errors': 0,
                'processed': 0
            }
            
            total_operations = len(dest_paths)
            
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
                
                # Define callback functions for this destination
                def progress_callback(current, total, filename):
                    """Callback function for progress updates"""
                    # Check for cancel request in callback
                    if self.cancel_requested:
                        return False  # Signal to core library to stop processing
                    
                    # Calculate overall progress across all destinations
                    overall_current = (dest_index * len(media_files)) + current
                    overall_total = total_operations * len(media_files)
                    
                    self.progress_display.set_progress(overall_current, overall_total)
                    self.progress_display.set_status(f"目标 {dest_index + 1}/{total_operations}: {filename}")
                    self.log_display.add_message(_("processing_file").format(filename))
                    self.log_display.update_display()
                    return True  # Continue processing
                
                def log_callback(message):
                    """Callback function for log messages"""
                    self.log_display.add_message(message)
                    self.log_display.update_display()
                
                try:
                    # Call the main organize function from core library for this destination
                    stats = organize_media_files(
                        source_dir=source_path,
                        dest_dir=dest_path,
                        move_mode=move_mode and dest_index == (len(dest_paths) - 1),  # Only move on last destination
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
                    
                    # Log individual destination results
                    self.log_display.add_message(f"目标 {dest_index + 1} 完成:")
                    self.log_display.add_message(f"  照片: {stats['photos']}")
                    self.log_display.add_message(f"  视频: {stats['videos']}")
                    self.log_display.add_message(f"  错误: {stats['errors']}")
                    self.log_display.add_message(f"  总计: {stats['processed']}")
                    
                except Exception as e:
                    self.log_display.add_message(f"目标目录 {dest_index + 1} 处理错误: {e}")
                    combined_stats['errors'] += len(media_files)  # Count all files as errors for this destination
            
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
            # 处理完成或取消后，重新切换回开始处理模式
            self.button_panel.set_processing_mode(False)
            self.progress_display.stop_progress()
            if not hasattr(self, '_processing_complete'):
                self.progress_display.reset_progress()
