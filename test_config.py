#!/usr/bin/env python3
"""
Test script for the new configuration system
"""

from core.config import get_config

def test_config():
    """Test the configuration functionality"""
    config = get_config()
    
    print("=== Testing Configuration System ===")
    
    # Test frequent directories functionality
    print("\n1. Testing frequent source directories:")
    print("Initial frequent sources:", config.get_frequent_source_directories())
    
    # Add some test directories
    test_sources = ["/Users/test/Pictures", "/Users/test/Downloads", "/Users/test/Desktop"]
    for source in test_sources:
        config.add_frequent_source_directory(source)
        print(f"Added source: {source}")
    
    print("Frequent sources after adding:", config.get_frequent_source_directories())
    
    # Test frequent destinations
    print("\n2. Testing frequent destination directories:")
    print("Initial frequent destinations:", config.get_frequent_destination_directories())
    
    test_destinations = ["/Users/test/MediaLibrary", "/Users/test/Photos"]
    for dest in test_destinations:
        config.add_frequent_destination_directory(dest)
        print(f"Added destination: {dest}")
    
    print("Frequent destinations after adding:", config.get_frequent_destination_directories())
    
    # Test last directories functionality
    print("\n3. Testing last directories:")
    config.set_last_source_directories(["/Users/test/LastSource"])
    config.set_last_destination_directories(["/Users/test/LastDest"])
    
    print("Last source directories:", config.get_last_source_directories())
    print("Last destination directories:", config.get_last_destination_directories())
    
    # Test remember setting
    print("\n4. Testing remember last directories setting:")
    print("Remember last dirs:", config.get_remember_last_dirs())
    config.set_remember_last_dirs(False)
    print("Remember last dirs after setting to False:", config.get_remember_last_dirs())
    config.set_remember_last_dirs(True)
    print("Remember last dirs after setting to True:", config.get_remember_last_dirs())
    
    # Test processing options
    print("\n5. Testing processing options:")
    print("Current processing options:", config.get_processing_options())
    config.set_processing_options(move_mode=True, dry_run=True)
    print("Processing options after update:", config.get_processing_options())
    
    print("\n=== Configuration test completed successfully! ===")

if __name__ == "__main__":
    test_config()
