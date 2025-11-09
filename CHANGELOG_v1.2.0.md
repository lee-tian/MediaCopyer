# MediaCopyer v1.2.0 更新日志 / Changelog

## 🎉 新功能 / New Features

### 💾 自动检测外置存储设备 / Auto External Storage Detection

**中文说明：**

MediaCopyer 现在可以在启动时自动检测并添加所有已连接的外置存储设备到源目录列表。这个功能极大地简化了从 SD 卡、USB 驱动器和外置硬盘导入照片和视频的流程。

**主要特性：**
- ✅ 自动扫描所有已连接的外置存储设备
- ✅ 智能添加到源目录列表
- ✅ 支持 macOS、Linux 和 Windows
- ✅ 自动去重，避免重复添加
- ✅ 显示设备详细信息（容量、可用空间等）

**支持的设备类型：**
- SD 卡（相机存储卡）
- USB 闪存驱动器
- 外置硬盘（HDD/SSD）
- 手机存储设备
- 其他可移动存储设备

**使用方法：**
1. 连接外置存储设备
2. 启动 MediaCopyer
3. 应用自动检测并添加设备到源目录列表
4. 检查列表，移除不需要的设备（可选）
5. 配置选项并开始处理

---

**English Description:**

MediaCopyer now automatically detects and adds all connected external storage devices to the source directory list on startup. This feature greatly simplifies the workflow of importing photos and videos from SD cards, USB drives, and external hard drives.

**Key Features:**
- ✅ Automatically scans all connected external storage devices
- ✅ Intelligently adds to source directory list
- ✅ Supports macOS, Linux, and Windows
- ✅ Automatic deduplication to avoid duplicate additions
- ✅ Shows device details (capacity, available space, etc.)

**Supported Device Types:**
- SD cards (camera memory cards)
- USB flash drives
- External hard drives (HDD/SSD)
- Phone storage devices
- Other removable storage devices

**How to Use:**
1. Connect external storage devices
2. Launch MediaCopyer
3. App automatically detects and adds devices to source directory list
4. Review list and remove unwanted devices (optional)
5. Configure options and start processing

---

## 🔧 技术改进 / Technical Improvements

### 新增模块 / New Modules

**`core/utils/external_storage.py`**
- `get_external_storage_devices()`: 检测所有外置存储设备
- `is_external_storage(path)`: 判断路径是否在外置存储上
- `get_device_info(device_path)`: 获取设备详细信息

### 修改的文件 / Modified Files

**`gui/directory_selector.py`**
- 在 `MultiSourceSelector` 类中添加 `_auto_add_external_storage()` 方法
- 在初始化时自动调用外置存储检测

**`core/utils/__init__.py`**
- 导出新的外置存储检测功能

**翻译文件 / Translation Files**
- `gui/locales/zh_CN.py`: 添加中文翻译
- `gui/locales/en_US.py`: 添加英文翻译

---

## 📚 文档更新 / Documentation Updates

- 新增 `docs/AUTO_EXTERNAL_STORAGE.md`: 详细的功能说明文档
- 更新 `README.md`: 添加新功能介绍
- 新增 `test_external_storage.py`: 测试脚本

---

## 🧪 测试 / Testing

运行测试脚本验证功能：
```bash
python test_external_storage.py
```

测试结果示例：
```
============================================================
External Storage Detection Test
============================================================
Operating System: Darwin
Platform: macOS-15.6.1-arm64-arm-64bit-Mach-O

Detecting external storage devices...
✅ Found 7 external storage device(s):

1. /Volumes/Video
   - Exists: True
   - Readable: True
   - Total Size: 30901.67 GB
   - Free Space: 15474.27 GB
   - Used Space: 15427.40 GB
   - Usage: 49.9%

2. /Volumes/SD_Card
   - Exists: True
   - Readable: True
   - Total Size: 238.29 GB
   - Free Space: 214.13 GB
   - Used Space: 24.16 GB
   - Usage: 10.1%
...
============================================================
```

---

## 🎯 使用场景 / Use Cases

### 场景 1: 从相机 SD 卡导入照片
1. 将相机 SD 卡插入读卡器
2. 启动 MediaCopyer
3. SD 卡自动添加到源目录列表
4. 选择目标目录并开始处理

### 场景 2: 从多个 USB 驱动器批量导入
1. 连接多个 USB 驱动器
2. 启动 MediaCopyer
3. 所有驱动器自动添加到源目录列表
4. 一次性处理所有设备的文件

### 场景 3: 从手机导入照片
1. 通过 USB 连接手机
2. 启动 MediaCopyer
3. 手机存储自动添加到源目录列表
4. 选择要导入的照片和视频

---

## ⚠️ 注意事项 / Important Notes

1. **权限要求**: 确保应用有权限访问外置存储设备
2. **设备挂载**: 设备必须正确挂载才能被检测到
3. **手动管理**: 可以随时添加或移除源目录
4. **跨平台差异**: 不同操作系统的检测行为略有不同

---

## 🔮 未来计划 / Future Plans

- [ ] 添加设备过滤配置选项
- [ ] 支持自定义排除规则
- [ ] 显示设备图标和类型
- [ ] 设备热插拔实时检测
- [ ] 设备使用历史记录

---

## 📝 版本信息 / Version Information

- **版本号 / Version**: 1.2.0
- **发布日期 / Release Date**: 2025-01-XX
- **兼容性 / Compatibility**: macOS 10.13+, Windows 10+, Linux (Ubuntu 18.04+)

---

## 🙏 致谢 / Acknowledgments

感谢所有用户的反馈和建议，这个功能的开发受到了社区需求的启发。

Thank you to all users for their feedback and suggestions. This feature was inspired by community needs.

---

## 📞 反馈 / Feedback

如有问题或建议，请访问：
- GitHub Issues: https://github.com/lee-tian/MediaCopyer/issues
- 文档: https://github.com/lee-tian/MediaCopyer/tree/main/docs

For questions or suggestions, please visit:
- GitHub Issues: https://github.com/lee-tian/MediaCopyer/issues
- Documentation: https://github.com/lee-tian/MediaCopyer/tree/main/docs
