#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MediaCopyer 版本信息
"""

__version__ = "1.1.1"
__build__ = "20251101"
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
    },
    "1.1.0": {
        "date": "2025-11-01",
        "changes": [
            "添加忽略重复文件选项",
            "增强了复制操作分析功能", 
            "显示详细的文件复制统计信息",
            "支持跳过重复文件而不是移动到重复文件夹"
        ]
    },
    "1.1.1": {
        "date": "2025-11-01",
        "changes": [
            "添加自动GitHub发布功能",
            "集成GitHub CLI实现一键发布",
            "新增完整的帮助菜单和用户指南",
            "修复macOS应用菜单显示问题",
            "优化安装界面，去除版本号显示",
            "更新所有GitHub链接到正确仓库地址",
            "改进发布流程和构建脚本"
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
    return "MediaCopyer"

def get_dmg_name():
    """获取DMG文件名"""
    return f"MediaCopyer-v{__version__}.dmg"

def get_app_bundle_name():
    """获取应用包名称"""
    return "MediaCopyer.app"