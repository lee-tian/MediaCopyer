#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
版本号更新脚本
"""

import sys
import re
from datetime import datetime

def update_version(new_version, changes=None):
    """更新版本号"""
    
    # 读取当前版本文件
    with open('version.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 更新版本号
    content = re.sub(r'__version__ = "[^"]*"', f'__version__ = "{new_version}"', content)
    
    # 更新构建号
    build_date = datetime.now().strftime("%Y%m%d")
    content = re.sub(r'__build__ = "[^"]*"', f'__build__ = "{build_date}"', content)
    
    # 如果提供了更新内容，添加到版本历史
    if changes:
        today = datetime.now().strftime("%Y-%m-%d")
        
        # 查找VERSION_HISTORY的位置
        history_pattern = r'(VERSION_HISTORY = \{.*?)(\n\})'
        
        # 格式化更新内容为多行格式
        formatted_changes = '[\n'
        for change in changes:
            formatted_changes += f'            "{change}",\n'
        formatted_changes = formatted_changes.rstrip(',\n') + '\n        ]'
        
        new_version_entry = f''',
    "{new_version}": {{
        "date": "{today}",
        "changes": {formatted_changes}
    }}'''
        
        def replace_history(match):
            existing_content = match.group(1)
            closing_brace = match.group(2)
            # 在现有内容后添加新版本
            return existing_content + new_version_entry + closing_brace
        
        content = re.sub(history_pattern, replace_history, content, flags=re.DOTALL)
    
    # 写回文件
    with open('version.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"版本已更新为: {new_version}")
    if changes:
        print("更新内容已添加到版本历史")

def show_help():
    """显示帮助信息"""
    print("MediaCopyer 版本更新脚本")
    print("=" * 40)
    print()
    print("用法:")
    print("  python update_version.py <新版本号> [更新内容...]")
    print()
    print("参数:")
    print("  新版本号    版本号格式为 x.y.z (如 1.0.0, 2.1.3)")
    print("  更新内容    可选，描述本次更新的内容")
    print()
    print("示例:")
    print("  python update_version.py 1.1.0")
    print("  python update_version.py 1.1.0 '修复了重复文件处理bug'")
    print("  python update_version.py 1.2.0 '添加忽略重复文件选项' '增强了复制操作分析'")
    print()
    print("选项:")
    print("  --help, -h  显示此帮助信息")

def main():
    """主函数"""
    if len(sys.argv) < 2 or sys.argv[1] in ['--help', '-h', 'help']:
        show_help()
        sys.exit(0)
    
    new_version = sys.argv[1]
    
    # 验证版本号格式
    if not re.match(r'^\d+\.\d+\.\d+$', new_version):
        print("错误: 版本号格式应为 x.y.z (如 1.0.0)")
        print()
        print("使用 --help 查看详细用法")
        sys.exit(1)
    
    # 获取更新内容
    changes = None
    if len(sys.argv) > 2:
        changes = sys.argv[2:]
    
    update_version(new_version, changes)

if __name__ == '__main__':
    main()