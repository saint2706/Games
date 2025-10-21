"""Top-level package for the consolidated games collection."""

from __future__ import annotations

from importlib import import_module
from typing import Final

from games_collection.catalog.registry import GameMetadata, get_all_games

__all__: Final = ("catalog", "core", "games", "get_all_games", "GameMetadata")

# Ensure subpackages are importable when the project is installed in editable mode.
import_module("games_collection.games")
import_module("games_collection.core")
