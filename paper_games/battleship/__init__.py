"""Battleship game package.

Battleship implementation with full fleets and a hunting AI opponent.
Re-exports core types so ``paper_games.battleship`` behaves like a facade for
both the game engine and the CLI.
"""

from .battleship import (
    DEFAULT_FLEET,
    BattleshipGame,
    Board,
    Coordinate,
    Ship,
)
from .cli import play

__all__ = [
    "BattleshipGame",
    "Board",
    "Ship",
    "Coordinate",
    "DEFAULT_FLEET",
    "play",
]
