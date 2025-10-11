"""Command-line interface for playing Hangman.

This module provides the terminal-based interactive experience for playing
Hangman with ASCII art and word guessing.
"""

from __future__ import annotations

from typing import Iterable

from .hangman import HANGMAN_ART_STYLES, HangmanGame, load_themed_words, load_words_by_difficulty


def _get_difficulty() -> str:
    """Prompt user to select difficulty level."""
    print("\nSelect difficulty:")
    print("1. Easy (6+ letter words)")
    print("2. Medium (4-5 letter words)")
    print("3. Hard (3 letter words)")
    print("4. All difficulties (default)")

    choice = input("Enter choice (1-4) or press Enter for all: ").strip()

    difficulty_map = {"1": "easy", "2": "medium", "3": "hard", "4": "all", "": "all"}
    return difficulty_map.get(choice, "all")


def _get_theme() -> str | None:
    """Prompt user to select a theme."""
    themes = load_themed_words()
    if not themes:
        return None

    print("\nSelect theme:")
    print("0. No theme (standard words)")
    theme_list = sorted(themes.keys())
    for idx, theme in enumerate(theme_list, 1):
        print(f"{idx}. {theme.capitalize()}")

    choice = input(f"Enter choice (0-{len(theme_list)}) or press Enter for no theme: ").strip()

    if choice == "" or choice == "0":
        return None

    try:
        idx = int(choice) - 1
        if 0 <= idx < len(theme_list):
            return theme_list[idx]
    except ValueError:
        pass

    return None


def _get_art_style() -> str:
    """Prompt user to select ASCII art style."""
    print("\nSelect ASCII art style:")
    styles = sorted(HANGMAN_ART_STYLES.keys())
    for idx, style in enumerate(styles, 1):
        print(f"{idx}. {style.capitalize()}")

    choice = input(f"Enter choice (1-{len(styles)}) or press Enter for classic: ").strip()

    if choice == "":
        return "classic"

    try:
        idx = int(choice) - 1
        if 0 <= idx < len(styles):
            return styles[idx]
    except ValueError:
        pass

    return "classic"


def _get_game_mode() -> str:
    """Prompt user to select game mode."""
    print("\nSelect game mode:")
    print("1. Single Player (default)")
    print("2. Multiplayer (take turns choosing words)")

    choice = input("Enter choice (1-2) or press Enter for single player: ").strip()

    if choice == "2":
        return "multiplayer"
    return "single"


def _play_multiplayer() -> None:
    """Run multiplayer mode where players take turns."""
    print("\n=== MULTIPLAYER MODE ===")
    print("Players will take turns choosing words for each other to guess.\n")

    num_players = 2
    try:
        num_input = input("How many players? (2-4, default 2): ").strip()
        if num_input:
            num_players = max(2, min(4, int(num_input)))
    except ValueError:
        num_players = 2

    players = []
    for i in range(num_players):
        name = input(f"Enter name for Player {i + 1}: ").strip()
        if not name:
            name = f"Player {i + 1}"
        players.append({"name": name, "score": 0})

    rounds_input = input("\nHow many rounds per player? (default 1): ").strip()
    try:
        rounds = max(1, int(rounds_input)) if rounds_input else 1
    except ValueError:
        rounds = 1

    total_rounds = rounds * num_players
    current_round = 0

    # Get art style once for the game
    art_style = _get_art_style()

    while current_round < total_rounds:
        choosing_player_idx = current_round % num_players
        guessing_player_idx = (current_round + 1) % num_players

        choosing_player = players[choosing_player_idx]
        guessing_player = players[guessing_player_idx]

        print(f"\n{'='*60}")
        print(f"Round {current_round + 1}/{total_rounds}")
        print(f"{choosing_player['name']} will choose a word for {guessing_player['name']} to guess.")
        print(f"{'='*60}")

        # Choosing player enters a secret word
        while True:
            word = input(f"\n{choosing_player['name']}, enter a secret word (letters only): ").strip().lower()
            if word and word.isalpha():
                break
            print("Please enter a valid word with letters only.")

        # Clear screen (print newlines)
        print("\n" * 50)

        # Guessing player plays
        print(f"\n{guessing_player['name']}'s turn to guess!")
        game = HangmanGame([word], max_attempts=6, hints_enabled=True, art_style=art_style)

        while not (game.is_won() or game.is_lost()):
            print()
            for line in game.status_lines():
                print(line)

            guess = input("Enter a letter, 'hint' for a hint, or guess the word: ").strip().lower()

            if guess == "hint":
                hint = game.get_hint()
                if hint:
                    print(f"Hint! The letter '{hint}' has been revealed.")
                else:
                    print("No hints available!")
                continue

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
            print(f"\n✓ {guessing_player['name']} guessed '{game.secret_word}' correctly!")
            guessing_player["score"] += 1
        else:
            print(f"\n✗ {guessing_player['name']} didn't guess the word: '{game.secret_word}'")

        current_round += 1

        # Show scores
        print("\n--- Current Scores ---")
        for player in players:
            print(f"{player['name']}: {player['score']}")

    # Final results
    print(f"\n{'='*60}")
    print("GAME OVER - Final Scores:")
    print(f"{'='*60}")
    sorted_players = sorted(players, key=lambda p: p["score"], reverse=True)
    for idx, player in enumerate(sorted_players, 1):
        print(f"{idx}. {player['name']}: {player['score']} points")

    winner = sorted_players[0]
    if sorted_players[0]["score"] > sorted_players[1]["score"]:
        print(f"\n🎉 {winner['name']} wins! Congratulations!")
    else:
        print("\n🤝 It's a tie!")


def play(words: Iterable[str] | None = None, max_attempts: int = 6) -> None:
    """Run an interactive hangman session in the terminal."""
    # If words are provided directly, use them (for backward compatibility)
    if words is not None:
        game = HangmanGame(words, max_attempts=max_attempts)
        print("Welcome to Hangman! Guess letters or attempt the entire word.")
        _play_single_game(game)
        return

    # Otherwise, show the full interactive menu
    print("=" * 60)
    print("WELCOME TO HANGMAN!")
    print("=" * 60)

    mode = _get_game_mode()

    if mode == "multiplayer":
        _play_multiplayer()
        return

    # Single player mode
    difficulty = _get_difficulty()
    theme = _get_theme()
    art_style = _get_art_style()

    # Load words based on selections
    if theme:
        word_list = load_themed_words(theme)
        theme_display = theme
    else:
        word_list = load_words_by_difficulty(difficulty)
        theme_display = None

    game = HangmanGame(word_list, max_attempts=max_attempts, theme=theme_display, hints_enabled=True, art_style=art_style)

    print(f"\nStarting game with {len(word_list)} possible words.")
    print("Type 'hint' at any time to reveal a letter (3 hints available).")
    print("Good luck!\n")

    _play_single_game(game)


def _play_single_game(game: HangmanGame) -> None:
    """Play a single game of hangman."""
    while not (game.is_won() or game.is_lost()):
        print()
        for line in game.status_lines():
            print(line)

        guess = input("Enter a letter, 'hint' for a hint, or guess the word: ").strip().lower()

        if guess == "hint":
            hint = game.get_hint()
            if hint:
                print(f"Hint! The letter '{hint}' has been revealed.")
            else:
                print("No hints available!")
            continue

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
        print(f"\n✓ Congratulations! You guessed '{game.secret_word}'.")
    else:
        print(f"\n✗ Game over! The word was '{game.secret_word}'.")
