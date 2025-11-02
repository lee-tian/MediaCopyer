# MediaCopyer

A Python application to automatically organize photos and videos by their creation date into a structured directory hierarchy. Available as both a command-line tool and a GUI application with internationalization support.

## ✨ Features

- **🗓️ Automatic Date Detection**: Uses EXIF data for photos and metadata for videos
- **📁 Smart Organization**: Creates organized directory structures by date, device, or file type
- **🔄 Flexible Operations**: Copy or move files with duplicate handling
- **🎯 Multiple Organization Modes**: By date, device, date+device, or file extension
- **🚫 Ignore Duplicates**: Option to skip duplicate files entirely
- **📊 Enhanced Analysis**: Detailed before/after copy operation statistics
- **🖥️ GUI Interface**: User-friendly interface with progress tracking
- **🌍 Internationalization**: English and Chinese language support
- **🔒 Safe Processing**: Dry-run mode and MD5 verification

## 📥 Quick Start

### Download Pre-built Application
**[📥 Download Latest Release](https://github.com/lee-tian/MediaCopyer/releases/latest)**

### Run from Source
```bash
git clone https://github.com/lee-tian/MediaCopyer.git
cd MediaCopyer
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python media_copyer_gui.py
```

## 🚀 Usage

### GUI Application (Recommended)
```bash
python media_copyer_gui.py
```

### Command Line
```bash
python media_copyer.py SOURCE_DIR DESTINATION_DIR [--move] [--dry-run]
```

## 📂 Output Structure

```
destination/
├── Picture/
│   ├── 2024-01-15/
│   │   ├── IMG_001.jpg
│   │   └── photo.heic
│   └── duplicate/          # When duplicates are organized
│       └── 2024-01-15/
└── Video/
    ├── 2024-06-15/
    │   └── birthday.mp4
    └── DJI/                # When organized by device
        └── 2024-07-04/
```

## 🎛️ Organization Modes

1. **By Date**: `Picture/2024-01-15/`
2. **By Device**: `Picture/DJI/`, `Video/iPhone/`
3. **By Date+Device**: `Picture/2024-01-15/DJI/`
4. **By Extension**: `JPG/`, `MP4/`, `PNG/`

## 📋 Supported Formats

**Photos**: JPG, PNG, HEIC, TIFF, ARW, CR2, NEF, DNG  
**Videos**: MP4, MOV, AVI, MKV, WMV, FLV, WebM, M4V

## 🔧 Development & Release

### Quick Release Commands

**一键发布 (推荐):**
```bash
# 全自动发布到GitHub Releases (无交互，推荐)
python scripts/release/auto_release.py

# 交互式发布 (需要GitHub CLI)
python scripts/release/quick_release.py

# 仅构建不发布
python scripts/release/quick_release.py --build-only
```

**传统发布方式:**
```bash
# 完整发布流程
python scripts/release/release.py

# 版本更新
python scripts/utils/update_version.py 1.2.0 "新功能" "修复bug"

# 仅构建
python scripts/build/build_app.py
```

**平台脚本:**
```bash
# macOS/Linux
chmod +x scripts/platform/release.sh
./scripts/platform/release.sh patch "Fix bug"      # 1.0.0 → 1.0.1
./scripts/platform/release.sh minor "New feature"  # 1.0.0 → 1.1.0

# Windows
scripts\platform\release.bat patch "Fix bug"
```

### Manual Version Update
```bash
python scripts/utils/update_version.py 1.2.0 "Add ignore duplicates" "Enhanced analysis"
```

### Development Setup
```bash
git clone <repository-url>
cd MediaCopyer
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install pylint black pytest  # Optional dev tools
```

## 🏗️ Project Structure

```
MediaCopyer/
├── core/                    # Core business logic
│   ├── organizer/          # File organization
│   ├── utils/              # Utilities
│   ├── metadata/           # Metadata extraction
│   └── device/             # Device detection
├── gui/                    # GUI application
│   ├── locales/           # Language files
│   └── *.py               # GUI components
├── scripts/                # Build and release scripts
│   ├── build/             # Build scripts
│   ├── release/           # Release scripts
│   ├── debug/             # Debug scripts
│   ├── utils/             # Utility scripts
│   └── platform/          # Platform scripts
├── config/                 # Configuration files
├── docs/                   # Documentation
├── tools/                  # Development tools
├── media_copyer.py         # CLI entry point
└── media_copyer_gui.py     # GUI entry point
```

## 🧪 Testing

```bash
# Test CLI
python media_copyer.py test_source test_dest --dry-run

# Test GUI
python media_copyer_gui.py

# Run specific tests
python tests/test_i18n_logs.py

# Debug release process
python scripts/debug/debug_release.py
```

## 📦 Requirements

- Python 3.6+
- Pillow (EXIF data)
- tkinter (GUI)
- ffmpeg (optional, enhanced video metadata)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Make changes and test
4. Commit: `git commit -m "Description"`
5. Push: `git push origin feature-name`
6. Create Pull Request

## 📄 License

[Add your license here]

---

**Latest Version**: v1.1.0 - Added ignore duplicates option and enhanced copy analysis