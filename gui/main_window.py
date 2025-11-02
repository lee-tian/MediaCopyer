#!/usr/bin/env python3
"""
Main application window for Media Copyer GUI
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
import webbrowser

from core.utils import check_dependencies
from .directory_selector import DirectorySelector, MultiSourceSelector, MultiDestinationSelector
from .progress_display import ProgressDisplay
from .log_display import LogDisplay
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
        
        # Set up cleanup when window is destroyed
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        # Setup menu bar first
        self._setup_menu()
        
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
    
    def _setup_menu(self):
        """Setup the application menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Check if we're on macOS
        is_macos = self.root.tk.call('tk', 'windowingsystem') == 'aqua'
        
        if is_macos:
            # On macOS, create the application menu (first menu)
            app_menu = tk.Menu(menubar, name='apple', tearoff=0)
            menubar.add_cascade(menu=app_menu)
            app_menu.add_command(label=_("about") + " MediaCopyer", command=self._show_about)
            app_menu.add_separator()
            # macOS will automatically add Quit, Hide, etc.
            
            # Help menu
            self.help_menu = tk.Menu(menubar, name='help', tearoff=0)
            menubar.add_cascade(label=_("help_menu"), menu=self.help_menu)
        else:
            # On other platforms, create a standard Help menu
            self.help_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label=_("help_menu"), menu=self.help_menu)
            
            # Add About to Help menu on non-macOS platforms
            self.help_menu.add_command(label=_("about"), command=self._show_about)
            self.help_menu.add_separator()
        
        # Add common help menu items
        self.help_menu.add_command(label=_("user_guide"), command=self._show_user_guide)
        self.help_menu.add_command(label=_("keyboard_shortcuts"), command=self._show_shortcuts)
        self.help_menu.add_separator()
        self.help_menu.add_command(label=_("report_issue"), command=self._report_issue)
        self.help_menu.add_command(label=_("check_updates"), command=self._check_updates)
        
        # Store menu reference for language updates
        self.menubar = menubar
        self.is_macos = is_macos
    
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
        
        self.language_var = tk.StringVar()
        self.language_combo = ttk.Combobox(
            lang_frame, textvariable=self.language_var, state="readonly", width=10,
            font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_SM)
        )
        
        languages = i18n.get_available_languages()
        self.language_combo['values'] = list(languages.values())
        
        # Set combo box to show the saved language preference (which may be 'auto')
        saved_lang_pref = i18n.get_saved_language_preference()
        if saved_lang_pref in languages:
            self.language_combo.set(languages[saved_lang_pref])
        else:
            # Fallback to current language
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
        
        self._dir_title_label = ModernWidget.create_title_label(dir_card, text=_("directory_selection"))
        self._dir_title_label.grid(row=0, column=0, sticky=tk.W, pady=(0, ModernStyle.PADDING_XS))
        
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
        
        self._options_title_label = ModernWidget.create_title_label(options_card, text=_("options"))
        self._options_title_label.grid(row=0, column=0, sticky=tk.W, pady=(0, ModernStyle.PADDING_XS))
        
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
        
        self._progress_title_label = ModernWidget.create_title_label(progress_card, text=_("progress"))
        self._progress_title_label.grid(row=0, column=0, sticky=tk.W, pady=(0, ModernStyle.PADDING_SM))
        
        self.progress_display = ProgressDisplay(progress_card)
        self.progress_display.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Log card
        log_card = ModernWidget.create_card_frame(exec_frame, padding=ModernStyle.PADDING_MD)
        log_card.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_card.columnconfigure(0, weight=1)
        log_card.rowconfigure(1, weight=1)
        
        self._log_title_label = ModernWidget.create_title_label(log_card, text=_("log"))
        self._log_title_label.grid(row=0, column=0, sticky=tk.W, pady=(0, ModernStyle.PADDING_SM))
        
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
                self.log_display.add_log(msg)
            self.log_display.add_log(_("dependency_warning") + "\n" + "="*50)
    
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
            ignore_duplicates=self.options_frame.get_ignore_duplicates(),
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
                
                # Also save to config if we have one
                from core.config import get_config
                config = get_config()
                if config:
                    config.set_language(code)
                break
    
    def _update_title(self):
        """Update window title"""
        from version import get_app_name
        self.root.title(get_app_name())
    
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
        
        # Update card titles directly by storing references
        self._update_card_titles()
        
        # Update card contents
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
        
        # Update menu
        self._update_menu_texts()
    
    def _update_card_titles(self):
        """Update card title labels using stored references"""
        # Update directory selection title
        if hasattr(self, '_dir_title_label'):
            self._dir_title_label.config(text=_("directory_selection"))
        
        # Update options title
        if hasattr(self, '_options_title_label'):
            self._options_title_label.config(text=_("options"))
        
        # Update progress title
        if hasattr(self, '_progress_title_label'):
            self._progress_title_label.config(text=_("progress"))
        
        # Update log title
        if hasattr(self, '_log_title_label'):
            self._log_title_label.config(text=_("log"))
    
    def _update_menu_texts(self):
        """Update menu texts when language changes"""
        if hasattr(self, 'menubar') and hasattr(self, 'help_menu'):
            # Clear and recreate the help menu
            self.help_menu.delete(0, 'end')
            
            if not getattr(self, 'is_macos', False):
                # On non-macOS, add About to Help menu
                self.help_menu.add_command(label=_("about"), command=self._show_about)
                self.help_menu.add_separator()
            
            # Re-add common help menu items with updated text
            self.help_menu.add_command(label=_("user_guide"), command=self._show_user_guide)
            self.help_menu.add_command(label=_("keyboard_shortcuts"), command=self._show_shortcuts)
            self.help_menu.add_separator()
            self.help_menu.add_command(label=_("report_issue"), command=self._report_issue)
            self.help_menu.add_command(label=_("check_updates"), command=self._check_updates)
            
            # Update cascade labels
            try:
                if getattr(self, 'is_macos', False):
                    # On macOS: App menu (0), Help menu (1)
                    self.menubar.entryconfig(1, label=_("help_menu"))
                else:
                    # On other platforms: Help menu (0)
                    self.menubar.entryconfig(0, label=_("help_menu"))
            except tk.TclError:
                # Ignore errors if menu structure is different
                pass
    
    def _show_user_guide(self):
        """Show user guide"""
        guide_text = _("""user_guide_content""")
        
        # Create a new window for the user guide
        guide_window = tk.Toplevel(self.root)
        guide_window.title(_("user_guide"))
        guide_window.geometry("600x500")
        guide_window.transient(self.root)
        guide_window.grab_set()
        
        # Center the window
        guide_window.update_idletasks()
        x = (guide_window.winfo_screenwidth() // 2) - (guide_window.winfo_width() // 2)
        y = (guide_window.winfo_screenheight() // 2) - (guide_window.winfo_height() // 2)
        guide_window.geometry(f"+{x}+{y}")
        
        # Create scrollable text widget
        frame = ttk.Frame(guide_window, padding=10)
        frame.pack(fill="both", expand=True)
        
        text_widget = tk.Text(frame, wrap=tk.WORD, font=("Arial", 11), 
                             bg="white", fg="black", padx=10, pady=10)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        text_widget.insert("1.0", guide_text)
        text_widget.config(state="disabled")
        
        # Close button
        button_frame = ttk.Frame(guide_window)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Button(button_frame, text=_("close"), 
                  command=guide_window.destroy).pack(side="right")
    
    def _show_shortcuts(self):
        """Show keyboard shortcuts"""
        shortcuts_text = _("""shortcuts_content""")
        
        messagebox.showinfo(_("keyboard_shortcuts"), shortcuts_text)
    
    def _report_issue(self):
        """Open issue reporting page"""
        try:
            webbrowser.open("https://github.com/lee-tian/MediaCopyer/issues")
        except Exception:
            messagebox.showinfo(_("report_issue"), 
                              _("Please visit: https://github.com/lee-tian/MediaCopyer/issues"))
    
    def _check_updates(self):
        """Check for updates"""
        try:
            webbrowser.open("https://github.com/lee-tian/MediaCopyer/releases")
        except Exception:
            messagebox.showinfo(_("check_updates"), 
                              _("Please visit: https://github.com/lee-tian/MediaCopyer/releases"))
    
    def _show_about(self):
        """Show about dialog"""
        from version import get_version, get_full_version, __author__, __description__
        
        about_text = f"""{_("app_name")}: MediaCopyer

{_("version")}: {get_full_version()}
{_("author")}: {__author__}

{_("description")}:
{__description__}

{_("features")}:
• {_("feature_auto_organize")}
• {_("feature_date_based")}
• {_("feature_duplicate_handling")}
• {_("feature_preview_mode")}
• {_("feature_multilingual")}
• {_("feature_batch_processing")}

{_("supported_formats")}:
{_("image_formats")}: JPG, JPEG, PNG, TIFF, BMP, GIF, HEIC, WEBP
{_("video_formats")}: MP4, MOV, AVI, MKV, WMV, FLV, WEBM, M4V

© 2024-2025 MediaCopyer Team
{_("license")}: MIT License"""
        
        # Create about dialog
        about_window = tk.Toplevel(self.root)
        about_window.title(_("about") + " MediaCopyer")
        about_window.geometry("500x600")
        about_window.transient(self.root)
        about_window.grab_set()
        about_window.resizable(False, False)
        
        # Center the window
        about_window.update_idletasks()
        x = (about_window.winfo_screenwidth() // 2) - (about_window.winfo_width() // 2)
        y = (about_window.winfo_screenheight() // 2) - (about_window.winfo_height() // 2)
        about_window.geometry(f"+{x}+{y}")
        
        # Main frame
        main_frame = ttk.Frame(about_window, padding=20)
        main_frame.pack(fill="both", expand=True)
        
        # App icon (if available)
        try:
            icon_path = 'resources/icon.png'
            if os.path.exists(icon_path):
                icon_image = tk.PhotoImage(file=icon_path)
                # Resize icon if needed
                icon_label = ttk.Label(main_frame, image=icon_image)
                icon_label.image = icon_image  # Keep reference
                icon_label.pack(pady=(0, 10))
        except Exception:
            pass
        
        # Scrollable text area
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill="both", expand=True)
        
        text_widget = tk.Text(text_frame, wrap=tk.WORD, font=("Arial", 10), 
                             bg="white", fg="black", padx=15, pady=15,
                             height=20, width=50)
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        text_widget.insert("1.0", about_text)
        text_widget.config(state="disabled")
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=(10, 0))
        
        ttk.Button(button_frame, text=_("close"), 
                  command=about_window.destroy).pack(side="right")
    
    def _on_closing(self):
        """Handle window closing event"""
        # Remove observer to prevent memory leaks
        i18n.remove_observer(self._update_texts)
        # Destroy the window
        self.root.destroy()


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
