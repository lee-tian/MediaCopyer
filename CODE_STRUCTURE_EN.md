# MediaCopyer Code Structure Documentation

## Project Overview

MediaCopyer is a media file organization tool that automatically organizes photos and videos by date or device type. The project follows a modular design, supports both graphical and command-line interfaces, and provides internationalization support.

## Directory Structure

```
MediaCopyer/
├── core/                    # Core functionality modules
│   ├── __init__.py         # Core module entry point, exports main features
│   ├── metadata/           # Metadata processing module
│   ├── device/             # Device identification module
│   ├── organizer/          # File organization module
│   └── utils/              # Utility functions module
├── gui/                    # Graphical User Interface module
│   ├── __init__.py         # GUI module entry point
│   ├── main_window.py      # Main window interface
│   ├── options_frame.py    # Options configuration interface
│   ├── processor.py        # File processing logic
│   ├── widgets.py          # Custom widgets
│   ├── styles.py           # Interface style definitions
│   ├── i18n.py            # Internationalization support
│   └── locales/           # Language pack directory
├── installer/              # Installer related files
├── resources/             # Resource files directory
├── build/                 # Build output directory
└── dist/                  # Distribution files directory
```

## Core Modules (core/)

### `core/__init__.py`
- **Function**: Unified entry point for the core module
- **Purpose**: Exports key functionalities from all submodules, providing a unified API interface
- **Main Exports**:
  - Metadata processing functions (`get_file_type`, `get_file_date`, `get_creation_date_from_exif`)
  - Device identification functions (`get_device_name`, `get_device_from_exif`)
  - File organization functions (`scan_directory`, `organize_file`, `organize_media_files`)
  - Utility functions (`validate_directory`, `format_file_size`, `safe_filename`)
  - Supported file extension constants (`PHOTO_EXTENSIONS`, `VIDEO_EXTENSIONS`)

### `core/metadata/`
- **Function**: Handles metadata information from media files
- **Main Features**:
  - Extract shooting date from photo EXIF data
  - Get creation time from video files
  - Identify file types (photo/video)
  - Support various RAW formats and standard formats

### `core/device/`
- **Function**: Identifies the source device of media files
- **Main Features**:
  - Extract device information from EXIF data
  - Get device names from video metadata
  - Infer device types based on filename patterns
  - Normalize device names

### `core/organizer/`
- **Function**: Core logic for file organization and management

#### `core/organizer/__init__.py`
- Exports main functionalities of the organizer module

#### `core/organizer/media_organizer.py`
- **Function**: Main logic for media file organization
- **Main Features**:
  - Organize files by date or device type
  - Generate target directory structure
  - Handle duplicate filenames
  - File copy and move operations

#### `core/organizer/scanner.py`
- **Function**: Directory scanning and file discovery
- **Main Features**:
  - Recursively scan source directories
  - Filter media files
  - Exclude hidden and system files
  - Generate file statistics

#### `core/organizer/file_operations.py`
- **Function**: File operation related functionalities
- **Main Features**:
  - Safe file copying and moving
  - File integrity verification
  - Error handling and recovery
  - Progress reporting

#### `core/organizer/hash_utils.py`
- **Function**: File hashing and duplicate detection
- **Main Features**:
  - Calculate file MD5/SHA256 hashes
  - Detect duplicate files
  - File integrity verification

### `core/utils/`
- **Function**: General utility functions

#### `core/utils/__init__.py`
- Exports utility module functionalities

#### `core/utils/filesystem.py`
- **Function**: File system related tools
- **Main Features**:
  - Directory validation and creation
  - Disk space checking
  - File size formatting
  - Path processing and normalization

#### `core/utils/string_utils.py`
- **Function**: String processing tools
- **Main Features**:
  - Safe filename generation
  - Character encoding handling
  - Path string processing

## Graphical User Interface Module (gui/)

### `gui/__init__.py`
- **Function**: GUI module entry point
- **Purpose**: Exports main GUI components and application classes

### `gui/main_window.py`
- **Function**: Main window interface implementation
- **Main Features**:
  - Create main application window
  - Set up window layout and controls
  - Handle user interaction events
  - Integrate various functional modules

### `gui/options_frame.py`
- **Function**: Options configuration interface
- **Main Features**:
  - Organization method selection (by date/by device)
  - Source and destination directory selection
  - Advanced options configuration
  - Settings saving and loading

### `gui/processor.py`
- **Function**: File processing background logic
- **Main Features**:
  - Background file processing tasks
  - Progress updates and status reporting
  - Error handling and user notifications
  - Thread-safe GUI updates

### `gui/widgets.py`
- **Function**: Custom GUI widgets
- **Main Features**:
  - Progress display widgets
  - File selection widgets
  - Status display components
  - Reusable UI elements

### `gui/styles.py`
- **Function**: GUI styles and theme definitions
- **Main Features**:
  - Color scheme definitions
  - Font and size settings
  - Widget style configurations
  - Responsive layout styles

### `gui/i18n.py`
- **Function**: Internationalization support
- **Main Features**:
  - Language switching management
  - Text localization
  - Regional settings handling
  - Dynamic language loading

### `gui/locales/`
- **Function**: Language pack directory

#### `gui/locales/zh_CN.py`
- **Function**: Simplified Chinese language pack
- **Content**: Chinese translations of all interface text

#### `gui/locales/en_US.py`
- **Function**: English language pack
- **Content**: English versions of all interface text

## Main Program Files

### `media_copyer_gui.py`
- **Function**: Main entry program for GUI version
- **Purpose**: Launch graphical interface application
- **Features**: Clean entry point, imports and starts GUI application

### `media_copyer.py`
- **Function**: Main program for command-line version
- **Purpose**: Provide command-line interface for media file organization
- **Features**: Support scripting and batch processing operations

## Build and Distribution

### `build_app.py`
- **Function**: Application build script
- **Purpose**: Build executable files using PyInstaller
- **Supported Platforms**: macOS, Windows, Linux

### `build_all.py`
- **Function**: Multi-platform build script
- **Purpose**: Automated building for multiple platform versions

### `media_copyer.spec`
- **Function**: PyInstaller configuration file
- **Purpose**: Define build parameters and dependencies

### `create_ico.py`
- **Function**: Icon generation script
- **Purpose**: Generate required icon formats for all platforms from PNG files

### `installer/`
- **Function**: Installer related files

#### `installer/build_installer.py`
- **Function**: Build installer
- **Purpose**: Create user-friendly installation packages

#### `installer/run_installer.py`
- **Function**: Installer execution script
- **Purpose**: Handle installation process and file deployment

## Resource Files

### `resources/`
- **Function**: Application resource directory

#### `resources/icon.png`
- **Function**: Main icon file
- **Usage**: Source file for application icon

#### `resources/MediaCopyer.icns`
- **Function**: macOS icon file
- **Usage**: macOS application icon

#### `resources/MediaCopyer.ico`
- **Function**: Windows icon file
- **Usage**: Windows application icon

#### `resources/MediaCopyer.iconset/`
- **Function**: macOS icon set directory
- **Content**: Icon files of various resolutions

## Configuration and Documentation

### `requirements.txt`
- **Function**: Python dependencies list
- **Content**: Required third-party libraries and version requirements

### `README.md`
- **Function**: Project documentation
- **Content**: Project introduction, installation instructions, usage methods

### `requirement.md`
- **Function**: Requirements documentation
- **Content**: Project functional requirements and technical requirements

### `.gitignore`
- **Function**: Git ignore file configuration
- **Content**: Specifies files and directories not under version control

## Testing and Tools

### `test_multi_source.py`
- **Function**: Multi-source testing script
- **Purpose**: Test multi-source directory processing functionality

### `fast_launcher.py`
- **Function**: Quick launcher script
- **Purpose**: Provide quick way to launch the application

### `run_media_copyer.sh`
- **Function**: Unix/Linux startup script
- **Purpose**: Shell script for program launcher

### `MULTI_SOURCE_CHANGES.md`
- **Function**: Multi-source feature changes documentation
- **Content**: Records development changes for multi-source support functionality

## Technical Features

### Core Functionality
- **File Organization**: Automatically organize media files by date or device type
- **Metadata Extraction**: Extract information from EXIF and video metadata
- **Device Recognition**: Intelligently identify file source devices
- **Duplicate Detection**: Hash-based duplicate file detection
- **Batch Processing**: Support batch organization of large numbers of files

### User Interface
- **Graphical Interface**: Modern GUI based on Tkinter
- **Internationalization**: Support Chinese and English interfaces
- **Progress Display**: Real-time processing progress and status feedback
- **Configuration Management**: Flexible option configuration and saving

### Cross-Platform Support
- **Multi-Platform**: Support Windows, macOS, Linux
- **Packaging Distribution**: Provide standalone executable files
- **Installer**: User-friendly installation experience

This project demonstrates good modular design, clear separation of responsibilities, and complete software development lifecycle support, from development to testing to distribution with corresponding tools and scripts.
