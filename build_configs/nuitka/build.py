#!/usr/bin/env python3
"""Nuitka build script for the Games Collection.

This script automates the process of building a standalone, single-file executable
for the Games Collection using Nuitka. It compiles the Python source code into C,
resulting in a high-performance, portable application.

The script is configured to:
- Create a single executable file.
- Automatically include all game packages and necessary modules.
- Place the final executable in the `dist/nuitka` directory.
- Handle platform-specific optimizations.

For more details on Nuitka, see the documentation: https://nuitka.net/doc/user-manual.html

Usage:
    python build_configs/nuitka/build.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def build_with_nuitka() -> int:
    """Configure and run the Nuitka build process.

    This function defines the Nuitka command with all necessary options,
    executes the build process, and returns the exit code.

    The build configuration includes:
    - Standalone mode to bundle all dependencies.
    - One-file compilation for a single executable.
    - Inclusion of all game packages and critical modules like `colorama`.
    - Disabling the console on Windows for a GUI-like experience (optional).

    Returns:
        The exit code from the Nuitka build process. 0 for success, non-zero for failure.
    """
    # Get the project root directory (the parent of `build_configs`)
    project_root = Path(__file__).parent.parent.parent
    # Define the path to the main entry script
    launcher_path = project_root / "scripts" / "launcher.py"

    # Ensure the main launcher script exists before proceeding
    if not launcher_path.exists():
        print(f"Error: Launcher script not found at {launcher_path}")
        return 1

    # Construct the Nuitka command as a list of arguments
    cmd = [
        sys.executable,  # Use the same Python interpreter that runs this script
        "-m",
        "nuitka",  # Run Nuitka as a module
        "--standalone",  # Create a standalone executable with all dependencies
        "--onefile",  # Bundle everything into a single executable file
        "--assume-yes-for-downloads",  # Automatically download dependencies if needed
        "--output-dir=dist/nuitka",  # Set the output directory for the build artifacts
        "--output-filename=games-collection",  # Name of the final executable
        # --- Package and Module Inclusion ---
        # Explicitly include all game packages to ensure they are part of the build
        "--include-package=card_games",
        "--include-package=paper_games",
        "--include-package=dice_games",
        "--include-package=word_games",
        "--include-package=logic_games",
        "--include-package=common",
        # Include the 'colorama' module, which is used for colored terminal output
        "--include-module=colorama",
        # --- Optimizations and Performance ---
        # Follow all imports to discover dependencies
        "--follow-imports",
        # --- Platform-Specific Options ---
        # On Windows, uncomment the line below to create a windowed (GUI) application
        # without a console window.
        # "--disable-console",
        # The main entry point for the application
        str(launcher_path),
    ]

    print("Building Games Collection with Nuitka...")
    print(f"Command: {' '.join(cmd)}")

    try:
        # Run the Nuitka command from the project root directory
        result = subprocess.run(cmd, cwd=project_root, check=False)
        # Return the exit code of the build process
        return result.returncode
    except FileNotFoundError:
        print("Error: Nuitka not found. Please install it with 'pip install nuitka'")
        return 1
    except Exception as e:
        print(f"An unexpected error occurred during the build: {e}")
        return 1


if __name__ == "__main__":
    # When the script is executed directly, start the build and exit with its status code
    sys.exit(build_with_nuitka())
