#!/usr/bin/env python3
"""
Chinese (Simplified) translations for MediaCopyer GUI
"""

translations = {
    # Main Window
    "app_title": "Media Copyer - 媒体文件整理工具",
    "main_title": "Media Copyer - 媒体文件整理工具",
    "language": "语言/language",
    "source_directory": "源目录 (Source Directory):",
    "destination_directory": "目标目录 (Destination Directory):",
    "select_source": "选择源目录",
    "select_destination": "选择目标目录",
    
    # Options Frame
    "options": "选项",
    "move_mode": "移动模式 (删除源目录文件)",
    "dry_run": "试运行模式 (Dry run - preview only)",
    "md5_check": "MD5完整性校验 (MD5 integrity verification)",
    "organization_mode": "组织方式 (Organization Mode)",
    "org_by_date": "按日期 (By Date): Video/2025/2025-07-25",
    "org_by_device": "按设备 (By Device): Video/2025/DJI",
    "org_by_date_device": "按日期+设备 (By Date+Device): Video/2025/2025-07-25/DJI",
    "org_by_extension": "按文件后缀 (By Extension): Video/mp4, Photo/jpg",
    "org_mode_date": "按日期",
    "org_mode_device": "按设备", 
    "org_mode_date_device": "按日期+设备",
    "org_mode_extension": "按文件后缀",
    "dry_run_mode": "试运行模式",
    "md5_verification": "MD5完整性校验",
    "ignore_duplicates": "忽略重复文件",
    "processing_log": "处理日志",
    "source_directories": "源目录列表",
    "destination_directories": "目标目录列表",
    "add_destination": "添加目录",
    "add_source": "添加源目录",
    "remove_selected": "删除所选",
    "destination": "目标",
    "source": "源",
    "path": "路径",
    "select_destination_directory": "选择目标目录",
    "select_source_directory": "选择源目录",
    
    # Frequent Directories
    "frequent_directories": "常用目录",
    "recent_directories": "最近目录", 
    "remember_last_dirs": "记住上次目录",
    "frequent_sources": "常用源目录",
    "frequent_destinations": "常用目标目录",
    "clear_frequent": "清空常用",
    "use_selected": "使用选中",
    "add_to_frequent": "添加到常用",
    "remove_from_frequent": "从常用中移除",
    
    # Buttons
    "start": "开始处理",
    "stop": "停止",
    "clear_log": "清空日志",
    "browse": "浏览",
    "start_processing": "开始处理",
    "cancel_processing": "取消",
    
    # Progress and Log
    "progress": "进度",
    "log": "日志",
    "status_ready": "就绪",
    "status_processing": "正在处理...",
    "status_completed": "完成",
    "status_stopped": "已停止",
    "status_error": "错误",
    
    # Processing Messages
    "error": "错误",
    "please_select_source_dir": "请选择源目录",
    "please_select_dest_dir": "请选择目标目录",
    "source_dir_invalid": "源目录无效: {}",
    "processing_files": "正在处理文件...",
    "start_processing_media": "开始处理媒体文件",
    "dest_directory": "目标目录: {}",
    "mode_info": "模式: {}",
    "move_mode_text": "移动模式",
    "copy_mode_text": "复制模式",
    "dry_run_info": "试运行模式 - 仅预览，不会实际移动或复制文件",
    "ignore_duplicates_info": "忽略重复文件模式 - 跳过重复文件，不进行处理",
    "no_media_files_found": "未找到媒体文件",
    "found_files_count": "找到 {} 个媒体文件",
    "processing_file_progress": "处理中... ({}/{}) {}",
    "processing_file": "正在处理: {}",
    "processing_complete": "处理完成",
    "photos_processed": "已处理照片: {} 张",
    "videos_processed": "已处理视频: {} 个",
    "errors_count": "处理出错: {} 个",
    "total_files": "总计处理: {} 个文件",
    "dry_run_notice": "这是试运行模式，实际上没有移动或复制文件。",
    "complete": "完成",
    "success_message": "成功处理了 {} 个文件！",
    "warning_message": "处理了 {} 个文件，其中 {} 个出现错误。请检查日志获取详情。",
    "serious_error": "发生严重错误: {}",
    "error_occurred": "处理过程中发生错误: {}",
    "ready_status": "就绪",
    "canceling_operation": "正在取消操作...",
    "operation_canceled": "操作已取消",
    
    # Tab Names
    "settings": "设置",
    "execution": "执行",
    "directory_selection": "目录选择",
    
    # Other Messages
    "dependency_warning": "可以继续，但日期识别准确性可能受到影响",
    "select_directories": "请先选择源目录和目标目录",
    "invalid_source": "源目录不存在或不可访问",
    "invalid_destination": "目标目录不存在或不可访问",
    
    # Settings guidance
    "setup_guidance": "请完成上方的目录选择和选项配置，然后点击开始执行按钮",
    "setup_complete_guidance": "设置已完成！点击右侧按钮开始执行文件处理",
    "go_to_execution": "开始执行",
    
    # External storage detection
    "auto_detected_external_storage": "自动检测到 {} 个外置存储设备",
    "external_storage_added": "已自动添加外置存储: {}",
    
    # Additional UI text
    "dependency_warning": "警告：某些功能可能不可用",
    
    # Multi-destination processing messages
    "source_dir_count": "源目录数量: {}",
    "source_dir_number": "源目录 {}: {}",
    "dest_dir_count": "目标目录数量: {}",
    "dest_dir_number": "目标目录 {}: {}",
    "processing_dest_dir": "处理目标目录 {}/{}: {}",
    "processing_source_to_dest": "源 {}/{}: {}",
    "source_to_dest_complete": "源 {} -> 目标 {} 完成:",
    "photos_count": "  照片: {}",
    "videos_count": "  视频: {}",
    "errors_count_detail": "  错误: {}",
    "total_count": "  总计: {}",
    "source_to_dest_error": "源 {} -> 目标 {} 处理错误: {}",
    "all_destinations_complete": "所有目标处理完成",
    "total_photos": "总照片数: {}",
    "total_videos": "总视频数: {}",
    "total_errors": "总错误数: {}",
    "total_processed": "总处理数: {}",
    "dest_progress_status": "目标 {}/{}, 源 {}/{}: {}",
    "success_multi_dest": "成功处理 {} 个文件到 {} 个目标目录",
    "warning_multi_dest": "处理了 {} 个文件，但有 {} 个错误",
    
    # Log messages for parallel processing
    "parallel_start_processing": "[并行] 开始处理: 源 {}/{} -> 目标 {}/{}",
    "parallel_source_dir": "[并行] 源目录: {}",
    "parallel_dest_dir": "[并行] 目标目录: {}",
    "parallel_no_media_files": "[并行] 源目录 {} 中没有找到媒体文件",
    "parallel_processing_file": "[并行] 处理文件: {}",
    "parallel_source_dest_complete": "[并行] 源 {} -> 目标 {} 完成:",
    "parallel_photos": "[并行]   照片: {}",
    "parallel_videos": "[并行]   视频: {}",
    "parallel_errors": "[并行]   错误: {}",
    "parallel_total": "[并行]   总计: {}",
    "parallel_task_exception": "[并行] 任务执行异常: 源 {} -> 目标 {}: {}",
    "parallel_all_complete": "✅ 所有目标处理完成 (并行模式)",
    "parallel_using_threads": "使用 {} 个并行线程处理 {} 个源目录",
    
    # Size analysis log messages
    "source_size_analysis": "📊 源目录大小分析",
    "source_dir_info": "源目录 {}: {}",
    "total_files": "  📁 总文件数: {}",
    "photos_info": "  📷 照片: {} 个 ({:.1f} MB)",
    "videos_info": "  🎥 视频: {} 个 ({:.1f} MB)",
    "media_files_total": "  📊 媒体文件总计: {} 个 ({:.1f} MB)",
    "all_sources_summary": "🎯 所有源目录汇总:",
    "total_media_files": "  📊 媒体文件总数: {}",
    "total_media_size": "  💾 媒体文件总大小: {:.1f} MB",
    "estimated_space_needed": "  🔧 预计需要空间: {:.1f} MB ({} 到 {} 个目标)",
    "dest_space_check": "💽 目标目录空间检查:",
    "space_status_sufficient": "✅ 充足",
    "space_status_insufficient": "⚠️ 不足",
    "dest_space_info": "  目标 {}: {:.1f} MB 可用 / {:.1f} MB 需要 - {}",
    "dest_space_check_failed": "  目标 {}: 无法检查空间 - {}",
    "space_warning": "⚠️ 空间警告: {}",
    "start_parallel_processing": "🚀 开始并行处理",
    "processing_dest_header": "处理目标目录 {}/{}: {}",
    "dest_size_analysis": "📊 目标目录大小分析",
    "dest_dir_info": "目标目录 {}: {}",
    "all_dests_summary": "🎯 所有目标目录汇总:",
    "size_comparison": "📈 大小对比分析:",
    "source_comparison": "  源目录: {} 个文件, {}",
    "dest_comparison": "  目标目录: {} 个文件, {}",
    "files_match_move": "  ✅ 文件数量匹配 (移动模式)",
    "files_mismatch": "  ⚠️ 文件数量不匹配: 差异 {} 个文件",
    "move_mode_text_short": "移动",
    "copy_mode_text_short": "复制",
    
    # Core module messages
    "removed_empty_directory": "删除空目录: {}",
    "cleaned_up_empty_directories": "清理了 {} 个空目录",
    "warning_empty_dir_cleanup": "警告: 清理空目录时出错: {}",
    
    # Copy completion messages
    "files_copy_complete": "  ✅ 文件复制完整 ({} 个目标)",
    "copy_ratio": "  📊 复制比例: {:.1f}x (预期 {}x)",
    "parallel_success_message": "成功并行处理 {} 个文件到 {} 个目标目录",
    "parallel_warning_message": "并行处理了 {} 个文件，但有 {} 个错误",
    "processing_complete_log": "处理完成: {} 个文件, {} 个错误",
    "parallel_progress_status": "[并行] 源{}->目标{}: {}",
    "parallel_processing_error": "[并行] 源 {} -> 目标 {} 处理错误: {}",
    
    # Duplicate file handling
    "total_duplicates": "总重复文件数: {}",
    "total_skipped": "总跳过文件数: {}",
    "parallel_duplicates": "[并行]   重复: {}",
    "parallel_skipped": "[并行]   跳过: {}",
    
    # Enhanced copy analysis
    "copy_operation_summary": "📋 本次复制操作汇总:",
    "files_copied_this_time": "  📤 本次复制文件数: {}",
    "size_copied_this_time": "  💾 本次复制大小: {}",
    "dest_increase_files": "  📈 目标目录增加文件: {}",
    "dest_increase_size": "  📈 目标目录增加大小: {}",
    "copy_match_analysis": "🔍 复制匹配分析:",
    "copy_files_match": "  ✅ 复制文件数匹配预期",
    "copy_files_mismatch": "  ⚠️ 复制文件数不匹配: 预期 {}, 实际 {}, 差异 {}",
    "copy_size_match": "  ✅ 复制大小匹配预期",
    "copy_size_mismatch": "  ⚠️ 复制大小不匹配: 预期 {}, 实际 {}, 差异 {}",
    "dest_before_after": "📊 目标目录前后对比:",
    "dest_before": "  📥 复制前: {} 个文件, {}",
    "dest_after": "  📤 复制后: {} 个文件, {}",
    "net_increase": "  📈 净增加: {} 个文件, {}",
    
    # Menu items
    "help_menu": "帮助",
    "window_menu": "窗口",
    "user_guide": "用户指南",
    "keyboard_shortcuts": "快捷键",
    "report_issue": "报告问题",
    "check_updates": "检查更新",
    "about": "关于",
    "close": "关闭",
    
    # About dialog
    "app_name": "应用名称",
    "version": "版本",
    "author": "作者",
    "description": "描述",
    "features": "功能特性",
    "feature_auto_organize": "自动按日期整理照片和视频",
    "feature_date_based": "基于EXIF数据的智能日期识别",
    "feature_duplicate_handling": "智能重复文件处理",
    "feature_preview_mode": "预览模式（试运行）",
    "feature_multilingual": "多语言支持（中文/英文）",
    "feature_batch_processing": "批量处理多个目录",
    "supported_formats": "支持格式",
    "image_formats": "图片格式",
    "video_formats": "视频格式",
    "license": "许可证",
    
    # User guide content
    "user_guide_content": """MediaCopyer 用户指南

📋 基本使用步骤：

1. 选择源目录
   • 点击"添加源目录"按钮选择包含照片和视频的文件夹
   • 可以添加多个源目录进行批量处理
   • 支持从SD卡、相机、手机等设备导入

2. 选择目标目录
   • 点击"添加目录"按钮选择整理后文件的存放位置
   • 可以添加多个目标目录，文件会复制到所有目标
   • 建议选择有足够空间的目录

3. 配置选项
   • 组织方式：选择按日期、设备或文件类型整理
   • 移动模式：勾选后会移动文件而不是复制
   • 试运行：勾选后只预览不实际操作文件
   • MD5校验：确保文件完整性
   • 忽略重复：跳过已存在的重复文件

4. 开始处理
   • 点击"开始执行"切换到执行界面
   • 查看进度和详细日志
   • 处理完成后查看统计信息

🔧 高级功能：

• 多目录并行处理：同时处理多个源目录到多个目标
• 智能日期识别：从EXIF数据、文件名、修改时间提取日期
• 重复文件检测：基于MD5哈希值识别重复文件
• 空间检查：自动检查目标目录可用空间
• 详细统计：显示处理的文件数量、大小等信息

📁 文件组织结构：

按日期组织：
  Photos/2025/2025-01-15/
  Videos/2025/2025-01-15/

按设备组织：
  Photos/iPhone/
  Videos/DJI/

按日期+设备：
  Photos/2025/2025-01-15/iPhone/
  Videos/2025/2025-01-15/DJI/

按文件类型：
  jpg/
  mp4/
  mov/

⚠️ 注意事项：

• 首次使用建议开启"试运行"模式预览结果
• 移动模式会删除源文件，请谨慎使用
• 处理大量文件时建议先检查目标目录空间
• 建议定期备份重要文件

💡 使用技巧：

• 使用"记住上次目录"功能快速重复操作
• 添加常用目录到收藏夹
• 查看详细日志了解处理过程
• 使用多语言界面（中文/英文）""",
    
    # Keyboard shortcuts content
    "shortcuts_content": """MediaCopyer 快捷键

⌨️ 通用快捷键：
• Ctrl+Q / Cmd+Q：退出应用
• Ctrl+, / Cmd+,：打开设置
• F1：显示帮助
• F5：刷新界面

📁 目录操作：
• Ctrl+O / Cmd+O：选择源目录
• Ctrl+Shift+O / Cmd+Shift+O：选择目标目录
• Delete：删除选中的目录

▶️ 处理操作：
• Ctrl+Enter / Cmd+Enter：开始处理
• Escape：停止处理
• Ctrl+L / Cmd+L：清空日志

🔄 界面切换：
• Ctrl+1 / Cmd+1：切换到设置标签
• Ctrl+2 / Cmd+2：切换到执行标签
• Tab：在控件间切换焦点

📋 其他：
• Ctrl+C / Cmd+C：复制日志内容
• Ctrl+A / Cmd+A：全选日志内容
• Ctrl+F / Cmd+F：在日志中查找""",
}
