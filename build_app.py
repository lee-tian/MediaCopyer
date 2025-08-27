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
    """在macOS上创建带有拖拽安装界面的DMG文件"""
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
        app_path = None
        if os.path.exists('dist/MediaCopyer.app'):
            # macOS app bundle
            app_path = 'dist/MediaCopyer.app'
            dest_path = os.path.join(temp_dir, 'MediaCopyer.app')
            shutil.copytree(app_path, dest_path)
        elif os.path.exists('dist/MediaCopyer'):
            # 检查是否为目录
            if os.path.isdir('dist/MediaCopyer'):
                app_path = 'dist/MediaCopyer'
                dest_path = os.path.join(temp_dir, 'MediaCopyer')
                shutil.copytree(app_path, dest_path)
            else:
                # 普通可执行文件
                app_path = 'dist/MediaCopyer'
                shutil.copy(app_path, temp_dir)
        else:
            print("错误: 未找到应用文件 dist/MediaCopyer 或 dist/MediaCopyer.app")
            return

        # 创建Applications文件夹的符号链接
        applications_link = os.path.join(temp_dir, 'Applications')
        os.symlink('/Applications', applications_link)

        # 创建临时DMG文件
        temp_dmg = 'temp_MediaCopyer.dmg'
        dmg_name = 'MediaCopyer.dmg'
        
        # 删除已存在的DMG文件
        if os.path.exists(dmg_name):
            os.remove(dmg_name)
        if os.path.exists(temp_dmg):
            os.remove(temp_dmg)

        # 创建可读写的DMG文件
        cmd = [
            'hdiutil', 'create', '-volname', 'MediaCopyer Installer',
            '-srcfolder', temp_dir, '-ov', '-format', 'UDRW',
            temp_dmg
        ]
        subprocess.run(cmd, check=True)

        # 挂载DMG文件进行自定义
        print("挂载DMG文件进行自定义...")
        mount_result = subprocess.run(['hdiutil', 'attach', temp_dmg], 
                                    capture_output=True, text=True)
        
        if mount_result.returncode == 0:
            # 解析挂载点
            mount_point = None
            for line in mount_result.stdout.split('\n'):
                if '/Volumes/' in line:
                    mount_point = line.split('\t')[-1].strip()
                    break
            
            if mount_point:
                print(f"DMG已挂载到: {mount_point}")
                
                # 创建AppleScript来设置Finder窗口属性
                app_name = "MediaCopyer.app" if os.path.exists('dist/MediaCopyer.app') else "MediaCopyer"
                applescript = f'''
tell application "Finder"
    tell disk "MediaCopyer Installer"
        open
        set current view of container window to icon view
        set toolbar visible of container window to false
        set statusbar visible of container window to false
        set the bounds of container window to {{100, 100, 600, 400}}
        set viewOptions to the icon view options of container window
        set arrangement of viewOptions to not arranged
        set icon size of viewOptions to 72
        set background picture of viewOptions to file ".background:background.png"
        set position of item "{app_name}" of container window to {{150, 200}}
        set position of item "Applications" of container window to {{350, 200}}
        close
        open
        update without registering applications
        delay 2
    end tell
end tell
'''
                
                # 创建背景图片目录
                bg_dir = os.path.join(mount_point, '.background')
                if not os.path.exists(bg_dir):
                    os.makedirs(bg_dir)
                
                # 创建简单的背景图片（如果有图片工具的话）
                create_background_image(bg_dir)
                
                # 执行AppleScript
                print("设置DMG窗口属性...")
                subprocess.run(['osascript', '-e', applescript])
                
                # 卸载DMG
                print("卸载DMG...")
                subprocess.run(['hdiutil', 'detach', mount_point])
                
                # 转换为只读压缩格式
                print("转换为最终DMG格式...")
                cmd = [
                    'hdiutil', 'convert', temp_dmg, 
                    '-format', 'UDZO', '-o', dmg_name
                ]
                subprocess.run(cmd, check=True)
                
                print(f"DMG文件已创建: {dmg_name}")
                
                # 清理临时文件
                os.remove(temp_dmg)
            else:
                print("无法找到DMG挂载点")
        
        # 清理临时目录
        shutil.rmtree(temp_dir)

    except Exception as e:
        print(f"创建DMG失败: {e}")
        import traceback
        traceback.print_exc()


def create_background_image(bg_dir):
    """创建DMG背景图片"""
    try:
        # 尝试使用PIL创建简单的背景图片
        from PIL import Image, ImageDraw, ImageFont
        
        # 创建500x300的背景图片
        img = Image.new('RGB', (500, 300), color='#f0f0f0')
        draw = ImageDraw.Draw(img)
        
        # 添加文字说明
        try:
            font = ImageFont.truetype('/System/Library/Fonts/Arial.ttf', 16)
        except:
            font = ImageFont.load_default()
        
        text = "拖拽 MediaCopyer 到 Applications 文件夹完成安装"
        text_width = draw.textlength(text, font=font)
        x = (500 - text_width) // 2
        draw.text((x, 50), text, fill='#666666', font=font)
        
        # 保存背景图片
        bg_path = os.path.join(bg_dir, 'background.png')
        img.save(bg_path)
        print(f"背景图片已创建: {bg_path}")
        
    except ImportError:
        print("PIL未安装，跳过背景图片创建")
    except Exception as e:
        print(f"创建背景图片失败: {e}")


def main():
    """主函数"""
    print("MediaCopyer 应用打包工具")
    print("=" * 40)
    
    # 清理之前的构建
    clean_build()
    
    # 构建应用程序
    if build_app():
        print("\n构建完成!")
        
        # 在macOS上自动创建DMG
        if sys.platform == 'darwin':
            print("\n正在创建DMG安装包...")
            create_dmg_macos()
        
        print("\n使用方法:")
        print("1. 运行可执行文件: ./dist/MediaCopyer")
        print("2. 或者双击 dist/MediaCopyer 文件")
        
    else:
        print("\n构建失败，请检查错误信息")
        sys.exit(1)


if __name__ == '__main__':
    main()
