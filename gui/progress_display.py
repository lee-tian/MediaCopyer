#!/usr/bin/env python3
"""
Progress display widget for Media Copyer GUI
"""

import tkinter as tk
from tkinter import ttk
from .i18n import i18n, _, I18nMixin
from .styles import ModernStyle, ModernWidget


class ProgressDisplay(ttk.Frame, I18nMixin):
    """A modern progress display with enhanced styling"""
    
    def __init__(self, parent, **kwargs):
        ttk.Frame.__init__(self, parent, style='Surface.TFrame', **kwargs)
        I18nMixin.__init__(self)
        
        self.progress_var = tk.StringVar()
        self.progress_var.set(_("ready_status"))
        self.percentage_var = tk.StringVar()
        self.percentage_var.set("")
        
        # Setup the layout with modern spacing
        self.columnconfigure(0, weight=1)
        
        # Create container frame
        container = ttk.Frame(self, style='Surface.TFrame')
        container.grid(row=0, column=0, sticky=(tk.W, tk.E), 
                      padx=ModernStyle.PADDING_MD, pady=ModernStyle.PADDING_MD)
        container.columnconfigure(0, weight=1)
        
        # Modern progress bar
        self.progress_bar = ttk.Progressbar(container, mode='indeterminate',
                                          style='Modern.Horizontal.TProgressbar')
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), 
                              pady=(0, ModernStyle.PADDING_SM))
        
        # Percentage label with modern styling
        self.percentage_label = ttk.Label(container, textvariable=self.percentage_var,
                                        style='Subtitle.TLabel')
        self.percentage_label.grid(row=1, column=0, pady=(0, ModernStyle.PADDING_SM))
        
        # Status label with modern styling
        self.status_label = ttk.Label(container, textvariable=self.progress_var,
                                    style='Modern.TLabel')
        self.status_label.grid(row=2, column=0)
    
    def update_texts(self):
        """Update texts when language changes"""
        # Update current status if it's still the default
        current_status = self.progress_var.get()
        if current_status in ["准备就绪", "Ready"] or current_status == _("ready_status"):
            self.progress_var.set(_("ready_status"))
    
    def start_progress(self):
        """Start the progress bar animation in indeterminate mode"""
        self.progress_bar.config(mode='indeterminate')
        self.progress_bar.start()
        self.percentage_var.set("")
    
    def stop_progress(self):
        """Stop the progress bar animation"""
        self.progress_bar.stop()
    
    def set_progress(self, current, total):
        """Set the progress bar to determinate mode and update percentage"""
        if total > 0:
            percentage = (current / total) * 100
            # Force stop any animation and reset to determinate mode
            self.progress_bar.stop()
            # Brief delay to ensure animation stops
            self.progress_bar.after_idle(lambda: self._set_determinate_progress(percentage, current, total))
    
    def _set_determinate_progress(self, percentage, current, total):
        """Helper method to set determinate progress after ensuring animation has stopped"""
        # Configure as determinate mode with specific value
        self.progress_bar.config(mode='determinate', maximum=100)
        self.progress_bar['value'] = percentage
        
        # Update percentage display
        self.percentage_var.set(f"{percentage:.1f}% ({current}/{total})")
    
    def set_status(self, status):
        """Set the status text"""
        self.progress_var.set(status)
    
    def reset_progress(self):
        """Reset progress bar to initial state"""
        self.progress_bar.stop()
        self.progress_bar.config(mode='indeterminate', value=0)
        self.percentage_var.set("")
        self.progress_var.set(_("ready_status"))
