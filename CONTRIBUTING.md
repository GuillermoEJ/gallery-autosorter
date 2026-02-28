# Contributing to Gallery Autosorter

Thanks for your interest in contributing! Please follow these guidelines to help improve the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/gallery-autosorter.git`
3. Create a virtual environment: `python -m venv venv`
4. Activate it: `source venv/bin/activate` (Windows: `venv\Scripts\activate`)
5. Install dependencies: `pip install -r requirements.txt`

## Development Workflow

1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Test your changes thoroughly
4. Commit with clear messages: `git commit -m "Add feature description"`
5. Push to your fork: `git push origin feature/your-feature-name`
6. Create a Pull Request with a clear description

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused on a single responsibility

## Testing

Please test your changes with different image types and scenarios:
- Images with EXIF data
- Images without EXIF data
- Large folders with many images
- Edge cases (empty folders, special characters in names)

## Documentation

- Update README.md if adding new features
- Update CHANGELOG.md following Keep a Changelog format
- Add docstrings to all new functions

## Reporting Issues

When reporting an issue, please include:
- Description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Python version and OS
- Relevant image files (if applicable)

## Questions?

Feel free to open an issue to discuss ideas or ask questions!

---

All contributors will be appreciated and acknowledged.
