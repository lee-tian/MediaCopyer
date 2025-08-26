#!/usr/bin/env python3
"""
Custom widgets and UI components for Media Copyer GUI
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog


class DirectorySelector(ttk.Frame):
    """A frame containing an entry field and browse button for directory selection"""
    
    def __init__(self, parent, label_text, browse_title, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.directory_var = tk.StringVar()
        self.browse_title = browse_title
        
        # Setup the layout
        self.columnconfigure(1, weight=1)
        
        # Label
        ttk.Label(self, text=label_text).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        # Entry field
        ttk.Entry(self, textvariable=self.directory_var, width=50).grid(
            row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 5)
        )
        
        # Browse button
        ttk.Button(self, text="浏览...", command=self._on_browse).grid(row=0, column=2, pady=5)
    
    def _on_browse(self):
        """Open file dialog to select directory"""
        directory = filedialog.askdirectory(title=self.browse_title)
        if directory:
            self.directory_var.set(directory)
    
    def get_directory(self):
        """Get the selected directory path"""
        return self.directory_var.get()
    
    def set_directory(self, path):
        """Set the directory path"""
        self.directory_var.set(path)


class ProgressDisplay(ttk.Frame):
    """A frame containing progress bar and status label"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.progress_var = tk.StringVar()
        self.progress_var.set("准备就绪")
        
        # Setup the layout
        self.columnconfigure(0, weight=1)
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(self, mode='indeterminate')
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # Status label
        ttk.Label(self, textvariable=self.progress_var).grid(row=1, column=0)
    
    def start_progress(self):
        """Start the progress bar animation"""
        self.progress_bar.start()
    
    def stop_progress(self):
        """Stop the progress bar animation"""
        self.progress_bar.stop()
    
    def set_status(self, status):
        """Set the status text"""
        self.progress_var.set(status)


class LogDisplay(ttk.LabelFrame):
    """A scrollable text area for displaying log messages"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, text="处理日志 (Processing Log)", padding="5", **kwargs)
        
        # Setup the layout
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        # Scrollable text area
        self.log_text = scrolledtext.ScrolledText(self, height=15, width=80)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    def add_message(self, message):
        """Add a message to the log display"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
    
    def clear(self):
        """Clear all messages from the log display"""
        self.log_text.delete(1.0, tk.END)
    
    def update_display(self):
        """Force update the display to show latest changes"""
        self.update_idletasks()


class ButtonPanel(ttk.Frame):
    """A frame containing control buttons"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Start processing button
        self.start_button = ttk.Button(self, text="开始处理 (Start Processing)")
        self.start_button.grid(row=0, column=0, padx=5)
        
        # Clear log button
        self.clear_log_button = ttk.Button(self, text="清空日志")
        self.clear_log_button.grid(row=0, column=1, padx=5)
    
    def set_start_command(self, command):
        """Set the command for the start button"""
        self.start_button.config(command=command)
    
    def set_clear_log_command(self, command):
        """Set the command for the clear log button"""
        self.clear_log_button.config(command=command)
    
    def set_start_button_state(self, state):
        """Enable or disable the start button"""
        self.start_button.config(state=state)
