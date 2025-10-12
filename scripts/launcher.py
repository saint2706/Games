#!/usr/bin/env python3
"""Universal launcher for Games Collection.

This script provides a menu-based interface to launch any game in the collection.
It's used as the entry point for standalone executables.
"""

from __future__ import annotations

import sys
from typing import Callable

# Try to use colorama if available, fall back to plain text
try:
    from colorama import Fore, Style, init as colorama_init

    colorama_init(autoreset=True)
    HAS_COLORAMA = True
except ImportError:
    HAS_COLORAMA = False

    # Define dummy color constants
    class Fore:
        RED = ""
        GREEN = ""
        YELLOW = ""
        BLUE = ""
        MAGENTA = ""
        CYAN = ""
        WHITE = ""

    class Style:
        BRIGHT = ""
        RESET_ALL = ""


def print_header() -> None:
    """Print the launcher header."""
    if HAS_COLORAMA:
        print(f"\n{Fore.CYAN}{Style.BRIGHT}{'=' * 60}")
        print(f"{Fore.CYAN}{Style.BRIGHT}{'GAMES COLLECTION':^60}")
        print(f"{Fore.CYAN}{Style.BRIGHT}{'=' * 60}{Style.RESET_ALL}\n")
    else:
        print("\n" + "=" * 60)
        print(f"{'GAMES COLLECTION':^60}")
        print("=" * 60 + "\n")


def print_menu() -> None:
    """Print the main menu."""
    categories = {
        "Card Games": [
            ("1", "Poker (Texas Hold'em)"),
            ("2", "Blackjack"),
            ("3", "Uno"),
            ("4", "Hearts"),
            ("5", "Spades"),
            ("6", "Bridge"),
            ("7", "Gin Rummy"),
            ("8", "Solitaire"),
            ("9", "Bluff"),
            ("10", "War"),
            ("11", "Go Fish"),
            ("12", "Crazy Eights"),
        ],
        "Paper Games": [
            ("13", "Tic-Tac-Toe"),
            ("14", "Battleship"),
            ("15", "Checkers"),
            ("16", "Connect Four"),
            ("17", "Othello"),
            ("18", "Dots and Boxes"),
            ("19", "Hangman"),
            ("20", "Nim"),
            ("21", "Sudoku"),
            ("22", "Mancala"),
        ],
        "Dice Games": [
            ("23", "Craps"),
            ("24", "Bunco"),
            ("25", "Liar's Dice"),
        ],
        "Word Games": [
            ("26", "Unscramble"),
            ("27", "Wordle"),
        ],
        "Logic Games": [
            ("28", "Mastermind"),
            ("29", "Codebreaker"),
        ],
    }

    for category, games in categories.items():
        if HAS_COLORAMA:
            print(f"{Fore.YELLOW}{Style.BRIGHT}{category}:{Style.RESET_ALL}")
        else:
            print(f"\n{category}:")
        for num, name in games:
            print(f"  {num}. {name}")
        print()

    if HAS_COLORAMA:
        print(f"{Fore.RED}0. Exit{Style.RESET_ALL}\n")
    else:
        print("0. Exit\n")


def launch_game(choice: str) -> bool:
    """Launch the selected game.

    Args:
        choice: The menu choice number

    Returns:
        True to continue, False to exit
    """
    game_map: dict[str, tuple[str, Callable[[], None]]] = {
        "1": ("poker", lambda: __import__("card_games.poker.poker", fromlist=["main"]).main()),
        "2": ("blackjack", lambda: __import__("card_games.blackjack.blackjack", fromlist=["main"]).main()),
        "3": ("uno", lambda: __import__("card_games.uno.uno", fromlist=["main"]).main()),
        "4": ("hearts", lambda: __import__("card_games.hearts.hearts", fromlist=["main"]).main()),
        "5": ("spades", lambda: __import__("card_games.spades.spades", fromlist=["main"]).main()),
        "6": ("bridge", lambda: __import__("card_games.bridge.bridge", fromlist=["main"]).main()),
        "7": ("gin_rummy", lambda: __import__("card_games.gin_rummy.gin_rummy", fromlist=["main"]).main()),
        "8": ("solitaire", lambda: __import__("card_games.solitaire.solitaire", fromlist=["main"]).main()),
        "9": ("bluff", lambda: __import__("card_games.bluff.bluff", fromlist=["main"]).main()),
        "10": ("war", lambda: __import__("card_games.war.war", fromlist=["main"]).main()),
        "11": ("go_fish", lambda: __import__("card_games.go_fish.go_fish", fromlist=["main"]).main()),
        "12": ("crazy_eights", lambda: __import__("card_games.crazy_eights.crazy_eights", fromlist=["main"]).main()),
        "13": ("tic_tac_toe", lambda: __import__("paper_games.tic_tac_toe.tic_tac_toe", fromlist=["main"]).main()),
        "14": ("battleship", lambda: __import__("paper_games.battleship.battleship", fromlist=["main"]).main()),
        "15": ("checkers", lambda: __import__("paper_games.checkers.checkers", fromlist=["main"]).main()),
        "16": ("connect_four", lambda: __import__("paper_games.connect_four.connect_four", fromlist=["main"]).main()),
        "17": ("othello", lambda: __import__("paper_games.othello.othello", fromlist=["main"]).main()),
        "18": ("dots_and_boxes", lambda: __import__("paper_games.dots_and_boxes.dots_and_boxes", fromlist=["main"]).main()),
        "19": ("hangman", lambda: __import__("paper_games.hangman.hangman", fromlist=["main"]).main()),
        "20": ("nim", lambda: __import__("paper_games.nim.nim", fromlist=["main"]).main()),
        "21": ("sudoku", lambda: __import__("paper_games.sudoku.sudoku", fromlist=["main"]).main()),
        "22": ("mancala", lambda: __import__("paper_games.mancala.mancala", fromlist=["main"]).main()),
        "23": ("craps", lambda: __import__("dice_games.craps.craps", fromlist=["main"]).main()),
        "24": ("bunco", lambda: __import__("dice_games.bunco.bunco", fromlist=["main"]).main()),
        "25": ("liars_dice", lambda: __import__("dice_games.liars_dice.liars_dice", fromlist=["main"]).main()),
        "26": ("unscramble", lambda: __import__("word_games.unscramble.unscramble", fromlist=["main"]).main()),
        "27": ("wordle", lambda: __import__("word_games.wordle.wordle", fromlist=["main"]).main()),
        "28": ("mastermind", lambda: __import__("logic_games.mastermind.mastermind", fromlist=["main"]).main()),
        "29": ("codebreaker", lambda: __import__("logic_games.codebreaker.codebreaker", fromlist=["main"]).main()),
    }

    if choice == "0":
        return False

    if choice in game_map:
        game_name, launcher = game_map[choice]
        if HAS_COLORAMA:
            print(f"\n{Fore.GREEN}Launching {game_name}...{Style.RESET_ALL}\n")
        else:
            print(f"\nLaunching {game_name}...\n")
        try:
            launcher()
        except Exception as e:
            if HAS_COLORAMA:
                print(f"\n{Fore.RED}Error launching game: {e}{Style.RESET_ALL}")
            else:
                print(f"\nError launching game: {e}")
        return True
    else:
        if HAS_COLORAMA:
            print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")
        else:
            print("Invalid choice. Please try again.")
        return True


def main() -> None:
    """Main launcher loop."""
    while True:
        print_header()
        print_menu()

        try:
            choice = input("Enter your choice: ").strip()
            if not launch_game(choice):
                if HAS_COLORAMA:
                    print(f"\n{Fore.CYAN}Thank you for playing!{Style.RESET_ALL}\n")
                else:
                    print("\nThank you for playing!\n")
                break
        except KeyboardInterrupt:
            if HAS_COLORAMA:
                print(f"\n\n{Fore.CYAN}Thank you for playing!{Style.RESET_ALL}\n")
            else:
                print("\n\nThank you for playing!\n")
            break
        except EOFError:
            break


if __name__ == "__main__":
    main()
