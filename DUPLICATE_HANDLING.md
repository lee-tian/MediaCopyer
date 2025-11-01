# 重复文件处理功能 / Duplicate File Handling

## 功能说明 / Feature Description

MediaCopyer 现在支持自动检测和处理重复文件。当遇到重复的文件时，会将其移动到目标目录的 `duplicate` 文件夹中。

MediaCopyer now supports automatic detection and handling of duplicate files. When duplicate files are encountered, they will be moved to the `duplicate` folder in the destination directory.

## 目录结构 / Directory Structure

### 正常文件 / Normal Files
```
目标目录/
├── Picture/
│   ├── 2025-11-01/
│   │   ├── IMG_001.jpg
│   │   └── IMG_002.jpg
│   └── 2025-11-02/
│       └── IMG_003.jpg
└── Video/
    ├── 2025-11-01/
    │   └── VID_001.mp4
    └── 2025-11-02/
        └── VID_002.mp4
```

### 重复文件 / Duplicate Files
```
目标目录/
├── Picture/
│   ├── duplicate/
│   │   ├── 2025-11-01/
│   │   │   ├── IMG_001.jpg  (重复文件)
│   │   │   └── IMG_002.jpg  (重复文件)
│   │   └── 2025-11-02/
│   │       └── IMG_003.jpg  (重复文件)
│   ├── 2025-11-01/
│   │   ├── IMG_001.jpg      (原始文件)
│   │   └── IMG_002.jpg      (原始文件)
│   └── 2025-11-02/
│       └── IMG_003.jpg      (原始文件)
└── Video/
    ├── duplicate/
    │   ├── 2025-11-01/
    │   │   └── VID_001.mp4  (重复文件)
    │   └── 2025-11-02/
    │       └── VID_002.mp4  (重复文件)
    ├── 2025-11-01/
    │   └── VID_001.mp4      (原始文件)
    └── 2025-11-02/
        └── VID_002.mp4      (原始文件)
```

## 重复检测机制 / Duplicate Detection Mechanism

1. **文件名匹配** / **Filename Matching**: 首先检查目标位置是否已存在同名文件
2. **文件大小比较** / **File Size Comparison**: 快速比较文件大小
3. **MD5哈希验证** / **MD5 Hash Verification**: 计算并比较文件的MD5哈希值以确保内容完全相同

## 组织模式支持 / Organization Mode Support

重复文件处理支持所有组织模式：

Duplicate file handling supports all organization modes:

- **按日期** / **By Date**: `Picture/duplicate/2025-11-01/`
- **按设备** / **By Device**: `Picture/duplicate/DJI/`
- **按日期+设备** / **By Date+Device**: `Picture/duplicate/2025-11-01/DJI/`
- **按文件后缀** / **By Extension**: `JPG/duplicate/`

## 统计信息 / Statistics

处理完成后，日志会显示：
After processing, the log will show:

- 总照片数 / Total photos
- 总视频数 / Total videos
- **总重复文件数** / **Total duplicates** (新增)
- 总错误数 / Total errors
- 总处理数 / Total processed

## 注意事项 / Notes

1. 重复检测基于文件内容（MD5哈希），而不仅仅是文件名
2. 重复文件会保持原有的组织结构，只是放在 `duplicate` 子文件夹中
3. 这个功能在所有模式下都可用（复制模式、移动模式、试运行模式）
4. 重复文件检测会略微增加处理时间，因为需要计算MD5哈希

1. Duplicate detection is based on file content (MD5 hash), not just filename
2. Duplicate files maintain the original organization structure, just placed in the `duplicate` subfolder
3. This feature is available in all modes (copy mode, move mode, dry run mode)
4. Duplicate file detection will slightly increase processing time due to MD5 hash calculation