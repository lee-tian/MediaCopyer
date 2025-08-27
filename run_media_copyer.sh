#!/bin/bash
# MediaCopyer Launcher Script

echo "Starting MediaCopyer..."
echo "Location: $(pwd)/dist/MediaCopyer"
echo "File size: $(ls -lh dist/MediaCopyer | awk '{print $5}')"
echo ""

# Check if the executable exists
if [ ! -f "dist/MediaCopyer" ]; then
    echo "Error: MediaCopyer executable not found in dist/ folder"
    echo "Please run the build process first using: pyinstaller media_copyer.spec"
    exit 1
fi

# Make sure it's executable
chmod +x dist/MediaCopyer

# Run the application
./dist/MediaCopyer
