#!/usr/bin/env python3
"""
Test the extension-based organization mode functionality
"""

import os
import tempfile
import shutil
from pathlib import Path
from core.organizer.media_organizer import MediaOrganizer


def test_extension_organization():
    """Test that files are organized correctly by extension"""
    print("Testing extension-based organization mode...")
    
    # Create temporary directories for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        dest_dir = Path(temp_dir) / "destination"
        
        # Create source directory
        source_dir.mkdir()
        
        # Create test files with different extensions
        test_files = [
            "photo1.jpg",
            "photo2.jpeg", 
            "photo3.png",
            "photo4.heic",
            "video1.mp4",
            "video2.mov",
            "video3.avi",
            "video4.mkv",
            "document.pdf",
            "music.mp3"
        ]
        
        # Create the test files
        for filename in test_files:
            test_file = source_dir / filename
            test_file.write_text(f"Test content for {filename}")
            print(f"Created test file: {test_file}")
        
        # Initialize MediaOrganizer
        organizer = MediaOrganizer()
        
        print(f"\nTesting extension organization mode...")
        print(f"Source directory: {source_dir}")
        print(f"Destination directory: {dest_dir}")
        
        # Process files using extension-based organization
        results = organizer.organize_files(
            source_dir=str(source_dir),
            target_dir=str(dest_dir),
            organize_by="extension",
            copy_mode=True,  # Copy mode
            duplicate_action="rename",
            verify_integrity=False
        )
        
        print(f"\nProcessing results:")
        print(f"Total files: {results.get('total_files', 0)}")
        print(f"Processed files: {results.get('processed_files', 0)}")
        print(f"Failed files: {results.get('failed_files', 0)}")
        print(f"Skipped files: {results.get('skipped_files', 0)}")
        print(f"Errors: {len(results.get('errors', []))}")
        
        if results.get('errors'):
            print("Error details:")
            for error in results.get('errors', []):
                print(f"  - {error}")
        
        # Verify the directory structure
        print(f"\nVerifying destination directory structure:")
        for root, dirs, files in os.walk(dest_dir):
            level = root.replace(str(dest_dir), '').count(os.sep)
            indent = ' ' * 2 * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 2 * (level + 1)
            for file in files:
                print(f"{subindent}{file}")
        
        # Check expected structure - extension mode organizes directly by extension
        expected_extensions = ["jpg", "jpeg", "png", "heic", "mp4", "mov", "avi", "mkv", "pdf", "mp3"]
        
        print(f"\nVerifying expected file organization:")
        all_correct = True
        
        for ext in expected_extensions:
            ext_dir = dest_dir / ext
            if not ext_dir.exists():
                print(f"❌ Extension directory missing: {ext}")
                all_correct = False
                continue
            
            # Check if files with this extension exist in the directory
            files_with_ext = list(ext_dir.glob(f"*.{ext}"))
            if not files_with_ext:
                print(f"❌ No files found in: {ext}/")
                all_correct = False
            else:
                print(f"✅ Found {len(files_with_ext)} files in: {ext}/")
        
        if all_correct:
            print(f"\n🎉 Extension-based organization test PASSED!")
        else:
            print(f"\n❌ Extension-based organization test FAILED!")
        
        return all_correct


if __name__ == "__main__":
    try:
        success = test_extension_organization()
        if success:
            print("\n✅ All extension organization tests passed!")
        else:
            print("\n❌ Some extension organization tests failed!")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
