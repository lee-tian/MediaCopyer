#!/usr/bin/env python3
"""
Options frame containing all the configuration options for the media copyer
"""

import tkinter as tk
from tkinter import ttk
from .i18n import i18n, _, I18nMixin
from .styles import ModernStyle, ModernWidget


class OptionsFrame(ttk.LabelFrame, I18nMixin):
    """Frame containing all processing options and settings"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, text=_("options"), 
                        style='Modern.TLabelframe', **kwargs)
        
        # Initialize variables
        self.move_mode = tk.BooleanVar()
        self.dry_run = tk.BooleanVar()
        self.md5_check = tk.BooleanVar()
        self.organization_mode = tk.StringVar(value="date")
        
        # Store references to widgets for updating texts
        self._widgets = {}
        
        self._setup_options()
    
    def _setup_options(self):
        """Setup all the option widgets with compact modern styling"""
        # Create container with reduced padding for compact layout
        container = ttk.Frame(self, style='Surface.TFrame')
        container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), 
                      padx=ModernStyle.PADDING_SM, pady=ModernStyle.PADDING_SM)
        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)
        
        # Left column for checkboxes
        checkbox_frame = ttk.Frame(container, style='Surface.TFrame')
        checkbox_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N), 
                           padx=(0, ModernStyle.PADDING_MD))
        
        # Move mode checkbox with compact style
        self._widgets['move_mode'] = ttk.Checkbutton(
            checkbox_frame, 
            text=_("move_mode"), 
            variable=self.move_mode,
            style='Modern.TCheckbutton'
        )
        self._widgets['move_mode'].grid(row=0, column=0, sticky=tk.W, 
                                       pady=(0, ModernStyle.PADDING_XS))
        
        # Dry run checkbox with compact style
        self._widgets['dry_run'] = ttk.Checkbutton(
            checkbox_frame, 
            text=_("dry_run_mode"), 
            variable=self.dry_run,
            style='Modern.TCheckbutton'
        )
        self._widgets['dry_run'].grid(row=1, column=0, sticky=tk.W,
                                     pady=(0, ModernStyle.PADDING_XS))
        
        # MD5 integrity check checkbox with compact style
        self._widgets['md5_check'] = ttk.Checkbutton(
            checkbox_frame, 
            text=_("md5_verification"), 
            variable=self.md5_check,
            style='Modern.TCheckbutton'
        )
        self._widgets['md5_check'].grid(row=2, column=0, sticky=tk.W)
        
        # Right column for organization mode
        org_frame = ttk.Frame(container, style='Surface.TFrame')
        org_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N))
        
        # Organization mode selection with compact styling
        self._widgets['org_mode_label'] = ttk.Label(org_frame, 
                                                  text=_("organization_mode") + ":",
                                                  style='Subtitle.TLabel')
        self._widgets['org_mode_label'].grid(row=0, column=0, sticky=tk.W, 
                                          pady=(0, ModernStyle.PADDING_XS))
        
        # Organization mode radio buttons with compact styling
        self._widgets['mode_date'] = ttk.Radiobutton(
            org_frame, 
            text=_("org_mode_date"), 
            variable=self.organization_mode, 
            value="date",
            style='Modern.TRadiobutton'
        )
        self._widgets['mode_date'].grid(row=1, column=0, sticky=tk.W,
                                       pady=(0, ModernStyle.PADDING_XS))
        
        self._widgets['mode_device'] = ttk.Radiobutton(
            org_frame, 
            text=_("org_mode_device"), 
            variable=self.organization_mode, 
            value="device",
            style='Modern.TRadiobutton'
        )
        self._widgets['mode_device'].grid(row=2, column=0, sticky=tk.W,
                                         pady=(0, ModernStyle.PADDING_XS))
        
        self._widgets['mode_date_device'] = ttk.Radiobutton(
            org_frame, 
            text=_("org_mode_date_device"), 
            variable=self.organization_mode, 
            value="date_device",
            style='Modern.TRadiobutton'
        )
        self._widgets['mode_date_device'].grid(row=3, column=0, sticky=tk.W)
    
    def update_texts(self):
        """Update all UI texts when language changes"""
        # Update frame title
        self.config(text=_("options"))
        
        # Update widget texts
        if hasattr(self, '_widgets'):
            self._widgets['move_mode'].config(text=_("move_mode"))
            self._widgets['dry_run'].config(text=_("dry_run_mode"))
            self._widgets['md5_check'].config(text=_("md5_verification"))
            self._widgets['org_mode_label'].config(text=_("organization_mode") + ":")
            self._widgets['mode_date'].config(text=_("org_mode_date"))
            self._widgets['mode_device'].config(text=_("org_mode_device"))
            self._widgets['mode_date_device'].config(text=_("org_mode_date_device"))
    
    def get_move_mode(self):
        """Get the move mode setting"""
        return self.move_mode.get()
    
    def get_dry_run(self):
        """Get the dry run setting"""
        return self.dry_run.get()
    
    def get_md5_check(self):
        """Get the MD5 check setting"""
        return self.md5_check.get()
    
    def get_organization_mode(self):
        """Get the organization mode setting"""
        return self.organization_mode.get()
    
    def set_move_mode(self, value):
        """Set the move mode setting"""
        self.move_mode.set(value)
    
    def set_dry_run(self, value):
        """Set the dry run setting"""
        self.dry_run.set(value)
    
    def set_md5_check(self, value):
        """Set the MD5 check setting"""
        self.md5_check.set(value)
    
    def set_organization_mode(self, value):
        """Set the organization mode setting"""
        self.organization_mode.set(value)
