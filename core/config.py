#!/usr/bin/env python3
"""
Configuration management for Media Copyer
Handles settings persistence including frequently used directories and last used paths
"""

import json
import os
from typing import List, Dict, Any
from pathlib import Path


class Config:
    """Configuration manager for Media Copyer settings"""
    
    def __init__(self, config_file: str = None):
        """Initialize configuration manager
        
        Args:
            config_file: Path to configuration file. If None, uses default location.
        """
        if config_file is None:
            # Use user's home directory for config
            home_dir = Path.home()
            config_dir = home_dir / '.mediacopyer'
            config_dir.mkdir(exist_ok=True)
            self.config_file = config_dir / 'config.json'
        else:
            self.config_file = Path(config_file)
        
        self.settings = self._load_default_settings()
        self.load()
    
    def _load_default_settings(self) -> Dict[str, Any]:
        """Load default configuration settings"""
        return {
            'version': '1.0',
            'last_directories': {
                'sources': [],
                'destinations': []
            },
            'frequent_directories': {
                'sources': [],
                'destinations': []
            },
            'ui_settings': {
                'language': 'auto',
                'remember_last_dirs': True,
                'max_frequent_dirs': 10
            },
            'processing_options': {
                'move_mode': False,
                'dry_run': False,
                'md5_check': True,
                'organization_mode': 'date'
            }
        }
    
    def load(self) -> None:
        """Load configuration from file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    self._merge_settings(self.settings, loaded_settings)
        except Exception as e:
            print(f"Warning: Could not load config file: {e}")
            # Keep default settings if loading fails
    
    def save(self) -> None:
        """Save configuration to file"""
        try:
            # Ensure directory exists
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Could not save config file: {e}")
    
    def _merge_settings(self, default: Dict, loaded: Dict) -> None:
        """Recursively merge loaded settings with defaults"""
        for key, value in loaded.items():
            if key in default:
                if isinstance(value, dict) and isinstance(default[key], dict):
                    self._merge_settings(default[key], value)
                else:
                    default[key] = value
    
    def get_last_source_directories(self) -> List[str]:
        """Get last used source directories"""
        return self.settings['last_directories']['sources'].copy()
    
    def get_last_destination_directories(self) -> List[str]:
        """Get last used destination directories"""
        return self.settings['last_directories']['destinations'].copy()
    
    def set_last_source_directories(self, directories: List[str]) -> None:
        """Set last used source directories"""
        self.settings['last_directories']['sources'] = directories.copy()
        self.save()
    
    def set_last_destination_directories(self, directories: List[str]) -> None:
        """Set last used destination directories"""
        self.settings['last_directories']['destinations'] = directories.copy()
        self.save()
    
    def get_frequent_source_directories(self) -> List[str]:
        """Get frequently used source directories"""
        return self.settings['frequent_directories']['sources'].copy()
    
    def get_frequent_destination_directories(self) -> List[str]:
        """Get frequently used destination directories"""
        return self.settings['frequent_directories']['destinations'].copy()
    
    def add_frequent_source_directory(self, directory: str) -> None:
        """Add a directory to frequently used sources"""
        frequent_sources = self.settings['frequent_directories']['sources']
        
        # Remove if already exists to avoid duplicates
        if directory in frequent_sources:
            frequent_sources.remove(directory)
        
        # Add to beginning
        frequent_sources.insert(0, directory)
        
        # Limit to max frequent directories
        max_dirs = self.settings['ui_settings']['max_frequent_dirs']
        if len(frequent_sources) > max_dirs:
            frequent_sources = frequent_sources[:max_dirs]
            self.settings['frequent_directories']['sources'] = frequent_sources
        
        self.save()
    
    def add_frequent_destination_directory(self, directory: str) -> None:
        """Add a directory to frequently used destinations"""
        frequent_destinations = self.settings['frequent_directories']['destinations']
        
        # Remove if already exists to avoid duplicates
        if directory in frequent_destinations:
            frequent_destinations.remove(directory)
        
        # Add to beginning
        frequent_destinations.insert(0, directory)
        
        # Limit to max frequent directories
        max_dirs = self.settings['ui_settings']['max_frequent_dirs']
        if len(frequent_destinations) > max_dirs:
            frequent_destinations = frequent_destinations[:max_dirs]
            self.settings['frequent_directories']['destinations'] = frequent_destinations
        
        self.save()
    
    def remove_frequent_source_directory(self, directory: str) -> None:
        """Remove a directory from frequently used sources"""
        frequent_sources = self.settings['frequent_directories']['sources']
        if directory in frequent_sources:
            frequent_sources.remove(directory)
            self.save()
    
    def remove_frequent_destination_directory(self, directory: str) -> None:
        """Remove a directory from frequently used destinations"""
        frequent_destinations = self.settings['frequent_directories']['destinations']
        if directory in frequent_destinations:
            frequent_destinations.remove(directory)
            self.save()
    
    def get_remember_last_dirs(self) -> bool:
        """Check if should remember last directories"""
        return self.settings['ui_settings']['remember_last_dirs']
    
    def set_remember_last_dirs(self, remember: bool) -> None:
        """Set whether to remember last directories"""
        self.settings['ui_settings']['remember_last_dirs'] = remember
        self.save()
    
    def get_processing_options(self) -> Dict[str, Any]:
        """Get processing options"""
        return self.settings['processing_options'].copy()
    
    def set_processing_options(self, **kwargs) -> None:
        """Set processing options"""
        for key, value in kwargs.items():
            if key in self.settings['processing_options']:
                self.settings['processing_options'][key] = value
        self.save()
    
    def get_language(self) -> str:
        """Get UI language setting"""
        return self.settings['ui_settings']['language']
    
    def set_language(self, language: str) -> None:
        """Set UI language setting"""
        self.settings['ui_settings']['language'] = language
        self.save()


# Global configuration instance
_config_instance = None


def get_config() -> Config:
    """Get global configuration instance"""
    global _config_instance
    if _config_instance is None:
        _config_instance = Config()
    return _config_instance
