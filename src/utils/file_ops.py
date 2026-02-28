"""File operations utilities for photo organization."""

import os
import shutil
from datetime import datetime


def copy_photos(source_dir, dest_dir):
    """Copy all photos from source to destination directory.
    
    Args:
        source_dir: Source directory path
        dest_dir: Destination directory path
    """
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    for filename in os.listdir(source_dir):
        source_file = os.path.join(source_dir, filename)
        if os.path.isfile(source_file):
            modification_time = os.path.getmtime(source_file)
            organize_by_date(source_file, dest_dir, modification_time)


def organize_by_date(file_path, dest_dir, modification_time):
    """Organize a file into year/month subdirectories based on modification time.
    
    Args:
        file_path: Path to the file
        dest_dir: Base destination directory
        modification_time: File modification timestamp
    """
    date = datetime.fromtimestamp(modification_time)
    year = date.strftime('%Y')
    month = date.strftime('%m')

    year_month_dir = os.path.join(dest_dir, year, month)
    if not os.path.exists(year_month_dir):
        os.makedirs(year_month_dir)

    shutil.copy(file_path, year_month_dir)