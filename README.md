# Gallery Autosorter

![Version](https://img.shields.io/badge/version-1.1-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.7+-blue.svg)

A Python application that automatically organizes photos into year/month folders based on EXIF metadata or file timestamps.

## Features

- **Automatic Organization**: Sorts photos into `YYYY/MM` folder structure based on image date
- **Smart Date Detection**: Extracts dates from:
  - EXIF metadata (using `piexif` and PIL)
  - File modification timestamp (fallback)
- **Date Range Filtering**: Optionally copy only photos from a specific date range
- **Graphical Interface**: User-friendly folder and date selection dialogs
- **Safe Operation**: Skips duplicate files instead of overwriting
- **Debug Tools**: Included utilities to inspect image metadata

## Installation

### Prerequisites
- Python 3.7+

### Setup

1. Clone or download this repository:
   ```bash
   git clone https://github.com/yourusername/gallery-autosorter.git
   cd gallery-autosorter
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Main Application

Run the main photo organizer:
```bash
python src/main.py
```

The application will guide you through:
1. Select source folder (where your photos are)
2. Select destination folder (where organized photos will be copied)
3. Optionally specify a date range to filter photos
4. Confirm and start the copy process

### Debug Tools

#### Inspect a Single Image
View EXIF metadata from a specific image:
```bash
python debug_exif.py
```

#### Analyze a Folder
See detected dates for all images in a folder:
```bash
python debug_folder.py
```

## Supported Image Formats

- `.jpg` / `.jpeg`
- `.png`
- `.gif`
- `.bmp`
- `.tiff`

## How It Works

1. **Date Detection**: The application tries multiple methods to find the image date:
   - EXIF IFD 0 DateTime
   - EXIF DateTimeOriginal / DateTimeDigitized
   - PIL EXIF extraction
   - File modification timestamp
   - Current time (last resort)

2. **Organization**: Photos are copied to: `destination/YYYY/MM/filename`

3. **Safety**: If a file already exists in the destination, it's skipped to prevent overwrites

## Dependencies

- **Pillow**: Image processing and EXIF extraction
- **piexif**: Additional EXIF metadata support

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Troubleshooting

### Dates not detected correctly
Run `debug_folder.py` to see which date extraction method is being used for your images. This helps identify metadata issues.

### Permission errors
Ensure you have read access to the source folder and write access to the destination folder.

### No EXIF data found
The application will automatically fall back to using the file's modification timestamp, so photos will still be organized correctly.

## Future Improvements

- [ ] Batch operations interface
- [ ] Move instead of copy option
- [ ] Custom folder naming schemes
- [ ] Recursive subdirectory copying
- [ ] Progress bar for large operations

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter issues or have questions, please open an issue on GitHub.

---

**Note**: This tool copies files by default. No original files are modified unless explicitly moved (future version). Always test with a small set of photos first!

