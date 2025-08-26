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
    parser.add_argument('--organization-mode', choices=['date', 'device', 'date_device'], 
                       default='date',
                       help='Organization mode: date (Video/2025/2025-07-25), device (Video/2025/DJI), or date_device (Video/2025/2025-07-25/DJI)')
    parser.add_argument('--verify-md5', action='store_true',
                       help='Verify file integrity using MD5 checksums after copying (slower but safer)')
    # Keep backward compatibility
    parser.add_argument('--by-device', action='store_true',
                       help='Organize files by device (same as --organization-mode device) - deprecated')
    
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
    
    # Determine organization mode (handle backward compatibility)
    organization_mode = args.organization_mode
    if args.by_device:
        organization_mode = 'device'
        print("Warning: --by-device is deprecated. Use --organization-mode device instead.")
    
    # Description mapping for display
    mode_descriptions = {
        'date': 'By Date (Video/2025/2025-07-25)',
        'device': 'By Device (Video/2025/DJI)',
        'date_device': 'By Date and Device (Video/2025/2025-07-25/DJI)'
    }
    
    print("Media Copyer - Organizing your media files")
    print("="*50)
    print(f"Source: {source_dir}")
    print(f"Destination: {dest_dir}")
    print(f"Mode: {'Move' if args.move else 'Copy'}")
    print(f"Organization: {mode_descriptions[organization_mode]}")
    if args.dry_run:
        print("DRY RUN: No files will actually be moved/copied")
    print("="*50)
    
    # Use the new modular organize function
    def progress_callback(current, total, filename):
        print(f"Processing [{current}/{total}]: {filename}")
    
    try:
        stats = organize_media_files(
            source_dir=source_dir,
            dest_dir=dest_dir,
            move_mode=args.move,
            dry_run=args.dry_run,
            verify_md5=args.verify_md5,
            organization_mode=organization_mode,
            progress_callback=progress_callback
        )
        
        # Print results
        print("\n" + "="*50)
        print("Organization Complete!")
        print(f"Total files processed: {stats['processed']}")
        print(f"Photos: {stats['photos']}")
        print(f"Videos: {stats['videos']}")
        print(f"Errors: {stats['errors']}")
        if stats['devices']:
            print(f"Devices found: {', '.join(sorted(stats['devices']))}")
        print("="*50)
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError during organization: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
