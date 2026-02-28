#!/usr/bin/env python3
"""Debug script to display EXIF metadata from image files."""

import os
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS

def debug_image_date(file):
    """Display all EXIF information from an image file.
    
    Args:
        file: Path to image file
    """
    print(f"\n{'='*70}")
    print(f"File: {file}")
    print(f"{'='*70}")
    
    try:
        image = Image.open(file)
        print(f"Format: {image.format}, Size: {image.size}")
        
        # Try to get EXIF data
        exif_data = image._getexif()
        
        if exif_data:
            print(f"\n✓ EXIF data found:\n")
            for tag_id, value in sorted(exif_data.items()):
                tag = TAGS.get(tag_id, tag_id)
                # Show only date/time tags
                if 'Date' in tag or 'Time' in tag:
                    print(f"  {tag}: {value}")
        else:
            print("\n✗ No EXIF data found")
        
        # Display file timestamps
        print(f"\nFile timestamps:")
        print(f"  Modified: {datetime.fromtimestamp(os.path.getmtime(file)).strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"  Created:  {datetime.fromtimestamp(os.path.getctime(file)).strftime('%d/%m/%Y %H:%M:%S')}")
        
    except Exception as e:
        print(f"✗ Error: {e}")


if __name__ == "__main__":
    import tkinter as tk
    from tkinter import filedialog
    
    # Open dialog to select an image file
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    
    file = filedialog.askopenfilename(
        title="Select an image to debug",
        filetypes=[("Images", "*.jpg *.jpeg *.png *.gif *.bmp *.tiff"), ("All", "*.*")]
    )
    
    root.destroy()
    
    if file:
        debug_image_date(file)
    else:
        print("No file selected")
