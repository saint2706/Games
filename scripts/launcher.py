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
            ("13", "Cribbage"),
            ("14", "Euchre"),
            ("15", "Rummy 500"),
        ],
        "Paper Games": [
            ("16", "Tic-Tac-Toe"),
            ("17", "Battleship"),
            ("18", "Checkers"),
            ("19", "Connect Four"),
            ("20", "Othello"),
            ("21", "Dots and Boxes"),
            ("22", "Hangman"),
            ("23", "Nim"),
            ("24", "Sudoku"),
            ("25", "Mancala"),
        ],
        "Dice Games": [
            ("26", "Craps"),
            ("27", "Bunco"),
            ("28", "Liar's Dice"),
        ],
        "Word Games": [
            ("29", "Unscramble"),
            ("30", "Wordle"),
        ],
        "Logic Games": [
            ("31", "Mastermind"),
            ("32", "Codebreaker"),
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
        "1": ("poker", lambda: __import__("card_games.poker.__main__", fromlist=["main"]).main()),
        "2": ("blackjack", lambda: __import__("card_games.blackjack.__main__", fromlist=["main"]).main()),
        "3": ("uno", lambda: __import__("card_games.uno.__main__", fromlist=["main"]).main()),
        "4": ("hearts", lambda: __import__("card_games.hearts.__main__", fromlist=["main"]).main()),
        "5": ("spades", lambda: __import__("card_games.spades.__main__", fromlist=["main"]).main()),
        "6": ("bridge", lambda: __import__("card_games.bridge.__main__", fromlist=["main"]).main()),
        "7": ("gin_rummy", lambda: __import__("card_games.gin_rummy.__main__", fromlist=["main"]).main()),
        "8": ("solitaire", lambda: __import__("card_games.solitaire.__main__", fromlist=["main"]).main()),
        "9": ("bluff", lambda: __import__("card_games.bluff.__main__", fromlist=["main"]).main()),
        "10": ("war", lambda: __import__("card_games.war.__main__", fromlist=["main"]).main()),
        "11": ("go_fish", lambda: __import__("card_games.go_fish.__main__", fromlist=["main"]).main()),
        "12": ("crazy_eights", lambda: __import__("card_games.crazy_eights.__main__", fromlist=["main"]).main()),
        "13": ("cribbage", lambda: __import__("card_games.cribbage.__main__", fromlist=["main"]).main()),
        "14": ("euchre", lambda: __import__("card_games.euchre.__main__", fromlist=["main"]).main()),
        "15": ("rummy500", lambda: __import__("card_games.rummy500.__main__", fromlist=["main"]).main()),
        "16": ("tic_tac_toe", lambda: __import__("paper_games.tic_tac_toe.__main__", fromlist=["main"]).main()),
        "17": ("battleship", lambda: __import__("paper_games.battleship.__main__", fromlist=["main"]).main()),
        "18": ("checkers", lambda: __import__("paper_games.checkers.__main__", fromlist=["main"]).main()),
        "19": ("connect_four", lambda: __import__("paper_games.connect_four.__main__", fromlist=["main"]).main()),
        "20": ("othello", lambda: __import__("paper_games.othello.__main__", fromlist=["main"]).main()),
        "21": ("dots_and_boxes", lambda: __import__("paper_games.dots_and_boxes.__main__", fromlist=["main"]).main()),
        "22": ("hangman", lambda: __import__("paper_games.hangman.__main__", fromlist=["main"]).main()),
        "23": ("nim", lambda: __import__("paper_games.nim.__main__", fromlist=["main"]).main()),
        "24": ("sudoku", lambda: __import__("paper_games.sudoku.__main__", fromlist=["main"]).main()),
        "25": ("mancala", lambda: __import__("paper_games.mancala.__main__", fromlist=["main"]).main()),
        "26": ("craps", lambda: __import__("dice_games.craps.__main__", fromlist=["main"]).main()),
        "27": ("bunco", lambda: __import__("dice_games.bunco.__main__", fromlist=["main"]).main()),
        "28": ("liars_dice", lambda: __import__("dice_games.liars_dice.__main__", fromlist=["main"]).main()),
        "29": ("unscramble", lambda: __import__("word_games.unscramble.__main__", fromlist=["main"]).main()),
        "30": ("wordle", lambda: __import__("word_games.wordle.__main__", fromlist=["main"]).main()),
        "31": ("mastermind", lambda: __import__("logic_games.mastermind.__main__", fromlist=["main"]).main()),
        "32": ("codebreaker", lambda: __import__("logic_games.codebreaker.__main__", fromlist=["main"]).main()),
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
