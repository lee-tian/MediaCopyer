#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MediaCopyer 发布快捷脚本
重定向到 scripts/release/release.py
"""

import subprocess
import sys
import os

def main():
    """主函数"""
    print("MediaCopyer 发布快捷脚本")
    print("重定向到: scripts/release/release.py")
    print("=" * 50)
    
    # 检查发布脚本是否存在
    release_script = "scripts/release/release.py"
    if not os.path.exists(release_script):
        print(f"错误: 未找到发布脚本 {release_script}")
        sys.exit(1)
    
    # 执行发布脚本
    try:
        result = subprocess.run([sys.executable, release_script] + sys.argv[1:])
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        print("\n发布已取消")
        sys.exit(1)
    except Exception as e:
        print(f"执行发布脚本时发生错误: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()