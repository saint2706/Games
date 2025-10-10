"""Terminal-based hangman implementation with tactile feedback."""

from __future__ import annotations

import json
import random
import string
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, List, Sequence, Set


WORDLIST_PATH = Path(__file__).with_name("wordlist.json")
_DEFAULT_WORD_CACHE: List[str] | None = None


def _load_words_from_disk() -> List[str]:
    data = json.loads(WORDLIST_PATH.read_text(encoding="utf-8"))
    collected: Set[str] = set()
    for difficulty in ("easy", "medium", "hard"):
        collected.update(word.lower() for word in data.get(difficulty, ()))
    if not collected:
        raise ValueError("No words found in bundled wordlist.json")
    return sorted(collected)


def load_default_words() -> List[str]:
    """Return a copy of the bundled hangman words."""

    global _DEFAULT_WORD_CACHE
    if _DEFAULT_WORD_CACHE is None:
        _DEFAULT_WORD_CACHE = _load_words_from_disk()
    return list(_DEFAULT_WORD_CACHE)


HANGMAN_STAGES: Sequence[str] = (
    r"""
      _______
     |/      |
     |
     |
     |
     |
    _|___
    """.rstrip(),
    r"""
      _______
     |/      |
     |      (_)
     |
     |
     |
    _|___
    """.rstrip(),
    r"""
      _______
     |/      |
     |      (_)
     |       |
     |       |
     |
    _|___
    """.rstrip(),
    r"""
      _______
     |/      |
     |      (_)
     |      \|
     |       |
     |
    _|___
    """.rstrip(),
    r"""
      _______
     |/      |
     |      (_)
     |      \|/
     |       |
     |
    _|___
    """.rstrip(),
    r"""
      _______
     |/      |
     |      (_)
     |      \|/
     |       |
     |      /
    _|___
    """.rstrip(),
    r"""
      _______
     |/      |
     |      (_)
     |      \|/
     |       |
     |      / \
    _|___
    """.rstrip(),
)


@dataclass
class HangmanGame:
    """Encapsulates the state and logic of a hangman round."""

    words: Iterable[str] = field(default_factory=load_default_words)
    max_attempts: int = 6

    def __post_init__(self) -> None:
        self.words = [word.lower() for word in self.words]
        if not self.words:
            raise ValueError("At least one word must be supplied.")
        if self.max_attempts < 1:
            raise ValueError("max_attempts must be at least one.")
        self.reset()

    def reset(self) -> None:
        """Select a new word and reset guesses."""

        self.secret_word: str = random.choice(list(self.words))
        self.guessed_letters: Set[str] = set()
        self.guessed_words: Set[str] = set()
        self.wrong_guesses: Set[str] = set()

    def guess(self, entry: str) -> bool:
        """Process a player's guessed letter or full word."""

        entry = entry.lower().strip()
        if not entry or any(ch not in string.ascii_lowercase for ch in entry):
            raise ValueError("Guesses must contain only letters.")

        if len(entry) == 1:
            if entry in self.guessed_letters or entry in self.wrong_guesses:
                raise ValueError(f"Letter '{entry}' has already been guessed.")
            if entry in self.secret_word:
                self.guessed_letters.add(entry)
                return True
            self.wrong_guesses.add(entry)
            return False

        if entry == self.secret_word:
            self.guessed_letters.update(set(self.secret_word))
            self.guessed_words.add(entry)
            return True

        if entry in self.guessed_words:
            raise ValueError(f"Word '{entry}' has already been attempted.")

        self.guessed_words.add(entry)
        self.wrong_guesses.add(entry)
        return False

    @property
    def attempts_left(self) -> int:
        """Return how many incorrect guesses remain."""

        return self.max_attempts - len(self.wrong_guesses)

    @property
    def obscured_word(self) -> str:
        """Return the secret word with unguessed letters hidden."""

        return " ".join(
            letter if letter in self.guessed_letters else "_"
            for letter in self.secret_word
        )

    @property
    def stage(self) -> str:
        """Return the ASCII gallows that reflects the current danger level."""

        wrong = self.max_attempts - self.attempts_left
        if self.max_attempts <= 0:
            return HANGMAN_STAGES[-1]
        scale = (len(HANGMAN_STAGES) - 1) / self.max_attempts
        index = min(len(HANGMAN_STAGES) - 1, int(round(wrong * scale)))
        return HANGMAN_STAGES[index]

    def status_lines(self) -> List[str]:
        """Human-friendly summary of the current round."""

        wrong_letters = sorted(guess for guess in self.wrong_guesses if len(guess) == 1)
        wrong_words = sorted(
            guess for guess in self.wrong_guesses if len(guess) > 1
        )
        lines = [self.stage, f"Word: {self.obscured_word}"]
        if wrong_letters:
            lines.append(f"Wrong letters: {' '.join(wrong_letters)}")
        if wrong_words:
            lines.append("Wrong words: " + ", ".join(wrong_words))
        lines.append(f"Attempts left: {self.attempts_left}")
        return lines

    def is_won(self) -> bool:
        """Return True if all letters have been guessed."""

        return all(letter in self.guessed_letters for letter in set(self.secret_word))

    def is_lost(self) -> bool:
        """Return True if the player has exhausted the allowed attempts."""

        return self.attempts_left <= 0


def play(words: Iterable[str] | None = None, max_attempts: int = 6) -> None:
    """Run an interactive hangman session in the terminal."""

    game = HangmanGame(words or load_default_words(), max_attempts=max_attempts)
    print("Welcome to Hangman! Guess letters or attempt the entire word.")
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
    if game.is_won():
        print(f"Congratulations! You guessed '{game.secret_word}'.")
    else:
        print(f"Game over! The word was '{game.secret_word}'.")


if __name__ == "__main__":
    play()
