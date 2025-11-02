#!/usr/bin/env python3
"""
Convert PNG icon to ICO format for Windows applications
"""

from PIL import Image
import os

def create_ico_from_png(png_path, ico_path):
    """Convert PNG to ICO format with multiple sizes"""
    try:
        # Open the original PNG image
        with Image.open(png_path) as img:
            # Convert to RGBA if not already
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # ICO format typically includes these sizes
            sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
            
            # Create images for each size
            images = []
            for size in sizes:
                # Resize the image while maintaining aspect ratio
                resized = img.resize(size, Image.Resampling.LANCZOS)
                images.append(resized)
            
            # Save as ICO with multiple sizes
            img.save(ico_path, format='ICO', sizes=[(img.width, img.height) for img in images])
            print(f"Successfully created {ico_path}")
            
    except Exception as e:
        print(f"Error creating ICO file: {e}")

def main():
    # Paths
    png_path = "resources/icon.png"
    ico_path = "resources/MediaCopyer.ico"
    
    # Check if PNG exists
    if not os.path.exists(png_path):
        print(f"Error: {png_path} not found")
        return
    
    # Create ICO file
    print(f"Converting {png_path} to {ico_path}...")
    create_ico_from_png(png_path, ico_path)

if __name__ == "__main__":
    main()