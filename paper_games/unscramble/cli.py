"""Command-line interface for playing Unscramble.

This module provides the terminal-based interactive experience for playing
the word unscrambling game.
"""

from __future__ import annotations

from .unscramble import UnscrambleGame


def play(rounds: int = 5) -> None:
    """Run a multi-round unscramble session."""
    game = UnscrambleGame()
    print("Unscramble the letters to reveal the word!")
    score = 0
    # Loop through the specified number of rounds.
    for round_number in range(1, rounds + 1):
        scrambled = game.new_round()
        print(f"\nRound {round_number}: {scrambled}")
        guess = input("Your guess: ")
        if game.guess(guess):
            print("Correct!")
            score += 1
        else:
            print(f"Close, but the word was '{game.secret_word}'.")
    # Print the final score at the end of the game.
    print(f"\nYou solved {score} out of {rounds} words.")
