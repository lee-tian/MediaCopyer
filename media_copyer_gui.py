#!/usr/bin/env python3
"""
Media Copyer GUI - Organize media files by date into structured directories
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from pathlib import Path
import threading

# Import from the new modular core library
from core import organize_media_files, validate_directory, scan_directory
from core.utils import check_dependencies

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
        self.organization_mode = tk.StringVar(value="date")  # "date", "device", "date_device"
        
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
        
        # Organization mode selection
        ttk.Label(options_frame, text="组织方式 (Organization Mode):").grid(row=2, column=0, sticky=tk.W, pady=(10,5))
        
        mode_frame = ttk.Frame(options_frame)
        mode_frame.grid(row=3, column=0, sticky=tk.W, padx=(20, 0))
        
        ttk.Radiobutton(mode_frame, text="按日期 (By Date): Video/2025/2025-07-25", 
                       variable=self.organization_mode, value="date").grid(row=0, column=0, sticky=tk.W)
        ttk.Radiobutton(mode_frame, text="按设备 (By Device): Video/2025/DJI", 
                       variable=self.organization_mode, value="device").grid(row=1, column=0, sticky=tk.W)
        ttk.Radiobutton(mode_frame, text="按日期+设备 (By Date+Device): Video/2025/2025-07-25/DJI", 
                       variable=self.organization_mode, value="date_device").grid(row=2, column=0, sticky=tk.W)
        
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
        messages = check_dependencies()
        
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
        if not validate_directory(str(source_path), must_exist=True):
            messagebox.showerror("错误", f"源目录不存在或无效: {source_path}")
            return
        
        # Start processing in a separate thread
        self.is_processing = True
        self.start_button.config(state='disabled')
        self.progress_bar.start()
        
        processing_thread = threading.Thread(target=self.process_files)
        processing_thread.daemon = True
        processing_thread.start()
    
    def process_files(self):
        """Process the media files using the core library"""
        try:
            source_path = Path(self.source_dir.get())
            dest_path = Path(self.dest_dir.get())
            
            self.progress_var.set("正在处理文件...")
            self.log_message(f"开始处理媒体文件")
            self.log_message(f"源目录: {source_path}")
            self.log_message(f"目标目录: {dest_path}")
            self.log_message(f"模式: {'移动' if self.move_mode.get() else '复制'}")
            if self.dry_run.get():
                self.log_message("试运行模式 - 不会实际移动/复制文件")
            self.log_message("="*50)
            
            # Quick scan to show file count
            media_files = scan_directory(source_path)
            if not media_files:
                self.log_message("未找到媒体文件!")
                return
            
            self.log_message(f"找到 {len(media_files)} 个媒体文件")
            
            # Use the core library's organize function with GUI progress callback
            def progress_callback(current, total, filename):
                """Callback function for progress updates"""
                self.progress_var.set(f"处理文件 {current}/{total}: {filename}")
                self.log_message(f"正在处理: {filename}")
            
            def log_callback(message):
                """Callback function for log messages"""
                self.log_message(message)
            
            # Call the main organize function from core library
            stats = organize_media_files(
                source_dir=source_path,
                dest_dir=dest_path,
                move_mode=self.move_mode.get(),
                dry_run=self.dry_run.get(),
                organization_mode=self.organization_mode.get(),
                progress_callback=progress_callback
            )
            
            # Print statistics
            self.log_message("\n" + "="*50)
            self.log_message("处理完成!")
            self.log_message("="*50)
            self.log_message(f"照片处理: {stats['photos']}")
            self.log_message(f"视频处理: {stats['videos']}")
            self.log_message(f"错误数量: {stats['errors']}")
            self.log_message(f"总文件数: {stats['processed']}")
            
            if self.dry_run.get():
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
