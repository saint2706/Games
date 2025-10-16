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

Both build configurations are designed to be easily customizable. The configuration files are heavily commented to guide you through the process.

### PyInstaller

The PyInstaller build is controlled by `pyinstaller/games.spec`. This is a Python script that gives you full control over the build process. The file is extensively commented to explain each option.

To customize the build, edit `pyinstaller/games.spec`:

-   **Add Hidden Imports**: If PyInstaller fails to detect a module, add it to the `hiddenimports` list.
-   **Include Data Files**: To bundle additional files (e.g., assets, documentation), add them to the `datas` list.
-   **Exclude Modules**: To reduce the executable size, add unnecessary modules to the `excludes` list in the `Analysis` section.
-   **Toggle Console Window**: For GUI applications on Windows, you can hide the console by setting `console=False` in the `EXE` object.
-   **Application Icon**: You can specify an application icon by adding the `icon` argument to the `EXE` object.

### Nuitka

The Nuitka build is controlled by `nuitka/build.py`. This script constructs and runs the Nuitka command-line build, and it is well-documented with comments explaining each argument.

To customize the build, edit `nuitka/build.py`:

-   **Include/Exclude Packages**: Modify the `--include-package` arguments in the `cmd` list to add or remove entire game packages.
-   **Change Output Directory**: Modify the `--output-dir` and `--output-filename` arguments to change where the executable is saved.
-   **Toggle Console Window**: On Windows, create a GUI-only application by uncommenting the `--disable-console` argument.
-   **Advanced Optimizations**: Add or remove Nuitka command-line flags to the `cmd` list to fine-tune the compilation process.

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
