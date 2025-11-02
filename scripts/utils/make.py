#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MediaCopyer Make脚本
提供简洁的构建和发布命令
"""

import sys
import subprocess
import os
from pathlib import Path

# 添加项目根目录到路径，以便导入version模块
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def show_help():
    """显示帮助信息"""
    print("MediaCopyer Make脚本")
    print("=" * 30)
    print()
    print("用法: python scripts/utils/make.py <命令> [参数...]")
    print()
    print("命令:")
    print("  build                    构建应用程序")
    print("  release <version>        发布新版本")
    print("  patch [changes...]       发布补丁版本 (x.y.Z)")
    print("  minor [changes...]       发布次版本 (x.Y.z)")
    print("  major [changes...]       发布主版本 (X.y.z)")
    print("  version                  显示当前版本")
    print("  clean                    清理构建文件")
    print("  help                     显示此帮助")
    print()
    print("示例:")
    print("  python scripts/utils/make.py build")
    print("  python scripts/utils/make.py release 1.2.0 '添加新功能' '修复bug'")
    print("  python scripts/utils/make.py patch '修复重要bug'")
    print("  python scripts/utils/make.py minor '添加忽略重复文件功能'")
    print("  python scripts/utils/make.py major '重构核心架构'")

def get_current_version():
    """获取当前版本"""
    try:
        from version import get_version
        return get_version()
    except ImportError:
        return "1.0.0"

def increment_version(current_version, version_type):
    """递增版本号"""
    parts = current_version.split('.')
    major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
    
    if version_type == 'patch':
        patch += 1
    elif version_type == 'minor':
        minor += 1
        patch = 0
    elif version_type == 'major':
        major += 1
        minor = 0
        patch = 0
    
    return f"{major}.{minor}.{patch}"

def run_command(cmd, description):
    """运行命令并显示结果"""
    print(f"🔄 {description}...")
    print(f"执行: {' '.join(cmd)}")
    print("-" * 40)
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print(f"✅ {description}成功!")
    else:
        print(f"❌ {description}失败!")
    
    return result.returncode == 0

def cmd_build():
    """构建命令"""
    build_script = project_root / 'scripts' / 'build' / 'build_app.py'
    if build_script.exists():
        return run_command(['python', str(build_script)], "构建应用程序")
    else:
        print("❌ 未找到构建脚本")
        return False

def cmd_release(version, changes):
    """发布命令"""
    # 首先更新版本
    update_script = project_root / 'scripts' / 'utils' / 'update_version.py'
    cmd = ['python', str(update_script), version]
    if changes:
        cmd.extend(changes)
    
    if not run_command(cmd, f"更新版本到 {version}"):
        return False
    
    # 然后执行发布
    release_script = project_root / 'scripts' / 'release' / 'release.py'
    return run_command(['python', str(release_script)], f"发布版本 {version}")

def cmd_version_bump(version_type, changes):
    """版本递增命令"""
    current_version = get_current_version()
    new_version = increment_version(current_version, version_type)
    
    print(f"📦 {version_type.title()} 版本更新: {current_version} → {new_version}")
    
    return cmd_release(new_version, changes)

def cmd_version():
    """显示版本命令"""
    current_version = get_current_version()
    print(f"当前版本: {current_version}")
    
    try:
        from version import get_full_version, VERSION_HISTORY
        print(f"完整版本: {get_full_version()}")
        
        if current_version in VERSION_HISTORY:
            version_info = VERSION_HISTORY[current_version]
            print(f"发布日期: {version_info['date']}")
            print("更新内容:")
            for change in version_info['changes']:
                print(f"  - {change}")
    except ImportError:
        pass

def cmd_clean():
    """清理命令"""
    print("🧹 清理构建文件...")
    
    # 清理常见的构建文件和目录
    clean_patterns = [
        'build/',
        'dist/',
        '*.dmg',
        '*.app',
        '*.exe',
        '__pycache__/',
        '*.pyc',
        '.DS_Store',
        'release-v*/'
    ]
    
    import glob
    import shutil
    
    cleaned = []
    for pattern in clean_patterns:
        matches = glob.glob(pattern, recursive=True)
        for match in matches:
            try:
                if os.path.isdir(match):
                    shutil.rmtree(match)
                else:
                    os.remove(match)
                cleaned.append(match)
            except Exception as e:
                print(f"⚠️  无法删除 {match}: {e}")
    
    if cleaned:
        print("已清理:")
        for item in cleaned:
            print(f"  - {item}")
    else:
        print("没有需要清理的文件")

def main():
    """主函数"""
    if len(sys.argv) < 2:
        show_help()
        sys.exit(0)
    
    command = sys.argv[1].lower()
    args = sys.argv[2:]
    
    if command in ['help', '--help', '-h']:
        show_help()
    
    elif command == 'build':
        if not cmd_build():
            sys.exit(1)
    
    elif command == 'release':
        if len(args) < 1:
            print("❌ 请指定版本号")
            print("用法: python scripts/utils/make.py release <version> [changes...]")
            sys.exit(1)
        
        version = args[0]
        changes = args[1:]
        if not cmd_release(version, changes):
            sys.exit(1)
    
    elif command == 'patch':
        if not cmd_version_bump('patch', args):
            sys.exit(1)
    
    elif command == 'minor':
        if not cmd_version_bump('minor', args):
            sys.exit(1)
    
    elif command == 'major':
        if not cmd_version_bump('major', args):
            sys.exit(1)
    
    elif command == 'version':
        cmd_version()
    
    elif command == 'clean':
        cmd_clean()
    
    else:
        print(f"❌ 未知命令: {command}")
        print("使用 'python scripts/utils/make.py help' 查看可用命令")
        sys.exit(1)

if __name__ == '__main__':
    main()