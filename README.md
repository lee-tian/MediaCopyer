# Media Copyer

A Python application to automatically organize photos and videos by their creation date into a structured directory hierarchy. Available as both a command-line tool and a GUI application with internationalization support.

## Features

- **Automatic Date Detection**: Uses EXIF data for photos and metadata for videos to determine creation dates
- **Fallback Support**: Uses file modification time when metadata is unavailable
- **Organized Structure**: Creates `Picture/YYYY/YYYY-MM-DD/` and `Video/YYYY/YYYY-MM-DD/` directory structures
- **Flexible Operation**: Supports both copy and move modes
- **Safe Processing**: Automatically handles duplicate filenames and provides dry-run mode
- **Wide Format Support**: Handles common photo formats (JPG, PNG, ARW, HEIC, etc.) and video formats (MP4, MOV, AVI, etc.)
- **GUI Interface**: User-friendly graphical interface with progress tracking
- **Internationalization**: Supports multiple languages (English and Chinese)
- **Modular Architecture**: Clean, maintainable code structure for easy development

## Download

### Pre-built Applications (Recommended)

Download the latest version from GitHub Releases:

**[📥 Download Latest Release](https://github.com/YOUR_USERNAME/MediaCopyer/releases/latest)**

- **macOS**: Download `MediaCopyer-v1.0.0.dmg`
- **Windows**: Download `MediaCopyer-v1.0.0.exe` (coming soon)
- **Linux**: Download `MediaCopyer-v1.0.0.AppImage` (coming soon)

> **Note**: Replace `YOUR_USERNAME` with your actual GitHub username in the download links.

### Installation from Source

#### For Users

1. Clone or download this repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/MediaCopyer.git
   cd MediaCopyer
   ```

2. Create and activate virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. **Optional**: Install ffmpeg for enhanced video metadata support:
   - macOS: `brew install ffmpeg`
   - Ubuntu/Debian: `sudo apt install ffmpeg`
   - Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html)

### For Developers

1. Clone the repository and set up a virtual environment:
   ```bash
   git clone <repository-url>
   cd MediaCopyer
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install development tools (optional):
   ```bash
   pip install pylint black pytest
   ```

## Usage

### GUI Application (Recommended)

Run the graphical interface:
```bash
python media_copyer_gui.py
```

The GUI provides:
- Easy source and destination folder selection
- Real-time progress tracking
- Language selection (English/Chinese)
- Dry-run mode for testing
- Copy/Move operation selection

### Command Line Interface

For automation or script usage:

```bash
python media_copyer.py SOURCE_DIR DESTINATION_DIR [OPTIONS]
```

#### Command Line Options

- `--move`: Move files instead of copying them
- `--dry-run`: Preview what would be done without actually moving/copying files

#### Examples

1. **Copy files** from source to destination:
   ```bash
   python media_copyer.py /path/to/source /path/to/destination
   ```

2. **Move files** (organize in place):
   ```bash
   python media_copyer.py /path/to/source /path/to/destination --move
   ```

3. **Preview operations** without making changes:
   ```bash
   python media_copyer.py /path/to/source /path/to/destination --dry-run
   ```

## Output Structure

The script organizes files into the following structure:

```
destination/
├── Picture/
│   ├── 2023/
│   │   ├── 2023-01-15/
│   │   │   ├── IMG_001.jpg
│   │   │   └── photo.heic
│   │   └── 2023-02-20/
│   │       └── vacation.png
│   └── 2024/
│       └── 2024-03-10/
│           └── family.jpg
└── Video/
    ├── 2023/
    │   └── 2023-06-15/
    │       └── birthday.mp4
    └── 2024/
        └── 2024-07-04/
            └── fireworks.mov
```

## Supported File Formats

### Photos
- JPEG (.jpg, .jpeg)
- PNG (.png)
- TIFF (.tiff, .tif)
- HEIC (.heic)
- Sony RAW (.arw)
- Canon RAW (.cr2)
- Nikon RAW (.nef)
- Adobe DNG (.dng)

### Videos
- MP4 (.mp4)
- QuickTime (.mov)
- AVI (.avi)
- Matroska (.mkv)
- Windows Media (.wmv)
- Flash Video (.flv)
- WebM (.webm)
- iTunes Video (.m4v)

## Project Structure

```
MediaCopyer/
├── core/                          # Core business logic
│   ├── organizer/                 # Media organization functionality
│   │   ├── media_organizer.py     # Main organizer class
│   │   ├── scanner.py             # File scanning
│   │   ├── file_operations.py     # File copy/move operations
│   │   └── hash_utils.py          # File deduplication
│   ├── utils/                     # Utility modules
│   │   ├── filesystem.py          # File system operations
│   │   └── string_utils.py        # String manipulation
│   ├── metadata/                  # Metadata extraction (future)
│   └── device/                    # Device detection (future)
├── gui/                           # GUI application
│   ├── main_window.py             # Main application window
│   ├── widgets.py                 # Custom UI widgets
│   ├── processor.py               # Background processing
│   ├── options_frame.py           # Options configuration
│   ├── i18n.py                    # Internationalization
│   └── locales/                   # Language files
│       ├── en_US.py               # English translations
│       └── zh_CN.py               # Chinese translations
├── media_copyer.py                # Command-line entry point
├── media_copyer_gui.py            # GUI entry point
└── requirements.txt               # Python dependencies
```

## Development

### Running Tests

Currently, the project uses manual testing. To test functionality:

1. **Test CLI version**:
   ```bash
   python media_copyer.py test_source test_dest --dry-run
   ```

2. **Test GUI version**:
   ```bash
   python media_copyer_gui.py
   ```

### Code Style

The project follows Python PEP 8 conventions. Use `black` for code formatting:
```bash
black .
```

### Adding New Features

1. **Core functionality**: Add to appropriate modules in `core/`
2. **GUI features**: Extend classes in `gui/`
3. **Internationalization**: Add translations to `gui/locales/`

### Architecture

- **Modular Design**: Separates core logic from GUI
- **Event-Driven GUI**: Uses threading for non-blocking operations  
- **Extensible**: Easy to add new file types or organization patterns
- **I18n Ready**: Built-in support for multiple languages

## Requirements

- Python 3.6+
- Pillow (for EXIF data reading)
- tkinter (for GUI, usually included with Python)
- ffmpeg (optional, for enhanced video metadata)

## Error Handling

- Files with unreadable metadata fall back to modification time
- Duplicate filenames are automatically renamed (e.g., `photo_1.jpg`)
- Processing errors are logged but don't stop the overall operation
- GUI provides real-time error reporting and progress updates
- Statistics are provided at the end of processing

## Release Management

### For Maintainers

#### Updating Version

1. Update version number and add changelog:
   ```bash
   python update_version.py 1.1.0 "Fixed duplicate file handling bug" "Added new file format support"
   ```

2. Build and release:
   ```bash
   python release.py
   ```

3. The release script will:
   - Build the application
   - Create Git tags
   - Prepare release assets
   - Push to GitHub

4. Complete the release on GitHub:
   - Go to GitHub Releases page
   - Edit the created tag
   - Upload the DMG file from `release-v{version}/` directory
   - Publish the release

#### Manual Build

To build the application manually:
```bash
# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Build application
python build_app.py
```

This will create:
- `dist/MediaCopyer.app` - macOS application bundle
- `MediaCopyer-v{version}.dmg` - macOS installer

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make changes and test thoroughly
4. Commit changes: `git commit -m "Description"`
5. Push to branch: `git push origin feature-name`
6. Create a Pull Request

## Notes

- The application preserves original file timestamps when copying
- EXIF data is prioritized for photos, video metadata for videos
- File modification time is used as fallback when metadata is unavailable
- The application recursively scans subdirectories in the source folder
- GUI version provides better user experience with progress tracking
- Both CLI and GUI versions use the same core processing engine
