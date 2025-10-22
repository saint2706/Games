"""Tests for the public launcher entry points."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

PROJECT_SRC = Path(__file__).resolve().parents[1] / "src"
if str(PROJECT_SRC) not in sys.path:
    sys.path.insert(0, str(PROJECT_SRC))


class TestGamesCollectionLauncher:
    """Tests for :mod:`games_collection.launcher`."""

    def test_main_callable(self) -> None:
        """``games_collection.launcher`` exposes a callable ``main`` entry point."""

        module = importlib.import_module("games_collection.launcher")
        assert callable(module.main)


class TestScriptsLauncherCompatibility:
    """Ensure the compatibility wrapper keeps the legacy import path working."""

    def test_wrapper_exports_main(self) -> None:
        """``scripts.launcher`` re-exports the ``games_collection.launcher`` main."""

        module = importlib.import_module("scripts.launcher")
        assert module.main is importlib.import_module("games_collection.launcher").main
