"""Interactive implementations of classic paper-and-pencil games."""

from .hangman import HangmanGame
from .tic_tac_toe import TicTacToeGame
from .dots_and_boxes import DotsAndBoxes
from .battleship import BattleshipGame
from .unscramble import UnscrambleGame
from .nim import NimGame

__all__ = [
    "HangmanGame",
    "TicTacToeGame",
    "DotsAndBoxes",
    "BattleshipGame",
    "UnscrambleGame",
    "NimGame",
]
