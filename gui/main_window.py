#!/usr/bin/env python3
"""
Main application window for Media Copyer GUI
"""

import tkinter as tk
from tkinter import ttk

from core.utils import check_dependencies
from .widgets import DirectorySelector, ProgressDisplay, LogDisplay, ButtonPanel
from .options_frame import OptionsFrame
from .processor import FileProcessor
from .i18n import i18n, _, I18nMixin


class MediaCopyerApp:
    """Main application class for Media Copyer GUI"""
    
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x600")
        
        # Subscribe to language changes
        i18n.add_observer(self._update_texts)
        
        self._setup_ui()
        self._setup_processor()
        self._check_dependencies()
        
        # Set initial title
        self._update_title()
    
    def _setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(7, weight=1)  # Make log area expandable
        
        # Header frame with title and language selector
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        header_frame.columnconfigure(0, weight=1)
        
        # Title
        self.title_label = ttk.Label(
            header_frame, 
            text=_("main_title"), 
            font=('TkDefaultFont', 16, 'bold')
        )
        self.title_label.grid(row=0, column=0, sticky=tk.W)
        
        # Language selector frame
        lang_frame = ttk.Frame(header_frame)
        lang_frame.grid(row=0, column=1, sticky=tk.E)
        
        ttk.Label(lang_frame, text=_("language") + ":").grid(row=0, column=0, padx=(0, 5))
        
        self.language_var = tk.StringVar(value=i18n.get_current_language())
        self.language_combo = ttk.Combobox(
            lang_frame, 
            textvariable=self.language_var,
            state="readonly",
            width=10
        )
        
        # Setup language options
        languages = i18n.get_available_languages()
        self.language_combo['values'] = list(languages.values())
        
        # Set current selection
        current_lang = i18n.get_current_language()
        if current_lang in languages:
            self.language_combo.set(languages[current_lang])
        
        self.language_combo.bind('<<ComboboxSelected>>', self._on_language_change)
        self.language_combo.grid(row=0, column=1)
        
        # Source directory selector
        self.source_selector = DirectorySelector(
            main_frame, 
            _("source_directory"), 
            _("select_source")
        )
        self.source_selector.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # Destination directory selector
        self.dest_selector = DirectorySelector(
            main_frame, 
            _("destination_directory"), 
            _("select_destination")
        )
        self.dest_selector.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # Options frame
        self.options_frame = OptionsFrame(main_frame)
        self.options_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=20)
        
        # Control buttons
        self.button_panel = ButtonPanel(main_frame)
        self.button_panel.grid(row=4, column=0, pady=20)
        
        # Progress display
        self.progress_display = ProgressDisplay(main_frame)
        self.progress_display.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=10)
        
        # Log display
        self.log_display = LogDisplay(main_frame)
        self.log_display.grid(row=6, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
    
    def _setup_processor(self):
        """Setup the file processor and connect callbacks"""
        self.processor = FileProcessor(
            self.progress_display, 
            self.log_display, 
            self.button_panel
        )
        
        # Connect button callbacks
        self.button_panel.set_start_command(self._start_processing)
        self.button_panel.set_clear_log_command(self._clear_log)
    
    def _check_dependencies(self):
        """Check if required dependencies are available"""
        messages = check_dependencies()
        
        if messages:
            for msg in messages:
                self.log_display.add_message(msg)
            self.log_display.add_message(_("dependency_warning") + "\n" + "="*50)
    
    def _start_processing(self):
        """Start the file processing"""
        self.processor.start_processing(
            source_dir=self.source_selector.get_directory(),
            dest_dir=self.dest_selector.get_directory(),
            move_mode=self.options_frame.get_move_mode(),
            dry_run=self.options_frame.get_dry_run(),
            md5_check=self.options_frame.get_md5_check(),
            organization_mode=self.options_frame.get_organization_mode()
        )
    
    def _clear_log(self):
        """Clear the log display"""
        self.log_display.clear()
    
    def _on_language_change(self, event=None):
        """Handle language selection change"""
        languages = i18n.get_available_languages()
        selected_text = self.language_combo.get()
        
        # Find the language code for the selected display text
        for code, display_text in languages.items():
            if display_text == selected_text:
                i18n.set_language(code)
                break
    
    def _update_title(self):
        """Update window title"""
        self.root.title(_("app_title"))
    
    def _update_texts(self):
        """Update all UI texts when language changes"""
        # Update window title
        self._update_title()
        
        # Update title label
        self.title_label.config(text=_("main_title"))
        
        # Update language selector components
        for child in self.title_label.master.grid_slaves():
            if isinstance(child, ttk.Frame):
                for subchild in child.grid_slaves():
                    if isinstance(subchild, ttk.Label) and ":" in subchild.cget("text"):
                        subchild.config(text=_("language") + ":")
        
        # Update directory selectors
        if hasattr(self, 'source_selector'):
            self.source_selector.update_texts(_("source_directory"), _("select_source"))
        if hasattr(self, 'dest_selector'):
            self.dest_selector.update_texts(_("destination_directory"), _("select_destination"))
        
        # Update options frame
        if hasattr(self, 'options_frame'):
            self.options_frame.update_texts()
        
        # Update button panel
        if hasattr(self, 'button_panel'):
            self.button_panel.update_texts()
        
        # Update progress display
        if hasattr(self, 'progress_display'):
            self.progress_display.update_texts()
        
        # Update log display
        if hasattr(self, 'log_display'):
            self.log_display.update_texts()


def create_app():
    """Create and return the main application"""
    root = tk.Tk()
    app = MediaCopyerApp(root)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    return root, app


def main():
    """Main function to run the GUI application"""
    root, app = create_app()
    root.mainloop()


if __name__ == "__main__":
    main()
