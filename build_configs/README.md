# Build Configurations

This directory contains build configurations for creating standalone executables of the Games Collection.

## Available Build Tools

### PyInstaller

PyInstaller freezes Python applications into standalone executables.

**Location**: `pyinstaller/games.spec`

**Build Command**:

```bash
pyinstaller build_configs/pyinstaller/games.spec --clean
```

**Output**: `dist/games-collection` (or `dist/games-collection.exe` on Windows)

**Features**:

- Single-file executable
- Includes all dependencies
- Cross-platform support
- UPX compression enabled

### Nuitka

Nuitka compiles Python to C code for better performance and smaller executables.

**Location**: `nuitka/build.py`

**Build Command**:

```bash
python build_configs/nuitka/build.py
```

**Output**: `dist/nuitka/games-collection`

**Features**:

- Native compilation
- Better performance
- Smaller executable size
- Advanced optimizations

## Quick Start

Use the convenience script:

```bash
# Build with PyInstaller (default)
./scripts/build_executable.sh pyinstaller

# Build with Nuitka
./scripts/build_executable.sh nuitka
```

## Customization

### PyInstaller

Edit `pyinstaller/games.spec` to customize:

- Application icon
- Console vs. windowed mode
- Additional data files
- Module exclusions
- Build options

### Nuitka

Edit `nuitka/build.py` to customize:

- Output directory
- Output filename
- Include/exclude packages
- Optimization level
- Platform-specific options

## Platform-Specific Notes

### Linux

- Executables are portable within the same distribution family
- May require `libffi` and `libz` on target systems
- GTK/Qt libraries needed for GUI games

### macOS

- Code signing may be required for distribution
- Notarization needed for Gatekeeper bypass
- Universal binaries possible with additional configuration

### Windows

- Windows Defender may flag executables (false positive)
- Code signing recommended for distribution
- Visual C++ runtime may be required

## Troubleshooting

### Import Errors

If you get import errors, add the module to `hiddenimports` in the spec file:

```python
hiddenimports=[
    'colorama',
    'tkinter',
    'your_module_here',
]
```

### Missing Data Files

Add data files to the `datas` list:

```python
datas=[
    ('path/to/data', 'destination'),
]
```

### Size Issues

- Use Nuitka for smaller executables
- Enable UPX compression in PyInstaller
- Exclude unnecessary modules

## CI/CD Integration

GitHub Actions automatically builds executables for all platforms on:

- Push to master/main
- Pull requests
- Tagged releases

See `.github/workflows/build-executables.yml` for configuration.

## More Information

- [PyInstaller Documentation](https://pyinstaller.org/en/stable/)
- [Nuitka Documentation](https://nuitka.net/doc/user-manual.html)
- [Deployment Guide](../docs/deployment/DEPLOYMENT.md)
