#!/usr/bin/env python3
"""
Options frame containing all the configuration options for the media copyer
"""

import tkinter as tk
from tkinter import ttk


class OptionsFrame(ttk.LabelFrame):
    """Frame containing all processing options and settings"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, text="选项 (Options)", padding="10", **kwargs)
        
        # Initialize variables
        self.move_mode = tk.BooleanVar()
        self.dry_run = tk.BooleanVar()
        self.organization_mode = tk.StringVar(value="date")
        
        self._setup_options()
    
    def _setup_options(self):
        """Setup all the option widgets"""
        # Move mode checkbox
        ttk.Checkbutton(
            self, 
            text="移动模式 (Move files instead of copy)", 
            variable=self.move_mode
        ).grid(row=0, column=0, sticky=tk.W)
        
        # Dry run checkbox
        ttk.Checkbutton(
            self, 
            text="试运行模式 (Dry run - preview only)", 
            variable=self.dry_run
        ).grid(row=1, column=0, sticky=tk.W)
        
        # Organization mode selection
        ttk.Label(self, text="组织方式 (Organization Mode):").grid(row=2, column=0, sticky=tk.W, pady=(10,5))
        
        mode_frame = ttk.Frame(self)
        mode_frame.grid(row=3, column=0, sticky=tk.W, padx=(20, 0))
        
        # Organization mode radio buttons
        ttk.Radiobutton(
            mode_frame, 
            text="按日期 (By Date): Video/2025/2025-07-25", 
            variable=self.organization_mode, 
            value="date"
        ).grid(row=0, column=0, sticky=tk.W)
        
        ttk.Radiobutton(
            mode_frame, 
            text="按设备 (By Device): Video/2025/DJI", 
            variable=self.organization_mode, 
            value="device"
        ).grid(row=1, column=0, sticky=tk.W)
        
        ttk.Radiobutton(
            mode_frame, 
            text="按日期+设备 (By Date+Device): Video/2025/2025-07-25/DJI", 
            variable=self.organization_mode, 
            value="date_device"
        ).grid(row=2, column=0, sticky=tk.W)
    
    def get_move_mode(self):
        """Get the move mode setting"""
        return self.move_mode.get()
    
    def get_dry_run(self):
        """Get the dry run setting"""
        return self.dry_run.get()
    
    def get_organization_mode(self):
        """Get the organization mode setting"""
        return self.organization_mode.get()
    
    def set_move_mode(self, value):
        """Set the move mode setting"""
        self.move_mode.set(value)
    
    def set_dry_run(self, value):
        """Set the dry run setting"""
        self.dry_run.set(value)
    
    def set_organization_mode(self, value):
        """Set the organization mode setting"""
        self.organization_mode.set(value)
