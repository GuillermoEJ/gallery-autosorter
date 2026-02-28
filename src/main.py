import os
import shutil
from datetime import datetime
from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS
import tkinter as tk
from tkinter import filedialog, simpledialog


try:
    import piexif
    HAS_PIEXIF = True
except ImportError:
    HAS_PIEXIF = False

IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')


def select_folder(title="Select a folder"):
    """Open a folder selection dialog.
    
    Args:
        title: Dialog title text
    
    Returns:
        str: Path to selected folder, or empty string if cancelled
    """
    root = tk.Tk()
    root.withdraw()  # Hide tkinter window
    root.attributes('-topmost', True)  # Bring dialog to foreground
        
    folder_path = filedialog.askdirectory(title=title)
    root.destroy()
    
    return folder_path


def select_folders():
    """Prompt user to select source and destination directories.
    
    Returns:
        tuple: (source_dir, dest_dir) paths, or (None, None) if cancelled
    """
    print("Opening dialog to select SOURCE folder...\n")
    source_dir = select_folder("Select SOURCE folder")
    
    if not source_dir:
        print("No source folder selected. Operation cancelled.")
        return None, None
    
    print(f"Source folder selected: {source_dir}\n")
    print("Opening dialog to select DESTINATION folder...\n")
    dest_dir = select_folder("Select DESTINATION folder")
    
    if not dest_dir:
        print("No destination folder selected. Operation cancelled.")
        return None, None
    
    print(f"Destination folder selected: {dest_dir}\n")
    return source_dir, dest_dir


def select_date_range():
    """Prompt user to select an optional date range for filtering images.
    
    Returns:
        tuple: (start_date, end_date) as datetime objects, or (None, None) if skipped
    """
    print("Do you want to specify a date range to copy only photos from that period?")
    response = input("(y/n): ").strip().lower()
    
    if response != 'y':
        return None, None
    
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    
    try:
        # Request start date
        start_date_str = simpledialog.askstring(
            "Start Date",
            "Enter start date (DD/MM/YYYY):\nExample: 01/01/2023"
        )
        
        if not start_date_str:
            print("Date selection cancelled.")
            return None, None
        
        # Request end date
        end_date_str = simpledialog.askstring(
            "End Date",
            "Enter end date (DD/MM/YYYY):\nExample: 31/12/2023"
        )
        
        if not end_date_str:
            print("Date selection cancelled.")
            return None, None
        
        start_date = datetime.strptime(start_date_str, '%d/%m/%Y')
        end_date = datetime.strptime(end_date_str, '%d/%m/%Y')
        print(f"\nDate range selected: {start_date_str} to {end_date_str}\n")
        return start_date, end_date
    except ValueError:
        print("Error: Dates must be in DD/MM/YYYY format")
        return None, None
    finally:
        root.destroy()


def get_image_date(file):
    """Extract image date from EXIF metadata using multiple fallback methods.
    
    Args:
        file: Path to image file
    
    Returns:
        datetime: Image date from EXIF, modification time, or current time as fallback
    """
    # Method 1: Use piexif if available
    if HAS_PIEXIF:
        try:
            exif_dict = piexif.load(file)
            
            # Search in IFD 0 (main image)
            for tag_id, value in exif_dict.get("0th", {}).items():
                tag_name = piexif.TAGS["0th"][tag_id]["name"]
                
                if tag_name == "DateTime":
                    try:
                        date_str = value.decode('utf-8')
                        return datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
                    except Exception:
                        pass
            
            # Search in IFD Exif
            for tag_id, value in exif_dict.get("Exif", {}).items():
                tag_name = piexif.TAGS["Exif"][tag_id]["name"]
                
                if tag_name in ["DateTimeOriginal", "DateTimeDigitized"]:
                    try:
                        date_str = value.decode('utf-8')
                        return datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
                    except Exception:
                        pass
        except Exception:
            pass  # Continue to next method
    
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
                        return datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
                    except (ValueError, TypeError):
                        continue
    except Exception:
        pass
    
    # Method 3: Fallback - use modification time (more reliable than creation time)
    try:
        modification_time = os.path.getmtime(file)
        return datetime.fromtimestamp(modification_time)
    except Exception:
        # Last resort: use current time
        return datetime.now()


def start():
    """Main function to orchestrate the photo copying and organization process."""
    source_dir, dest_dir = select_folders()
    
    if not source_dir or not dest_dir:
        return
    
    if not os.path.exists(source_dir):
        print(f"Error: Source folder does not exist: {source_dir}")
        return
    
    if not os.path.exists(dest_dir):
        print(f"Creating destination folder: {dest_dir}")
        os.makedirs(dest_dir)
    
    # Select optional date range
    start_date, end_date = select_date_range()
    
    confirmation = input("Do you want to continue? (y/n): ").strip().lower()
    if confirmation != 'y':
        print("Operation cancelled.")
        return
    
    total_copied = 0
    errors = 0
    skipped_by_date = 0

    print(f"\n{'='*60}")
    print("Starting copy process...")
    print(f"{'='*60}\n")

    for filename in os.listdir(source_dir):
        if not filename.lower().endswith(IMAGE_EXTENSIONS):
            continue  # Skip non-image files

        file = os.path.join(source_dir, filename)
        
        # Skip if it's a directory
        if os.path.isdir(file):
            continue
            
        try:
            date = get_image_date(file)
            date_str = date.strftime('%d/%m/%Y')
            
            # Validate date range if specified
            if start_date and end_date:
                if date < start_date or date > end_date:
                    skipped_by_date += 1
                    print(f"Skipped by date: {filename} ({date_str})")
                    continue
            
            # Get destination folder based on date
            final_loc = check_dir(date, dest_dir)
            dest_path = os.path.join(final_loc, filename)
            
            print(f"  {filename} ({date_str})", end="")
            
            if os.path.exists(dest_path):
                print(f" -> Already exists")
                continue  # Skip if already exists
            
            shutil.copy(file, dest_path)
            total_copied += 1
            print(f" -> Copied to {final_loc}")
            
        except Exception as e:
            errors += 1
            print(f" x Error with {filename}: {e}")

    print(f"\n{'='*60}")
    print(f"Total photos copied: {total_copied}")
    if start_date and end_date:
        print(f"Total photos skipped by date: {skipped_by_date}")
    print(f"Total errors: {errors}")
    print(f"{'='*60}")


def check_dir(date, dest_dir):
    """Create year and month subdirectories if they don't exist.
    
    Args:
        date: datetime object to extract year and month from
        dest_dir: Base destination directory path
    
    Returns:
        str: Path to the year/month subdirectory
    """
    year = date.strftime('%Y')
    month = date.strftime('%m')

    year_dir = os.path.join(dest_dir, year)
    if not os.path.exists(year_dir):
        os.makedirs(year_dir)

    month_dir = os.path.join(year_dir, month)
    if not os.path.exists(month_dir):
        os.makedirs(month_dir)

    return month_dir


if __name__ == "__main__":
    start()
