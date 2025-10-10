"""
A collection of interactive implementations of classic paper-and-pencil games.

This package provides classes for various games that can be played in the terminal.
Each game is contained in its own submodule.
"""

# Import the main game classes from their respective submodules.
from .hangman import HangmanGame
from .tic_tac_toe import TicTacToeGame
from .dots_and_boxes import DotsAndBoxes
from .battleship import BattleshipGame
from .unscramble import UnscrambleGame
from .nim import NimGame

# The __all__ variable defines the public API of the package.
# When a user writes `from paper_games import *`, only these names will be imported.
__all__ = [
    "HangmanGame",
    "TicTacToeGame",
    "DotsAndBoxes",
    "BattleshipGame",
    "UnscrambleGame",
    "NimGame",
]
