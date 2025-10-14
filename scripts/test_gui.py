#!/usr/bin/env python
"""Script to test GUI applications with different frameworks.

This utility helps developers test GUI applications with both tkinter and PyQt5
to ensure consistency during the migration process.
"""

from __future__ import annotations

import argparse
import sys
from typing import Optional


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


def list_gui_games() -> dict[str, list[str]]:
    """List all games with GUI implementations."""
    return {
        "paper_games": ["dots_and_boxes", "battleship"],
        "card_games": [
            "blackjack",
            "bluff",
            "bridge",
            "crazy_eights",
            "gin_rummy",
            "go_fish",
            "hearts",
            "poker",
            "solitaire",
            "spades",
            "uno",
            "war",
        ],
    }


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
    parser.add_argument("--check-framework", choices=["tkinter", "pyqt5", "all"], help="Check framework availability")
    parser.add_argument("--check-game", help="Check if specific game has GUI support (format: category/game)")
    parser.add_argument("--framework", choices=["tkinter", "pyqt5"], default="pyqt5", help="Framework to check")

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

        for category, game_list in games.items():
            print(f"\n{category.upper().replace('_', ' ')}:")
            for game in sorted(game_list):
                # Check both frameworks
                tk_exists, _ = check_gui_implementation(category, game, "tkinter")
                pyqt_exists, _ = check_gui_implementation(category, game, "pyqt5")

                tk_status = "✓" if tk_exists else "✗"
                pyqt_status = "✓" if pyqt_exists else "✗"

                print(f"  {game:20} [Tkinter: {tk_status}] [PyQt5: {pyqt_status}]")

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
