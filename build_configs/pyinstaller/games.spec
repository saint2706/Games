# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec file for the Games Collection.

This file configures PyInstaller to build a standalone, single-file executable
for the Games Collection. It specifies the entry point, includes necessary
packages and data files, and sets various build options.

Key configurations in this file:
- Main entry point: `scripts/launcher.py`
- Hidden imports for libraries that are not automatically detected.
- Inclusion of data files like README.md and LICENSE.
- Optional inclusion of PyQt5 for GUI-based games.
- UPX compression to reduce executable size.
- Exclusion of development-only packages like pytest and black.

For more details on spec files, see the PyInstaller documentation:
https://pyinstaller.org/en/stable/spec-files.html

Usage:
    pyinstaller build_configs/pyinstaller/games.spec
"""

from __future__ import annotations

import sys
from pathlib import Path

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# --- Project Path Setup ---
# Add the project root directory to the Python path. This ensures that
# PyInstaller can find the game modules and scripts correctly.
# `SPECPATH` is a built-in PyInstaller variable that holds the directory
# containing this spec file.
project_root = Path(SPECPATH).parent.parent
sys.path.insert(0, str(project_root))

# `block_cipher` is used for encrypting Python bytecode. It is disabled here.
block_cipher = None

# --- Game Module Identification ---
# This list identifies all game packages. While not directly used in the
# Analysis section below, it's good practice for clarity and can be used
# for more complex scripting within this file.
game_modules = [
    'card_games',
    'paper_games',
    'dice_games',
    'word_games',
    'logic_games',
    'common',
]

# --- Hidden Imports ---
# `hiddenimports` tells PyInstaller about modules that are used in the code
# but are not automatically detected (e.g., through dynamic imports or plugins).
hidden_imports = [
    'colorama',  # For colored terminal output.
    'tkinter',   # Standard GUI library, often needs to be explicitly included.
]

# --- Optional PyQt5 Inclusion ---
# This section dynamically detects if PyQt5 is installed and, if so, collects
# all its necessary submodules and data files (like Qt plugins and translations).
# This is crucial for any games that use PyQt5 for their user interface.
pyqt5_packages = [
    'PyQt5',
    'PyQt5.QtCore',
    'PyQt5.QtGui',
    'PyQt5.QtWidgets',
    'PyQt5.QtPrintSupport',
]

pyqt5_hidden_imports: list[str] = []
pyqt5_datas: list[tuple[str, str]] = []

try:
    # Check if PyQt5 is installed
    import PyQt5  # noqa: F401  # pylint: disable=unused-import
except ModuleNotFoundError:
    print('PyQt5 not installed - skipping PyQt5 hidden import and data collection')
else:
    # If installed, collect all submodules and data files
    for package in pyqt5_packages:
        pyqt5_hidden_imports.extend(collect_submodules(package))
        pyqt5_datas.extend(collect_data_files(package))

# Add the collected PyQt5 hidden imports to the main list
if pyqt5_hidden_imports:
    hidden_imports = sorted({*hidden_imports, *pyqt5_hidden_imports})

# --- Data Files ---
# `datas` specifies non-binary files to be included in the executable.
# Each entry is a tuple: (source_path, destination_in_bundle).
# Here, we include the README and LICENSE in the root of the bundle.
datas = [
    (str(project_root / 'README.md'), '.'),
    (str(project_root / 'LICENSE'), '.'),
]

# Add the collected PyQt5 data files to the main list, ensuring no duplicates.
if pyqt5_datas:
    combined_datas = [*datas, *pyqt5_datas]
    seen_datas: set[tuple[str, str]] = set()
    deduped_datas: list[tuple[str, str]] = []
    for entry in combined_datas:
        if entry in seen_datas:
            continue
        seen_datas.add(entry)
        deduped_datas.append(entry)
    datas = deduped_datas


# --- Main Analysis ---
# The `Analysis` object is the core of the spec file. It analyzes the source
# code to find all dependencies.
a = Analysis(
    # Entry point: The main script that starts the application.
    [str(project_root / 'scripts' / 'launcher.py')],
    # `pathex`: A list of paths to search for modules (already configured above).
    pathex=[str(project_root)],
    # `binaries`: A list of any non-python libraries (.dll, .so, .dylib) to include.
    binaries=[],
    # `datas`: The list of data files to bundle.
    datas=datas,
    # `hiddenimports`: The list of modules to force-include.
    hiddenimports=hidden_imports,
    # `hookspath`: A list of directories to search for custom PyInstaller hooks.
    hookspath=[],
    hooksconfig={},
    # `runtime_hooks`: A list of scripts to run at startup.
    runtime_hooks=[],
    # `excludes`: A list of modules to exclude from the build to save space.
    excludes=['pytest', 'black', 'ruff', 'mypy'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# --- Python Library Archive ---
# `PYZ` creates a PYZ archive, which contains all the compiled Python modules (.pyc).
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)


# --- Executable ---
# `EXE` builds the final executable file from the analysis results.
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    # `name`: The filename of the final executable.
    name='games-collection',
    # `debug`: Set to True to get debug output at runtime.
    debug=False,
    bootloader_ignore_signals=False,
    # `strip`: If True, strip symbols from the executable (macOS/Linux).
    strip=False,
    # `upx`: If True, compress the executable with UPX (if installed).
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    # `console`: Set to True for a console application, False for a windowed (GUI) one.
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
