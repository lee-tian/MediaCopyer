# Media Copyer

A Python script to automatically organize photos and videos by their creation date into a structured directory hierarchy.

## Features

- **Automatic Date Detection**: Uses EXIF data for photos and metadata for videos to determine creation dates
- **Fallback Support**: Uses file modification time when metadata is unavailable
- **Organized Structure**: Creates `Picture/YYYY/YYYY-MM-DD/` and `Video/YYYY/YYYY-MM-DD/` directory structures
- **Flexible Operation**: Supports both copy and move modes
- **Safe Processing**: Automatically handles duplicate filenames and provides dry-run mode
- **Wide Format Support**: Handles common photo formats (JPG, PNG, ARW, HEIC, etc.) and video formats (MP4, MOV, AVI, etc.)

## Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. **Optional**: Install ffmpeg for video metadata support:
   - macOS: `brew install ffmpeg`
   - Ubuntu/Debian: `sudo apt install ffmpeg`
   - Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html)

## Usage

### Basic Usage

```bash
python3 media_copyer.py SOURCE_DIR DESTINATION_DIR
```

### Command Line Options

- `--move`: Move files instead of copying them
- `--dry-run`: Preview what would be done without actually moving/copying files

### Examples

1. **Copy files** from source to destination:
   ```bash
   python3 media_copyer.py /path/to/source /path/to/destination
   ```

2. **Move files** (organize in place):
   ```bash
   python3 media_copyer.py /path/to/source /path/to/destination --move
   ```

3. **Preview operations** without making changes:
   ```bash
   python3 media_copyer.py /path/to/source /path/to/destination --dry-run
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

## Requirements

- Python 3.6+
- Pillow (for EXIF data reading)
- ffmpeg (optional, for video metadata)

## Error Handling

- Files with unreadable metadata fall back to modification time
- Duplicate filenames are automatically renamed (e.g., `photo_1.jpg`)
- Processing errors are logged but don't stop the overall operation
- Statistics are provided at the end of processing

## Notes

- The script preserves original file timestamps when copying
- EXIF data is prioritized for photos, video metadata for videos
- File modification time is used as fallback when metadata is unavailable
- The script recursively scans subdirectories in the source folder
