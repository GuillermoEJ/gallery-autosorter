#!/usr/bin/env python3
"""Debug script to display detected dates for all images in a folder."""
import os
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS

try:
    import piexif
    HAS_PIEXIF = True
except ImportError:
    HAS_PIEXIF = False

IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')

def get_image_date(file):
    """Extract image date from EXIF metadata.
    
    Returns:
        tuple: (datetime, source_string) indicating the extraction method used
    """
    # Método 1: Usar piexif si está disponible
    if HAS_PIEXIF:
        try:
            exif_dict = piexif.load(file)
            
            for tag_id, value in exif_dict.get("0th", {}).items():
                tag_name = piexif.TAGS["0th"][tag_id]["name"]
                if tag_name == "DateTime":
                    try:
                        date_str = value.decode('utf-8')
                        return datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S'), "EXIF (DateTime)"
                    except:
                        pass
            
            for tag_id, value in exif_dict.get("Exif", {}).items():
                tag_name = piexif.TAGS["Exif"][tag_id]["name"]
                if tag_name in ["DateTimeOriginal", "DateTimeDigitized"]:
                    try:
                        date_str = value.decode('utf-8')
                        return datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S'), f"EXIF ({tag_name})"
                    except Exception:
                        pass
        except Exception:
            pass
    
    # Method 2: Use PIL
    try:
        image = Image.open(file)
        exif_data = image._getexif()
        
        if exif_data:
            date_tags = ['DateTimeOriginal', 'DateTime', 'DateTimeDigitized']
            
            for tag_id, value in exif_data.items():
                tag = TAGS.get(tag_id, tag_id)
                if tag in date_tags and value:
                    try:
                        return datetime.strptime(value, '%Y:%m:%d %H:%M:%S'), f"PIL ({tag})"
                    except (ValueError, TypeError):
                        continue
    except Exception:
        pass
    
    # Method 3: Fallback - use modification time
    try:
        modification_time = os.path.getmtime(file)
        return datetime.fromtimestamp(modification_time), "MODIFICATION"
    except Exception:
        return datetime.now(), "CURRENT"

if __name__ == "__main__":
    import tkinter as tk
    from tkinter import filedialog
    
    # Open dialog to select folder
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    
    folder = filedialog.askdirectory(title="Select folder with images")
    root.destroy()
    
    if not folder:
        print("No folder selected")
        exit()
    
    print(f"\n{'='*100}")
    print(f"Analyzing images in: {folder}")
    print(f"{'='*100}\n")
    print(f"{'File':<50} {'Detected Date':<20} {'Source':<30}")
    print(f"{'-'*100}\n")
    
    images = []
    for filename in sorted(os.listdir(folder)):
        if not filename.lower().endswith(IMAGE_EXTENSIONS):
            continue
        
        filepath = os.path.join(folder, filename)
        if os.path.isdir(filepath):
            continue
        
        date, origin = get_image_date(filepath)
        date_str = date.strftime('%d/%m/%Y %H:%M:%S')
        
        print(f"{filename:<50} {date_str:<20} {origin:<30}")
        images.append((filename, date, origin))
    
    print(f"\n{'='*100}")
    print(f"Total: {len(images)} images\n")
    
    # Group by date
    from collections import defaultdict
    by_date = defaultdict(list)
    for filename, date, origin in images:
        date_key = date.strftime('%d/%m/%Y')
        by_date[date_key].append(filename)
    
    print("Summary by date:")
    for date_key in sorted(by_date.keys()):
        print(f"  {date_key}: {len(by_date[date_key])} images")
