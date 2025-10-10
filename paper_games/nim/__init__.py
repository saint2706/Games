"""Nim game package.

Classic Nim with configurable rules and an optimal computer opponent.
Re-exports core types so ``paper_games.nim`` behaves like a facade for
both the game engine and the CLI.
"""

from .cli import play
from .nim import NimGame

__all__ = ["NimGame", "play"]
