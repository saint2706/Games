"""Entry point for War card game."""

from __future__ import annotations

import argparse
import random

from card_games.war.cli import game_loop
from card_games.war.game import WarGame


def main() -> None:
    """Main entry point for the War game."""
    parser = argparse.ArgumentParser(description="Play the card game War")
    parser.add_argument("--seed", type=int, help="Random seed for reproducible games")
    parser.add_argument("--auto", action="store_true", help="Automatically play all rounds")
    parser.add_argument("--delay", type=float, default=0.5, help="Delay between rounds in auto mode (seconds)")
    args = parser.parse_args()

    rng = None
    if args.seed is not None:
        rng = random.Random(args.seed)

    game = WarGame(rng=rng)
    game_loop(game, auto_play=args.auto, delay=args.delay)


if __name__ == "__main__":
    main()
