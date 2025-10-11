"""Entry point for Solitaire (Klondike) game."""

from __future__ import annotations

import argparse
import random

from card_games.solitaire.cli import game_loop
from card_games.solitaire.game import SolitaireGame


def main() -> None:
    """Main entry point for the Solitaire game."""
    parser = argparse.ArgumentParser(description="Play Klondike Solitaire")
    parser.add_argument("--seed", type=int, help="Random seed for reproducible games")
    args = parser.parse_args()

    rng = None
    if args.seed is not None:
        rng = random.Random(args.seed)

    game = SolitaireGame(rng=rng)
    game_loop(game)


if __name__ == "__main__":
    main()
