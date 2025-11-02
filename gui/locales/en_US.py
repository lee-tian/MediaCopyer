#!/usr/bin/env python3
"""
English (US) translations for MediaCopyer GUI
"""

translations = {
    # Main Window
    "app_title": "Media Copyer - Media File Organization Tool",
    "main_title": "Media Copyer - Media File Organization Tool",
    "language": "language/语言",
    "source_directory": "Source Directory:",
    "destination_directory": "Destination Directory:",
    "select_source": "Select Source Directory",
    "select_destination": "Select Destination Directory",
    
    # Options Frame
    "options": "Options",
    "move_mode": "Move mode (Move files instead of copy)",
    "dry_run": "Dry run mode (Preview only)",
    "md5_check": "MD5 integrity verification",
    "organization_mode": "Organization Mode",
    "org_by_date": "By Date: Video/2025/2025-07-25",
    "org_by_device": "By Device: Video/2025/DJI",
    "org_by_date_device": "By Date+Device: Video/2025/2025-07-25/DJI",
    "org_by_extension": "By Extension: Video/mp4, Photo/jpg",
    "org_mode_date": "By Date",
    "org_mode_device": "By Device",
    "org_mode_date_device": "By Date+Device",
    "org_mode_extension": "By Extension",
    "dry_run_mode": "Dry run mode",
    "md5_verification": "MD5 integrity verification",
    "ignore_duplicates": "Ignore duplicate files",
    "processing_log": "Processing Log", 
    "source_directories": "Source Directories",
    "destination_directories": "Destination Directories",
    "add_destination": "Add Destination",
    "remove_selected": "Remove Selected",
    "destination": "Destination",
    "source": "Source",
    "path": "Path",
    "select_destination_directory": "Select Destination Directory",
    "select_source_directory": "Select Source Directory",
    
    # Frequent Directories
    "frequent_directories": "Frequent Directories",
    "recent_directories": "Recent Directories",
    "remember_last_dirs": "Remember last directories",
    "frequent_sources": "Frequent Sources",
    "frequent_destinations": "Frequent Destinations",
    "clear_frequent": "Clear Frequent",
    "use_selected": "Use Selected",
    "add_to_frequent": "Add to Frequent",
    "remove_from_frequent": "Remove from Frequent",
    
    # Buttons
    "start": "Start Processing",
    "stop": "Stop",
    "clear_log": "Clear Log",
    "browse": "Browse",
    "start_processing": "Start Processing",
    "cancel_processing": "Cancel",
    
    # Progress and Log
    "progress": "Progress",
    "log": "Log",
    "status_ready": "Ready",
    "status_processing": "Processing...",
    "status_completed": "Completed",
    "status_stopped": "Stopped",
    "status_error": "Error",
    
    # Processing Messages
    "error": "Error",
    "please_select_source_dir": "Please select source directory",
    "please_select_dest_dir": "Please select destination directory",
    "source_dir_invalid": "Source directory is invalid: {}",
    "processing_files": "Processing files...",
    "start_processing_media": "Starting media file processing",
    "dest_directory": "Destination directory: {}",
    "mode_info": "Mode: {}",
    "move_mode_text": "Move mode",
    "copy_mode_text": "Copy mode",
    "dry_run_info": "Dry run mode - Preview only, files will not be actually moved or copied",
    "ignore_duplicates_info": "Ignore duplicates mode - Skip duplicate files without processing",
    "no_media_files_found": "No media files found",
    "found_files_count": "Found {} media files",
    "processing_file_progress": "Processing... ({}/{}) {}",
    "processing_file": "Processing: {}",
    "processing_complete": "Processing completed",
    "photos_processed": "Photos processed: {}",
    "videos_processed": "Videos processed: {}",
    "errors_count": "Errors: {}",
    "total_files": "Total processed: {} files",
    "dry_run_notice": "This was a dry run. No files were actually moved or copied.",
    "complete": "Complete",
    "success_message": "Successfully processed {} files!",
    "warning_message": "Processed {} files with {} errors. Please check the log for details.",
    "serious_error": "A serious error occurred: {}",
    "error_occurred": "An error occurred during processing: {}",
    "ready_status": "Ready",
    "canceling_operation": "Canceling operation...",
    "operation_canceled": "Operation canceled",
    "add_source": "Add Source",
    
    # Tab Names
    "settings": "Settings",
    "execution": "Execution",
    "directory_selection": "Directory Selection",
    
    # Other Messages
    "dependency_warning": "Warning: Some features may be unavailable",
    "select_directories": "Please select source and destination directories first",
    "invalid_source": "Source directory does not exist or is not accessible",
    "invalid_destination": "Destination directory does not exist or is not accessible",
    
    # Settings guidance
    "setup_guidance": "Please complete the directory selection and options configuration above, then switch to the execution tab to start processing files",
    "setup_complete_guidance": "Setup complete! Click the button on the right to switch to the execution tab and start processing files",
    "go_to_execution": "Go to Execution",
    
    # Multi-destination processing messages
    "source_dir_count": "Source directories: {}",
    "source_dir_number": "Source directory {}: {}",
    "dest_dir_count": "Destination directories: {}",
    "dest_dir_number": "Destination directory {}: {}",
    "processing_dest_dir": "Processing destination directory {}/{}: {}",
    "processing_source_to_dest": "Source {}/{}: {}",
    "source_to_dest_complete": "Source {} -> Destination {} complete:",
    "photos_count": "  Photos: {}",
    "videos_count": "  Videos: {}",
    "errors_count_detail": "  Errors: {}",
    "total_count": "  Total: {}",
    "source_to_dest_error": "Source {} -> Destination {} processing error: {}",
    "all_destinations_complete": "All destinations processing complete",
    "total_photos": "Total photos: {}",
    "total_videos": "Total videos: {}",
    "total_errors": "Total errors: {}",
    "total_processed": "Total processed: {}",
    "dest_progress_status": "Destination {}/{}, Source {}/{}: {}",
    "success_multi_dest": "Successfully processed {} files to {} destination directories",
    "warning_multi_dest": "Processed {} files, but {} errors occurred",
    
    # Log messages for parallel processing
    "parallel_start_processing": "[Parallel] Starting processing: Source {}/{} -> Destination {}/{}",
    "parallel_source_dir": "[Parallel] Source directory: {}",
    "parallel_dest_dir": "[Parallel] Destination directory: {}",
    "parallel_no_media_files": "[Parallel] No media files found in source directory {}",
    "parallel_processing_file": "[Parallel] Processing file: {}",
    "parallel_source_dest_complete": "[Parallel] Source {} -> Destination {} complete:",
    "parallel_photos": "[Parallel]   Photos: {}",
    "parallel_videos": "[Parallel]   Videos: {}",
    "parallel_errors": "[Parallel]   Errors: {}",
    "parallel_total": "[Parallel]   Total: {}",
    "parallel_task_exception": "[Parallel] Task execution exception: Source {} -> Destination {}: {}",
    "parallel_all_complete": "✅ All destinations processing complete (Parallel mode)",
    "parallel_using_threads": "Using {} parallel threads to process {} source directories",
    
    # Size analysis log messages
    "source_size_analysis": "📊 Source Directory Size Analysis",
    "source_dir_info": "Source directory {}: {}",
    "total_files": "  📁 Total files: {}",
    "photos_info": "  📷 Photos: {} files ({:.1f} MB)",
    "videos_info": "  🎥 Videos: {} files ({:.1f} MB)",
    "media_files_total": "  📊 Media files total: {} files ({:.1f} MB)",
    "all_sources_summary": "🎯 All source directories summary:",
    "total_media_files": "  📊 Total media files: {}",
    "total_media_size": "  💾 Total media size: {:.1f} MB",
    "estimated_space_needed": "  🔧 Estimated space needed: {:.1f} MB ({} to {} destinations)",
    "dest_space_check": "💽 Destination Directory Space Check:",
    "space_status_sufficient": "✅ Sufficient",
    "space_status_insufficient": "⚠️ Insufficient",
    "dest_space_info": "  Destination {}: {:.1f} MB available / {:.1f} MB needed - {}",
    "dest_space_check_failed": "  Destination {}: Unable to check space - {}",
    "space_warning": "⚠️ Space warning: {}",
    "start_parallel_processing": "🚀 Starting Parallel Processing",
    "processing_dest_header": "Processing destination directory {}/{}: {}",
    "dest_size_analysis": "📊 Destination Directory Size Analysis",
    "dest_dir_info": "Destination directory {}: {}",
    "all_dests_summary": "🎯 All destination directories summary:",
    "size_comparison": "📈 Size Comparison Analysis:",
    "source_comparison": "  Source directories: {} files, {}",
    "dest_comparison": "  Destination directories: {} files, {}",
    "files_match_move": "  ✅ File count matches (Move mode)",
    "files_mismatch": "  ⚠️ File count mismatch: difference of {} files",
    "move_mode_text_short": "move",
    "copy_mode_text_short": "copy",
    
    # Core module messages
    "removed_empty_directory": "Removed empty directory: {}",
    "cleaned_up_empty_directories": "Cleaned up {} empty directories",
    "warning_empty_dir_cleanup": "Warning: Error during empty directory cleanup: {}",
    
    # Copy completion messages
    "files_copy_complete": "  ✅ Files copied completely ({} destinations)",
    "copy_ratio": "  📊 Copy ratio: {:.1f}x (expected {}x)",
    "parallel_success_message": "Successfully processed {} files in parallel to {} destination directories",
    "parallel_warning_message": "Processed {} files in parallel, but {} errors occurred",
    "processing_complete_log": "Processing complete: {} files, {} errors",
    "parallel_progress_status": "[Parallel] Source{}->Destination{}: {}",
    "parallel_processing_error": "[Parallel] Source {} -> Destination {} processing error: {}",
    
    # Duplicate file handling
    "total_duplicates": "Total duplicates: {}",
    "total_skipped": "Total skipped: {}",
    "parallel_duplicates": "[Parallel]   Duplicates: {}",
    "parallel_skipped": "[Parallel]   Skipped: {}",
    
    # Enhanced copy analysis
    "copy_operation_summary": "📋 Copy Operation Summary:",
    "files_copied_this_time": "  📤 Files copied this time: {}",
    "size_copied_this_time": "  💾 Size copied this time: {}",
    "dest_increase_files": "  📈 Destination files increased by: {}",
    "dest_increase_size": "  📈 Destination size increased by: {}",
    "copy_match_analysis": "🔍 Copy Match Analysis:",
    "copy_files_match": "  ✅ Copied file count matches expected",
    "copy_files_mismatch": "  ⚠️ Copied file count mismatch: expected {}, actual {}, difference {}",
    "copy_size_match": "  ✅ Copied size matches expected",
    "copy_size_mismatch": "  ⚠️ Copied size mismatch: expected {}, actual {}, difference {}",
    "dest_before_after": "📊 Destination Before/After Comparison:",
    "dest_before": "  📥 Before copy: {} files, {}",
    "dest_after": "  📤 After copy: {} files, {}",
    "net_increase": "  📈 Net increase: {} files, {}",
    
    # Menu items
    "help_menu": "Help",
    "window_menu": "Window",
    "user_guide": "User Guide",
    "keyboard_shortcuts": "Keyboard Shortcuts",
    "report_issue": "Report Issue",
    "check_updates": "Check for Updates",
    "about": "About",
    "close": "Close",
    
    # About dialog
    "app_name": "Application Name",
    "version": "Version",
    "author": "Author",
    "description": "Description",
    "features": "Features",
    "feature_auto_organize": "Automatically organize photos and videos by date",
    "feature_date_based": "Smart date recognition based on EXIF data",
    "feature_duplicate_handling": "Intelligent duplicate file handling",
    "feature_preview_mode": "Preview mode (dry run)",
    "feature_multilingual": "Multi-language support (Chinese/English)",
    "feature_batch_processing": "Batch processing of multiple directories",
    "supported_formats": "Supported Formats",
    "image_formats": "Image Formats",
    "video_formats": "Video Formats",
    "license": "License",
    
    # User guide content
    "user_guide_content": """MediaCopyer User Guide

📋 Basic Usage Steps:

1. Select Source Directories
   • Click "Add Source" button to select folders containing photos and videos
   • You can add multiple source directories for batch processing
   • Supports importing from SD cards, cameras, phones, etc.

2. Select Destination Directories
   • Click "Add Destination" button to select where organized files will be stored
   • You can add multiple destination directories to copy files to all targets
   • Recommend selecting directories with sufficient space

3. Configure Options
   • Organization Mode: Choose to organize by date, device, or file type
   • Move Mode: Check to move files instead of copying
   • Dry Run: Check to preview without actually operating on files
   • MD5 Verification: Ensure file integrity
   • Ignore Duplicates: Skip existing duplicate files

4. Start Processing
   • Click "Go to Execution" to switch to execution interface
   • View progress and detailed logs
   • Check statistics after processing completes

🔧 Advanced Features:

• Multi-directory parallel processing: Process multiple sources to multiple destinations simultaneously
• Smart date recognition: Extract dates from EXIF data, filenames, modification times
• Duplicate file detection: Identify duplicates based on MD5 hash values
• Space checking: Automatically check available space in destination directories
• Detailed statistics: Show number of processed files, sizes, etc.

📁 File Organization Structure:

By Date:
  Photos/2025/2025-01-15/
  Videos/2025/2025-01-15/

By Device:
  Photos/iPhone/
  Videos/DJI/

By Date+Device:
  Photos/2025/2025-01-15/iPhone/
  Videos/2025/2025-01-15/DJI/

By File Type:
  jpg/
  mp4/
  mov/

⚠️ Important Notes:

• First-time users should enable "Dry Run" mode to preview results
• Move mode will delete source files, use with caution
• Check destination directory space before processing large amounts of files
• Regularly backup important files

💡 Usage Tips:

• Use "Remember last directories" feature for quick repeated operations
• Add frequently used directories to favorites
• Check detailed logs to understand the processing
• Use multi-language interface (Chinese/English)""",
    
    # Keyboard shortcuts content
    "shortcuts_content": """MediaCopyer Keyboard Shortcuts

⌨️ General Shortcuts:
• Ctrl+Q / Cmd+Q: Quit application
• Ctrl+, / Cmd+,: Open preferences
• F1: Show help
• F5: Refresh interface

📁 Directory Operations:
• Ctrl+O / Cmd+O: Select source directory
• Ctrl+Shift+O / Cmd+Shift+O: Select destination directory
• Delete: Remove selected directory

▶️ Processing Operations:
• Ctrl+Enter / Cmd+Enter: Start processing
• Escape: Stop processing
• Ctrl+L / Cmd+L: Clear log

🔄 Interface Navigation:
• Ctrl+1 / Cmd+1: Switch to Settings tab
• Ctrl+2 / Cmd+2: Switch to Execution tab
• Tab: Switch focus between controls

📋 Other:
• Ctrl+C / Cmd+C: Copy log content
• Ctrl+A / Cmd+A: Select all log content
• Ctrl+F / Cmd+F: Find in log""",
}
