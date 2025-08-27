#!/usr/bin/env python3
"""
Modern UI styling and theming for Media Copyer
"""

import tkinter as tk
from tkinter import ttk


class ModernStyle:
    """Modern color scheme and styling constants"""
    
    # Color palette - Modern blue-gray theme
    PRIMARY = "#2563EB"      # Modern blue
    PRIMARY_DARK = "#1E40AF"  # Darker blue for hover
    SECONDARY = "#64748B"     # Gray-blue
    BACKGROUND = "#F8FAFC"    # Light gray background
    SURFACE = "#FFFFFF"       # White surface
    SURFACE_ALT = "#F1F5F9"   # Alternate surface
    BORDER = "#E2E8F0"        # Light border
    TEXT_PRIMARY = "#0F172A"  # Dark text
    TEXT_SECONDARY = "#64748B" # Gray text
    SUCCESS = "#10B981"       # Green
    WARNING = "#F59E0B"       # Orange
    ERROR = "#EF4444"         # Red
    
    # Spacing
    PADDING_XS = 4
    PADDING_SM = 8
    PADDING_MD = 12
    PADDING_LG = 16
    PADDING_XL = 24
    
    # Border radius (simulated with relief and borderwidth)
    BORDER_RADIUS = 6
    
    # Fonts
    FONT_FAMILY = "SF Pro Display" if tk.TkVersion >= 8.6 else "Helvetica"
    FONT_SIZE_SM = 11
    FONT_SIZE_MD = 12
    FONT_SIZE_LG = 14
    FONT_SIZE_XL = 16


def configure_modern_style():
    """Configure ttk styles for modern appearance"""
    style = ttk.Style()
    
    # Use a modern theme as base
    try:
        style.theme_use('clam')
    except:
        style.theme_use('default')
    
    # Configure main frame style
    style.configure('Modern.TFrame',
                   background=ModernStyle.BACKGROUND,
                   relief='flat')
    
    # Configure surface frame style
    style.configure('Surface.TFrame',
                   background=ModernStyle.SURFACE,
                   relief='flat',
                   borderwidth=1)
    
    # Configure card-like frame style
    style.configure('Card.TFrame',
                   background=ModernStyle.SURFACE,
                   relief='solid',
                   borderwidth=1)
    
    # Configure labels
    style.configure('Modern.TLabel',
                   background=ModernStyle.SURFACE,
                   foreground=ModernStyle.TEXT_PRIMARY,
                   font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_MD))
    
    style.configure('Title.TLabel',
                   background=ModernStyle.SURFACE,
                   foreground=ModernStyle.TEXT_PRIMARY,
                   font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_LG, 'bold'))
    
    style.configure('Subtitle.TLabel',
                   background=ModernStyle.SURFACE,
                   foreground=ModernStyle.TEXT_SECONDARY,
                   font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_SM))
    
    # Configure buttons
    style.configure('Modern.TButton',
                   background=ModernStyle.PRIMARY,
                   foreground='white',
                   font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_MD, 'bold'),
                   focuscolor='none',
                   relief='flat',
                   borderwidth=0,
                   padding=(ModernStyle.PADDING_MD, ModernStyle.PADDING_SM))
    
    style.map('Modern.TButton',
             background=[('active', ModernStyle.PRIMARY_DARK),
                        ('pressed', ModernStyle.PRIMARY_DARK)])
    
    # Secondary button style
    style.configure('Secondary.TButton',
                   background=ModernStyle.SURFACE,
                   foreground=ModernStyle.TEXT_PRIMARY,
                   font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_MD),
                   focuscolor='none',
                   relief='solid',
                   borderwidth=1,
                   padding=(ModernStyle.PADDING_MD, ModernStyle.PADDING_SM))
    
    style.map('Secondary.TButton',
             background=[('active', ModernStyle.SURFACE_ALT),
                        ('pressed', ModernStyle.SURFACE_ALT)])
    
    # Configure entry fields
    style.configure('Modern.TEntry',
                   fieldbackground=ModernStyle.SURFACE,
                   foreground=ModernStyle.TEXT_PRIMARY,
                   borderwidth=1,
                   relief='solid',
                   insertcolor=ModernStyle.PRIMARY,
                   font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_MD),
                   padding=(ModernStyle.PADDING_SM, ModernStyle.PADDING_SM))
    
    style.map('Modern.TEntry',
             bordercolor=[('focus', ModernStyle.PRIMARY),
                         ('!focus', ModernStyle.BORDER)])
    
    # Configure checkbuttons
    style.configure('Modern.TCheckbutton',
                   background=ModernStyle.SURFACE,
                   foreground=ModernStyle.TEXT_PRIMARY,
                   font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_MD),
                   focuscolor='none')
    
    # Configure radiobuttons
    style.configure('Modern.TRadiobutton',
                   background=ModernStyle.SURFACE,
                   foreground=ModernStyle.TEXT_PRIMARY,
                   font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_MD),
                   focuscolor='none')
    
    # Configure progress bar
    style.configure('Modern.Horizontal.TProgressbar',
                   background=ModernStyle.PRIMARY,
                   troughcolor=ModernStyle.SURFACE_ALT,
                   borderwidth=0,
                   lightcolor=ModernStyle.PRIMARY,
                   darkcolor=ModernStyle.PRIMARY)
    
    # Configure labelframes
    style.configure('Modern.TLabelframe',
                   background=ModernStyle.SURFACE,
                   relief='solid',
                   borderwidth=1,
                   labelmargins=(ModernStyle.PADDING_SM, 0, 0, 0))
    
    style.configure('Modern.TLabelframe.Label',
                   background=ModernStyle.SURFACE,
                   foreground=ModernStyle.TEXT_PRIMARY,
                   font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_MD, 'bold'))
    
    # Configure separator
    style.configure('Modern.TSeparator',
                   background=ModernStyle.BORDER)
    
    return style


class ModernWidget:
    """Helper class for creating modern-styled widgets"""
    
    @staticmethod
    def create_card_frame(parent, **kwargs):
        """Create a card-like frame with modern styling"""
        return ttk.Frame(parent, style='Card.TFrame', **kwargs)
    
    @staticmethod
    def create_title_label(parent, text, **kwargs):
        """Create a title label with modern styling"""
        return ttk.Label(parent, text=text, style='Title.TLabel', **kwargs)
    
    @staticmethod
    def create_subtitle_label(parent, text, **kwargs):
        """Create a subtitle label with modern styling"""
        return ttk.Label(parent, text=text, style='Subtitle.TLabel', **kwargs)
    
    @staticmethod
    def create_modern_button(parent, text, **kwargs):
        """Create a modern primary button"""
        return ttk.Button(parent, text=text, style='Modern.TButton', **kwargs)
    
    @staticmethod
    def create_secondary_button(parent, text, **kwargs):
        """Create a modern secondary button"""
        return ttk.Button(parent, text=text, style='Secondary.TButton', **kwargs)
    
    @staticmethod
    def create_modern_entry(parent, **kwargs):
        """Create a modern entry field"""
        return ttk.Entry(parent, style='Modern.TEntry', **kwargs)
    
    @staticmethod
    def create_modern_checkbutton(parent, text, **kwargs):
        """Create a modern checkbutton"""
        return ttk.Checkbutton(parent, text=text, style='Modern.TCheckbutton', **kwargs)
    
    @staticmethod
    def create_modern_radiobutton(parent, text, **kwargs):
        """Create a modern radiobutton"""
        return ttk.Radiobutton(parent, text=text, style='Modern.TRadiobutton', **kwargs)
    
    @staticmethod
    def create_modern_labelframe(parent, text, **kwargs):
        """Create a modern labelframe"""
        return ttk.LabelFrame(parent, text=text, style='Modern.TLabelframe', **kwargs)
    
    @staticmethod
    def create_modern_separator(parent, **kwargs):
        """Create a modern separator"""
        return ttk.Separator(parent, style='Modern.TSeparator', **kwargs)
