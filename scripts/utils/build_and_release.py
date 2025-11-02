#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MediaCopyer 一键构建和发布脚本
集成版本更新、构建和发布流程
"""

import os
import sys
import subprocess
import argparse
from datetime import datetime
import re
from pathlib import Path

# 添加项目根目录到路径，以便导入version模块
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def show_help():
    """显示帮助信息"""
    print("MediaCopyer 一键构建和发布脚本")
    print("=" * 50)
    print()
    print("用法:")
    print("  python scripts/utils/build_and_release.py <新版本号> [选项] [更新内容...]")
    print()
    print("参数:")
    print("  新版本号        版本号格式为 x.y.z (如 1.0.0, 2.1.3)")
    print("  更新内容        描述本次更新的内容")
    print()
    print("选项:")
    print("  --build-only    仅构建，不发布")
    print("  --no-git        不进行Git操作（标签、推送）")
    print("  --skip-build    跳过构建步骤")
    print("  --help, -h      显示此帮助信息")
    print()
    print("示例:")
    print("  # 更新版本并完整发布")
    print("  python scripts/utils/build_and_release.py 1.2.0 '添加新功能' '修复重要bug'")
    print()
    print("  # 仅构建不发布")
    print("  python scripts/utils/build_and_release.py 1.2.0 --build-only '添加新功能'")
    print()
    print("  # 跳过构建直接发布（假设已经构建过）")
    print("  python scripts/utils/build_and_release.py 1.2.0 --skip-build '修复bug'")

def update_version(new_version, changes):
    """更新版本号"""
    print(f"📝 更新版本号到 {new_version}...")
    
    # 构建更新版本的命令
    update_script = project_root / 'scripts' / 'utils' / 'update_version.py'
    cmd = ['python', str(update_script), new_version]
    if changes:
        cmd.extend(changes)
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ 版本更新失败: {result.stderr}")
        return False
    
    print(result.stdout)
    return True

def build_application():
    """构建应用程序"""
    print("🔨 构建应用程序...")
    
    # 检查构建脚本
    build_script = project_root / 'scripts' / 'build' / 'build_app.py'
    if not build_script.exists():
        print("❌ 未找到构建脚本")
        return False
    
    # 激活虚拟环境并构建
    if os.path.exists('venv'):
        if sys.platform == 'win32':
            activate_cmd = 'venv\\Scripts\\activate'
        else:
            activate_cmd = 'source venv/bin/activate'
        
        build_cmd = f"{activate_cmd} && python {build_script}"
    else:
        build_cmd = f"python {build_script}"
    
    print(f"执行构建命令: {build_cmd}")
    result = subprocess.run(build_cmd, shell=True)
    if result.returncode != 0:
        print("❌ 构建失败!")
        return False
    
    print("✅ 构建成功!")
    return True

def run_release_script():
    """运行发布脚本"""
    print("🚀 开始发布流程...")
    
    release_script = project_root / 'scripts' / 'release' / 'release.py'
    if not release_script.exists():
        print("❌ 未找到发布脚本")
        return False
    
    result = subprocess.run(['python', str(release_script)])
    if result.returncode != 0:
        print("❌ 发布失败!")
        return False
    
    print("✅ 发布完成!")
    return True

def commit_version_changes(version):
    """提交版本更改"""
    print("📝 提交版本更改...")
    
    # 添加版本文件到Git
    subprocess.run(['git', 'add', 'version.py'])
    
    # 提交更改
    commit_message = f"chore: bump version to {version}"
    result = subprocess.run(['git', 'commit', '-m', commit_message], 
                          capture_output=True, text=True)
    
    if result.returncode != 0:
        if "nothing to commit" in result.stdout:
            print("📝 没有需要提交的更改")
        else:
            print(f"❌ 提交失败: {result.stderr}")
            return False
    else:
        print(f"✅ 已提交版本更改: {commit_message}")
    
    return True

def validate_version(version):
    """验证版本号格式"""
    if not re.match(r'^\d+\.\d+\.\d+$', version):
        print("❌ 错误: 版本号格式应为 x.y.z (如 1.0.0)")
        return False
    return True

def check_working_directory():
    """检查工作目录"""
    required_files = ['version.py']
    missing_files = []
    
    for file in required_files:
        if not (project_root / file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ 缺少必要文件: {', '.join(missing_files)}")
        return False
    
    return True

def main():
    """主函数"""
    # 解析命令行参数
    if len(sys.argv) < 2 or sys.argv[1] in ['--help', '-h', 'help']:
        show_help()
        sys.exit(0)
    
    # 检查工作目录
    if not check_working_directory():
        sys.exit(1)
    
    # 解析参数
    args = sys.argv[1:]
    new_version = args[0]
    
    # 验证版本号
    if not validate_version(new_version):
        sys.exit(1)
    
    # 解析选项
    build_only = '--build-only' in args
    no_git = '--no-git' in args
    skip_build = '--skip-build' in args
    
    # 移除选项，剩下的是更新内容
    changes = [arg for arg in args[1:] if not arg.startswith('--')]
    
    print(f"🚀 MediaCopyer 构建和发布脚本")
    print(f"📦 目标版本: {new_version}")
    print(f"🔧 构建模式: {'仅构建' if build_only else '完整发布'}")
    if no_git:
        print(f"📝 Git操作: 跳过")
    if skip_build:
        print(f"🔨 构建步骤: 跳过")
    print("=" * 50)
    
    try:
        # 步骤1: 更新版本号
        if not update_version(new_version, changes):
            sys.exit(1)
        
        # 步骤2: 提交版本更改（如果不跳过Git操作）
        if not no_git:
            if not commit_version_changes(new_version):
                print("⚠️  版本提交失败，但继续执行...")
        
        # 步骤3: 构建应用程序（如果不跳过构建）
        if not skip_build:
            if not build_application():
                sys.exit(1)
        else:
            print("⏭️  跳过构建步骤")
        
        # 步骤4: 发布（如果不是仅构建模式）
        if not build_only:
            if not run_release_script():
                sys.exit(1)
        else:
            print("⏭️  跳过发布步骤（仅构建模式）")
        
        # 完成
        print("\n" + "=" * 50)
        print("🎉 所有步骤完成!")
        print(f"📦 版本: {new_version}")
        
        if build_only:
            print("🔨 构建完成，可以手动运行 python scripts/release/release.py 进行发布")
        else:
            print("🚀 构建和发布完成!")
            
        if changes:
            print("📝 更新内容:")
            for change in changes:
                print(f"   - {change}")
    
    except KeyboardInterrupt:
        print("\n❌ 用户中断操作")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()