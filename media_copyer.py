#!/usr/bin/env python3
"""
Media Copyer - Organize media files by date into structured directories
"""

import sys
import argparse
from pathlib import Path

# Import from the new modular core library
from core import organize_media_files, validate_directory

def main():
    parser = argparse.ArgumentParser(description='Organize media files by date into structured directories')
    parser.add_argument('source', help='Source directory containing media files')
    parser.add_argument('destination', help='Destination directory for organized files')
    parser.add_argument('--move', action='store_true', 
                       help='Move files instead of copying (default: copy)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be done without actually moving/copying files')
    parser.add_argument('--by-device', action='store_true',
                       help='Organize files by device (camera/drone) instead of type and date')
    
    args = parser.parse_args()
    
    source_dir = Path(args.source)
    dest_dir = Path(args.destination)
    
    # Validate source directory using the new utility function
    if not validate_directory(str(source_dir), must_exist=True):
        print(f"Error: Source directory '{source_dir}' does not exist or is not a directory!")
        sys.exit(1)
    
    # Validate destination directory (create if needed)
    if not validate_directory(str(dest_dir), must_exist=False):
        print(f"Error: Cannot create or access destination directory '{dest_dir}'!")
        sys.exit(1)
    
    print("Media Copyer - Organizing your media files")
    print("="*50)
    print(f"Source: {source_dir}")
    print(f"Destination: {dest_dir}")
    print(f"Mode: {'Move' if args.move else 'Copy'}")
    print(f"Organization: {'By Device' if args.by_device else 'By Type and Date'}")
    print("="*50)
    
    # Use the new modular organize function
    try:
        organize_media_files(
            source_dir=source_dir,
            dest_dir=dest_dir,
            move_mode=args.move,
            dry_run=args.dry_run,
            by_device=args.by_device
        )
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError during organization: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
