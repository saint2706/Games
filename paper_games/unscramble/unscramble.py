"""Game engine and logic for the Unscramble-the-word party game.

This module provides the core game logic for Unscramble, including word
selection, scrambling, and guess validation.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Iterable

from ..hangman import load_default_words


@dataclass
class UnscrambleGame:
    """Present a scrambled word and track guesses."""

    words: Iterable[str] = field(default_factory=load_default_words)
    rng: random.Random = field(default_factory=random.Random)

    def __post_init__(self) -> None:
        """Initializes the game state after the dataclass is created."""
        self.words = [word.lower() for word in self.words]
        if not self.words:
            raise ValueError("Provide at least one word to scramble.")
        self.secret_word = ""
        self.scrambled = ""

    def new_round(self) -> str:
        """Starts a new round with a new secret word."""
        self.secret_word = self.rng.choice(self.words)
        letters = list(self.secret_word)
        self.rng.shuffle(letters)
        # Ensure the scrambled word is different from the original word.
        if letters == list(self.secret_word):
            # A simple way to ensure it's different is to move the last letter to the front.
            letters.insert(0, letters.pop())
        self.scrambled = "".join(letters)
        return self.scrambled

    def guess(self, word: str) -> bool:
        """Checks if a guessed word matches the secret word."""
        if not self.secret_word:
            raise ValueError("Start a round before guessing.")
        return word.lower().strip() == self.secret_word
