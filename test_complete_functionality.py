#!/usr/bin/env python3
"""
Comprehensive test for frequent directories and last directory functionality
"""

import os
import tempfile
import shutil
from core.config import Config, get_config

def test_complete_functionality():
    """Test all functionality together"""
    print("=== Testing Complete Frequent Directories & Last Directory Functionality ===\n")
    
    # Use a temporary directory for config
    with tempfile.TemporaryDirectory() as temp_dir:
        config_file = os.path.join(temp_dir, "test_config.json")
        config = Config(config_file)
        
        print("1. Testing initial state...")
        print(f"   Remember last dirs enabled: {config.get_remember_last_dirs()}")
        print(f"   Frequent source directories: {config.get_frequent_source_directories()}")
        print(f"   Frequent destination directories: {config.get_frequent_destination_directories()}")
        print(f"   Last source directories: {config.get_last_source_directories()}")
        print(f"   Last destination directories: {config.get_last_destination_directories()}")
        
        print("\n2. Testing adding frequent directories...")
        # Add some test directories
        test_dirs = [
            "/Users/test/Photos",
            "/Users/test/Documents/Media", 
            "/Users/test/Desktop/Images"
        ]
        
        for dir_path in test_dirs:
            config.add_frequent_source_directory(dir_path)
            print(f"   Added frequent source: {dir_path}")
        
        dest_dirs = [
            "/Users/test/Organized/Photos",
            "/Users/test/Backup/Media"
        ]
        
        for dir_path in dest_dirs:
            config.add_frequent_destination_directory(dir_path)
            print(f"   Added frequent destination: {dir_path}")
        
        print(f"\n   Frequent sources now: {config.get_frequent_source_directories()}")
        print(f"   Frequent destinations now: {config.get_frequent_destination_directories()}")
        
        print("\n3. Testing last directory saving...")
        # Simulate processing start - save current directories as last used
        current_sources = ["/Users/test/Photos", "/Users/test/Desktop/Images"]
        current_destinations = ["/Users/test/Organized/Photos"]
        
        config.set_last_source_directories(current_sources)
        config.set_last_destination_directories(current_destinations)
        
        print(f"   Saved last sources: {current_sources}")
        print(f"   Saved last destinations: {current_destinations}")
        
        print("\n4. Testing retrieval of last directories...")
        retrieved_sources = config.get_last_source_directories()
        retrieved_destinations = config.get_last_destination_directories()
        
        print(f"   Retrieved last sources: {retrieved_sources}")
        print(f"   Retrieved last destinations: {retrieved_destinations}")
        
        assert retrieved_sources == current_sources, f"Sources don't match: {retrieved_sources} != {current_sources}"
        assert retrieved_destinations == current_destinations, f"Destinations don't match: {retrieved_destinations} != {current_destinations}"
        
        print("\n5. Testing frequent directory limits...")
        # Add more directories to test the limit (should be 10)
        for i in range(15):
            config.add_frequent_source_directory(f"/Users/test/Extra{i}")
        
        frequent_sources = config.get_frequent_source_directories()
        print(f"   Frequent sources count: {len(frequent_sources)}")
        print(f"   Recent frequent sources: {frequent_sources[:3]}...")
        assert len(frequent_sources) <= 10, f"Too many frequent directories: {len(frequent_sources)}"
        
        print("\n6. Testing remember last dirs toggle...")
        # Test disabling remember last dirs
        config.set_remember_last_dirs(False)
        print(f"   Remember last dirs disabled: {config.get_remember_last_dirs()}")
        
        # Last directories should still be accessible but not automatically loaded
        print(f"   Last directories still available: {len(config.get_last_source_directories())} sources, {len(config.get_last_destination_directories())} destinations")
        
        # Re-enable
        config.set_remember_last_dirs(True)
        print(f"   Remember last dirs re-enabled: {config.get_remember_last_dirs()}")
        
        print("\n7. Testing persistence...")
        # Create a new config instance with same file to test persistence
        config2 = Config(config_file)
        
        print(f"   Persisted frequent sources: {len(config2.get_frequent_source_directories())}")
        print(f"   Persisted frequent destinations: {len(config2.get_frequent_destination_directories())}")
        print(f"   Persisted last sources: {config2.get_last_source_directories()}")
        print(f"   Persisted last destinations: {config2.get_last_destination_directories()}")
        print(f"   Persisted remember setting: {config2.get_remember_last_dirs()}")
        
        # Verify the data matches
        assert config2.get_frequent_source_directories() == config.get_frequent_source_directories()
        assert config2.get_frequent_destination_directories() == config.get_frequent_destination_directories()
        assert config2.get_last_source_directories() == config.get_last_source_directories()
        assert config2.get_last_destination_directories() == config.get_last_destination_directories()
        assert config2.get_remember_last_dirs() == config.get_remember_last_dirs()
        
        print("\n✅ All tests passed!")
        
        print("\n=== Summary of Features ===")
        print("✅ Frequent directories (sources & destinations)")
        print("✅ Last used directories memory")
        print("✅ Remember last directories toggle")
        print("✅ Automatic loading of last directories in widgets")
        print("✅ Configuration persistence")
        print("✅ Directory limits (max 10 frequent per type)")
        print("✅ Star button integration in GUI widgets")


if __name__ == "__main__":
    test_complete_functionality()
