# MediaCopyer 项目结构概览

## 📁 项目目录结构

```
MediaCopyer/
├── 📁 core/                    # 核心功能模块
│   ├── __init__.py            # 核心模块入口
│   ├── config.py              # 配置管理
│   ├── 📁 device/             # 设备识别模块
│   ├── 📁 metadata/           # 元数据处理模块
│   ├── 📁 organizer/          # 文件组织模块
│   └── 📁 utils/              # 工具函数模块
├── 📁 gui/                     # 图形界面模块
│   ├── __init__.py            # GUI模块入口
│   ├── main_window.py         # 主窗口
│   ├── options_frame.py       # 选项配置
│   ├── processor.py           # 文件处理逻辑
│   ├── widgets.py             # 自定义控件
│   ├── styles.py              # 界面样式
│   ├── i18n.py               # 国际化支持
│   └── 📁 locales/           # 语言包目录
├── 📁 scripts/                 # 脚本工具目录 ✨
│   ├── 📁 build/              # 构建脚本
│   │   └── build_app.py       # 应用构建脚本
│   ├── 📁 release/            # 发布脚本
│   │   ├── release.py         # 主发布脚本
│   │   ├── auto_release.py    # 自动发布脚本
│   │   └── quick_release.py   # 快速发布脚本
│   ├── 📁 debug/              # 调试脚本
│   │   ├── debug_release.py   # 发布调试脚本
│   │   ├── simple_debug.py    # 简单调试脚本
│   │   └── test_release.py    # 发布测试脚本
│   ├── 📁 utils/              # 工具脚本
│   │   ├── update_version.py  # 版本更新脚本
│   │   ├── make.py           # Make工具脚本
│   │   └── build_and_release.py # 一键构建发布脚本
│   └── 📁 platform/           # 平台脚本
│       ├── release.sh         # Unix/macOS发布脚本
│       ├── release.bat        # Windows发布脚本
│       └── run_media_copyer.sh # 运行脚本
├── 📁 config/                  # 配置文件目录 ✨
│   ├── media_copyer.spec      # PyInstaller配置
│   └── installer.spec         # 安装程序配置
├── 📁 docs/                    # 文档目录 ✨
│   ├── CODE_STRUCTURE.md      # 代码结构文档
│   ├── CODE_STRUCTURE_EN.md   # 英文代码结构文档
│   ├── DUPLICATE_HANDLING.md  # 重复文件处理文档
│   ├── RELEASE_GUIDE.md       # 发布指南
│   ├── VERSION_MANAGEMENT.md  # 版本管理文档
│   └── requirement.md         # 需求文档
├── 📁 tools/                   # 开发工具目录 ✨
│   └── create_ico.py          # 图标创建工具
├── 📁 resources/               # 资源文件目录
│   ├── icon.png               # 主图标文件
│   ├── MediaCopyer.icns       # macOS图标
│   └── MediaCopyer.ico        # Windows图标
├── 📁 tests/                   # 测试目录
├── 📁 build/                   # 构建输出目录
├── 📁 dist/                    # 分发目录
├── 📁 venv/                    # 虚拟环境
├── 📁 release-v*/              # 发布版本目录
├── 📄 media_copyer.py          # CLI入口程序
├── 📄 media_copyer_gui.py      # GUI入口程序
├── 📄 version.py               # 版本信息
├── 📄 requirements.txt         # 依赖列表
├── 📄 README.md                # 项目说明
├── 📄 build.py                 # 构建快捷脚本 ✨
├── 📄 release.py               # 发布快捷脚本 ✨
├── 📄 REFACTOR_SUMMARY.md      # 重构总结 ✨
├── 📄 PROJECT_STRUCTURE.md     # 本文档 ✨
├── 📄 .gitignore               # Git忽略配置
└── 📄 *.dmg                    # macOS安装包
```

## 🎯 主要功能模块

### 核心功能 (core/)
- **元数据处理**: 提取照片EXIF和视频元数据
- **设备识别**: 智能识别文件来源设备
- **文件组织**: 按日期或设备类型组织文件
- **工具函数**: 文件系统操作、字符串处理等

### 图形界面 (gui/)
- **主窗口**: 用户友好的图形界面
- **国际化**: 支持中英文界面
- **进度显示**: 实时处理进度反馈
- **配置管理**: 灵活的选项设置

### 脚本工具 (scripts/)
- **构建脚本**: 自动化应用程序构建
- **发布脚本**: 版本发布和GitHub集成
- **调试工具**: 发布过程调试和测试
- **工具脚本**: 版本管理、Make工具等
- **平台脚本**: 跨平台兼容脚本

## 🚀 快速开始

### 开发环境设置
```bash
# 克隆项目
git clone <repository-url>
cd MediaCopyer

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 运行应用
```bash
# GUI版本
python media_copyer_gui.py

# 命令行版本
python media_copyer.py source_dir dest_dir
```

### 构建应用
```bash
# 使用快捷脚本
python build.py

# 或使用完整路径
python scripts/build/build_app.py
```

### 发布新版本
```bash
# 使用快捷脚本
python release.py

# 或使用完整路径
python scripts/release/release.py

# 自动发布（无交互）
python scripts/release/auto_release.py
```

## 📋 开发工作流

### 版本管理
1. 更新版本号：`python scripts/utils/update_version.py 1.2.0 "新功能"`
2. 构建应用：`python scripts/build/build_app.py`
3. 发布版本：`python scripts/release/release.py`

### 调试工具
- 发布调试：`python scripts/debug/debug_release.py`
- 简单调试：`python scripts/debug/simple_debug.py`
- 发布测试：`python scripts/debug/test_release.py`

### 平台脚本
```bash
# macOS/Linux
./scripts/platform/release.sh build
./scripts/platform/release.sh patch "修复bug"

# Windows
scripts\platform\release.bat build
scripts\platform\release.bat patch "修复bug"
```

## 📚 文档资源

- **[代码结构文档](docs/CODE_STRUCTURE.md)**: 详细的代码架构说明
- **[发布指南](docs/RELEASE_GUIDE.md)**: 完整的发布流程指南
- **[版本管理](docs/VERSION_MANAGEMENT.md)**: 版本管理系统说明
- **[重复文件处理](docs/DUPLICATE_HANDLING.md)**: 重复文件处理功能说明
- **[需求文档](docs/requirement.md)**: 项目功能需求

## 🔧 配置文件

- **[PyInstaller配置](config/media_copyer.spec)**: 应用程序打包配置
- **[安装程序配置](config/installer.spec)**: 安装程序构建配置

## 🛠️ 开发工具

- **[图标创建工具](tools/create_ico.py)**: PNG转ICO图标工具

## ✨ 重构亮点

1. **清晰的目录结构**: 按功能分类，易于维护
2. **完整的脚本工具链**: 从开发到发布的全流程自动化
3. **向后兼容性**: 保留根目录快捷脚本
4. **文档完善**: 详细的使用指南和技术文档
5. **跨平台支持**: 支持Windows、macOS、Linux

这个项目结构为MediaCopyer提供了良好的可维护性和可扩展性基础，支持高效的开发和发布流程。