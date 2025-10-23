"""Central registry describing all games included in the collection."""

from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from importlib import resources
from typing import Dict, Iterable, Tuple

REGISTRY_RESOURCE = "registry.json"


@dataclass(frozen=True)
class GameMetadata:
    """Metadata describing a game implementation bundled with the project."""

    slug: str
    name: str
    genre: str
    package: str
    entry_point: str
    description: str
    tags: Tuple[str, ...]
    mechanics: Tuple[str, ...] = ()
    average_duration: int | None = None
    difficulty: int | None = None
    synopsis: str | None = None
    screenshot_path: str | None = None
    thumbnail_path: str | None = None


@lru_cache(maxsize=1)
def _load_registry() -> Tuple[GameMetadata, ...]:
    """Load the immutable registry from the packaged JSON resource."""

    with resources.files(__package__).joinpath(REGISTRY_RESOURCE).open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    games: Iterable[GameMetadata] = (
        GameMetadata(
            slug=item["slug"],
            name=item["name"],
            genre=item["genre"],
            package=item["package"],
            entry_point=item["entry_point"],
            description=item["description"],
            synopsis=item.get("synopsis", item["description"]),
            tags=tuple(item.get("tags", ())),
            mechanics=tuple(item.get("mechanics", ())),
            average_duration=item.get("average_duration"),
            difficulty=item.get("difficulty"),
            screenshot_path=item.get("screenshot_path"),
            thumbnail_path=item.get("thumbnail_path"),
        )
        for item in payload.get("games", [])
    )
    return tuple(sorted(games, key=lambda metadata: metadata.slug))


def get_all_games() -> Tuple[GameMetadata, ...]:
    """Return all registered games."""

    return _load_registry()


def get_game_by_slug(slug: str) -> GameMetadata | None:
    """Return the metadata for ``slug`` if it exists."""

    normalized = slug.strip().lower()
    for metadata in _load_registry():
        if metadata.slug == normalized:
            return metadata
    return None


def iter_genre(genre: str) -> Tuple[GameMetadata, ...]:
    """Return the games registered under ``genre``."""

    normalized = genre.strip().lower()
    return tuple(metadata for metadata in _load_registry() if metadata.genre == normalized)


def as_slug_map() -> Dict[str, GameMetadata]:
    """Return a mapping of slugs to metadata for quick lookups."""

    return {metadata.slug: metadata for metadata in _load_registry()}


GENRES: Tuple[str, ...] = tuple(sorted({metadata.genre for metadata in _load_registry()}))
