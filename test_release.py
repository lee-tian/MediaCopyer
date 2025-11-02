#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试发布脚本 - 简化版本用于调试
"""

import os
import subprocess
from version import get_version, get_dmg_name

def test_github_cli():
    """测试GitHub CLI功能"""
    print("🔍 测试GitHub CLI...")
    
    # 检查版本
    try:
        result = subprocess.run(['gh', '--version'], capture_output=True, text=True, timeout=10)
        print(f"✅ GitHub CLI版本: {result.stdout.strip()}")
    except Exception as e:
        print(f"❌ GitHub CLI版本检查失败: {e}")
        return False
    
    # 检查认证状态
    try:
        result = subprocess.run(['gh', 'auth', 'status'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ GitHub CLI已认证")
        else:
            print(f"❌ GitHub CLI认证失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ GitHub CLI认证检查失败: {e}")
        return False
    
    return True

def test_git_operations():
    """测试Git操作"""
    print("🔍 测试Git操作...")
    
    # 检查git状态
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True, timeout=10)
        if result.stdout.strip():
            print(f"⚠️ 有未提交的更改:\n{result.stdout}")
        else:
            print("✅ 工作目录干净")
    except Exception as e:
        print(f"❌ Git状态检查失败: {e}")
        return False
    
    # 检查当前分支
    try:
        result = subprocess.run(['git', 'branch', '--show-current'], capture_output=True, text=True, timeout=10)
        branch = result.stdout.strip()
        print(f"✅ 当前分支: {branch}")
    except Exception as e:
        print(f"❌ 分支检查失败: {e}")
        return False
    
    return True

def test_build():
    """测试构建"""
    print("🔍 测试构建...")
    
    try:
        # 检查构建脚本是否存在
        if not os.path.exists('build_app.py'):
            print("❌ build_app.py 不存在")
            return False
        
        print("✅ 构建脚本存在")
        
        # 检查DMG文件
        dmg_name = get_dmg_name()
        if os.path.exists(dmg_name):
            size = os.path.getsize(dmg_name) / (1024 * 1024)  # MB
            print(f"✅ DMG文件存在: {dmg_name} ({size:.1f} MB)")
        else:
            print(f"⚠️ DMG文件不存在: {dmg_name}")
        
        return True
    except Exception as e:
        print(f"❌ 构建检查失败: {e}")
        return False

def create_test_release():
    """创建测试release"""
    print("🚀 创建测试release...")
    
    version = get_version()
    tag_name = f"v{version}-test"
    
    try:
        # 检查标签是否存在
        result = subprocess.run(['git', 'tag', '-l', tag_name], capture_output=True, text=True, timeout=10)
        if result.stdout.strip():
            print(f"⚠️ 测试标签 {tag_name} 已存在，删除中...")
            subprocess.run(['git', 'tag', '-d', tag_name], timeout=10)
            subprocess.run(['gh', 'release', 'delete', tag_name, '--yes'], capture_output=True, timeout=10)
        
        # 创建标签
        print(f"📝 创建标签: {tag_name}")
        result = subprocess.run(['git', 'tag', '-a', tag_name, '-m', f'Test release {version}'], timeout=10)
        if result.returncode != 0:
            print("❌ 标签创建失败")
            return False
        
        # 推送标签
        print("📤 推送标签...")
        result = subprocess.run(['git', 'push', 'origin', tag_name], capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            print(f"❌ 标签推送失败: {result.stderr}")
            return False
        
        # 创建GitHub release
        print("🎯 创建GitHub Release...")
        dmg_name = get_dmg_name()
        
        cmd = [
            'gh', 'release', 'create', tag_name,
            '--title', f'MediaCopyer v{version} (Test)',
            '--notes', f'Test release for MediaCopyer v{version}\n\nThis is an automated test release.',
            '--prerelease'
        ]
        
        if os.path.exists(dmg_name):
            cmd.append(dmg_name)
            print(f"📎 附加文件: {dmg_name}")
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print("✅ GitHub Release创建成功!")
            print(f"🔗 URL: https://github.com/lee-tian/MediaCopyer/releases/tag/{tag_name}")
            return True
        else:
            print(f"❌ GitHub Release创建失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 创建release时发生异常: {e}")
        return False

def main():
    """主函数"""
    version = get_version()
    print(f"🧪 MediaCopyer v{version} 发布测试")
    print("=" * 50)
    
    # 测试各个组件
    if not test_github_cli():
        print("❌ GitHub CLI测试失败")
        return
    
    if not test_git_operations():
        print("❌ Git操作测试失败")
        return
    
    if not test_build():
        print("❌ 构建测试失败")
        return
    
    # 询问是否创建测试release
    response = input("\n🤔 是否创建测试release? (y/N): ")
    if response.lower() == 'y':
        if create_test_release():
            print("\n🎉 测试release创建成功!")
        else:
            print("\n❌ 测试release创建失败")
    else:
        print("✅ 所有测试通过，可以进行正式发布")

if __name__ == '__main__':
    main()