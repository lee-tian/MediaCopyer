#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MediaCopyer 自动发布脚本 - 无交互版本
专门用于自动化发布，不需要用户交互
"""

import os
import sys
import subprocess
import shutil
from datetime import datetime
from version import get_version, get_dmg_name, get_app_bundle_name, VERSION_HISTORY

def run_command(cmd, description="", timeout=300):
    """运行命令并处理错误"""
    if description:
        print(f"🔄 {description}...")
    
    try:
        if isinstance(cmd, list):
            result = subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=timeout)
        else:
            result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True, timeout=timeout)
        
        if description:
            print(f"✅ {description}完成")
        return True, result.stdout
    except subprocess.TimeoutExpired:
        print(f"❌ {description}超时 (>{timeout}秒)")
        return False, "命令执行超时"
    except subprocess.CalledProcessError as e:
        print(f"❌ {description}失败: {e.stderr}")
        return False, e.stderr

def check_prerequisites():
    """检查发布前提条件（自动模式）"""
    print("🔍 检查发布前提条件...")
    
    # 检查GitHub CLI
    success, _ = run_command("gh --version", timeout=10)
    if not success:
        print("❌ GitHub CLI未安装")
        return False
    
    # 检查GitHub认证
    success, _ = run_command("gh auth status", timeout=15)
    if not success:
        print("❌ GitHub CLI未认证")
        return False
    
    # 检查git仓库
    if not os.path.exists('.git'):
        print("❌ 当前目录不是git仓库")
        return False
    
    print("✅ 所有前提条件满足")
    return True

def build_application():
    """构建应用程序"""
    print("🔨 构建应用程序...")
    
    success, output = run_command("python build_app.py", "构建应用", timeout=600)
    return success

def create_release_notes():
    """创建发布说明"""
    version = get_version()
    
    if version not in VERSION_HISTORY:
        print(f"警告: 版本 {version} 没有在 VERSION_HISTORY 中找到")
        return ""
    
    version_info = VERSION_HISTORY[version]
    release_notes = f"""# MediaCopyer v{version}

发布日期: {version_info['date']}

## 更新内容

"""
    
    for change in version_info['changes']:
        release_notes += f"- {change}\n"
    
    release_notes += f"""
## 下载

- **macOS**: [{get_dmg_name()}](https://github.com/lee-tian/MediaCopyer/releases/download/v{version}/{get_dmg_name()})

## 安装说明

### macOS
1. 下载 `{get_dmg_name()}`
2. 双击打开DMG文件
3. 将 `{get_app_bundle_name()}` 拖拽到 Applications 文件夹
4. 在 Applications 文件夹中找到并运行 MediaCopyer

## 系统要求

- macOS 10.13 或更高版本
- Python 3.6+ (仅源码安装需要)

## 问题反馈

如果遇到问题，请在 [GitHub Issues](https://github.com/lee-tian/MediaCopyer/issues) 中反馈。
"""
    
    return release_notes

def prepare_release_assets():
    """准备发布资源"""
    print("📦 准备发布资源...")
    
    version = get_version()
    release_dir = f"release-v{version}"
    
    # 创建发布目录
    if os.path.exists(release_dir):
        shutil.rmtree(release_dir)
    os.makedirs(release_dir)
    
    # 复制DMG文件
    dmg_name = get_dmg_name()
    if os.path.exists(dmg_name):
        shutil.copy(dmg_name, release_dir)
        print(f"✅ 已复制: {dmg_name}")
    else:
        print(f"⚠️ 未找到 {dmg_name}")
    
    # 创建发布说明文件
    release_notes = create_release_notes()
    with open(os.path.join(release_dir, 'RELEASE_NOTES.md'), 'w', encoding='utf-8') as f:
        f.write(release_notes)
    
    print(f"✅ 发布资源已准备完成: {release_dir}/")
    return release_dir, release_notes

def create_and_push_tag():
    """创建并推送Git标签"""
    version = get_version()
    tag_name = f"v{version}"
    
    print(f"🏷️ 创建Git标签: {tag_name}")
    
    # 检查标签是否已存在，如果存在则删除
    result = subprocess.run(['git', 'tag', '-l', tag_name], capture_output=True, text=True)
    if result.stdout.strip():
        print(f"⚠️ 标签 {tag_name} 已存在，删除中...")
        subprocess.run(['git', 'tag', '-d', tag_name], capture_output=True)
        subprocess.run(['gh', 'release', 'delete', tag_name, '--yes'], capture_output=True)
        subprocess.run(['git', 'push', 'origin', '--delete', tag_name], capture_output=True)
    
    # 创建标签
    tag_message = f"Release version {version}"
    if version in VERSION_HISTORY:
        changes = VERSION_HISTORY[version]['changes']
        tag_message += "\n\n更新内容:\n" + "\n".join(f"- {change}" for change in changes)
    
    success, _ = run_command(['git', 'tag', '-a', tag_name, '-m', tag_message], "创建标签")
    if not success:
        return False, None
    
    # 推送代码和标签
    success, _ = run_command(['git', 'push'], "推送代码", timeout=120)
    if not success:
        return False, None
    
    success, _ = run_command(['git', 'push', '--tags'], "推送标签", timeout=120)
    if not success:
        return False, None
    
    return True, tag_name

def create_github_release(tag_name, release_dir, release_notes):
    """创建GitHub Release"""
    print("🚀 创建GitHub Release...")
    
    version = get_version()
    
    # 创建临时的发布说明文件
    notes_file = os.path.join(release_dir, 'temp_release_notes.md')
    with open(notes_file, 'w', encoding='utf-8') as f:
        f.write(release_notes)
    
    try:
        # 创建release命令
        cmd = [
            'gh', 'release', 'create', tag_name,
            '--title', f'MediaCopyer v{version}',
            '--notes-file', notes_file
        ]
        
        # 添加DMG文件
        dmg_path = os.path.join(release_dir, get_dmg_name())
        if os.path.exists(dmg_path):
            cmd.append(dmg_path)
        
        success, output = run_command(cmd, "创建GitHub Release", timeout=180)
        
        if success:
            print("✅ GitHub Release 创建成功!")
            print(f"🔗 Release URL: https://github.com/lee-tian/MediaCopyer/releases/tag/{tag_name}")
            return True
        else:
            return False
            
    finally:
        # 清理临时文件
        if os.path.exists(notes_file):
            os.remove(notes_file)

def main():
    """主函数"""
    version = get_version()
    print(f"🤖 MediaCopyer v{version} 自动发布脚本")
    print("=" * 50)
    
    # 检查前提条件
    if not check_prerequisites():
        print("❌ 前提条件检查失败")
        sys.exit(1)
    
    # 构建应用程序
    if not build_application():
        print("❌ 构建失败")
        sys.exit(1)
    
    # 准备发布资源
    release_dir, release_notes = prepare_release_assets()
    
    # 创建并推送标签
    success, tag_name = create_and_push_tag()
    if not success:
        print("❌ 标签创建或推送失败")
        sys.exit(1)
    
    # 创建GitHub Release
    if create_github_release(tag_name, release_dir, release_notes):
        print(f"\n🎉 自动发布完成!")
        print(f"版本: v{version}")
        print(f"标签: {tag_name}")
        print(f"Release URL: https://github.com/lee-tian/MediaCopyer/releases/tag/{tag_name}")
        print(f"\n✅ 用户现在可以直接从GitHub Releases下载 {get_dmg_name()}")
    else:
        print("❌ GitHub Release创建失败")
        sys.exit(1)

if __name__ == '__main__':
    main()