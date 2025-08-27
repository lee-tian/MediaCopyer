#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MediaCopyer 应用打包脚本
"""

import os
import shutil
import subprocess
import sys


def clean_build():
    """清理之前的构建文件"""
    print("清理之前的构建文件...")
    
    # 删除构建目录
    build_dirs = ['build', 'dist', '__pycache__']
    for dir_name in build_dirs:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"已删除: {dir_name}")
    
    # 删除 .pyc 文件
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pyc'):
                os.remove(os.path.join(root, file))
        
        # 删除 __pycache__ 目录
        if '__pycache__' in dirs:
            shutil.rmtree(os.path.join(root, '__pycache__'))


def build_app():
    """构建应用程序"""
    print("开始构建应用程序...")
    
    try:
        # 使用 PyInstaller 构建
        cmd = ['pyinstaller', '--clean', 'media_copyer.spec']
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        print("构建成功!")
        print("可执行文件位于: dist/MediaCopyer")
        
        # 检查输出文件是否存在
        if os.path.exists('dist/MediaCopyer'):
            file_size = os.path.getsize('dist/MediaCopyer')
            print(f"文件大小: {file_size / (1024 * 1024):.2f} MB")
        else:
            print("警告: 构建完成但未找到可执行文件")
        
    except subprocess.CalledProcessError as e:
        print(f"构建失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False
    
    return True


def create_dmg_macos():
    """在macOS上创建DMG文件（可选）"""
    if sys.platform != 'darwin':
        return
    
    print("创建macOS DMG安装包...")
    
    try:
        # 创建临时目录
        temp_dir = 'temp_dmg'
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)
        
        # 复制应用到临时目录
        if os.path.exists('dist/MediaCopyer'):
            shutil.copy('dist/MediaCopyer', temp_dir)
        
        # 创建DMG文件
        dmg_name = 'MediaCopyer.dmg'
        cmd = [
            'hdiutil', 'create', '-volname', 'MediaCopyer',
            '-srcfolder', temp_dir, '-ov', '-format', 'UDZO',
            dmg_name
        ]
        
        subprocess.run(cmd, check=True)
        print(f"DMG文件已创建: {dmg_name}")
        
        # 清理临时目录
        shutil.rmtree(temp_dir)
        
    except Exception as e:
        print(f"创建DMG失败: {e}")


def main():
    """主函数"""
    print("MediaCopyer 应用打包工具")
    print("=" * 40)
    
    # 清理之前的构建
    clean_build()
    
    # 构建应用程序
    if build_app():
        print("\n构建完成!")
        
        # 在macOS上可选择创建DMG
        if sys.platform == 'darwin':
            choice = input("是否创建DMG安装包? (y/n): ").lower()
            if choice == 'y':
                create_dmg_macos()
        
        print("\n使用方法:")
        print("1. 运行可执行文件: ./dist/MediaCopyer")
        print("2. 或者双击 dist/MediaCopyer 文件")
        
    else:
        print("\n构建失败，请检查错误信息")
        sys.exit(1)


if __name__ == '__main__':
    main()
