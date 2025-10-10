"""Bluff (Cheat) card game engine and user interfaces."""

from .bluff import BluffGame, DifficultyLevel, Phase, run_cli

try:  # pragma: no cover - optional GUI dependency
    from .gui import BluffGUI, run_gui
except Exception:  # pragma: no cover - gracefully degrade without Tk
    BluffGUI = None  # type: ignore[assignment]

    def run_gui(*args, **kwargs):  # type: ignore[override]
        raise RuntimeError(
            "Tkinter is required for the bluff GUI but is not available."
        )


__all__ = [
    "BluffGame",
    "DifficultyLevel",
    "Phase",
    "run_cli",
    "BluffGUI",
    "run_gui",
]
