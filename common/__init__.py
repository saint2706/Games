"""Common utilities and base classes for all games.

This module provides reusable components, abstract base classes, and shared
functionality across different game implementations.
"""

from .ai_strategy import AIStrategy, HeuristicStrategy, MinimaxStrategy, RandomStrategy
from .game_engine import GameEngine, GameState

__all__ = [
    "GameEngine",
    "GameState",
    "AIStrategy",
    "RandomStrategy",
    "MinimaxStrategy",
    "HeuristicStrategy",
]

# Import GUI components only if tkinter is available
try:
    from .gui_base import BaseGUI, GUIConfig

    __all__.extend(["BaseGUI", "GUIConfig"])
except ImportError:
    pass
