#!/usr/bin/env python3
"""
Media Copyer GUI - Organize media files by date into structured directories
"""

import os
import sys
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from pathlib import Path
from datetime import datetime
from typing import Optional
import subprocess
import json
import threading

try:
    from PIL import Image
    from PIL.ExifTags import TAGS
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

def get_creation_date_from_exif(file_path: str) -> Optional[datetime]:
    """Extract creation date from image EXIF data"""
    if not PIL_AVAILABLE:
        return None
    
    try:
        with Image.open(file_path) as image:
            exif_data = image._getexif()
            if exif_data:
                for tag, value in exif_data.items():
                    tag_name = TAGS.get(tag, tag)
                    if tag_name == 'DateTimeOriginal' or tag_name == 'DateTime':
                        return datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
    except Exception as e:
        print(f"Warning: Could not read EXIF from {file_path}: {e}")
    
    return None

def get_creation_date_from_video(file_path: str) -> Optional[datetime]:
    """Extract creation date from video metadata using ffprobe"""
    try:
        # Use ffprobe to get metadata
        cmd = [
            'ffprobe', '-v', 'quiet', '-print_format', 'json',
            '-show_format', '-show_streams', file_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            return None
            
        metadata = json.loads(result.stdout)
        
        # Check format tags first
        if 'format' in metadata and 'tags' in metadata['format']:
            tags = metadata['format']['tags']
            
            # Try different tag names
            for date_tag in ['creation_time', 'date', 'DATE', 'com.apple.quicktime.creationdate']:
                if date_tag in tags:
                    date_str = tags[date_tag]
                    try:
                        # Handle different date formats
                        if 'T' in date_str:
                            # ISO format
                            return datetime.fromisoformat(date_str.replace('Z', '+00:00')).replace(tzinfo=None)
                        else:
                            # Try other formats
                            return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                    except ValueError:
                        continue
        
        # Check stream tags
        if 'streams' in metadata:
            for stream in metadata['streams']:
                if 'tags' in stream:
                    tags = stream['tags']
                    for date_tag in ['creation_time', 'date', 'DATE']:
                        if date_tag in tags:
                            date_str = tags[date_tag]
                            try:
                                if 'T' in date_str:
                                    return datetime.fromisoformat(date_str.replace('Z', '+00:00')).replace(tzinfo=None)
                                else:
                                    return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                            except ValueError:
                                continue
                                
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, json.JSONDecodeError, FileNotFoundError):
        pass
    
    return None

def get_file_date(file_path: str, file_type: str) -> datetime:
    """Get the creation date of a file, trying metadata first, then file mtime"""
    
    if file_type == 'photo':
        # Try EXIF first for photos
        date = get_creation_date_from_exif(file_path)
        if date:
            return date
    elif file_type == 'video':
        # Try video metadata first
        date = get_creation_date_from_video(file_path)
        if date:
            return date
    
    # Fallback to file modification time
    mtime = os.path.getmtime(file_path)
    return datetime.fromtimestamp(mtime)

def get_file_type(file_path: str) -> Optional[str]:
    """Determine if file is a photo or video based on extension"""
    ext = Path(file_path).suffix.lower()
    
    photo_extensions = {'.jpg', '.jpeg', '.arw', '.png', '.tiff', '.tif', '.heic', '.cr2', '.nef', '.dng'}
    video_extensions = {'.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv', '.webm', '.m4v'}
    
    if ext in photo_extensions:
        return 'photo'
    elif ext in video_extensions:
        return 'video'
    
    return None

def get_device_name(file_path: str, file_type: str) -> str:
    """Extract device name from file metadata or filename"""
    device_name = "Unknown"
    
    if file_type == 'photo':
        # Try to get camera make/model from EXIF
        device_name = get_device_from_exif(str(file_path))
    elif file_type == 'video':
        # Try to get device info from video metadata
        device_name = get_device_from_video(str(file_path))
    
    # If no device found from metadata, try filename patterns
    if device_name == "Unknown":
        device_name = get_device_from_filename(str(file_path))
    
    return device_name

def get_device_from_exif(file_path: str) -> str:
    """Extract camera make from EXIF data"""
    if not PIL_AVAILABLE:
        return "Unknown"
    
    try:
        with Image.open(file_path) as image:
            exif_data = image._getexif()
            if exif_data:
                make = None
                model = None
                
                for tag, value in exif_data.items():
                    tag_name = TAGS.get(tag, tag)
                    if tag_name == 'Make':
                        make = value.strip()
                    elif tag_name == 'Model':
                        model = value.strip()
                
                if make:
                    # Normalize common camera brands
                    make_lower = make.lower()
                    if 'canon' in make_lower:
                        return 'Canon'
                    elif 'nikon' in make_lower:
                        return 'Nikon'
                    elif 'sony' in make_lower:
                        return 'Sony'
                    elif 'fujifilm' in make_lower or 'fuji' in make_lower:
                        return 'Fujifilm'
                    elif 'olympus' in make_lower:
                        return 'Olympus'
                    elif 'panasonic' in make_lower:
                        return 'Panasonic'
                    elif 'leica' in make_lower:
                        return 'Leica'
                    elif 'apple' in make_lower:
                        return 'iPhone'
                    elif 'dji' in make_lower:
                        return 'DJI'
                    else:
                        return make
                        
    except Exception as e:
        pass
    
    return "Unknown"

def get_device_from_video(file_path: str) -> str:
    """Extract device info from video metadata"""
    try:
        cmd = [
            'ffprobe', '-v', 'quiet', '-print_format', 'json',
            '-show_format', '-show_streams', file_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            return "Unknown"
            
        metadata = json.loads(result.stdout)
        
        # Check format tags first
        if 'format' in metadata and 'tags' in metadata['format']:
            tags = metadata['format']['tags']
            
            # Look for device/camera info in various tag names
            device_tags = ['make', 'model', 'camera_make', 'camera_model', 'com.apple.quicktime.make', 'com.apple.quicktime.model']
            
            for tag in device_tags:
                if tag in tags:
                    device_info = tags[tag].strip()
                    device_lower = device_info.lower()
                    
                    if 'dji' in device_lower:
                        return 'DJI'
                    elif 'sony' in device_lower:
                        return 'Sony'
                    elif 'canon' in device_lower:
                        return 'Canon'
                    elif 'panasonic' in device_lower:
                        return 'Panasonic'
                    elif 'gopro' in device_lower:
                        return 'GoPro'
                    elif 'apple' in device_lower or 'iphone' in device_lower:
                        return 'iPhone'
                    elif device_info and device_info != "Unknown":
                        return device_info
        
        # Check stream tags
        if 'streams' in metadata:
            for stream in metadata['streams']:
                if 'tags' in stream:
                    tags = stream['tags']
                    for tag in ['handler_name', 'encoder']:
                        if tag in tags:
                            handler = tags[tag].lower()
                            if 'dji' in handler:
                                return 'DJI'
                            elif 'gopro' in handler:
                                return 'GoPro'
                                
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, json.JSONDecodeError, FileNotFoundError):
        pass
    
    return "Unknown"

def get_device_from_filename(file_path: str) -> str:
    """Try to determine device from filename patterns"""
    filename = Path(file_path).name.upper()
    
    # Common filename patterns
    if filename.startswith('DJI_'):
        return 'DJI'
    elif filename.startswith('GOPR') or filename.startswith('GP'):
        return 'GoPro'
    elif filename.startswith('DSC') or filename.startswith('IMG'):
        # These are common but not device-specific
        pass
    elif 'PANO' in filename:
        # Could be DJI panorama
        return 'DJI'
    
    return "Unknown"

def generate_unique_filename(target_path: Path) -> Path:
    """Generate a unique filename if file already exists"""
    if not target_path.exists():
        return target_path
    
    base_name = target_path.stem
    extension = target_path.suffix
    parent = target_path.parent
    
    counter = 1
    while True:
        new_name = f"{base_name}_{counter}{extension}"
        new_path = parent / new_name
        if not new_path.exists():
            return new_path
        counter += 1

def scan_directory(source_dir: Path) -> list:
    """Recursively scan directory for media files"""
    media_files = []
    
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            file_path = Path(root) / file
            file_type = get_file_type(str(file_path))
            
            if file_type:
                media_files.append((file_path, file_type))
    
    return media_files

class MediaCopyerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Media Copyer - 媒体文件整理工具")
        self.root.geometry("800x600")
        
        # Variables
        self.source_dir = tk.StringVar()
        self.dest_dir = tk.StringVar()
        self.move_mode = tk.BooleanVar()
        self.dry_run = tk.BooleanVar()
        self.by_device = tk.BooleanVar()
        
        self.is_processing = False
        
        self.setup_ui()
        self.check_dependencies()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Media Copyer - 媒体文件整理工具", 
                               font=('TkDefaultFont', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Source directory selection
        ttk.Label(main_frame, text="源目录 (Source Directory):").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.source_dir, width=50).grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 5))
        ttk.Button(main_frame, text="浏览...", command=self.select_source_dir).grid(row=1, column=2, pady=5)
        
        # Destination directory selection
        ttk.Label(main_frame, text="目标目录 (Destination Directory):").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.dest_dir, width=50).grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 5))
        ttk.Button(main_frame, text="浏览...", command=self.select_dest_dir).grid(row=2, column=2, pady=5)
        
        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="选项 (Options)", padding="10")
        options_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=20)
        
        ttk.Checkbutton(options_frame, text="移动模式 (Move files instead of copy)", 
                       variable=self.move_mode).grid(row=0, column=0, sticky=tk.W)
        ttk.Checkbutton(options_frame, text="试运行模式 (Dry run - preview only)", 
                       variable=self.dry_run).grid(row=1, column=0, sticky=tk.W)
        ttk.Checkbutton(options_frame, text="按设备分类 (Organize by device - e.g., /Movies/2025/DJI)", 
                       variable=self.by_device).grid(row=2, column=0, sticky=tk.W)
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=20)
        
        self.start_button = ttk.Button(button_frame, text="开始处理 (Start Processing)", 
                                      command=self.start_processing)
        self.start_button.grid(row=0, column=0, padx=5)
        
        ttk.Button(button_frame, text="清空日志", command=self.clear_log).grid(row=0, column=1, padx=5)
        
        # Progress bar
        self.progress_var = tk.StringVar()
        self.progress_var.set("准备就绪")
        
        progress_frame = ttk.Frame(main_frame)
        progress_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(progress_frame, textvariable=self.progress_var).grid(row=1, column=0)
        
        # Log area
        log_frame = ttk.LabelFrame(main_frame, text="处理日志 (Processing Log)", padding="5")
        log_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(6, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, width=80)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    def select_source_dir(self):
        """Select source directory"""
        directory = filedialog.askdirectory(title="选择源目录")
        if directory:
            self.source_dir.set(directory)
    
    def select_dest_dir(self):
        """Select destination directory"""
        directory = filedialog.askdirectory(title="选择目标目录")
        if directory:
            self.dest_dir.set(directory)
    
    def clear_log(self):
        """Clear the log text area"""
        self.log_text.delete(1.0, tk.END)
    
    def log_message(self, message):
        """Add message to log text area"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def check_dependencies(self):
        """Check if required dependencies are available"""
        messages = []
        
        if not PIL_AVAILABLE:
            messages.append("⚠️ PIL/Pillow 未安装，无法读取图片EXIF信息")
        
        try:
            subprocess.run(['ffprobe', '-version'], capture_output=True, check=True)
        except (subprocess.SubprocessError, FileNotFoundError):
            messages.append("⚠️ ffprobe 未找到，无法读取视频元数据")
        
        if messages:
            for msg in messages:
                self.log_message(msg)
            self.log_message("可以继续使用，但会影响日期识别精度\n" + "="*50)
    
    def start_processing(self):
        """Start the file processing in a separate thread"""
        if self.is_processing:
            return
        
        # Validate inputs
        if not self.source_dir.get():
            messagebox.showerror("错误", "请选择源目录")
            return
        
        if not self.dest_dir.get():
            messagebox.showerror("错误", "请选择目标目录")
            return
        
        source_path = Path(self.source_dir.get())
        if not source_path.exists():
            messagebox.showerror("错误", f"源目录不存在: {source_path}")
            return
        
        if not source_path.is_dir():
            messagebox.showerror("错误", f"源路径不是一个目录: {source_path}")
            return
        
        # Start processing in a separate thread
        self.is_processing = True
        self.start_button.config(state='disabled')
        self.progress_bar.start()
        
        processing_thread = threading.Thread(target=self.process_files)
        processing_thread.daemon = True
        processing_thread.start()
    
    def process_files(self):
        """Process the media files"""
        try:
            source_path = Path(self.source_dir.get())
            dest_path = Path(self.dest_dir.get())
            move_mode = self.move_mode.get()
            dry_run = self.dry_run.get()
            
            self.progress_var.set("正在扫描文件...")
            self.log_message(f"开始处理媒体文件")
            self.log_message(f"源目录: {source_path}")
            self.log_message(f"目标目录: {dest_path}")
            self.log_message(f"模式: {'移动' if move_mode else '复制'}")
            if dry_run:
                self.log_message("试运行模式 - 不会实际移动/复制文件")
            self.log_message("="*50)
            
            # Scan for media files
            media_files = scan_directory(source_path)
            
            if not media_files:
                self.log_message("未找到媒体文件!")
                return
            
            self.log_message(f"找到 {len(media_files)} 个媒体文件")
            
            stats = {
                'photos': 0,
                'videos': 0,
                'errors': 0,
                'processed': 0
            }
            
            total_files = len(media_files)
            
            for i, (file_path, file_type) in enumerate(media_files):
                try:
                    self.progress_var.set(f"处理文件 {i+1}/{total_files}: {file_path.name}")
                    
                    # Get file creation date
                    file_date = get_file_date(str(file_path), file_type)
                    
                    # Create target directory structure
                    year = file_date.strftime('%Y')
                    
                    if self.by_device.get():
                        # Get device name for organization
                        device_name = get_device_name(str(file_path), file_type)
                        if 'devices' not in stats:
                            stats['devices'] = set()
                        stats['devices'].add(device_name)
                        
                        # Organize by device: /Movies/2025/DJI or /Movies/2025/Sony
                        target_dir = dest_path / year / device_name
                        self.log_message(f"  设备检测: {device_name}")
                    else:
                        # Original organization by type and date
                        date_str = file_date.strftime('%Y-%m-%d')
                        
                        if file_type == 'photo':
                            target_dir = dest_path / 'Picture' / year / date_str
                        else:  # video
                            target_dir = dest_path / 'Video' / year / date_str
                    
                    if file_type == 'photo':
                        stats['photos'] += 1
                    else:
                        stats['videos'] += 1
                    
                    # Create target directory if it doesn't exist
                    if not dry_run:
                        target_dir.mkdir(parents=True, exist_ok=True)
                    
                    # Generate unique target filename
                    target_path = target_dir / file_path.name
                    if not dry_run:
                        target_path = generate_unique_filename(target_path)
                    
                    self.log_message(f"{file_path} -> {target_path}")
                    
                    if not dry_run:
                        if move_mode:
                            shutil.move(str(file_path), str(target_path))
                            self.log_message(f"  ✓ 已移动: {file_path.name}")
                        else:
                            shutil.copy2(str(file_path), str(target_path))
                            self.log_message(f"  ✓ 已复制: {file_path.name}")
                    else:
                        self.log_message(f"  [试运行] 将{'移动' if move_mode else '复制'}到: {target_path}")
                    
                    stats['processed'] += 1
                    
                except Exception as e:
                    self.log_message(f"❌ 处理文件时出错 {file_path}: {e}")
                    stats['errors'] += 1
            
            # Print statistics
            self.log_message("\n" + "="*50)
            self.log_message("处理完成!")
            self.log_message("="*50)
            self.log_message(f"照片处理: {stats['photos']}")
            self.log_message(f"视频处理: {stats['videos']}")
            self.log_message(f"错误数量: {stats['errors']}")
            self.log_message(f"总文件数: {stats['processed']}")
            
            if dry_run:
                self.log_message("\n(这是试运行 - 没有实际移动/复制文件)")
            
            self.progress_var.set("处理完成!")
            
            if stats['errors'] == 0:
                messagebox.showinfo("完成", f"成功处理了 {stats['processed']} 个文件!")
            else:
                messagebox.showwarning("完成", f"处理了 {stats['processed']} 个文件，但有 {stats['errors']} 个错误。请查看日志了解详情。")
        
        except Exception as e:
            self.log_message(f"❌ 发生严重错误: {e}")
            messagebox.showerror("错误", f"发生错误: {e}")
        
        finally:
            # Reset UI state
            self.is_processing = False
            self.start_button.config(state='normal')
            self.progress_bar.stop()
            if not hasattr(self, '_processing_complete'):
                self.progress_var.set("准备就绪")

def main():
    """Main function to run the GUI application"""
    root = tk.Tk()
    app = MediaCopyerGUI(root)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()
