#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MediaCopyer 快速发布脚本
提供常见发布场景的快捷命令
"""

import sys
import subprocess
import os

def show_menu():
    """显示发布菜单"""
    print("MediaCopyer 快速发布菜单")
    print("=" * 40)
    print("1. 🐛 Bug修复版本 (补丁版本 x.y.Z)")
    print("2. ✨ 功能更新版本 (次版本 x.Y.z)")
    print("3. 🚀 重大更新版本 (主版本 X.y.z)")
    print("4. 🔨 仅构建当前版本")
    print("5. 📝 自定义版本")
    print("0. 退出")
    print()

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

def get_changes_input():
    """获取更新内容输入"""
    print("\n请输入更新内容 (每行一个，空行结束):")
    changes = []
    while True:
        change = input("- ").strip()
        if not change:
            break
        changes.append(change)
    return changes

def run_build_and_release(version, changes, options=None):
    """运行构建和发布脚本"""
    cmd = ['python', 'build_and_release.py', version]
    
    if options:
        cmd.extend(options)
    
    if changes:
        cmd.extend(changes)
    
    print(f"\n执行命令: {' '.join(cmd)}")
    print("=" * 50)
    
    result = subprocess.run(cmd)
    return result.returncode == 0

def main():
    """主函数"""
    if not os.path.exists('build_and_release.py'):
        print("❌ 未找到 build_and_release.py 脚本")
        print("请确保在正确的项目目录中运行此脚本")
        sys.exit(1)
    
    current_version = get_current_version()
    
    while True:
        print(f"\n当前版本: {current_version}")
        show_menu()
        
        try:
            choice = input("请选择 (0-5): ").strip()
            
            if choice == '0':
                print("👋 再见!")
                break
            
            elif choice == '1':
                # Bug修复版本
                new_version = increment_version(current_version, 'patch')
                print(f"\n🐛 Bug修复版本: {current_version} → {new_version}")
                changes = get_changes_input()
                if run_build_and_release(new_version, changes):
                    current_version = new_version
            
            elif choice == '2':
                # 功能更新版本
                new_version = increment_version(current_version, 'minor')
                print(f"\n✨ 功能更新版本: {current_version} → {new_version}")
                changes = get_changes_input()
                if run_build_and_release(new_version, changes):
                    current_version = new_version
            
            elif choice == '3':
                # 重大更新版本
                new_version = increment_version(current_version, 'major')
                print(f"\n🚀 重大更新版本: {current_version} → {new_version}")
                changes = get_changes_input()
                if run_build_and_release(new_version, changes):
                    current_version = new_version
            
            elif choice == '4':
                # 仅构建
                print(f"\n🔨 仅构建当前版本: {current_version}")
                run_build_and_release(current_version, [], ['--build-only', '--skip-build'])
            
            elif choice == '5':
                # 自定义版本
                new_version = input(f"\n请输入新版本号 (当前: {current_version}): ").strip()
                if not new_version:
                    continue
                
                print(f"📝 自定义版本: {current_version} → {new_version}")
                changes = get_changes_input()
                if run_build_and_release(new_version, changes):
                    current_version = new_version
            
            else:
                print("❌ 无效选择，请重新输入")
        
        except KeyboardInterrupt:
            print("\n\n👋 用户中断，再见!")
            break
        except Exception as e:
            print(f"\n❌ 发生错误: {e}")

if __name__ == '__main__':
    main()