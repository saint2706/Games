from __future__ import annotations

import argparse
import importlib
import importlib.util
from typing import Dict, List, Optional

from games_collection.catalog.registry import GameMetadata, iter_genre

FRAMEWORK_SUFFIXES: Dict[str, str] = {"tkinter": "gui", "pyqt5": "gui_pyqt"}
GENRE_PACKAGES: Dict[str, str] = {genre: f"games_collection.games.{genre}" for genre in ("card", "paper", "dice", "logic", "word")}
PYQT5_MIGRATED = {("paper", "dots_and_boxes"), ("card", "go_fish"), ("card", "bluff")}


def test_tkinter_available() -> bool:
    """Return ``True`` when Tkinter can be imported."""

    try:
        import tkinter  # noqa: F401
    except ImportError:
        return False
    return True


def test_pyqt5_available() -> bool:
    """Return ``True`` when PyQt5 can be imported."""

    try:
        from PyQt5 import QtWidgets  # noqa: F401
    except ImportError:
        return False
    return True


def _frameworks_for_game(metadata: GameMetadata) -> List[str]:
    """Return the GUI frameworks available for ``metadata``."""

    frameworks: List[str] = []
    for framework, suffix in FRAMEWORK_SUFFIXES.items():
        module_name = f"{metadata.package}.{suffix}"
        if importlib.util.find_spec(module_name) is not None:
            frameworks.append(framework)
    return sorted(frameworks)


def discover_gui_games(genre: str) -> dict[str, list[str]]:
    """Discover GUI implementations for the provided genre."""

    discovered: dict[str, list[str]] = {}
    for metadata in iter_genre(genre):
        frameworks = _frameworks_for_game(metadata)
        if frameworks:
            discovered[metadata.slug] = frameworks
    return dict(sorted(discovered.items()))


def list_gui_games() -> dict[str, dict[str, list[str]]]:
    """List all games with GUI implementations grouped by package path."""

    catalogue: dict[str, dict[str, list[str]]] = {}
    for genre, package in GENRE_PACKAGES.items():
        games = discover_gui_games(genre)
        if games:
            catalogue[package] = games
    return catalogue


def _resolve_metadata(category: str, game: str) -> Optional[GameMetadata]:
    """Return the metadata for the requested category/game pair."""

    genre = category.split(".")[-1].lower()
    for metadata in iter_genre(genre):
        if metadata.slug == game:
            return metadata
    return None


def check_gui_implementation(category: str, game: str, framework: str) -> tuple[bool, Optional[str]]:
    """Check if a game has a GUI implementation for the given framework."""

    metadata = _resolve_metadata(category, game)
    if metadata is None:
        return False, None

    module_suffix = FRAMEWORK_SUFFIXES.get(framework)
    if module_suffix is None:
        raise ValueError(f"Unknown framework '{framework}'")

    module_name = f"{metadata.package}.{module_suffix}"
    try:
        importlib.import_module(module_name)
        return True, module_name
    except (ImportError, RuntimeError):
        return False, None


def main() -> int:
    """Main entry point."""

    parser = argparse.ArgumentParser(
        description="Test GUI applications with different frameworks.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("--list", action="store_true", help="List all games with GUI support.")
    parser.add_argument(
        "--check-framework",
        choices=[*FRAMEWORK_SUFFIXES.keys(), "all"],
        help="Check framework availability.",
    )
    parser.add_argument(
        "--check-game",
        help="Check if a specific game has GUI support.\nFormat: package/game (e.g., games_collection.games.paper/dots_and_boxes)",
    )
    parser.add_argument(
        "--framework",
        choices=list(FRAMEWORK_SUFFIXES.keys()),
        default="pyqt5",
        help="Framework to check (default: pyqt5).",
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
            print(f"\n{category}:")
            if not game_map:
                print("  (no GUI implementations found)")
                continue

            genre = category.split(".")[-1].lower()
            for game, frameworks in game_map.items():
                status_parts = []
                for framework, label in ("tkinter", "Tkinter"), ("pyqt5", "PyQt5"):
                    symbol = "✓" if framework in frameworks else "✗"
                    status_parts.append(f"{label}: {symbol}")

                migration_marker = " *" if (genre, game) in PYQT5_MIGRATED else ""
                print(f"  {game:20}{migration_marker} [{' | '.join(status_parts)}]")

        if PYQT5_MIGRATED:
            print("\n* denotes games with completed PyQt5 migrations.")

        return 0

    if args.check_game:
        try:
            category, game = args.check_game.split("/")
        except ValueError:
            print("Invalid format for --check-game. Use package/game.")
            return 1

        exists, module_name = check_gui_implementation(category, game, args.framework)
        if exists:
            print(f"{args.framework} GUI available for {category}.{game} (module: {module_name})")
        else:
            print(f"{args.framework} GUI not available for {category}.{game}")
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
