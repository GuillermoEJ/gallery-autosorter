import os
import shutil
from datetime import datetime

def copy_photos(source_dir, dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    for filename in os.listdir(source_dir):
        source_file = os.path.join(source_dir, filename)
        if os.path.isfile(source_file):
            creation_time = os.path.getctime(source_file)
            organize_by_date(source_file, dest_dir, creation_time)

def organize_by_date(file_path, dest_dir, creation_time):
    date = datetime.fromtimestamp(creation_time)
    year = date.strftime('%Y')
    month = date.strftime('%m')

    year_month_dir = os.path.join(dest_dir, year, month)
    if not os.path.exists(year_month_dir):
        os.makedirs(year_month_dir)

    shutil.copy(file_path, year_month_dir)