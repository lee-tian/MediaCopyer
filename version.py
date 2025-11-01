#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MediaCopyer 版本信息
"""

__version__ = "1.0.0"
__build__ = "20241101"
__author__ = "MediaCopyer Team"
__description__ = "A Python application to automatically organize photos and videos by their creation date"

# 版本历史
VERSION_HISTORY = {
    "1.0.0": {
        "date": "2024-11-01",
        "changes": [
            "初始版本发布",
            "支持照片和视频按日期自动整理",
            "提供GUI和命令行两种界面",
            "支持中英文双语",
            "支持复制和移动两种模式",
            "支持预览模式（dry-run）",
            "自动处理重复文件名",
            "支持多种图片和视频格式"
        ]
    }
}

def get_version():
    """获取版本号"""
    return __version__

def get_full_version():
    """获取完整版本信息"""
    return f"{__version__} (build {__build__})"

def get_app_name():
    """获取应用名称"""
    return f"MediaCopyer v{__version__}"

def get_dmg_name():
    """获取DMG文件名"""
    return f"MediaCopyer-v{__version__}.dmg"

def get_app_bundle_name():
    """获取应用包名称"""
    return f"MediaCopyer-v{__version__}.app"