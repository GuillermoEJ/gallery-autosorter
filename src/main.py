import os
import shutil
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS

source_dir = 'C:/Users/USER/Desktop/origen'
dest_dir = 'C:/Users/USER/Desktop/destino'

IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')

def get_unique_filename(dest_folder, filename):
    name, ext = os.path.splitext(filename)
    counter = 1
    new_filename = filename
    while os.path.exists(os.path.join(dest_folder, new_filename)):
        new_filename = f"{name}_{counter}{ext}"
        counter += 1
    return new_filename

def get_image_date(file):
    try:
        image = Image.open(file)
        exif_data = image._getexif()
        if exif_data:
            for tag_id, value in exif_data.items():
                tag = TAGS.get(tag_id, tag_id)
                if tag == 'DateTimeOriginal':
                    return datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
    except Exception:
        pass
    # Si no hay EXIF, usar fecha de creación del archivo
    creation_time = os.path.getctime(file)
    return datetime.fromtimestamp(creation_time)

def start():
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    total_copiadas = 0
    errores = 0

    for filename in os.listdir(source_dir):
        if not filename.lower().endswith(IMAGE_EXTENSIONS):
            continue  # Salta archivos que no son imágenes

        file = os.path.join(source_dir, filename)
        try:
            date = get_image_date(file)
            final_loc = check_dir(date)
            dest_path = os.path.join(final_loc, filename)
            if os.path.exists(dest_path):
                print(f"Ya existe: {filename} → {dest_path}. No se copia.")
                continue  # Salta si ya existe
            shutil.copy(file, dest_path)
            total_copiadas += 1
            print(f"Copiada: {filename} → {dest_path}")
        except Exception as e:
            errores += 1
            print(f"Error al copiar {filename}: {e}")

    print(f"\nTotal de fotos copiadas: {total_copiadas}")
    print(f"Total de errores: {errores}")

def check_dir (date):
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