#!/usr/bin/env python3
"""
Main application window for Media Copyer GUI
"""

import tkinter as tk
from tkinter import ttk

from core.utils import check_dependencies
from .widgets import DirectorySelector, ProgressDisplay, LogDisplay, ButtonPanel
from .options_frame import OptionsFrame
from .processor import FileProcessor


class MediaCopyerApp:
    """Main application class for Media Copyer GUI"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Media Copyer - 媒体文件整理工具")
        self.root.geometry("800x600")
        
        self._setup_ui()
        self._setup_processor()
        self._check_dependencies()
    
    def _setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(6, weight=1)  # Make log area expandable
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="Media Copyer - 媒体文件整理工具", 
            font=('TkDefaultFont', 16, 'bold')
        )
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Source directory selector
        self.source_selector = DirectorySelector(
            main_frame, 
            "源目录 (Source Directory):", 
            "选择源目录"
        )
        self.source_selector.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # Destination directory selector
        self.dest_selector = DirectorySelector(
            main_frame, 
            "目标目录 (Destination Directory):", 
            "选择目标目录"
        )
        self.dest_selector.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # Options frame
        self.options_frame = OptionsFrame(main_frame)
        self.options_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=20)
        
        # Control buttons
        self.button_panel = ButtonPanel(main_frame)
        self.button_panel.grid(row=4, column=0, pady=20)
        
        # Progress display
        self.progress_display = ProgressDisplay(main_frame)
        self.progress_display.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=10)
        
        # Log display
        self.log_display = LogDisplay(main_frame)
        self.log_display.grid(row=6, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
    
    def _setup_processor(self):
        """Setup the file processor and connect callbacks"""
        self.processor = FileProcessor(
            self.progress_display, 
            self.log_display, 
            self.button_panel
        )
        
        # Connect button callbacks
        self.button_panel.set_start_command(self._start_processing)
        self.button_panel.set_clear_log_command(self._clear_log)
    
    def _check_dependencies(self):
        """Check if required dependencies are available"""
        messages = check_dependencies()
        
        if messages:
            for msg in messages:
                self.log_display.add_message(msg)
            self.log_display.add_message("可以继续使用，但会影响日期识别精度\n" + "="*50)
    
    def _start_processing(self):
        """Start the file processing"""
        self.processor.start_processing(
            source_dir=self.source_selector.get_directory(),
            dest_dir=self.dest_selector.get_directory(),
            move_mode=self.options_frame.get_move_mode(),
            dry_run=self.options_frame.get_dry_run(),
            organization_mode=self.options_frame.get_organization_mode()
        )
    
    def _clear_log(self):
        """Clear the log display"""
        self.log_display.clear()


def create_app():
    """Create and return the main application"""
    root = tk.Tk()
    app = MediaCopyerApp(root)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    return root, app


def main():
    """Main function to run the GUI application"""
    root, app = create_app()
    root.mainloop()


if __name__ == "__main__":
    main()
