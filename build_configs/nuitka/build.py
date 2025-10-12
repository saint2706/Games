#!/usr/bin/env python3
"""Nuitka build script for Games Collection.

This script configures and builds a standalone executable using Nuitka.
Usage: python build_configs/nuitka/build.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def build_with_nuitka() -> int:
    """Build the Games Collection with Nuitka.

    Returns:
        Exit code from the build process
    """
    project_root = Path(__file__).parent.parent.parent
    launcher_path = project_root / "scripts" / "launcher.py"

    if not launcher_path.exists():
        print(f"Error: Launcher not found at {launcher_path}")
        return 1

    # Nuitka build command
    cmd = [
        sys.executable,
        "-m",
        "nuitka",
        "--standalone",
        "--onefile",
        "--assume-yes-for-downloads",
        "--output-dir=dist/nuitka",
        "--output-filename=games-collection",
        # Include all game packages
        "--include-package=card_games",
        "--include-package=paper_games",
        "--include-package=dice_games",
        "--include-package=word_games",
        "--include-package=logic_games",
        "--include-package=common",
        # Include colorama
        "--include-module=colorama",
        # Platform-specific optimizations
        "--follow-imports",
        # Disable console on Windows if needed (can be changed)
        # "--disable-console",
        str(launcher_path),
    ]

    print("Building Games Collection with Nuitka...")
    print(f"Command: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, cwd=project_root, check=False)
        return result.returncode
    except Exception as e:
        print(f"Error during build: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(build_with_nuitka())
