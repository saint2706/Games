"""Dots and Boxes game package.

Dots and Boxes for the terminal with a chain-aware AI opponent.
Re-exports core types so ``paper_games.dots_and_boxes`` behaves like a facade for
both the game engine and the CLI.
"""

from .cli import play
from .dots_and_boxes import DotsAndBoxes

__all__ = ["DotsAndBoxes", "play"]
