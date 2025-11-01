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
        history_pattern = r'(VERSION_HISTORY = \{[^}]*)\}'
        
        new_version_entry = f'''    "{new_version}": {{
        "date": "{today}",
        "changes": {changes}
    }},'''
        
        def replace_history(match):
            existing_content = match.group(1)
            # 在现有内容后添加新版本
            return existing_content + '\n' + new_version_entry + '\n}'
        
        content = re.sub(history_pattern, replace_history, content, flags=re.DOTALL)
    
    # 写回文件
    with open('version.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"版本已更新为: {new_version}")
    if changes:
        print("更新内容已添加到版本历史")

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python update_version.py <新版本号> [更新内容...]")
        print("示例: python update_version.py 1.1.0 '修复了重复文件处理bug' '添加了新的文件格式支持'")
        sys.exit(1)
    
    new_version = sys.argv[1]
    
    # 验证版本号格式
    if not re.match(r'^\d+\.\d+\.\d+$', new_version):
        print("错误: 版本号格式应为 x.y.z (如 1.0.0)")
        sys.exit(1)
    
    # 获取更新内容
    changes = None
    if len(sys.argv) > 2:
        changes = sys.argv[2:]
        # 转换为Python列表格式
        changes = str(changes).replace("'", '"')
    
    update_version(new_version, changes)

if __name__ == '__main__':
    main()