#!/usr/bin/env python3
"""
Internationalization (i18n) support for MediaCopyer GUI
"""

import tkinter as tk
import json
import os
from typing import Dict, Any, Optional
import importlib.util
import sys


class I18nManager:
    """Internationalization manager for handling multiple languages"""
    
    def __init__(self):
        self.current_language = "auto"  # Default to auto-detect language
        self.languages = {}
        self.observers = []  # List of callbacks to notify when language changes
        self._load_languages()
        self._load_saved_language()
    
    def _load_languages(self):
        """Load language definitions from separate locale files"""
        self.languages = {}
        
        # Get the directory where this file is located
        current_dir = os.path.dirname(os.path.abspath(__file__))
        locales_dir = os.path.join(current_dir, 'locales')
        
        # Available languages and their corresponding files
        language_files = {
            'zh_CN': 'zh_CN.py',
            'en_US': 'en_US.py'
        }
        
        for lang_code, filename in language_files.items():
            try:
                file_path = os.path.join(locales_dir, filename)
                if os.path.exists(file_path):
                    # Load the locale module dynamically
                    spec = importlib.util.spec_from_file_location(f"locale_{lang_code}", file_path)
                    locale_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(locale_module)
                    
                    # Get the translations dictionary from the module
                    if hasattr(locale_module, 'translations'):
                        self.languages[lang_code] = locale_module.translations
                    else:
                        print(f"Warning: No 'translations' found in {filename}")
                else:
                    print(f"Warning: Language file {filename} not found")
            except Exception as e:
                print(f"Error loading language file {filename}: {e}")
        
        # Fallback to ensure we have at least basic English support
        if not self.languages:
            self.languages = {
                "en_US": {
                    "error": "Error",
                    "app_title": "Media Copyer - Media File Organization Tool"
                }
            }
    
    def _load_saved_language(self):
        """Load the saved language from configuration"""
        try:
            # Import here to avoid circular imports
            from core.config import get_config
            config = get_config()
            saved_language = config.get_language()
            
            # If saved language is 'auto', detect system language
            if saved_language == 'auto':
                saved_language = self._detect_system_language()
            
            # Only set if the saved language is available
            if saved_language in self.languages:
                self.current_language = saved_language
            else:
                # If saved language is not available, fall back to English and save it
                self.current_language = "en_US"
                config.set_language(self.current_language)
        except Exception as e:
            print(f"Warning: Could not load saved language: {e}")
            self.current_language = self._detect_system_language()
    
    def _detect_system_language(self):
        """Detect system language and return appropriate language code"""
        try:
            import locale
            # Get system locale
            system_locale = locale.getdefaultlocale()[0]
            
            if system_locale:
                # Convert common locale formats to our language codes
                if system_locale.startswith('zh'):
                    return 'zh_CN'
                elif system_locale.startswith('en'):
                    return 'en_US'
            
            # Default to English if detection fails
            return 'en_US'
        except Exception:
            # If locale detection fails, default to English
            return 'en_US'
    
    def get_text(self, key: str, default: str = None) -> str:
        """Get localized text for the given key"""
        if self.current_language in self.languages:
            return self.languages[self.current_language].get(key, default or key)
        return default or key
    
    def set_language(self, language: str):
        """Set the current language and notify observers"""
        if language == 'auto':
            # For 'auto', detect system language and use it
            detected_language = self._detect_system_language()
            if detected_language in self.languages:
                self.current_language = detected_language
                self._notify_observers()
        elif language in self.languages:
            self.current_language = language
            self._notify_observers()
    
    def get_available_languages(self) -> Dict[str, str]:
        """Get available languages with their display names"""
        return {
            "auto": "Auto",
            "zh_CN": "中文",
            "en_US": "English"
        }
    
    def get_current_language(self) -> str:
        """Get current language code"""
        return self.current_language
    
    def get_saved_language_preference(self) -> str:
        """Get the saved language preference (including 'auto')"""
        try:
            from core.config import get_config
            return get_config().get_language()
        except Exception:
            return 'auto'
    
    def add_observer(self, callback):
        """Add an observer to be notified when language changes"""
        if callback not in self.observers:
            self.observers.append(callback)
    
    def remove_observer(self, callback):
        """Remove an observer"""
        if callback in self.observers:
            self.observers.remove(callback)
    
    def _notify_observers(self):
        """Notify all observers about language change"""
        for callback in self.observers:
            try:
                callback()
            except Exception as e:
                print(f"Error notifying observer: {e}")


# Global i18n manager instance
i18n = I18nManager()


def _(key: str, default: str = None) -> str:
    """Shortcut function for getting localized text"""
    return i18n.get_text(key, default)


class I18nMixin:
    """Mixin class to add i18n support to tkinter widgets"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._i18n_keys = {}  # Maps widget attributes to i18n keys
        i18n.add_observer(self._update_i18n_text)
    
    def set_i18n_text(self, attribute: str, key: str):
        """Set i18n key for a widget attribute"""
        self._i18n_keys[attribute] = key
        self._update_attribute_text(attribute, key)
    
    def _update_attribute_text(self, attribute: str, key: str):
        """Update a single attribute with localized text"""
        text = _(key)
        if hasattr(self, attribute):
            if hasattr(self, 'config'):
                self.config(**{attribute: text})
            else:
                setattr(self, attribute, text)
    
    def _update_i18n_text(self):
        """Update all i18n texts when language changes"""
        for attribute, key in self._i18n_keys.items():
            self._update_attribute_text(attribute, key)
        
        # Also call the widget's update_texts method if it exists
        if hasattr(self, 'update_texts'):
            self.update_texts()
    
    def destroy(self):
        """Clean up i18n observer when widget is destroyed"""
        i18n.remove_observer(self._update_i18n_text)
        # Only call super().destroy() if it exists
        if hasattr(super(), 'destroy'):
            super().destroy()
