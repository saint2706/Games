"""Namespace package for all game genres bundled with the collection."""

from __future__ import annotations

from typing import Final

from games_collection.catalog.registry import GENRES

__all__: Final = tuple(sorted(GENRES))
