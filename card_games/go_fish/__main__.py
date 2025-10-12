"""Entry point for Go Fish card game."""

from __future__ import annotations

import argparse
import random

from card_games.go_fish.cli import game_loop
from card_games.go_fish.game import GoFishGame


def main() -> None:
    """Main entry point for the Go Fish game."""
    parser = argparse.ArgumentParser(description="Play the card game Go Fish")
    parser.add_argument("--players", type=int, default=2, choices=range(2, 7), help="Number of players (2-6)")
    parser.add_argument("--seed", type=int, help="Random seed for reproducible games")
    parser.add_argument("--names", nargs="+", help="Player names")
    args = parser.parse_args()

    rng = None
    if args.seed is not None:
        rng = random.Random(args.seed)

    player_names = args.names if args.names else None
    game = GoFishGame(num_players=args.players, player_names=player_names, rng=rng)
    game_loop(game)


if __name__ == "__main__":
    main()
