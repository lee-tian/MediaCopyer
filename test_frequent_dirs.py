#!/usr/bin/env python3
"""
Test script for frequent directories functionality
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.config import Config

def test_config_manager():
    """Test the ConfigManager functionality"""
    print("Testing ConfigManager...")
    
    # Create a test config manager
    config = Config()
    
    # Test default values
    print(f"Default frequent sources: {config.get_frequent_source_directories()}")
    print(f"Default frequent destinations: {config.get_frequent_destination_directories()}")
    print(f"Default remember last dirs: {config.get_remember_last_dirs()}")
    
    # Add some frequent directories
    config.add_frequent_source_directory("/Users/test/Photos")
    config.add_frequent_source_directory("/Users/test/Videos")
    config.add_frequent_destination_directory("/Users/test/Organized")
    
    print(f"After adding - frequent sources: {config.get_frequent_source_directories()}")
    print(f"After adding - frequent destinations: {config.get_frequent_destination_directories()}")
    
    # Test duplicate handling
    config.add_frequent_source_directory("/Users/test/Photos")  # Should not duplicate
    print(f"After duplicate add - frequent sources: {config.get_frequent_source_directories()}")
    
    # Test removal
    config.remove_frequent_source_directory("/Users/test/Videos")
    print(f"After removal - frequent sources: {config.get_frequent_source_directories()}")
    
    # Test last directories
    config.set_last_source_directories(["/Users/test/LastSource"])
    config.set_last_destination_directories(["/Users/test/LastDest"])
    print(f"Last source: {config.get_last_source_directories()}")
    print(f"Last destination: {config.get_last_destination_directories()}")
    
    # Test remember setting
    config.set_remember_last_dirs(True)
    print(f"Remember last dirs: {config.get_remember_last_dirs()}")
    
    # Test save and load
    config.save()
    print("Configuration saved")
    
    # Create new instance to test loading
    config2 = Config()
    print(f"Loaded frequent sources: {config2.get_frequent_source_directories()}")
    print(f"Loaded frequent destinations: {config2.get_frequent_destination_directories()}")
    print(f"Loaded remember last dirs: {config2.get_remember_last_dirs()}")
    print(f"Loaded last source: {config2.get_last_source_directories()}")
    print(f"Loaded last destination: {config2.get_last_destination_directories()}")
    
    print("Test completed successfully!")

if __name__ == "__main__":
    test_config_manager()
