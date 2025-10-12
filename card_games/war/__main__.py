"""Entry point for War card game."""

from __future__ import annotations

import argparse
import random
import time

from card_games.war.cli import STATS_AVAILABLE, game_loop
from card_games.war.game import WarGame

if STATS_AVAILABLE:
    from card_games.common.stats import CardGameStats


def main() -> None:
    """Main entry point for the War game."""
    parser = argparse.ArgumentParser(description="Play the card game War")
    parser.add_argument("--seed", type=int, help="Random seed for reproducible games")
    parser.add_argument("--auto", action="store_true", help="Automatically play all rounds")
    parser.add_argument("--delay", type=float, default=0.5, help="Delay between rounds in auto mode (seconds)")
    parser.add_argument("--no-stats", action="store_true", help="Disable statistics tracking")
    parser.add_argument("--show-stats", action="store_true", help="Show player statistics and exit")
    parser.add_argument("--leaderboard", action="store_true", help="Show leaderboard and exit")
    parser.add_argument("--player", type=str, help="Player name to show stats for (use with --show-stats)")
    args = parser.parse_args()

    # Handle stats display commands
    if STATS_AVAILABLE:
        if args.leaderboard:
            stats = CardGameStats("war")
            stats.display_leaderboard()
            return

        if args.show_stats:
            stats = CardGameStats("war")
            player_name = args.player or "Player 1"
            stats.display_player_stats(player_name)
            return

    rng = None
    if args.seed is not None:
        rng = random.Random(args.seed)

    start_time = time.time()
    game = WarGame(rng=rng)
    game_loop(game, auto_play=args.auto, delay=args.delay, track_stats=not args.no_stats, start_time=start_time)


if __name__ == "__main__":
    main()
