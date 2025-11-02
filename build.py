#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MediaCopyer 构建快捷脚本
重定向到 scripts/build/build_app.py
"""

import subprocess
import sys
import os

def main():
    """主函数"""
    print("MediaCopyer 构建快捷脚本")
    print("重定向到: scripts/build/build_app.py")
    print("=" * 50)
    
    # 检查构建脚本是否存在
    build_script = "scripts/build/build_app.py"
    if not os.path.exists(build_script):
        print(f"错误: 未找到构建脚本 {build_script}")
        sys.exit(1)
    
    # 执行构建脚本
    try:
        result = subprocess.run([sys.executable, build_script] + sys.argv[1:])
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        print("\n构建已取消")
        sys.exit(1)
    except Exception as e:
        print(f"执行构建脚本时发生错误: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()