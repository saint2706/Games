"""Command-line interface for playing Hangman.

This module provides the terminal-based interactive experience for playing
Hangman with ASCII art and word guessing.
"""

from __future__ import annotations

from typing import Iterable

from .hangman import HangmanGame, load_default_words


def play(words: Iterable[str] | None = None, max_attempts: int = 6) -> None:
    """Run an interactive hangman session in the terminal."""
    game = HangmanGame(words or load_default_words(), max_attempts=max_attempts)
    print("Welcome to Hangman! Guess letters or attempt the entire word.")
    # Main game loop continues until the game is won or lost.
    while not (game.is_won() or game.is_lost()):
        print()
        for line in game.status_lines():
            print(line)
        guess = input("Enter a letter or guess the word: ").strip().lower()
        try:
            correct = game.guess(guess)
        except ValueError as exc:
            print(exc)
            continue
        # Provide feedback to the player based on their guess.
        if correct:
            if len(guess) == 1:
                print("Good guess!")
            else:
                print("Incredible! You solved the word outright.")
        else:
            if len(guess) == 1:
                print("Nope, that letter isn't in the word.")
            else:
                print("That's not the word. The gallows creak ominously...")
    # Announce the final result of the game.
    if game.is_won():
        print(f"Congratulations! You guessed '{game.secret_word}'.")
    else:
        print(f"Game over! The word was '{game.secret_word}'.")
