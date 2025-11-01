#!/usr/bin/env python3
"""
测试国际化日志功能
"""

import sys
from pathlib import Path

# Add the project root to the path (parent of tests directory)
sys.path.insert(0, str(Path(__file__).parent.parent))

from gui.i18n import i18n, _

def test_i18n_logs():
    """测试国际化日志消息"""
    
    print("测试国际化日志功能...")
    print()
    
    # 测试中文
    print("=== 中文测试 ===")
    i18n.set_language('zh_CN')
    
    test_messages = [
        ("parallel_start_processing", (1, 2, 1, 3)),
        ("parallel_source_dir", ("/path/to/source",)),
        ("parallel_dest_dir", ("/path/to/dest",)),
        ("source_size_analysis", ()),
        ("total_files", (150,)),
        ("photos_info", (100, 250.5)),
        ("videos_info", (50, 1024.8)),
        ("space_status_sufficient", ()),
        ("space_status_insufficient", ()),
        ("parallel_all_complete", ()),
        ("parallel_success_message", (100, 3)),
        ("parallel_warning_message", (100, 5)),
        ("files_copy_complete", (3,)),
        ("copy_ratio", (3.0, 3)),
    ]
    
    for key, args in test_messages:
        try:
            message = _(key)
            if args:
                message = message.format(*args)
            print(f"  {key}: {message}")
        except Exception as e:
            print(f"  {key}: ERROR - {e}")
    
    print()
    
    # 测试英文
    print("=== English Test ===")
    i18n.set_language('en_US')
    
    for key, args in test_messages:
        try:
            message = _(key)
            if args:
                message = message.format(*args)
            print(f"  {key}: {message}")
        except Exception as e:
            print(f"  {key}: ERROR - {e}")
    
    print()
    
    # 测试自动检测
    print("=== Auto Detection Test ===")
    i18n.set_language('auto')
    current_lang = i18n.get_current_language()
    print(f"Auto detected language: {current_lang}")
    
    # 测试一些消息
    print(f"Sample message: {_('parallel_start_processing').format(1, 2, 1, 3)}")
    
    print()
    print("✅ 国际化日志测试完成")

if __name__ == "__main__":
    test_i18n_logs()