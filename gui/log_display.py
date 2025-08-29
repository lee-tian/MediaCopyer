#!/usr/bin/env python3
"""
Log display widget for Media Copyer GUI
"""

import tkinter as tk
from tkinter import ttk
from .i18n import i18n, _, I18nMixin
from .styles import ModernStyle, ModernWidget


class LogDisplay(ttk.Frame, I18nMixin):
    """A scrollable log display with modern styling"""
    
    def __init__(self, parent, **kwargs):
        ttk.Frame.__init__(self, parent, style='Surface.TFrame', **kwargs)
        I18nMixin.__init__(self)
        
        # Setup the layout
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        
        # Title label
        title_label = ttk.Label(self, text=_("log_title"), style='Title.TLabel')
        title_label.grid(row=0, column=0, sticky=(tk.W, tk.E), 
                        padx=ModernStyle.PADDING_MD, pady=(ModernStyle.PADDING_MD, 0))
        
        # Create scrollable text area
        text_frame = ttk.Frame(self, style='Surface.TFrame')
        text_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), 
                       padx=ModernStyle.PADDING_MD, pady=ModernStyle.PADDING_MD)
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        # Text widget with scrollbar
        self.text_widget = tk.Text(text_frame, 
                                  wrap=tk.WORD, 
                                  state='disabled',
                                  height=10,
                                  font=('Consolas', 10) if tk.sys.platform == 'win32' else ('Monaco', 10),
                                  bg='#ffffff',
                                  fg='#333333',
                                  selectbackground='#0078d4',
                                  selectforeground='#ffffff',
                                  relief='flat',
                                  borderwidth=1,
                                  highlightthickness=1,
                                  highlightcolor='#0078d4',
                                  highlightbackground='#e1e1e1')
        
        # Configure text tags for different log levels
        self.text_widget.tag_configure('info', foreground='#333333')
        self.text_widget.tag_configure('success', foreground='#107c10')
        self.text_widget.tag_configure('warning', foreground='#ff8c00')
        self.text_widget.tag_configure('error', foreground='#d13438')
        self.text_widget.tag_configure('debug', foreground='#6c6c6c')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(text_frame, orient='vertical', command=self.text_widget.yview)
        self.text_widget.configure(yscrollcommand=scrollbar.set)
        
        # Grid layout
        self.text_widget.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Control frame
        control_frame = ttk.Frame(self, style='Surface.TFrame')
        control_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), 
                          padx=ModernStyle.PADDING_MD, pady=(0, ModernStyle.PADDING_MD))
        
        # Clear button
        self.clear_button = ModernWidget.create_secondary_button(control_frame, _("clear_log"), 
                                                               command=self.clear_log)
        self.clear_button.pack(side='right')
        
        # Auto-scroll checkbox
        self.auto_scroll_var = tk.BooleanVar(value=True)
        self.auto_scroll_check = ttk.Checkbutton(control_frame, 
                                               text=_("auto_scroll"), 
                                               variable=self.auto_scroll_var,
                                               style='Modern.TCheckbutton')
        self.auto_scroll_check.pack(side='left')
        
        self.max_lines = 1000  # Maximum number of lines to keep
    
    def update_texts(self):
        """Update texts when language changes"""
        # Find the title label and update it
        for child in self.winfo_children():
            if isinstance(child, ttk.Label) and hasattr(child, 'cget'):
                try:
                    if 'Title' in str(child.cget('style')):
                        child.config(text=_("log_title"))
                        break
                except:
                    pass
        
        # Update button and checkbox texts
        self.clear_button.config(text=_("clear_log"))
        self.auto_scroll_check.config(text=_("auto_scroll"))
    
    def add_log(self, message, level='info'):
        """Add a log message with specified level
        
        Args:
            message: The message to log
            level: Log level ('info', 'success', 'warning', 'error', 'debug')
        """
        self.text_widget.config(state='normal')
        
        # Add timestamp
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        # Insert the message with appropriate tag
        self.text_widget.insert(tk.END, formatted_message, level)
        
        # Limit the number of lines
        self._trim_lines()
        
        # Auto-scroll if enabled
        if self.auto_scroll_var.get():
            self.text_widget.see(tk.END)
        
        self.text_widget.config(state='disabled')
        
        # Update the display
        self.text_widget.update_idletasks()
    
    def _trim_lines(self):
        """Trim the text widget to maintain max_lines"""
        lines = self.text_widget.get('1.0', tk.END).split('\n')
        if len(lines) > self.max_lines:
            # Remove excess lines from the beginning
            excess_lines = len(lines) - self.max_lines
            self.text_widget.delete('1.0', f'{excess_lines + 1}.0')
    
    def clear_log(self):
        """Clear all log messages"""
        self.text_widget.config(state='normal')
        self.text_widget.delete('1.0', tk.END)
        self.text_widget.config(state='disabled')
    
    def log_info(self, message):
        """Log an info message"""
        self.add_log(message, 'info')
    
    def log_success(self, message):
        """Log a success message"""
        self.add_log(message, 'success')
    
    def log_warning(self, message):
        """Log a warning message"""
        self.add_log(message, 'warning')
    
    def log_error(self, message):
        """Log an error message"""
        self.add_log(message, 'error')
    
    def log_debug(self, message):
        """Log a debug message"""
        self.add_log(message, 'debug')
    
    def set_auto_scroll(self, enabled):
        """Enable or disable auto-scroll"""
        self.auto_scroll_var.set(enabled)
    
    def add_message(self, message, level='info'):
        """Add a message (compatibility method for add_log)"""
        self.add_log(message, level)
    
    def update_display(self):
        """Update the display (compatibility method)"""
        self.text_widget.update_idletasks()
