# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec file for Games Collection.

This builds a standalone executable for all games in the collection.
Usage: pyinstaller build_configs/pyinstaller/games.spec
"""

from __future__ import annotations

import sys
from pathlib import Path

# Add project root to path
# Note: SPECPATH is a PyInstaller builtin variable pointing to the spec file's directory
project_root = Path(SPECPATH).parent.parent
sys.path.insert(0, str(project_root))

block_cipher = None

# Collect all game modules
game_modules = [
    'card_games',
    'paper_games',
    'dice_games',
    'word_games',
    'logic_games',
    'common',
]

# Hidden imports for dynamic imports
hidden_imports = [
    'colorama',
    'tkinter',
]

# Collect all data files
datas = [
    (str(project_root / 'README.md'), '.'),
    (str(project_root / 'LICENSE'), '.'),
]

a = Analysis(
    [str(project_root / 'scripts' / 'launcher.py')],
    pathex=[str(project_root)],
    binaries=[],
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['pytest', 'black', 'ruff', 'mypy'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='games-collection',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
