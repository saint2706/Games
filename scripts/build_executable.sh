#!/bin/bash
"""Build standalone executable for Games Collection.

This script builds a standalone executable using either PyInstaller or Nuitka.
Usage: 
  ./scripts/build_executable.sh pyinstaller
  ./scripts/build_executable.sh nuitka
"""

set -e

# Get the build tool (default to pyinstaller)
BUILD_TOOL="${1:-pyinstaller}"

# Get the project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "Building Games Collection with $BUILD_TOOL..."
echo "Project root: $PROJECT_ROOT"

if [ "$BUILD_TOOL" = "pyinstaller" ]; then
    echo "Installing PyInstaller..."
    pip install pyinstaller
    
    echo "Building with PyInstaller..."
    pyinstaller build_configs/pyinstaller/games.spec --clean
    
    echo "Build complete!"
    echo "Executable location: dist/games-collection"
    
elif [ "$BUILD_TOOL" = "nuitka" ]; then
    echo "Installing Nuitka..."
    pip install nuitka
    
    echo "Building with Nuitka..."
    python build_configs/nuitka/build.py
    
    echo "Build complete!"
    echo "Executable location: dist/nuitka/games-collection"
    
else
    echo "Error: Unknown build tool '$BUILD_TOOL'"
    echo "Usage: $0 [pyinstaller|nuitka]"
    exit 1
fi

echo ""
echo "You can now run the executable to launch any game in the collection!"
