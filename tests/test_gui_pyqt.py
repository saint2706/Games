"""Tests for PyQt5 GUI implementations.

These tests verify that PyQt5-based GUI components work correctly.
"""

from __future__ import annotations

import pathlib
import sys

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

pytestmark = pytest.mark.skipif(not PYQT5_AVAILABLE, reason="PyQt5 not available")


@pytest.mark.gui
class TestDotsAndBoxesPyQt:
    """Test Dots and Boxes PyQt5 GUI components."""

    @pytest.mark.skipif(not sys.platform.startswith("linux") or not sys.stdout.isatty(), reason="Requires display")
    def test_dots_boxes_pyqt_gui_initialization(self, qtbot):
        """Test Dots and Boxes PyQt5 GUI initialization."""
        try:
            from paper_games.dots_and_boxes.gui_pyqt import DotsAndBoxesGUI

            window = DotsAndBoxesGUI(size=2, show_hints=False)
            qtbot.addWidget(window)
            assert window is not None
            assert window.game is not None
            assert window.size == 2
            assert window.player_turn is True
        except Exception as e:
            if "display" in str(e).lower() or "DISPLAY" in str(e):
                pytest.skip("No display available for GUI testing")
            raise


@pytest.mark.gui
class TestBattleshipPyQt:
    """Test Battleship PyQt5 GUI components."""

    @pytest.mark.skipif(not sys.platform.startswith("linux") or not sys.stdout.isatty(), reason="Requires display")
    def test_battleship_pyqt_gui_initialization(self, qtbot):
        """Test Battleship PyQt5 GUI initialization."""
        try:
            from paper_games.battleship.gui_pyqt import BattleshipGUI

            window = BattleshipGUI(size=8, fleet_type="small", difficulty="easy", salvo_mode=False)
            qtbot.addWidget(window)
            assert window.game is not None
            assert window.size == 8
            assert window.setup_phase is True
            assert window.placing_ship_index == 0
        except Exception as e:
            if "display" in str(e).lower() or "DISPLAY" in str(e):
                pytest.skip("No display available for GUI testing")
            raise


@pytest.mark.gui
class TestBaseGUIPyQt:
    """Test PyQt5 BaseGUI components."""

    def test_base_gui_pyqt_import(self):
        """Test that PyQt5 BaseGUI can be imported."""
        from common.gui_base_pyqt import BaseGUI, GUIConfig

        assert BaseGUI is not None
        assert GUIConfig is not None

    def test_gui_config_defaults(self):
        """Test GUIConfig default values."""
        from common.gui_base_pyqt import GUIConfig

        config = GUIConfig()
        assert config.window_title == "Game"
        assert config.window_width == 800
        assert config.window_height == 600
        assert config.enable_sounds is False
        assert config.enable_animations is True


@pytest.mark.gui
class TestGoFishPyQt:
    """Test Go Fish PyQt5 GUI components."""

    @pytest.mark.skipif(not sys.platform.startswith("linux") or not sys.stdout.isatty(), reason="Requires display")
    def test_go_fish_pyqt_gui_initialization(self, qtbot):
        """Test Go Fish PyQt5 GUI initialization."""
        try:
            from card_games.go_fish.game import GoFishGame
            from card_games.go_fish.gui_pyqt import GoFishGUI

            game = GoFishGame(num_players=2)
            window = GoFishGUI(game)
            qtbot.addWidget(window)
            assert window is not None
            assert window.game is not None
            assert len(window.player_rows) == 2
        except Exception as e:
            if "display" in str(e).lower() or "DISPLAY" in str(e):
                pytest.skip("No display available for GUI testing")
            raise


GUI_IMPORT_CASES = [
    ("paper_games.dots_and_boxes.gui_pyqt", "DotsAndBoxesGUI"),
    ("paper_games.battleship.gui_pyqt", "BattleshipGUI"),
    ("card_games.go_fish.gui_pyqt", "GoFishGUI"),
]


@pytest.mark.gui
@pytest.mark.parametrize("module_path, attr_name", GUI_IMPORT_CASES)
def test_pyqt_gui_imports(module_path: str, attr_name: str) -> None:
    """Ensure core PyQt GUI modules can be imported."""

    module = __import__(module_path, fromlist=[attr_name])
    assert hasattr(module, attr_name)


@pytest.mark.gui
def test_pyqt5_modules_available():
    """Test that PyQt5 GUI modules can be imported."""
    gui_modules = [
        "paper_games.battleship.gui_pyqt",
        "paper_games.dots_and_boxes.gui_pyqt",
        "card_games.go_fish.gui_pyqt",
        "common.gui_base_pyqt",
    ]

    available_modules = []
    for module_name in gui_modules:
        try:
            __import__(module_name)
            available_modules.append(module_name)
        except ImportError as e:
            if "pyqt5" not in str(e).lower():
                raise

    # At least some GUI modules should be available if PyQt5 is present
    if PYQT5_AVAILABLE:
        assert len(available_modules) > 0, "No PyQt5 GUI modules available despite PyQt5 being present"
