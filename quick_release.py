#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MediaCopyer 快速发布脚本
一键构建、标签、推送和发布到GitHub Releases
"""

import os
import sys
import subprocess
import argparse
from version import get_version

def run_command(cmd, description="", timeout=300):
    """运行命令并处理错误"""
    if description:
        print(f"🔄 {description}...")
    
    try:
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

def check_prerequisites(auto_mode=False):
    """检查发布前提条件"""
    print("🔍 检查发布前提条件...")
    
    # 检查是否在git仓库中
    if not os.path.exists('.git'):
        print("❌ 当前目录不是git仓库")
        return False
    
    # 检查是否有未提交的更改
    success, output = run_command("git status --porcelain")
    if not success:
        return False
    
    if output.strip():
        print("⚠️ 有未提交的更改:")
        print(output)
        if auto_mode:
            print("🤖 自动模式：忽略未提交的更改，继续发布")
        else:
            response = input("是否继续? (y/N): ")
            if response.lower() != 'y':
                return False
    
    # 检查GitHub CLI
    success, _ = run_command("gh --version")
    if not success:
        print("⚠️ GitHub CLI未安装，将使用手动发布模式")
        print("💡 安装GitHub CLI以启用自动发布: https://cli.github.com/")
        return "manual"
    
    # 检查GitHub认证
    success, _ = run_command("gh auth status")
    if not success:
        print("⚠️ GitHub CLI未认证")
        print("💡 请运行: gh auth login")
        return "manual"
    
    print("✅ 所有前提条件满足")
    return True

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='MediaCopyer 快速发布脚本')
    parser.add_argument('--auto', action='store_true', help='自动模式，不询问确认')
    parser.add_argument('--build-only', action='store_true', help='仅构建，不发布')
    args = parser.parse_args()
    
    version = get_version()
    print(f"🚀 MediaCopyer v{version} 快速发布")
    print("=" * 50)
    
    # 检查前提条件
    prereq_result = check_prerequisites(auto_mode=args.auto)
    if prereq_result is False:
        sys.exit(1)
    
    auto_release = prereq_result is True
    
    if not args.auto and not args.build_only:
        print(f"\n📋 发布信息:")
        print(f"版本: v{version}")
        print(f"模式: {'自动发布' if auto_release else '手动发布'}")
        
        response = input("\n是否继续发布? (y/N): ")
        if response.lower() != 'y':
            print("发布已取消")
            sys.exit(0)
    
    # 步骤1: 构建应用
    success, _ = run_command("python build_app.py", "构建应用")
    if not success:
        sys.exit(1)
    
    if args.build_only:
        print("✅ 构建完成")
        sys.exit(0)
    
    # 步骤2: 运行完整发布脚本
    if auto_release:
        print("🚀 启动自动发布...")
        success, _ = run_command("python release.py", "自动发布")
    else:
        print("📋 启动手动发布...")
        success, _ = run_command("python release.py", "准备手动发布")
    
    if success:
        print(f"\n🎉 发布流程完成!")
        if auto_release:
            print(f"🔗 Release URL: https://github.com/lee-tian/MediaCopyer/releases/tag/v{version}")
        else:
            print(f"📝 请按照提示完成手动发布步骤")
    else:
        print("❌ 发布失败")
        sys.exit(1)

if __name__ == '__main__':
    main()