#!/usr/bin/env python3
"""
Directory selector widget for Media Copyer GUI
"""

import tkinter as tk
from tkinter import ttk, filedialog
from .i18n import i18n, _, I18nMixin
from .styles import ModernStyle, ModernWidget, configure_modern_style
from core.config import get_config


class DirectorySelector(ttk.Frame, I18nMixin):
    """A modern directory selector with improved styling and frequent directories"""
    
    def __init__(self, parent, label_key, browse_title_key, selector_type='source', **kwargs):
        ttk.Frame.__init__(self, parent, style='Surface.TFrame', **kwargs)
        I18nMixin.__init__(self)
        
        self.directory_var = tk.StringVar()
        self.browse_title_key = browse_title_key
        self.label_key = label_key
        self.selector_type = selector_type  # 'source' or 'destination'
        self.config = get_config()
        
        # Setup the layout with better spacing
        self.columnconfigure(1, weight=1)
        
        # Store widget references for updating texts
        self._setup_widgets()
        
        # Load last directory if remember is enabled
        self._load_last_directory()
    
    def _setup_widgets(self):
        """Setup the modern widgets"""
        # Create a container frame for better organization
        container = ttk.Frame(self, style='Surface.TFrame')
        container.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), 
                      padx=ModernStyle.PADDING_MD, pady=ModernStyle.PADDING_SM)
        container.columnconfigure(1, weight=1)
        
        # Modern label
        self.label = ModernWidget.create_title_label(container, _(self.label_key))
        self.label.grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, ModernStyle.PADDING_SM))
        
        # Row with entry, frequent dirs button, and browse button
        entry_frame = ttk.Frame(container, style='Surface.TFrame')
        entry_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E))
        entry_frame.columnconfigure(0, weight=1)
        
        # Modern entry field
        self.entry = ModernWidget.create_modern_entry(entry_frame, textvariable=self.directory_var)
        self.entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, ModernStyle.PADDING_SM))
        
        # Frequent directories button
        self.frequent_button = ModernWidget.create_secondary_button(entry_frame, "★", 
                                                                   command=self._show_frequent_menu)
        self.frequent_button.grid(row=0, column=1, padx=(0, ModernStyle.PADDING_SM))
        
        # Modern browse button
        self.browse_button = ModernWidget.create_secondary_button(entry_frame, _("browse"), 
                                                                 command=self._on_browse)
        self.browse_button.grid(row=0, column=2, sticky=tk.W)
    
    def _load_last_directory(self):
        """Load the last used directory if remember is enabled"""
        if self.config.get_remember_last_dirs():
            if self.selector_type == 'source':
                last_dirs = self.config.get_last_source_directories()
            else:
                last_dirs = self.config.get_last_destination_directories()
            
            if last_dirs:
                self.directory_var.set(last_dirs[0])
    
    def _show_frequent_menu(self):
        """Show menu with frequent directories"""
        if self.selector_type == 'source':
            frequent_dirs = self.config.get_frequent_source_directories()
        else:
            frequent_dirs = self.config.get_frequent_destination_directories()
        
        if not frequent_dirs:
            return
        
        # Create popup menu
        menu = tk.Menu(self, tearoff=0)
        for directory in frequent_dirs:
            # Truncate long paths for display
            display_path = directory
            if len(directory) > 50:
                display_path = "..." + directory[-47:]
            
            menu.add_command(label=display_path, 
                           command=lambda d=directory: self._select_frequent_directory(d))
        
        # Show menu at button location
        try:
            menu.tk_popup(self.frequent_button.winfo_rootx(), 
                         self.frequent_button.winfo_rooty() + self.frequent_button.winfo_height())
        finally:
            menu.grab_release()
    
    def _select_frequent_directory(self, directory):
        """Select a directory from frequent directories"""
        self.directory_var.set(directory)
    
    def _on_browse(self):
        """Open file dialog to select directory"""
        directory = filedialog.askdirectory(title=_(self.browse_title_key))
        if directory:
            self.directory_var.set(directory)
            # Add to frequent directories
            if self.selector_type == 'source':
                self.config.add_frequent_source_directory(directory)
            else:
                self.config.add_frequent_destination_directory(directory)
    
    def update_texts(self):
        """Update texts when language changes"""
        # Update the label with the translated text
        self.label.config(text=_(self.label_key))
        self.browse_button.config(text=_("browse"))
    
    def get_directory(self):
        """Get the selected directory path"""
        directory = self.directory_var.get()
        # Save as last used directory
        if directory and self.config.get_remember_last_dirs():
            if self.selector_type == 'source':
                self.config.set_last_source_directories([directory])
            else:
                self.config.set_last_destination_directories([directory])
        return directory
    
    def set_directory(self, path):
        """Set the directory path"""
        self.directory_var.set(path)


class MultiSourceSelector(ttk.Frame, I18nMixin):
    """Widget for managing multiple source directories"""
    
    def __init__(self, parent, **kwargs):
        ttk.Frame.__init__(self, parent, style='Surface.TFrame', **kwargs)
        I18nMixin.__init__(self)
        
        self.config = get_config()
        self.source_directories = []
        self.directory_vars = []
        self.browse_buttons = []  # Store browse button references
        
        self.columnconfigure(0, weight=1)
        self._setup_widgets()
        self._load_last_directories()
    
    def _setup_widgets(self):
        """Setup the widgets for multiple source selection"""
        # Title
        self.title_label = ModernWidget.create_subtitle_label(self, _("source_directories"))
        self.title_label.grid(row=0, column=0, sticky=tk.W, pady=(0, ModernStyle.PADDING_XS))
        
        # Container for source entries
        self.sources_frame = ttk.Frame(self, style='Surface.TFrame')
        self.sources_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        self.sources_frame.columnconfigure(0, weight=1)
        
        # Add initial source selector
        self._add_source_selector()
        
        # Add source button
        add_button_frame = ttk.Frame(self, style='Surface.TFrame')
        add_button_frame.grid(row=2, column=0, sticky=tk.W, pady=(ModernStyle.PADDING_XS, 0))
        
        self.add_source_button = ModernWidget.create_secondary_button(
            add_button_frame, _("add_source"), command=self._add_source_selector
        )
        self.add_source_button.grid(row=0, column=0)
    
    def _add_source_selector(self):
        """Add a new source directory selector"""
        row = len(self.directory_vars)
        
        # Create frame for this source
        source_frame = ttk.Frame(self.sources_frame, style='Surface.TFrame')
        source_frame.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, ModernStyle.PADDING_XS))
        source_frame.columnconfigure(0, weight=1)
        
        # Directory variable
        dir_var = tk.StringVar()
        self.directory_vars.append(dir_var)
        
        # Entry frame
        entry_frame = ttk.Frame(source_frame, style='Surface.TFrame')
        entry_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        entry_frame.columnconfigure(0, weight=1)
        
        # Entry field
        entry = ModernWidget.create_modern_entry(entry_frame, textvariable=dir_var)
        entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, ModernStyle.PADDING_SM))
        
        # Frequent directories button
        frequent_button = ModernWidget.create_secondary_button(
            entry_frame, "★", command=lambda: self._show_frequent_menu(dir_var)
        )
        frequent_button.grid(row=0, column=1, padx=(0, ModernStyle.PADDING_SM))
        
        # Browse button
        browse_button = ModernWidget.create_secondary_button(
            entry_frame, _("browse"), command=lambda: self._browse_directory(dir_var)
        )
        browse_button.grid(row=0, column=2, padx=(0, ModernStyle.PADDING_SM))
        self.browse_buttons.append(browse_button)  # Store reference for updates
        
        # Remove button (only show if more than one source)
        if len(self.directory_vars) > 1:
            remove_button = ModernWidget.create_secondary_button(
                entry_frame, "✕", command=lambda f=source_frame, v=dir_var: self._remove_source(f, v)
            )
            remove_button.grid(row=0, column=3)
    
    def _remove_source(self, frame, dir_var):
        """Remove a source directory selector"""
        if len(self.directory_vars) > 1:
            # Find and remove the corresponding browse button from our list
            for widget in frame.winfo_children():
                if isinstance(widget, ttk.Frame):
                    for child in widget.winfo_children():
                        if isinstance(child, ttk.Button) and child in self.browse_buttons:
                            self.browse_buttons.remove(child)
                            break
            
            frame.destroy()
            self.directory_vars.remove(dir_var)
    
    def _browse_directory(self, dir_var):
        """Browse for a source directory"""
        directory = tk.filedialog.askdirectory(title=_("select_source_directory"))
        if directory:
            dir_var.set(directory)
            self.config.add_frequent_source_directory(directory)
    
    def _show_frequent_menu(self, dir_var):
        """Show menu with frequent source directories"""
        frequent_dirs = self.config.get_frequent_source_directories()
        if not frequent_dirs:
            return
        
        menu = tk.Menu(self, tearoff=0)
        for directory in frequent_dirs:
            display_path = directory
            if len(directory) > 50:
                display_path = "..." + directory[-47:]
            menu.add_command(label=display_path, command=lambda d=directory: dir_var.set(d))
        
        # Show menu at mouse position
        try:
            menu.tk_popup(self.winfo_pointerx(), self.winfo_pointery())
        finally:
            menu.grab_release()
    
    def _load_last_directories(self):
        """Load last used source directories"""
        if self.config.get_remember_last_dirs():
            last_dirs = self.config.get_last_source_directories()
            if last_dirs and self.directory_vars:
                self.directory_vars[0].set(last_dirs[0])
    
    def get_sources(self):
        """Get list of selected source directories"""
        sources = []
        for var in self.directory_vars:
            path = var.get().strip()
            if path and path not in sources:
                sources.append(path)
        return sources
    
    def update_texts(self):
        """Update texts when language changes"""
        self.title_label.config(text=_("source_directories"))
        self.add_source_button.config(text=_("add_source"))
        
        # Update all browse buttons
        for button in self.browse_buttons:
            try:
                button.config(text=_("browse"))
            except tk.TclError:
                # Button might have been destroyed, remove from list
                self.browse_buttons.remove(button)


class MultiDestinationSelector(ttk.Frame, I18nMixin):
    """Widget for managing multiple destination directories"""
    
    def __init__(self, parent, **kwargs):
        ttk.Frame.__init__(self, parent, style='Surface.TFrame', **kwargs)
        I18nMixin.__init__(self)
        
        self.config = get_config()
        self.destination_directories = []
        self.directory_vars = []
        self.browse_buttons = []  # Store browse button references
        
        self.columnconfigure(0, weight=1)
        self._setup_widgets()
        self._load_last_directories()
    
    def _setup_widgets(self):
        """Setup the widgets for multiple destination selection"""
        # Title
        self.title_label = ModernWidget.create_subtitle_label(self, _("destination_directories"))
        self.title_label.grid(row=0, column=0, sticky=tk.W, pady=(ModernStyle.PADDING_SM, ModernStyle.PADDING_XS))
        
        # Container for destination entries
        self.destinations_frame = ttk.Frame(self, style='Surface.TFrame')
        self.destinations_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        self.destinations_frame.columnconfigure(0, weight=1)
        
        # Add initial destination selector
        self._add_destination_selector()
        
        # Add destination button
        add_button_frame = ttk.Frame(self, style='Surface.TFrame')
        add_button_frame.grid(row=2, column=0, sticky=tk.W, pady=(ModernStyle.PADDING_XS, 0))
        
        self.add_dest_button = ModernWidget.create_secondary_button(
            add_button_frame, _("add_destination"), command=self._add_destination_selector
        )
        self.add_dest_button.grid(row=0, column=0)
    
    def _add_destination_selector(self):
        """Add a new destination directory selector"""
        row = len(self.directory_vars)
        
        # Create frame for this destination
        dest_frame = ttk.Frame(self.destinations_frame, style='Surface.TFrame')
        dest_frame.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, ModernStyle.PADDING_XS))
        dest_frame.columnconfigure(0, weight=1)
        
        # Directory variable
        dir_var = tk.StringVar()
        self.directory_vars.append(dir_var)
        
        # Entry frame
        entry_frame = ttk.Frame(dest_frame, style='Surface.TFrame')
        entry_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        entry_frame.columnconfigure(0, weight=1)
        
        # Entry field
        entry = ModernWidget.create_modern_entry(entry_frame, textvariable=dir_var)
        entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, ModernStyle.PADDING_SM))
        
        # Frequent directories button
        frequent_button = ModernWidget.create_secondary_button(
            entry_frame, "★", command=lambda: self._show_frequent_menu(dir_var)
        )
        frequent_button.grid(row=0, column=1, padx=(0, ModernStyle.PADDING_SM))
        
        # Browse button
        browse_button = ModernWidget.create_secondary_button(
            entry_frame, _("browse"), command=lambda: self._browse_directory(dir_var)
        )
        browse_button.grid(row=0, column=2, padx=(0, ModernStyle.PADDING_SM))
        self.browse_buttons.append(browse_button)  # Store reference for updates
        
        # Remove button (only show if more than one destination)
        if len(self.directory_vars) > 1:
            remove_button = ModernWidget.create_secondary_button(
                entry_frame, "✕", command=lambda f=dest_frame, v=dir_var: self._remove_destination(f, v)
            )
            remove_button.grid(row=0, column=3)
    
    def _remove_destination(self, frame, dir_var):
        """Remove a destination directory selector"""
        if len(self.directory_vars) > 1:
            # Find and remove the corresponding browse button from our list
            for widget in frame.winfo_children():
                if isinstance(widget, ttk.Frame):
                    for child in widget.winfo_children():
                        if isinstance(child, ttk.Button) and child in self.browse_buttons:
                            self.browse_buttons.remove(child)
                            break
            
            frame.destroy()
            self.directory_vars.remove(dir_var)
    
    def _browse_directory(self, dir_var):
        """Browse for a destination directory"""
        directory = tk.filedialog.askdirectory(title=_("select_destination_directory"))
        if directory:
            dir_var.set(directory)
            self.config.add_frequent_destination_directory(directory)
    
    def _show_frequent_menu(self, dir_var):
        """Show menu with frequent destination directories"""
        frequent_dirs = self.config.get_frequent_destination_directories()
        if not frequent_dirs:
            return
        
        menu = tk.Menu(self, tearoff=0)
        for directory in frequent_dirs:
            display_path = directory
            if len(directory) > 50:
                display_path = "..." + directory[-47:]
            menu.add_command(label=display_path, command=lambda d=directory: dir_var.set(d))
        
        # Show menu at mouse position
        try:
            menu.tk_popup(self.winfo_pointerx(), self.winfo_pointery())
        finally:
            menu.grab_release()
    
    def _load_last_directories(self):
        """Load last used destination directories"""
        if self.config.get_remember_last_dirs():
            last_dirs = self.config.get_last_destination_directories()
            if last_dirs and self.directory_vars:
                self.directory_vars[0].set(last_dirs[0])
    
    def get_destinations(self):
        """Get list of selected destination directories"""
        destinations = []
        for var in self.directory_vars:
            path = var.get().strip()
            if path and path not in destinations:
                destinations.append(path)
        return destinations
    
    def update_texts(self):
        """Update texts when language changes"""
        self.title_label.config(text=_("destination_directories"))
        self.add_dest_button.config(text=_("add_destination"))
        
        # Update all browse buttons
        for button in self.browse_buttons:
            try:
                button.config(text=_("browse"))
            except tk.TclError:
                # Button might have been destroyed, remove from list
                self.browse_buttons.remove(button)
