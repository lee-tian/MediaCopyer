#!/usr/bin/env python3
"""
Internationalization (i18n) support for MediaCopyer GUI
"""

import tkinter as tk
import json
import os
from typing import Dict, Any, Optional


class I18nManager:
    """Internationalization manager for handling multiple languages"""
    
    def __init__(self):
        self.current_language = "zh_CN"  # Default to Chinese
        self.languages = {}
        self.observers = []  # List of callbacks to notify when language changes
        self._load_languages()
    
    def _load_languages(self):
        """Load language definitions"""
        self.languages = {
            "zh_CN": {
                # Main Window
                "app_title": "Media Copyer - 媒体文件整理工具",
                "main_title": "Media Copyer - 媒体文件整理工具",
                "language": "语言",
                "source_directory": "源目录 (Source Directory):",
                "destination_directory": "目标目录 (Destination Directory):",
                "select_source": "选择源目录",
                "select_destination": "选择目标目录",
                
                # Options Frame
                "options": "选项",
                "move_mode": "移动模式 (Move files instead of copy)",
                "dry_run": "试运行模式 (Dry run - preview only)",
                "md5_check": "MD5完整性校验 (MD5 integrity verification)",
                "organization_mode": "组织方式 (Organization Mode):",
                "org_by_date": "按日期 (By Date): Video/2025/2025-07-25",
                "org_by_device": "按设备 (By Device): Video/2025/DJI",
                "org_by_date_device": "按日期+设备 (By Date+Device): Video/2025/2025-07-25/DJI",
                "org_mode_date": "按日期",
                "org_mode_device": "按设备", 
                "org_mode_date_device": "按日期+设备",
                "dry_run_mode": "试运行模式",
                "md5_verification": "MD5完整性校验",
                "processing_log": "处理日志",
                
                # Buttons
                "start": "开始处理",
                "stop": "停止",
                "clear_log": "清空日志",
                "browse": "浏览",
                "start_processing": "开始处理",
                
                # Progress and Log
                "progress": "进度",
                "log": "日志",
                "status_ready": "就绪",
                "status_processing": "正在处理...",
                "status_completed": "完成",
                "status_stopped": "已停止",
                "status_error": "错误",
                
                # Processing Messages
                "error": "错误",
                "please_select_source_dir": "请选择源目录",
                "please_select_dest_dir": "请选择目标目录",
                "source_dir_invalid": "源目录无效: {}",
                "processing_files": "正在处理文件...",
                "start_processing_media": "开始处理媒体文件",
                "dest_directory": "目标目录: {}",
                "mode_info": "模式: {}",
                "move_mode_text": "移动模式",
                "copy_mode_text": "复制模式",
                "dry_run_info": "试运行模式 - 仅预览，不会实际移动或复制文件",
                "no_media_files_found": "未找到媒体文件",
                "found_files_count": "找到 {} 个媒体文件",
                "processing_file_progress": "处理中... ({}/{}) {}",
                "processing_file": "正在处理: {}",
                "processing_complete": "处理完成",
                "photos_processed": "已处理照片: {} 张",
                "videos_processed": "已处理视频: {} 个",
                "errors_count": "处理出错: {} 个",
                "total_files": "总计处理: {} 个文件",
                "dry_run_notice": "这是试运行模式，实际上没有移动或复制文件。",
                "complete": "完成",
                "success_message": "成功处理了 {} 个文件！",
                "warning_message": "处理了 {} 个文件，其中 {} 个出现错误。请检查日志获取详情。",
                "serious_error": "发生严重错误: {}",
                "error_occurred": "处理过程中发生错误: {}",
                "ready_status": "就绪",
                
                # Other Messages
                "dependency_warning": "可以继续使用，但会影响日期识别精度",
                "select_directories": "请先选择源目录和目标目录",
                "invalid_source": "源目录不存在或无法访问",
                "invalid_destination": "目标目录不存在或无法访问",
            },
            
            "en_US": {
                # Main Window
                "app_title": "Media Copyer - Media File Organization Tool",
                "main_title": "Media Copyer - Media File Organization Tool",
                "language": "Language",
                "source_directory": "Source Directory:",
                "destination_directory": "Destination Directory:",
                "select_source": "Select Source Directory",
                "select_destination": "Select Destination Directory",
                
                # Options Frame
                "options": "Options",
                "move_mode": "Move mode (Move files instead of copy)",
                "dry_run": "Dry run mode (Preview only)",
                "md5_check": "MD5 integrity verification",
                "organization_mode": "Organization Mode:",
                "org_by_date": "By Date: Video/2025/2025-07-25",
                "org_by_device": "By Device: Video/2025/DJI",
                "org_by_date_device": "By Date+Device: Video/2025/2025-07-25/DJI",
                "org_mode_date": "By Date",
                "org_mode_device": "By Device",
                "org_mode_date_device": "By Date+Device",
                "dry_run_mode": "Dry run mode",
                "md5_verification": "MD5 integrity verification",
                "processing_log": "Processing Log",
                
                # Buttons
                "start": "Start Processing",
                "stop": "Stop",
                "clear_log": "Clear Log",
                "browse": "Browse",
                "start_processing": "Start Processing",
                
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
                
                # Other Messages
                "dependency_warning": "Can continue, but date recognition accuracy may be affected",
                "select_directories": "Please select source and destination directories first",
                "invalid_source": "Source directory does not exist or is not accessible",
                "invalid_destination": "Destination directory does not exist or is not accessible",
            }
        }
    
    def get_text(self, key: str, default: str = None) -> str:
        """Get localized text for the given key"""
        if self.current_language in self.languages:
            return self.languages[self.current_language].get(key, default or key)
        return default or key
    
    def set_language(self, language: str):
        """Set the current language and notify observers"""
        if language in self.languages:
            self.current_language = language
            self._notify_observers()
    
    def get_available_languages(self) -> Dict[str, str]:
        """Get available languages with their display names"""
        return {
            "zh_CN": "中文",
            "en_US": "English"
        }
    
    def get_current_language(self) -> str:
        """Get current language code"""
        return self.current_language
    
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
    
    def destroy(self):
        """Clean up i18n observer when widget is destroyed"""
        i18n.remove_observer(self._update_i18n_text)
        super().destroy()
