"""Tests for PyQt5 GUI implementations.

These tests verify that PyQt5-based GUI components work correctly."""

from __future__ import annotations

import pathlib
import sys
from importlib import import_module
from typing import Sequence, TYPE_CHECKING

import pytest

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Check if PyQt5 is available
try:
    from PyQt5 import QtWidgets  # noqa: F401

    PYQT5_AVAILABLE = True
except ImportError:
    PYQT5_AVAILABLE = False

if TYPE_CHECKING:
    from pytestqt.qtbot import QtBot

_DISPLAY_ERROR_MARKERS: tuple[str, ...] = (
    "could not connect to display",
    "no display name",
    "no protocol specified",
    "failed to initialize platform xcb",
    "qxcbconnection",
    "qt.qpa.plugin: could not load the qt platform plugin",
)

pytestmark = [pytest.mark.skipif(not PYQT5_AVAILABLE, reason="PyQt5 not available"), pytest.mark.gui]

_IMPORT_TARGETS: tuple[tuple[str, Sequence[str]], ...] = (
    ("paper_games.dots_and_boxes.gui_pyqt", ("DotsAndBoxesGUI",)),
    ("card_games.go_fish.gui_pyqt", ("GoFishGUI",)),
    ("common.gui_base_pyqt", ("BaseGUI", "GUIConfig")),
)


def _skip_if_display_error(exception: Exception) -> None:
    """Skip the current test if the exception indicates a missing display."""

    message = str(exception).lower()
    if any(marker in message for marker in _DISPLAY_ERROR_MARKERS):
        pytest.skip("No display available for GUI testing")


@pytest.mark.parametrize(("module_name", "attribute_names"), _IMPORT_TARGETS)
def test_pyqt5_gui_module_importable(module_name: str, attribute_names: Sequence[str]) -> None:
    """Ensure PyQt5 GUI modules can be imported and expose expected attributes."""

    module = import_module(module_name)
    for attribute_name in attribute_names:
        assert hasattr(module, attribute_name), f"{module_name} is missing attribute {attribute_name}"


def test_dots_boxes_pyqt_gui_initialization(qtbot: "QtBot") -> None:
    """Test Dots and Boxes PyQt5 GUI initialization using qtbot."""

    from paper_games.dots_and_boxes.gui_pyqt import DotsAndBoxesGUI

    try:
        window = DotsAndBoxesGUI(size=2, show_hints=False)
        qtbot.addWidget(window)
        assert window.game is not None
        assert window.size == 2
        assert window.player_turn is True
    except Exception as exc:  # pragma: no cover - defensive path
        _skip_if_display_error(exc)
        raise


def test_base_gui_pyqt_config_defaults() -> None:
    """Test GUIConfig default values provided by the PyQt base module."""

    from common.gui_base_pyqt import GUIConfig

    config = GUIConfig()
    assert config.window_title == "Game"
    assert config.window_width == 800
    assert config.window_height == 600
    assert config.enable_sounds is False
    assert config.enable_animations is True


def test_go_fish_pyqt_gui_initialization(qtbot: "QtBot") -> None:
    """Test Go Fish PyQt5 GUI initialization using qtbot."""

    from card_games.go_fish.game import GoFishGame
    from card_games.go_fish.gui_pyqt import GoFishGUI

    try:
        game = GoFishGame(num_players=2)
        window = GoFishGUI(game)
        qtbot.addWidget(window)
        assert window.game is not None
        assert len(window.player_rows) == 2
    except Exception as exc:  # pragma: no cover - defensive path
        _skip_if_display_error(exc)
        raise
