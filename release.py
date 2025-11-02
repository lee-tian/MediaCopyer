#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MediaCopyer 发布脚本
用于自动化版本发布流程，包括自动上传到GitHub Releases
"""

import os
import sys
import subprocess
import shutil
import json
from datetime import datetime
from version import get_version, get_dmg_name, get_app_bundle_name, VERSION_HISTORY

def check_git_status():
    """检查Git状态"""
    print("检查Git状态...")
    
    # 检查是否有未提交的更改
    result = subprocess.run(['git', 'status', '--porcelain'], 
                          capture_output=True, text=True)
    if result.stdout.strip():
        print("警告: 有未提交的更改:")
        print(result.stdout)
        response = input("是否继续发布? (y/N): ")
        if response.lower() != 'y':
            print("发布已取消")
            return False
    
    # 检查当前分支
    result = subprocess.run(['git', 'branch', '--show-current'], 
                          capture_output=True, text=True)
    current_branch = result.stdout.strip()
    print(f"当前分支: {current_branch}")
    
    if current_branch != 'master' and current_branch != 'main':
        response = input(f"当前不在主分支 ({current_branch})，是否继续? (y/N): ")
        if response.lower() != 'y':
            print("发布已取消")
            return False
    
    return True

def create_git_tag():
    """创建Git标签"""
    version = get_version()
    tag_name = f"v{version}"
    
    print(f"创建Git标签: {tag_name}")
    
    # 检查标签是否已存在
    result = subprocess.run(['git', 'tag', '-l', tag_name], 
                          capture_output=True, text=True)
    if result.stdout.strip():
        print(f"标签 {tag_name} 已存在")
        response = input("是否删除现有标签并重新创建? (y/N): ")
        if response.lower() == 'y':
            subprocess.run(['git', 'tag', '-d', tag_name])
            subprocess.run(['git', 'push', 'origin', '--delete', tag_name], 
                         capture_output=True)
        else:
            return False
    
    # 创建标签
    tag_message = f"Release version {version}"
    if version in VERSION_HISTORY:
        changes = VERSION_HISTORY[version]['changes']
        tag_message += "\n\n更新内容:\n" + "\n".join(f"- {change}" for change in changes)
    
    subprocess.run(['git', 'tag', '-a', tag_name, '-m', tag_message])
    print(f"标签 {tag_name} 创建成功")
    
    return tag_name

def build_application():
    """构建应用程序"""
    print("构建应用程序...")
    
    # 激活虚拟环境并构建
    if os.path.exists('venv'):
        if sys.platform == 'win32':
            activate_cmd = 'venv\\Scripts\\activate'
        else:
            activate_cmd = 'source venv/bin/activate'
        
        build_cmd = f"{activate_cmd} && python build_app.py"
    else:
        build_cmd = "python build_app.py"
    
    result = subprocess.run(build_cmd, shell=True)
    if result.returncode != 0:
        print("构建失败!")
        return False
    
    print("构建成功!")
    return True

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
    print("准备发布资源...")
    
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
        print(f"已复制: {dmg_name}")
    else:
        print(f"警告: 未找到 {dmg_name}")
    
    # 创建发布说明文件
    release_notes = create_release_notes()
    with open(os.path.join(release_dir, 'RELEASE_NOTES.md'), 'w', encoding='utf-8') as f:
        f.write(release_notes)
    
    print(f"发布资源已准备完成: {release_dir}/")
    return release_dir

def check_github_cli():
    """检查GitHub CLI是否可用"""
    try:
        result = subprocess.run(['gh', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ GitHub CLI 可用")
            return True
        else:
            print("✗ GitHub CLI 不可用")
            return False
    except FileNotFoundError:
        print("✗ GitHub CLI 未安装")
        print("请安装 GitHub CLI: https://cli.github.com/")
        return False

def check_github_auth():
    """检查GitHub CLI认证状态"""
    try:
        result = subprocess.run(['gh', 'auth', 'status'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ GitHub CLI 已认证")
            return True
        else:
            print("✗ GitHub CLI 未认证")
            print("请运行: gh auth login")
            return False
    except Exception as e:
        print(f"✗ 检查GitHub认证失败: {e}")
        return False

def push_to_github():
    """推送到GitHub"""
    print("推送到GitHub...")
    
    # 推送代码
    result = subprocess.run(['git', 'push'], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"推送代码失败: {result.stderr}")
        return False
    
    # 推送标签
    result = subprocess.run(['git', 'push', '--tags'], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"推送标签失败: {result.stderr}")
        return False
    
    print("推送成功!")
    return True

def create_github_release(tag_name, release_dir):
    """创建GitHub Release并上传文件"""
    print("创建GitHub Release...")
    
    version = get_version()
    release_notes = create_release_notes()
    
    # 创建临时的发布说明文件
    notes_file = os.path.join(release_dir, 'temp_release_notes.md')
    with open(notes_file, 'w', encoding='utf-8') as f:
        f.write(release_notes)
    
    try:
        # 创建release
        cmd = [
            'gh', 'release', 'create', tag_name,
            '--title', f'MediaCopyer v{version}',
            '--notes-file', notes_file
        ]
        
        # 添加文件
        dmg_path = os.path.join(release_dir, get_dmg_name())
        if os.path.exists(dmg_path):
            cmd.append(dmg_path)
        
        print(f"执行命令: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print("✅ GitHub Release 创建成功!")
            print(f"Release URL: https://github.com/lee-tian/MediaCopyer/releases/tag/{tag_name}")
            return True
        else:
            print(f"✗ 创建GitHub Release失败:")
            print(f"错误输出: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"✗ 创建GitHub Release时发生异常: {e}")
        return False
    finally:
        # 清理临时文件
        if os.path.exists(notes_file):
            os.remove(notes_file)

def main():
    """主函数"""
    version = get_version()
    print(f"MediaCopyer v{version} 自动发布脚本")
    print("=" * 50)
    
    # 检查GitHub CLI
    if not check_github_cli():
        print("\n手动发布模式:")
        print("1. 安装 GitHub CLI: https://cli.github.com/")
        print("2. 运行 gh auth login 进行认证")
        print("3. 重新运行此脚本进行自动发布")
        manual_release()
        return
    
    if not check_github_auth():
        print("\n请先认证GitHub CLI，然后重新运行脚本")
        return
    
    # 检查Git状态
    if not check_git_status():
        return
    
    # 构建应用程序
    if not build_application():
        print("构建失败，发布终止")
        return
    
    # 准备发布资源
    release_dir = prepare_release_assets()
    
    # 创建Git标签
    tag_name = create_git_tag()
    if not tag_name:
        print("标签创建失败，发布终止")
        return
    
    # 推送到GitHub
    if not push_to_github():
        print("推送失败，发布终止")
        return
    
    # 创建GitHub Release
    if create_github_release(tag_name, release_dir):
        print(f"\n🎉 自动发布完成!")
        print(f"版本: v{version}")
        print(f"标签: {tag_name}")
        print(f"Release URL: https://github.com/lee-tian/MediaCopyer/releases/tag/{tag_name}")
        print(f"\n✅ 用户现在可以直接从GitHub Releases下载 {get_dmg_name()}")
    else:
        print(f"\n⚠️ 自动发布失败，切换到手动模式")
        manual_release_instructions(version, tag_name, release_dir)

def manual_release():
    """手动发布模式"""
    version = get_version()
    print(f"\n📋 手动发布模式 - MediaCopyer v{version}")
    print("=" * 50)
    
    # 检查Git状态
    if not check_git_status():
        return
    
    # 构建应用程序
    if not build_application():
        print("构建失败，发布终止")
        return
    
    # 准备发布资源
    release_dir = prepare_release_assets()
    
    # 创建Git标签
    tag_name = create_git_tag()
    if not tag_name:
        print("标签创建失败，发布终止")
        return
    
    # 推送到GitHub
    if not push_to_github():
        print("推送失败，发布终止")
        return
    
    manual_release_instructions(version, tag_name, release_dir)

def manual_release_instructions(version, tag_name, release_dir):
    """显示手动发布说明"""
    print(f"\n📋 手动发布说明:")
    print(f"版本: v{version}")
    print(f"标签: {tag_name}")
    print(f"发布资源: {release_dir}/")
    print(f"\n📝 下一步操作:")
    print(f"1. 访问: https://github.com/lee-tian/MediaCopyer/releases")
    print(f"2. 点击 'Create a new release'")
    print(f"3. 选择标签: {tag_name}")
    print(f"4. 设置标题: MediaCopyer v{version}")
    print(f"5. 复制发布说明从: {release_dir}/RELEASE_NOTES.md")
    print(f"6. 上传文件: {release_dir}/{get_dmg_name()}")
    print(f"7. 点击 'Publish release'")
    print(f"\n💡 提示: 安装GitHub CLI可以实现自动发布")
    print(f"   brew install gh  # macOS")
    print(f"   gh auth login    # 认证")

if __name__ == '__main__':
    main()