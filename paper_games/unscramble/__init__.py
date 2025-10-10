"""Unscramble game package.

Unscramble-the-word party game.
Re-exports core types so ``paper_games.unscramble`` behaves like a facade for
both the game engine and the CLI.
"""

from .cli import play
from .unscramble import UnscrambleGame

__all__ = ["UnscrambleGame", "play"]
