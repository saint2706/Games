"""Entry point for running blackjack via ``python -m card_games.blackjack``."""

from __future__ import annotations

import argparse
from typing import Iterable

from card_games.blackjack.cli import game_loop
from card_games.blackjack.game import BlackjackGame
from card_games.blackjack.gui import run_app


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Play blackjack against the dealer using a GUI or CLI interface.",
    )
    parser.add_argument("--bankroll", type=int, default=500, help="Starting bankroll (default: 500)")
    parser.add_argument("--min-bet", type=int, default=10, help="Minimum bet size (default: 10)")
    parser.add_argument("--decks", type=int, default=6, help="Number of decks in the shoe (default: 6)")
    parser.add_argument("--seed", type=int, help="Optional random seed for deterministic shuffles")
    parser.add_argument(
        "--cli",
        action="store_true",
        help="Launch the text-based interface instead of the graphical table.",
    )
    return parser


def main(argv: Iterable[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

    rng = None
    if args.seed is not None:
        import random

        rng = random.Random(args.seed)

    if args.cli:
        game = BlackjackGame(bankroll=args.bankroll, min_bet=args.min_bet, decks=args.decks, rng=rng)
        game_loop(game)
    else:
        run_app(bankroll=args.bankroll, min_bet=args.min_bet, decks=args.decks, rng=rng)


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()
