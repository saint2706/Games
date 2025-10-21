"""Metadata catalogue describing the games shipped with the collection.

This lightweight catalogue is consumed by the recommendation system and other
cross-game surfaces (launcher, analytics) that need to reason about the games
without importing their heavy modules. Each entry exposes high level
characteristics such as mechanics, typical play duration, and optional tagging
that help the recommendation engine justify suggestions to the player.
"""

from __future__ import annotations

from typing import Dict

from games_collection.catalog.registry import GameMetadata, get_all_games
from games_collection.core.recommendation_service import GameDescriptor


def _descriptor_from_metadata(metadata: GameMetadata) -> GameDescriptor:
    """Translate :class:`GameMetadata` values into :class:`GameDescriptor`."""

    mechanics = metadata.mechanics or metadata.tags
    return GameDescriptor(
        game_id=metadata.slug,
        name=metadata.name,
        mechanics=tuple(mechanics),
        tags=metadata.tags,
        average_duration=metadata.average_duration,
        difficulty=metadata.difficulty,
    )


_DEFAULT_GAME_CATALOGUE: Dict[str, GameDescriptor] = {metadata.slug: _descriptor_from_metadata(metadata) for metadata in get_all_games()}


def get_default_game_catalogue() -> Dict[str, GameDescriptor]:
    """Return a copy of the curated game metadata catalogue."""

    return dict(_DEFAULT_GAME_CATALOGUE)


# Backwards compatibility helper for older documentation references.
get_default_game_catalog = get_default_game_catalogue
