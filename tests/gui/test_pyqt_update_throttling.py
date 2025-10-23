"""Tests verifying PyQt throttled update logic for BaseGUI."""

from __future__ import annotations

import time
from typing import FrozenSet, Tuple

import pytest

import sys
from pathlib import Path

PROJECT_SRC = Path(__file__).resolve().parents[2] / "src"
if str(PROJECT_SRC) not in sys.path:  # pragma: no cover - deterministic import path fix
    sys.path.insert(0, str(PROJECT_SRC))

pytest.importorskip("PyQt5")

from PyQt5.QtWidgets import QLabel, QMainWindow, QVBoxLayout, QWidget

from games_collection.core.gui_base_pyqt import BaseGUI, GUIConfig, PYQT5_AVAILABLE


pytestmark = pytest.mark.skipif(not PYQT5_AVAILABLE, reason="PyQt5 required for GUI throttling tests")


class _ProbeGUI(QMainWindow, BaseGUI):
    """Minimal concrete GUI used to exercise BaseGUI throttling helpers."""

    def __init__(self) -> None:
        QMainWindow.__init__(self)
        BaseGUI.__init__(self, root=self, config=GUIConfig(window_title="Probe"))
        self._update_interval_ms = 5  # Speed up tests
        self.updates: list[Tuple[float, FrozenSet[str]]] = []
        self.build_layout()

    def build_layout(self) -> None:  # pragma: no cover - trivial wiring
        central = QWidget(self)
        layout = QVBoxLayout()
        central.setLayout(layout)
        layout.addWidget(QLabel("probe", central))
        self.setCentralWidget(central)

    def update_display(self) -> None:  # pragma: no cover - executed via tests
        self.updates.append((time.perf_counter(), frozenset(self.current_dirty_regions)))


def _wait_for_updates(gui: _ProbeGUI, qtbot, expected: int, timeout: int = 300) -> None:
    qtbot.waitUntil(lambda: len(gui.updates) >= expected, timeout=timeout)


def test_coalesces_multiple_regions(qtbot) -> None:
    gui = _ProbeGUI()
    qtbot.addWidget(gui)

    gui.request_update_display("status")
    gui.request_update_display("scoreboard")

    _wait_for_updates(gui, qtbot, expected=1)

    timestamps = gui.updates
    assert len(timestamps) == 1
    regions = timestamps[0][1]
    assert {"status", "scoreboard"}.issubset(regions)


def test_immediate_refresh_bypasses_timer(qtbot) -> None:
    gui = _ProbeGUI()
    qtbot.addWidget(gui)

    gui.request_update_display("hand", immediate=True)
    assert len(gui.updates) == 1
    assert gui.updates[0][1] == frozenset({"hand"})


def test_burst_requests_throttled(qtbot) -> None:
    gui = _ProbeGUI()
    qtbot.addWidget(gui)

    for _ in range(10):
        gui.request_update_display("status")

    _wait_for_updates(gui, qtbot, expected=1)
    qtbot.wait(60)

    assert len(gui.updates) <= 3

    intervals = [second - first for (first, _), (second, _) in zip(gui.updates, gui.updates[1:])]
    if intervals:
        assert all(interval >= gui._update_interval_ms / 1000 - 0.01 for interval in intervals)
