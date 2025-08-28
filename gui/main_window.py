#!/usr/bin/env python3
"""
Main application window for Media Copyer GUI
"""

import tkinter as tk
from tkinter import ttk
import os

from core.utils import check_dependencies
from .widgets import DirectorySelector, MultiSourceSelector, MultiDestinationSelector, ProgressDisplay, LogDisplay
from .options_frame import OptionsFrame
from .processor import FileProcessor
from .i18n import i18n, _, I18nMixin
from .styles import ModernStyle, ModernWidget, configure_modern_style


class MediaCopyerApp:
    """Main application class for Media Copyer GUI"""
    
    def __init__(self, root):
        self.root = root
        self.root.geometry("900x700")   # More reasonable size for various screens
        self.root.minsize(800, 600)     # Minimum size to ensure all content fits
        
        # Configure modern styling
        configure_modern_style()
        
        # Set window properties
        self.root.configure(bg=ModernStyle.BACKGROUND)
        
        # Set window icon if available
        self._set_window_icon()
        
        # Subscribe to language changes
        i18n.add_observer(self._update_texts)
        
        self._setup_ui()
        self._setup_processor()
        self._check_dependencies()
        
        # Set initial title
        self._update_title()
    
    def _set_window_icon(self):
        """Set window icon if available"""
        try:
            icon_paths = [
                'resources/icon.png',
                'resources/icon.ico',
                'icon.png',
                'icon.ico'
            ]
            
            for icon_path in icon_paths:
                if os.path.exists(icon_path):
                    if icon_path.endswith('.ico'):
                        # For ICO files, use wm_iconbitmap
                        self.root.wm_iconbitmap(icon_path)
                    else:
                        # For PNG files, use PhotoImage
                        try:
                            icon_image = tk.PhotoImage(file=icon_path)
                            self.root.wm_iconphoto(True, icon_image)
                            # Keep a reference to prevent garbage collection
                            self.root.icon_image = icon_image
                        except tk.TclError:
                            # If PhotoImage fails, try with wm_iconbitmap anyway
                            try:
                                self.root.wm_iconbitmap(icon_path)
                            except tk.TclError:
                                pass
                    break
        except Exception:
            # If setting icon fails, just continue without it
            pass
    
    def _setup_ui(self):
        """Setup the tabbed user interface"""
        # Main container
        main_frame = ttk.Frame(self.root, style='Modern.TFrame', padding=ModernStyle.PADDING_LG)
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Header card with title and language
        header_card = ModernWidget.create_card_frame(main_frame, padding=ModernStyle.PADDING_MD)
        header_card.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, ModernStyle.PADDING_SM))
        header_card.columnconfigure(0, weight=1)
        
        title_frame = ttk.Frame(header_card, style='Modern.TFrame')
        title_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        title_frame.columnconfigure(0, weight=1)
        
        self.title_label = ModernWidget.create_title_label(title_frame, text=_("main_title"))
        self.title_label.grid(row=0, column=0, sticky=tk.W)
        
        # Language selector
        lang_frame = ttk.Frame(title_frame, style='Modern.TFrame')
        lang_frame.grid(row=0, column=1, sticky=tk.E)
        
        ttk.Label(lang_frame, text=_("language") + ":", style='Modern.TLabel').grid(row=0, column=0, padx=(0, ModernStyle.PADDING_SM))
        
        self.language_var = tk.StringVar(value=i18n.get_current_language())
        self.language_combo = ttk.Combobox(
            lang_frame, textvariable=self.language_var, state="readonly", width=10,
            font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_SM)
        )
        
        languages = i18n.get_available_languages()
        self.language_combo['values'] = list(languages.values())
        current_lang = i18n.get_current_language()
        if current_lang in languages:
            self.language_combo.set(languages[current_lang])
        
        self.language_combo.bind('<<ComboboxSelected>>', self._on_language_change)
        self.language_combo.grid(row=0, column=1)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame, style='Modern.TNotebook')
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Setup tabs
        self._setup_settings_tab()
        self._setup_execution_tab()
        
    def _setup_settings_tab(self):
        """Setup the settings tab with scrollable content"""
        # Settings tab container
        settings_container = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(settings_container, text=_("settings"))
        
        # Create canvas and scrollbar for scrollable content
        canvas = tk.Canvas(settings_container, bg=ModernStyle.BACKGROUND, highlightthickness=0)
        scrollbar = ttk.Scrollbar(settings_container, orient="vertical", command=canvas.yview)
        
        # Scrollable frame inside canvas
        scrollable_frame = ttk.Frame(canvas, style='Modern.TFrame')
        
        # Configure scrolling
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Configure canvas scrolling with mouse wheel
        def _bound_to_mousewheel(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        def _unbound_to_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")
        
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind('<Enter>', _bound_to_mousewheel)
        canvas.bind('<Leave>', _unbound_to_mousewheel)
        
        # Configure scrollable frame
        def configure_scroll_region(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
            
        def configure_canvas_width(event=None):
            # Set the width of the scrollable frame to match canvas width
            canvas_width = event.width
            canvas.itemconfig(canvas_window, width=canvas_width)
        
        scrollable_frame.bind('<Configure>', configure_scroll_region)
        canvas.bind('<Configure>', configure_canvas_width)
        
        # Add content to scrollable frame with reduced padding
        content_frame = ttk.Frame(scrollable_frame, style='Modern.TFrame', padding=ModernStyle.PADDING_SM)
        content_frame.pack(fill="both", expand=True, padx=ModernStyle.PADDING_SM, pady=ModernStyle.PADDING_SM)
        
        content_frame.columnconfigure(0, weight=1)
        
        # Directory selection card with compact layout
        dir_card = ModernWidget.create_card_frame(content_frame, padding=ModernStyle.PADDING_SM)
        dir_card.pack(fill="x", pady=(0, ModernStyle.PADDING_SM))
        dir_card.columnconfigure(0, weight=1)
        
        dir_title = ModernWidget.create_title_label(dir_card, text=_("directory_selection"))
        dir_title.grid(row=0, column=0, sticky=tk.W, pady=(0, ModernStyle.PADDING_XS))
        
        self.source_selector = MultiSourceSelector(dir_card)
        self.source_selector.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, ModernStyle.PADDING_XS))
        
        self.multi_dest_selector = MultiDestinationSelector(dir_card)
        self.multi_dest_selector.grid(row=2, column=0, sticky=(tk.W, tk.E))
        
        guidance_card = ModernWidget.create_card_frame(content_frame, padding=ModernStyle.PADDING_SM)
        guidance_card.pack(fill="x", pady=(0, ModernStyle.PADDING_SM))
        guidance_card.columnconfigure(1, weight=1)
        
        # Status icon
        self.status_icon_label = ttk.Label(guidance_card, text="⏸", 
                                          font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_LG), 
                                          style='Modern.TLabel')
        self.status_icon_label.grid(row=0, column=0, padx=(0, ModernStyle.PADDING_SM), sticky=tk.W)
        
        # Guidance text
        self.guidance_text = ttk.Label(guidance_card, text=_("setup_guidance"), 
                                      style='Modern.TLabel', wraplength=500)
        self.guidance_text.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        # Next step button
        self.next_step_button = ttk.Button(guidance_card, text=_("go_to_execution"), 
                                          command=self._start_processing, 
                                          style='Accent.TButton', state='disabled')
        self.next_step_button.grid(row=0, column=2, padx=(ModernStyle.PADDING_SM, 0), sticky=tk.E)
        
        # Options card with compact layout (moved to bottom)
        options_card = ModernWidget.create_card_frame(content_frame, padding=ModernStyle.PADDING_SM)
        options_card.pack(fill="x", pady=(0, ModernStyle.PADDING_SM))
        options_card.columnconfigure(0, weight=1)
        
        options_title = ModernWidget.create_title_label(options_card, text=_("options"))
        options_title.grid(row=0, column=0, sticky=tk.W, pady=(0, ModernStyle.PADDING_XS))
        
        self.options_frame = OptionsFrame(options_card)
        self.options_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Store canvas reference for future use
        self._settings_canvas = canvas
        
        # Bind events to check settings completion
        self._setup_settings_validation()
        
    def _setup_execution_tab(self):
        """Setup the execution tab"""
        # Execution tab frame
        exec_frame = ttk.Frame(self.notebook, style='Modern.TFrame', padding=ModernStyle.PADDING_MD)
        self.notebook.add(exec_frame, text=_("execution"))
        
        exec_frame.columnconfigure(0, weight=1)
        exec_frame.rowconfigure(2, weight=1)
        
        # Progress display
        progress_card = ModernWidget.create_card_frame(exec_frame, padding=ModernStyle.PADDING_MD)
        progress_card.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, ModernStyle.PADDING_MD))
        progress_card.columnconfigure(0, weight=1)
        
        progress_title = ModernWidget.create_title_label(progress_card, text=_("progress"))
        progress_title.grid(row=0, column=0, sticky=tk.W, pady=(0, ModernStyle.PADDING_SM))
        
        self.progress_display = ProgressDisplay(progress_card)
        self.progress_display.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Log card
        log_card = ModernWidget.create_card_frame(exec_frame, padding=ModernStyle.PADDING_MD)
        log_card.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_card.columnconfigure(0, weight=1)
        log_card.rowconfigure(1, weight=1)
        
        log_title = ModernWidget.create_title_label(log_card, text=_("log"))
        log_title.grid(row=0, column=0, sticky=tk.W, pady=(0, ModernStyle.PADDING_SM))
        
        self.log_display = LogDisplay(log_card)
        self.log_display.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    def _setup_processor(self):
        """Setup the file processor and connect callbacks"""
        self.processor = FileProcessor(
            self.progress_display, 
            self.log_display
        )
    
    def _check_dependencies(self):
        """Check if required dependencies are available"""
        messages = check_dependencies()
        
        if messages:
            for msg in messages:
                self.log_display.add_message(msg)
            self.log_display.add_message(_("dependency_warning") + "\n" + "="*50)
    
    def _start_processing(self):
        """Start the file processing"""
        # Get directories
        source_dirs = self.source_selector.get_sources()
        dest_dirs = self.multi_dest_selector.get_destinations()
        
        # Save last used directories if remember is enabled
        from core.config import get_config
        config = get_config()
        if config.get_remember_last_dirs():
            if source_dirs:
                config.set_last_source_directories(source_dirs)
            if dest_dirs:
                config.set_last_destination_directories(dest_dirs)
        
        # First switch to the execution tab
        self._go_to_execution_tab()
        
        # Then start processing
        self.processor.start_processing(
            source_dirs=source_dirs,
            dest_dirs=dest_dirs,
            move_mode=self.options_frame.get_move_mode(),
            dry_run=self.options_frame.get_dry_run(),
            md5_check=self.options_frame.get_md5_check(),
            organization_mode=self.options_frame.get_organization_mode()
        )
    
    def _clear_log(self):
        """Clear the log display"""
        self.log_display.clear()
    
    def _setup_settings_validation(self):
        """Setup validation for settings completion"""
        # Check settings completion periodically
        self.root.after(500, self._check_settings_completion)
    
    def _check_settings_completion(self):
        """Check if all required settings are completed"""
        source_dirs = self.source_selector.get_sources()
        dest_dirs = self.multi_dest_selector.get_destinations()
        
        is_complete = bool(source_dirs and dest_dirs)
        
        if is_complete:
            self.status_icon_label.config(text="✓", foreground="green")
            self.guidance_text.config(text=_("setup_complete_guidance"))
            self.next_step_button.config(state='normal')
        else:
            self.status_icon_label.config(text="⏸", foreground="orange")
            self.guidance_text.config(text=_("setup_guidance"))
            self.next_step_button.config(state='disabled')
        
        # Continue checking
        self.root.after(1000, self._check_settings_completion)
    
    def _go_to_execution_tab(self):
        """Switch to execution tab"""
        self.notebook.select(1)  # Select the execution tab (index 1)
    
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
        
        # Update language selector label
        lang_frame = None
        for child in self.title_label.master.winfo_children():
            if isinstance(child, ttk.Frame):
                lang_frame = child
                break
        
        if lang_frame:
            for widget in lang_frame.winfo_children():
                if isinstance(widget, ttk.Label) and ":" in widget.cget("text"):
                    widget.config(text=_("language") + ":")
        
        # Update notebook tab titles
        if hasattr(self, 'notebook'):
            self.notebook.tab(0, text=_("settings"))
            self.notebook.tab(1, text=_("execution"))
        
        # Update card titles
        if hasattr(self, 'source_selector'):
            self.source_selector.update_texts()
        if hasattr(self, 'multi_dest_selector'):
            self.multi_dest_selector.update_texts()
        
        # Update options frame
        if hasattr(self, 'options_frame'):
            self.options_frame.update_texts()
        
        # Update progress display
        if hasattr(self, 'progress_display'):
            self.progress_display.update_texts()
        
        # Update log display
        if hasattr(self, 'log_display'):
            self.log_display.update_texts()
        
        # Update guidance text and button
        if hasattr(self, 'guidance_text'):
            source_dirs = self.source_selector.get_sources() if hasattr(self, 'source_selector') else []
            dest_dirs = self.multi_dest_selector.get_destinations() if hasattr(self, 'multi_dest_selector') else []
            is_complete = bool(source_dirs and dest_dirs)
            
            if is_complete:
                self.guidance_text.config(text=_("setup_complete_guidance"))
            else:
                self.guidance_text.config(text=_("setup_guidance"))
        
        if hasattr(self, 'next_step_button'):
            self.next_step_button.config(text=_("go_to_execution"))
        
        # Update other card titles by searching for title labels
        for widget in self.root.winfo_children():
            self._update_card_titles_recursive(widget)
    
    def _update_card_titles_recursive(self, widget):
        """Recursively update card title labels"""
        try:
            for child in widget.winfo_children():
                if isinstance(child, ttk.Label):
                    text = child.cget("text")
                    # Update known title texts
                    if "目录选择" in text or "Directory Selection" in text:
                        child.config(text=_("directory_selection"))
                    elif "选项" in text or "Options" in text:
                        child.config(text=_("options"))
                    elif "进度" in text or "Progress" in text:
                        child.config(text=_("progress"))
                    elif "日志" in text or "Log" in text:
                        child.config(text=_("log"))
                
                # Recursively check children
                if hasattr(child, 'winfo_children'):
                    self._update_card_titles_recursive(child)
        except tk.TclError:
            # Widget may have been destroyed, ignore
            pass


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
