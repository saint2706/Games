"""Hangman game package.

Terminal-based hangman implementation with tactile feedback.
Re-exports core types so ``paper_games.hangman`` behaves like a facade for
both the game engine and the CLI.
"""

from .cli import play
from .hangman import HANGMAN_STAGES, HangmanGame, load_default_words

__all__ = ["HangmanGame", "HANGMAN_STAGES", "load_default_words", "play"]
