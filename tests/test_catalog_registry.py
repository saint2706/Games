"""Tests for the catalogue registry metadata helpers."""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from games_collection.catalog import registry


@pytest.fixture(autouse=True)
def clear_registry_cache() -> None:
    """Ensure the registry cache is cleared before and after each test."""

    registry._load_registry.cache_clear()
    yield
    registry._load_registry.cache_clear()


def test_registry_metadata_includes_rich_fields() -> None:
    """Loaded metadata should expose synopsis and asset hints."""

    games = registry.get_all_games()
    assert games, "Registry should contain bundled games"
    for metadata in games:
        assert metadata.synopsis is not None
        assert len(metadata.synopsis) >= len(metadata.description)
        assert metadata.screenshot_path is not None
        assert metadata.thumbnail_path is not None


def test_registry_handles_missing_optional_fields(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """The loader should gracefully default optional fields when absent."""

    payload = {
        "games": [
            {
                "slug": "sample_game",
                "name": "Sample Game",
                "genre": "logic",
                "package": "games_collection.games.logic.sample",
                "entry_point": "games_collection.games.logic.sample.__main__:main",
                "description": "Sample logic game entry.",
                "tags": ["logic"],
            }
        ]
    }
    dummy_registry = tmp_path / registry.REGISTRY_RESOURCE
    dummy_registry.write_text(json.dumps(payload), encoding="utf-8")

    monkeypatch.setattr(registry, "resources", SimpleNamespace(files=lambda _pkg: tmp_path))

    games = registry.get_all_games()
    assert len(games) == 1
    metadata = games[0]
    assert metadata.synopsis == metadata.description
    assert metadata.screenshot_path is None
    assert metadata.thumbnail_path is None
