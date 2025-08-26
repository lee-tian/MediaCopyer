#!/usr/bin/env python3
"""
Custom widgets and UI components for Media Copyer GUI
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
from .i18n import i18n, _, I18nMixin


class DirectorySelector(ttk.Frame, I18nMixin):
    """A frame containing an entry field and browse button for directory selection"""
    
    def __init__(self, parent, label_text, browse_title, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.directory_var = tk.StringVar()
        self.browse_title = browse_title
        self.label_text = label_text
        
        # Setup the layout
        self.columnconfigure(1, weight=1)
        
        # Store widget references for updating texts
        self._setup_widgets()
    
    def _setup_widgets(self):
        """Setup the widgets"""
        # Label
        self.label = ttk.Label(self, text=self.label_text)
        self.label.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        # Entry field
        self.entry = ttk.Entry(self, textvariable=self.directory_var, width=50)
        self.entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 5))
        
        # Browse button
        self.browse_button = ttk.Button(self, text=_("browse"), command=self._on_browse)
        self.browse_button.grid(row=0, column=2, pady=5)
    
    def _on_browse(self):
        """Open file dialog to select directory"""
        directory = filedialog.askdirectory(title=self.browse_title)
        if directory:
            self.directory_var.set(directory)
    
    def update_texts(self, label_text, browse_title):
        """Update texts when language changes"""
        self.label_text = label_text
        self.browse_title = browse_title
        self.label.config(text=label_text)
        self.browse_button.config(text=_("browse"))
    
    def get_directory(self):
        """Get the selected directory path"""
        return self.directory_var.get()
    
    def set_directory(self, path):
        """Set the directory path"""
        self.directory_var.set(path)


class ProgressDisplay(ttk.Frame, I18nMixin):
    """A frame containing progress bar and status label"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.progress_var = tk.StringVar()
        self.progress_var.set(_("ready_status"))
        
        # Setup the layout
        self.columnconfigure(0, weight=1)
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(self, mode='indeterminate')
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # Status label
        self.status_label = ttk.Label(self, textvariable=self.progress_var)
        self.status_label.grid(row=1, column=0)
    
    def update_texts(self):
        """Update texts when language changes"""
        # Update current status if it's still the default
        if self.progress_var.get() in ["准备就绪", "Ready"]:
            self.progress_var.set(_("ready_status"))
    
    def start_progress(self):
        """Start the progress bar animation"""
        self.progress_bar.start()
    
    def stop_progress(self):
        """Stop the progress bar animation"""
        self.progress_bar.stop()
    
    def set_status(self, status):
        """Set the status text"""
        self.progress_var.set(status)


class LogDisplay(ttk.LabelFrame, I18nMixin):
    """A scrollable text area for displaying log messages"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, text=_("processing_log"), padding="5", **kwargs)
        
        # Setup the layout
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        # Scrollable text area
        self.log_text = scrolledtext.ScrolledText(self, height=15, width=80)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    def update_texts(self):
        """Update texts when language changes"""
        self.config(text=_("processing_log"))
    
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


class ButtonPanel(ttk.Frame, I18nMixin):
    """A frame containing control buttons"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Start processing button
        self.start_button = ttk.Button(self, text=_("start_processing"))
        self.start_button.grid(row=0, column=0, padx=5)
        
        # Clear log button
        self.clear_log_button = ttk.Button(self, text=_("clear_log"))
        self.clear_log_button.grid(row=0, column=1, padx=5)
    
    def update_texts(self):
        """Update texts when language changes"""
        self.start_button.config(text=_("start_processing"))
        self.clear_log_button.config(text=_("clear_log"))
    
    def set_start_command(self, command):
        """Set the command for the start button"""
        self.start_button.config(command=command)
    
    def set_clear_log_command(self, command):
        """Set the command for the clear log button"""
        self.clear_log_button.config(command=command)
    
    def set_start_button_state(self, state):
        """Enable or disable the start button"""
        self.start_button.config(state=state)
