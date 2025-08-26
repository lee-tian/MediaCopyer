#!/usr/bin/env python3
"""
File processor module that handles the actual file processing logic
"""

import threading
from pathlib import Path
from tkinter import messagebox

from core import organize_media_files, validate_directory, scan_directory


class FileProcessor:
    """Handles the file processing operations in a separate thread"""
    
    def __init__(self, progress_display, log_display, button_panel):
        self.progress_display = progress_display
        self.log_display = log_display
        self.button_panel = button_panel
        self.is_processing = False
    
    def start_processing(self, source_dir, dest_dir, move_mode, dry_run, md5_check, organization_mode):
        """Start the file processing in a separate thread"""
        if self.is_processing:
            return
        
        # Validate inputs
        if not source_dir:
            messagebox.showerror("错误", "请选择源目录")
            return
        
        if not dest_dir:
            messagebox.showerror("错误", "请选择目标目录")
            return
        
        source_path = Path(source_dir)
        if not validate_directory(str(source_path), must_exist=True):
            messagebox.showerror("错误", f"源目录不存在或无效: {source_path}")
            return
        
        # Start processing in a separate thread
        self.is_processing = True
        self.button_panel.set_start_button_state('disabled')
        self.progress_display.start_progress()
        
        processing_thread = threading.Thread(
            target=self._process_files,
            args=(source_path, Path(dest_dir), move_mode, dry_run, md5_check, organization_mode)
        )
        processing_thread.daemon = True
        processing_thread.start()
    
    def _process_files(self, source_path, dest_path, move_mode, dry_run, md5_check, organization_mode):
        """Process the media files using the core library"""
        try:
            self.progress_display.set_status("正在处理文件...")
            self.log_display.add_message(f"开始处理媒体文件")
            self.log_display.add_message(f"源目录: {source_path}")
            self.log_display.add_message(f"目标目录: {dest_path}")
            self.log_display.add_message(f"模式: {'移动' if move_mode else '复制'}")
            if dry_run:
                self.log_display.add_message("试运行模式 - 不会实际移动/复制文件")
            self.log_display.add_message("="*50)
            self.log_display.update_display()
            
            # Quick scan to show file count
            media_files = scan_directory(source_path)
            if not media_files:
                self.log_display.add_message("未找到媒体文件!")
                return
            
            self.log_display.add_message(f"找到 {len(media_files)} 个媒体文件")
            self.log_display.update_display()
            
            # Define callback functions
            def progress_callback(current, total, filename):
                """Callback function for progress updates"""
                self.progress_display.set_status(f"处理文件 {current}/{total}: {filename}")
                self.log_display.add_message(f"正在处理: {filename}")
                self.log_display.update_display()
            
            def log_callback(message):
                """Callback function for log messages"""
                self.log_display.add_message(message)
                self.log_display.update_display()
            
            # Call the main organize function from core library
            stats = organize_media_files(
                source_dir=source_path,
                dest_dir=dest_path,
                move_mode=move_mode,
                dry_run=dry_run,
                verify_md5=md5_check,
                organization_mode=organization_mode,
                progress_callback=progress_callback
            )
            
            # Print statistics
            self.log_display.add_message("\n" + "="*50)
            self.log_display.add_message("处理完成!")
            self.log_display.add_message("="*50)
            self.log_display.add_message(f"照片处理: {stats['photos']}")
            self.log_display.add_message(f"视频处理: {stats['videos']}")
            self.log_display.add_message(f"错误数量: {stats['errors']}")
            self.log_display.add_message(f"总文件数: {stats['processed']}")
            
            if dry_run:
                self.log_display.add_message("\n(这是试运行 - 没有实际移动/复制文件)")
            
            self.progress_display.set_status("处理完成!")
            
            if stats['errors'] == 0:
                messagebox.showinfo("完成", f"成功处理了 {stats['processed']} 个文件!")
            else:
                messagebox.showwarning("完成", f"处理了 {stats['processed']} 个文件，但有 {stats['errors']} 个错误。请查看日志了解详情。")
        
        except Exception as e:
            self.log_display.add_message(f"❌ 发生严重错误: {e}")
            messagebox.showerror("错误", f"发生错误: {e}")
        
        finally:
            # Reset UI state
            self.is_processing = False
            self.button_panel.set_start_button_state('normal')
            self.progress_display.stop_progress()
            if not hasattr(self, '_processing_complete'):
                self.progress_display.set_status("准备就绪")
