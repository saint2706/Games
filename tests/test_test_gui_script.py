"""Tests for the GUI test script."""

from __future__ import annotations

import importlib.machinery
import importlib.util

import pytest

from scripts import test_gui


def test_list_gui_games_includes_existing_pyqt() -> None:
    """Ensure dynamic discovery detects existing PyQt implementations."""

    games = test_gui.list_gui_games()
    assert "games_collection.games.paper" in games
    dots_support = games["games_collection.games.paper"].get("dots_and_boxes")
    assert dots_support is not None
    assert "pyqt5" in dots_support


def test_list_gui_games_detects_new_pyqt_module(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify that newly available PyQt modules are reported without manual updates."""

    from games_collection.catalog.registry import GameMetadata
    from games_collection.catalog.registry import iter_genre as original_iter_genre

    original_find_spec = importlib.util.find_spec

    # Create a fake game metadata
    fake_game = GameMetadata(
        slug="fake_new_game",
        name="Fake New Game",
        genre="card",
        package="games_collection.games.card.fake_new_game",
        entry_point="games_collection.games.card.fake_new_game.__main__:main",
        description="A fake game for testing",
        tags=("test",),
    )

    def fake_iter_genre(genre: str):  # type: ignore[override]
        """Return games including the fake game for card genre."""
        original_games = original_iter_genre(genre)
        if genre == "card":
            return original_games + (fake_game,)
        return original_games

    def fake_find_spec(name: str):  # type: ignore[override]
        if name == "games_collection.games.card.fake_new_game.gui_pyqt":
            return importlib.machinery.ModuleSpec(name, loader=None)
        if name == "games_collection.games.card.fake_new_game.gui":
            return None
        return original_find_spec(name)

    # Patch the imported function in the test_gui module
    monkeypatch.setattr(test_gui, "iter_genre", fake_iter_genre)
    monkeypatch.setattr(importlib.util, "find_spec", fake_find_spec)

    games = test_gui.list_gui_games()
    assert "fake_new_game" in games["games_collection.games.card"]
    assert games["games_collection.games.card"]["fake_new_game"] == ["pyqt5"]
