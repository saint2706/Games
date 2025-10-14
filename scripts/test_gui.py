#!/usr/bin/env python
"""Script to test GUI applications with different frameworks.

This utility helps developers test GUI applications with both tkinter and PyQt5
to ensure consistency during the migration process.
"""

from __future__ import annotations

import argparse
import importlib
import importlib.util
import pkgutil
import sys
from typing import Dict, List, Optional

FRAMEWORK_SUFFIXES: Dict[str, str] = {"tkinter": "gui", "pyqt5": "gui_pyqt"}


PYQT_MODULE_OVERRIDES = {
    "paper_games/battleship": "paper_games.battleship.gui_pyqt",
}

TKINTER_MODULE_OVERRIDES = {}


def test_tkinter_available() -> bool:
    """Check if tkinter is available."""
    try:
        import tkinter  # noqa: F401

        return True
    except ImportError:
        return False


def test_pyqt5_available() -> bool:
    """Check if PyQt5 is available."""
    try:
        from PyQt5 import QtWidgets  # noqa: F401

        return True
    except ImportError:
        return False


PYQT5_MIGRATED = {
    ("paper_games", "dots_and_boxes"),
    ("card_games", "go_fish"),
    ("card_games", "bluff"),
}


def discover_gui_games(package_name: str) -> dict[str, list[str]]:
    """Discover GUI implementations for the provided package.

    Args:
        package_name: The top-level package containing game modules (e.g., ``paper_games``).

    Returns:
        Mapping of game name to the frameworks that provide GUI support.
    """
    try:
        package = importlib.import_module(package_name)
    except ImportError:
        return {}

    package_path = getattr(package, "__path__", None)
    if package_path is None:
        return {}

    prefix = f"{package.__name__}."
    discovered: dict[str, list[str]] = {}

    for module_info in pkgutil.walk_packages(package_path, prefix=prefix):
        if not module_info.ispkg:
            continue

        relative_name = module_info.name[len(prefix) :]
        if not relative_name or "." in relative_name:
            continue

        frameworks: List[str] = []
        for framework, module_suffix in FRAMEWORK_SUFFIXES.items():
            module_name = f"{module_info.name}.{module_suffix}"
            if importlib.util.find_spec(module_name) is not None:
                frameworks.append(framework)

        if frameworks:
            discovered[relative_name] = sorted(frameworks)

    return dict(sorted(discovered.items()))


def list_gui_games() -> dict[str, dict[str, list[str]]]:
    """List all games with GUI implementations grouped by category."""

    categories = ("paper_games", "card_games")
    return {category: discover_gui_games(category) for category in categories}


def check_gui_implementation(category: str, game: str, framework: str) -> tuple[bool, Optional[str]]:
    """Check if a game has a GUI implementation for the given framework.

    Args:
        category: Game category (paper_games or card_games)
        game: Game name
        framework: GUI framework (tkinter or pyqt5)

    Returns:
        Tuple of (exists, module_path)
    """
    key = f"{category}/{game}"
    if framework == "tkinter":
        module_name = TKINTER_MODULE_OVERRIDES.get(key, f"{category}.{game}.gui")
    else:  # pyqt5
        module_name = PYQT_MODULE_OVERRIDES.get(key, f"{category}.{game}.gui_pyqt")
    module_suffix = FRAMEWORK_SUFFIXES.get(framework)
    if module_suffix is None:
        raise ValueError(f"Unknown framework '{framework}'")

    module_name = f"{category}.{game}.{module_suffix}"

    try:
        __import__(module_name)
        return True, module_name
    except (ImportError, RuntimeError):
        # RuntimeError can occur when a GUI module checks for tkinter availability
        return False, None


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Test GUI applications with different frameworks")
    parser.add_argument("--list", action="store_true", help="List all games with GUI support")
    parser.add_argument(
        "--check-framework",
        choices=[*FRAMEWORK_SUFFIXES.keys(), "all"],
        help="Check framework availability",
    )
    parser.add_argument("--check-game", help="Check if specific game has GUI support (format: category/game)")
    parser.add_argument(
        "--framework",
        choices=list(FRAMEWORK_SUFFIXES.keys()),
        default="pyqt5",
        help="Framework to check",
    )

    args = parser.parse_args()

    if args.check_framework:
        print("GUI Framework Availability:")
        print("-" * 40)

        if args.check_framework in ("tkinter", "all"):
            tkinter_available = test_tkinter_available()
            status = "✓ Available" if tkinter_available else "✗ Not available"
            print(f"Tkinter: {status}")

        if args.check_framework in ("pyqt5", "all"):
            pyqt5_available = test_pyqt5_available()
            status = "✓ Available" if pyqt5_available else "✗ Not available"
            print(f"PyQt5:   {status}")

        return 0

    if args.list:
        games = list_gui_games()
        print("Games with GUI Support:")
        print("=" * 60)

        for category, game_map in games.items():
            print(f"\n{category.upper().replace('_', ' ')}:")
            if not game_map:
                print("  (no GUI implementations found)")
                continue

            for game, frameworks in game_map.items():
                status_parts = []
                for framework, label in ("tkinter", "Tkinter"), ("pyqt5", "PyQt5"):
                    symbol = "✓" if framework in frameworks else "✗"
                    status_parts.append(f"[{label}: {symbol}]")

                migration_marker = " *" if (category, game) in PYQT5_MIGRATED else ""
                print(f"  {game:20}{migration_marker} {' '.join(status_parts)}")

        if PYQT5_MIGRATED:
            print("\n* denotes games with completed PyQt5 migrations.")

        return 0

    if args.check_game:
        try:
            category, game = args.check_game.split("/")
        except ValueError:
            print("Error: Game must be in format 'category/game' (e.g., 'paper_games/dots_and_boxes')")
            return 1

        exists, module_path = check_gui_implementation(category, game, args.framework)

        if exists:
            print(f"✓ {game} has {args.framework} GUI support")
            print(f"  Module: {module_path}")
            return 0
        else:
            print(f"✗ {game} does not have {args.framework} GUI support")
            return 1

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
