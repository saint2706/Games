"""Utilities to introspect GUI framework support across the game collection."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Iterable, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from common.gui_framework import available_frameworks, load_run_gui


def list_gui_games() -> dict[str, list[str]]:
    """Return the games that advertise GUI implementations."""

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


def check_gui_implementation(module_base: str, framework: str) -> Tuple[bool, str]:
    """Check whether the requested GUI framework can be imported for a game."""

    try:
        _, resolved = load_run_gui(module_base, framework)
    except RuntimeError as exc:
        return False, str(exc)
    return True, resolved


def print_framework_status(selected: Iterable[str]) -> None:
    """Display framework availability information."""

    detected = set(available_frameworks())
    print("GUI Framework Availability:")
    print("-" * 40)
    for framework in selected:
        display = "PyQt5" if framework == "pyqt5" else "Tkinter"
        status = "✓ Available" if framework in detected else "✗ Not available"
        print(f"{display}: {status}")


def main() -> int:
    """Entry point for the GUI diagnostic utility."""

    parser = argparse.ArgumentParser(description="Inspect GUI framework support for the bundled games")
    parser.add_argument("--list", action="store_true", help="List all games with GUI support")
    parser.add_argument(
        "--check-framework",
        choices=["tkinter", "pyqt5", "all"],
        help="Check framework availability",
    )
    parser.add_argument("--check-game", help="Check if specific game has GUI support (format: category/game)")
    parser.add_argument(
        "--framework",
        choices=["auto", "tkinter", "pyqt5", "all"],
        default="auto",
        help="Framework to check when using --check-game",
    )

    args = parser.parse_args()

    if args.check_framework:
        targets = ["tkinter", "pyqt5"] if args.check_framework == "all" else [args.check_framework]
        print_framework_status(targets)
        return 0

    if args.list:
        games = list_gui_games()
        print("Games with GUI Support:")
        print("=" * 60)

        for category, game_list in games.items():
            print(f"\n{category.upper().replace('_', ' ')}:")
            for game in sorted(game_list):
                module_base = f"{category}.{game}"
                tk_exists, _ = check_gui_implementation(module_base, "tkinter")
                pyqt_exists, _ = check_gui_implementation(module_base, "pyqt5")

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

        module_base = f"{category}.{game}"

        if args.framework == "all":
            frameworks: Iterable[str] = ("pyqt5", "tkinter")
        elif args.framework == "auto":
            frameworks = ("auto",)
        else:
            frameworks = (args.framework,)

        all_success = True
        for framework in frameworks:
            success, details = check_gui_implementation(module_base, framework)
            if success:
                resolved = details if framework == "auto" else framework
                print(f"✓ {game} can load the {resolved} GUI (requested: {framework}).")
            else:
                all_success = False
                print(f"✗ {game} {framework} check failed: {details}")

        return 0 if all_success else 1

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
