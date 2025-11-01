# MediaCopyer 版本管理系统

## 概述

MediaCopyer 现在具有完整的版本管理系统，支持自动化构建和发布流程。

## 主要功能

### ✅ 版本号管理
- 集中式版本配置 (`version.py`)
- 语义化版本号 (1.0.0)
- 自动构建号生成
- 版本历史记录

### ✅ 自动化构建
- 带版本号的应用包 (`MediaCopyer-v1.0.0.app`)
- 带版本号的安装包 (`MediaCopyer-v1.0.0.dmg`)
- 自动化DMG创建，包含拖拽安装界面
- 虚拟环境支持

### ✅ 发布管理
- 自动Git标签创建
- 发布资源准备
- GitHub Actions集成
- 发布说明生成

### ✅ 用户体验
- 应用标题显示版本号
- README中的下载链接
- 清晰的安装说明

## 文件结构

```
MediaCopyer/
├── version.py                 # 版本信息配置
├── build_app.py              # 构建脚本 (已更新)
├── release.py                # 发布脚本 (新增)
├── update_version.py         # 版本更新脚本 (新增)
├── RELEASE_GUIDE.md          # 发布指南 (新增)
├── VERSION_MANAGEMENT.md     # 本文档 (新增)
├── .github/workflows/
│   └── release.yml           # GitHub Actions (新增)
├── gui/main_window.py        # GUI主窗口 (已更新)
├── media_copyer_gui.py       # GUI入口 (已更新)
├── README.md                 # 项目说明 (已更新)
└── requirements.txt          # 依赖列表 (已更新)
```

## 使用方法

### 开发者发布新版本

1. **更新版本号**:
   ```bash
   python update_version.py 1.1.0 "新功能描述" "Bug修复描述"
   ```

2. **自动发布**:
   ```bash
   python release.py
   ```

3. **在GitHub完成发布**:
   - 访问 GitHub Releases
   - 编辑新标签
   - 上传DMG文件
   - 发布Release

### 用户下载使用

1. **访问GitHub Releases页面**
2. **下载最新的DMG文件** (`MediaCopyer-v1.0.0.dmg`)
3. **安装应用**:
   - 双击DMG文件
   - 拖拽应用到Applications文件夹
   - 运行MediaCopyer

## 技术实现

### 版本信息集中管理
```python
# version.py
__version__ = "1.0.0"
__build__ = "20241101"

def get_app_name():
    return f"MediaCopyer v{__version__}"
```

### 构建脚本集成
- 自动使用版本号命名文件
- DMG卷标包含版本信息
- 应用包重命名为带版本号格式

### GUI集成
- 窗口标题显示版本号
- 从version.py导入版本信息

### GitHub Actions
- 标签推送时自动构建
- 自动创建Release
- 上传构建产物

## 优势

1. **一致性**: 所有地方的版本号都来自同一个源
2. **自动化**: 减少手动操作，降低出错概率
3. **可追溯**: 完整的版本历史和变更记录
4. **用户友好**: 清晰的版本标识和下载流程
5. **开发效率**: 简化发布流程，专注于开发

## 下一步计划

- [ ] 添加Windows构建支持
- [ ] 添加Linux构建支持
- [ ] 自动更新检查功能
- [ ] 更详细的发布说明模板
- [ ] 自动化测试集成

## 当前状态

✅ **已完成**: macOS版本管理和发布系统
🚀 **可用**: 完整的发布流程
📦 **产出**: `MediaCopyer-v1.0.0.dmg` 安装包