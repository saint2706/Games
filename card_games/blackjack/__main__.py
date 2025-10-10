"""Main entry point for the Blackjack game application.

This script allows the Blackjack game to be run as a standalone application
either through a command-line interface (CLI) or a graphical user interface (GUI).
It handles command-line argument parsing to configure the game settings and to
choose the interface.

To run the GUI (default):
    python -m card_games.blackjack

To run the CLI:
    python -m card_games.blackjack --cli
"""

from __future__ import annotations

import argparse
from typing import Iterable

from card_games.blackjack.cli import game_loop
from card_games.blackjack.game import BlackjackGame

# Attempt to import the GUI components, but degrade gracefully if Tkinter is not available.
try:  # pragma: no cover - optional GUI dependency
    from card_games.blackjack.gui import run_app

    _GUI_IMPORT_ERROR: Exception | None = None
except ImportError as exc:  # pragma: no cover - degrade gracefully without Tk
    run_app = None
    _GUI_IMPORT_ERROR = exc


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser for the Blackjack application.

    Returns:
        argparse.ArgumentParser: The configured argument parser.
    """
    parser = argparse.ArgumentParser(
        description="Play blackjack against the dealer using a GUI or CLI interface.",
    )
    parser.add_argument(
        "--bankroll", type=int, default=500, help="Starting bankroll (default: 500)"
    )
    parser.add_argument(
        "--min-bet", type=int, default=10, help="Minimum bet size (default: 10)"
    )
    parser.add_argument(
        "--decks", type=int, default=6, help="Number of decks in the shoe (default: 6)"
    )
    parser.add_argument(
        "--seed", type=int, help="Optional random seed for deterministic shuffles"
    )
    parser.add_argument(
        "--cli",
        action="store_true",
        help="Launch the text-based interface instead of the graphical table.",
    )
    return parser


def main(argv: Iterable[str] | None = None) -> None:
    """The main function for the Blackjack application.

    Parses command-line arguments and launches the appropriate interface (GUI or CLI).

    Args:
        argv (Iterable[str] | None): Command-line arguments to parse.
    """
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

    # Initialize a random number generator if a seed is provided
    rng = None
    if args.seed is not None:
        import random

        # As in the CLI, use a dedicated RNG so deterministic sessions do not
        # interfere with global randomness in other modules.
        rng = random.Random(args.seed)

    # Launch either the CLI or GUI based on the --cli flag
    if args.cli:
        game = BlackjackGame(
            bankroll=args.bankroll, min_bet=args.min_bet, decks=args.decks, rng=rng
        )
        game_loop(game)
    else:
        if run_app is None:
            # If GUI is requested but not available, raise an error.
            raise RuntimeError(
                "Tkinter is required for the blackjack GUI but is not available."
            ) from _GUI_IMPORT_ERROR
        run_app(bankroll=args.bankroll, min_bet=args.min_bet, decks=args.decks, rng=rng)


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()
