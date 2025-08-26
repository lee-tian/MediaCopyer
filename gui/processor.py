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
    
    def start_processing(self, source_dir, dest_dir, move_mode, dry_run, md5_check, organization_mode):
        """Start the file processing in a separate thread"""
        if self.is_processing:
            return
        
        # Validate inputs
        if not source_dir:
            messagebox.showerror(_("error"), _("please_select_source_dir"))
            return
        
        if not dest_dir:
            messagebox.showerror(_("error"), _("please_select_dest_dir"))
            return
        
        source_path = Path(source_dir)
        if not validate_directory(str(source_path), must_exist=True):
            messagebox.showerror(_("error"), _("source_dir_invalid").format(source_path))
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
            self.progress_display.set_status(_("processing_files"))
            self.log_display.add_message(_("start_processing_media"))
            self.log_display.add_message(_("source_directory").format(source_path))
            self.log_display.add_message(_("dest_directory").format(dest_path))
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
            
            # Define callback functions
            def progress_callback(current, total, filename):
                """Callback function for progress updates"""
                # Update progress bar with percentage
                self.progress_display.set_progress(current, total)
                self.progress_display.set_status(_("processing_file_progress").format(current, total, filename))
                self.log_display.add_message(_("processing_file").format(filename))
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
            self.log_display.add_message(_("processing_complete"))
            self.log_display.add_message("="*50)
            self.log_display.add_message(_("photos_processed").format(stats['photos']))
            self.log_display.add_message(_("videos_processed").format(stats['videos']))
            self.log_display.add_message(_("errors_count").format(stats['errors']))
            self.log_display.add_message(_("total_files").format(stats['processed']))
            
            if dry_run:
                self.log_display.add_message("\n" + _("dry_run_notice"))
            
            self.progress_display.set_status(_("processing_complete"))
            
            if stats['errors'] == 0:
                messagebox.showinfo(_("complete"), _("success_message").format(stats['processed']))
            else:
                messagebox.showwarning(_("complete"), _("warning_message").format(stats['processed'], stats['errors']))
        
        except Exception as e:
            self.log_display.add_message(_("serious_error").format(e))
            messagebox.showerror(_("error"), _("error_occurred").format(e))
        
        finally:
            # Reset UI state
            self.is_processing = False
            self.button_panel.set_start_button_state('normal')
            self.progress_display.stop_progress()
            if not hasattr(self, '_processing_complete'):
                self.progress_display.reset_progress()
