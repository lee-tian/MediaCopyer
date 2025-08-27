#!/usr/bin/env python3
"""
Custom widgets and UI components for Media Copyer GUI
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
from .i18n import i18n, _, I18nMixin
from .styles import ModernStyle, ModernWidget, configure_modern_style


class DirectorySelector(ttk.Frame, I18nMixin):
    """A modern directory selector with improved styling"""
    
    def __init__(self, parent, label_text, browse_title, **kwargs):
        super().__init__(parent, style='Surface.TFrame', **kwargs)
        
        self.directory_var = tk.StringVar()
        self.browse_title = browse_title
        self.label_text = label_text
        
        # Setup the layout with better spacing
        self.columnconfigure(1, weight=1)
        
        # Store widget references for updating texts
        self._setup_widgets()
    
    def _setup_widgets(self):
        """Setup the modern widgets"""
        # Create a container frame for better organization
        container = ttk.Frame(self, style='Surface.TFrame')
        container.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), 
                      padx=ModernStyle.PADDING_MD, pady=ModernStyle.PADDING_SM)
        container.columnconfigure(1, weight=1)
        
        # Modern label
        self.label = ModernWidget.create_title_label(container, self.label_text)
        self.label.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, ModernStyle.PADDING_SM))
        
        # Modern entry field
        self.entry = ModernWidget.create_modern_entry(container, textvariable=self.directory_var)
        self.entry.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=(0, ModernStyle.PADDING_SM))
        
        # Modern browse button
        self.browse_button = ModernWidget.create_secondary_button(container, _("browse"), command=self._on_browse)
        self.browse_button.grid(row=1, column=1, sticky=tk.W)
    
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
    """A modern progress display with enhanced styling"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, style='Surface.TFrame', **kwargs)
        
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
        if self.progress_var.get() in ["准备就绪", "Ready"]:
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
            # Switch to determinate mode if not already
            if self.progress_bar.cget('mode') == 'indeterminate':
                self.progress_bar.stop()
                self.progress_bar.config(mode='determinate', maximum=100, value=0)
            
            # Update progress value and percentage display
            self.progress_bar.config(value=percentage)
            self.percentage_var.set(f"{percentage:.1f}% ({current}/{total})")
    
    def set_status(self, status):
        """Set the status text"""
        self.progress_var.set(status)
    
    def reset_progress(self):
        """Reset progress bar to initial state"""
        self.progress_bar.config(mode='indeterminate', value=0)
        self.percentage_var.set("")
        self.progress_var.set(_("ready_status"))


class LogDisplay(ttk.LabelFrame, I18nMixin):
    """A modern scrollable text area for displaying log messages"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, text=_("processing_log"), 
                        style='Modern.TLabelframe', **kwargs)
        
        # Setup the layout
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        # Create container with padding
        container = ttk.Frame(self, style='Surface.TFrame')
        container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), 
                      padx=ModernStyle.PADDING_MD, pady=ModernStyle.PADDING_MD)
        container.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)
        
        # Compact scrollable text area
        self.log_text = scrolledtext.ScrolledText(container, height=8, width=80,
                                                 font=('Consolas', 9),
                                                 bg=ModernStyle.SURFACE,
                                                 fg=ModernStyle.TEXT_PRIMARY,
                                                 selectbackground=ModernStyle.PRIMARY,
                                                 relief='flat',
                                                 borderwidth=1)
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
    """A modern frame containing control buttons"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, style='Surface.TFrame', **kwargs)
        
        # Create container with modern spacing
        container = ttk.Frame(self, style='Surface.TFrame')
        container.grid(row=0, column=0, sticky=(tk.W, tk.E), 
                      padx=ModernStyle.PADDING_MD, pady=ModernStyle.PADDING_MD)
        
        # Modern start processing button (primary)
        self.start_button = ModernWidget.create_modern_button(container, _("start_processing"))
        self.start_button.grid(row=0, column=0, padx=(0, ModernStyle.PADDING_SM))
        
        # Modern clear log button (secondary)
        self.clear_log_button = ModernWidget.create_secondary_button(container, _("clear_log"))
        self.clear_log_button.grid(row=0, column=1)
    
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
