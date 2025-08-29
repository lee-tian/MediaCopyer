#!/usr/bin/env python3
"""
Control buttons widget for Media Copyer GUI
"""

import tkinter as tk
from tkinter import ttk
from .i18n import i18n, _, I18nMixin
from .styles import ModernStyle, ModernWidget


class ControlButtons(ttk.Frame, I18nMixin):
    """Control buttons with modern styling for main operations"""
    
    def __init__(self, parent, **kwargs):
        ttk.Frame.__init__(self, parent, style='Surface.TFrame', **kwargs)
        I18nMixin.__init__(self)
        
        self.scan_command = None
        self.copy_command = None
        self.stop_command = None
        
        # Setup the layout
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        
        # Create container frame with modern spacing
        container = ttk.Frame(self, style='Surface.TFrame')
        container.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), 
                      padx=ModernStyle.PADDING_MD, pady=ModernStyle.PADDING_MD)
        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)
        container.columnconfigure(2, weight=1)
        
        # Scan button - primary action
        self.scan_button = ModernWidget.create_primary_button(container, _("scan_media"), 
                                                             command=self._on_scan)
        self.scan_button.grid(row=0, column=0, sticky=(tk.W, tk.E), 
                             padx=(0, ModernStyle.PADDING_SM))
        
        # Copy button - primary action
        self.copy_button = ModernWidget.create_primary_button(container, _("copy_media"), 
                                                             command=self._on_copy)
        self.copy_button.grid(row=0, column=1, sticky=(tk.W, tk.E), 
                             padx=ModernStyle.PADDING_SM)
        self.copy_button.config(state='disabled')  # Initially disabled
        
        # Stop button - danger action
        self.stop_button = ModernWidget.create_danger_button(container, _("stop_operation"), 
                                                            command=self._on_stop)
        self.stop_button.grid(row=0, column=2, sticky=(tk.W, tk.E), 
                             padx=(ModernStyle.PADDING_SM, 0))
        self.stop_button.config(state='disabled')  # Initially disabled
    
    def _on_scan(self):
        """Handle scan button click"""
        if self.scan_command:
            self.scan_command()
    
    def _on_copy(self):
        """Handle copy button click"""
        if self.copy_command:
            self.copy_command()
    
    def _on_stop(self):
        """Handle stop button click"""
        if self.stop_command:
            self.stop_command()
    
    def set_scan_command(self, command):
        """Set the command for the scan button"""
        self.scan_command = command
    
    def set_copy_command(self, command):
        """Set the command for the copy button"""
        self.copy_command = command
    
    def set_stop_command(self, command):
        """Set the command for the stop button"""
        self.stop_command = command
    
    def set_scan_enabled(self, enabled):
        """Enable/disable the scan button"""
        self.scan_button.config(state='normal' if enabled else 'disabled')
    
    def set_copy_enabled(self, enabled):
        """Enable/disable the copy button"""
        self.copy_button.config(state='normal' if enabled else 'disabled')
    
    def set_stop_enabled(self, enabled):
        """Enable/disable the stop button"""
        self.stop_button.config(state='normal' if enabled else 'disabled')
    
    def update_texts(self):
        """Update texts when language changes"""
        self.scan_button.config(text=_("scan_media"))
        self.copy_button.config(text=_("copy_media"))
        self.stop_button.config(text=_("stop_operation"))
    
    def set_operation_state(self, state):
        """Set the operation state for proper button enabling/disabling
        
        Args:
            state: 'idle', 'scanning', 'copying', or 'ready_to_copy'
        """
        if state == 'idle':
            self.set_scan_enabled(True)
            self.set_copy_enabled(False)
            self.set_stop_enabled(False)
        elif state == 'scanning':
            self.set_scan_enabled(False)
            self.set_copy_enabled(False)
            self.set_stop_enabled(True)
        elif state == 'copying':
            self.set_scan_enabled(False)
            self.set_copy_enabled(False)
            self.set_stop_enabled(True)
        elif state == 'ready_to_copy':
            self.set_scan_enabled(True)
            self.set_copy_enabled(True)
            self.set_stop_enabled(False)
