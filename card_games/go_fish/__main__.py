"""Entry point for Go Fish card game."""

from __future__ import annotations

import argparse
import random

from card_games.go_fish.cli import game_loop
from card_games.go_fish.game import GoFishGame
from common.gui_framework import load_run_gui


def main() -> None:
    """Main entry point for the Go Fish game."""
    parser = argparse.ArgumentParser(description="Play the card game Go Fish")
    parser.add_argument("--players", type=int, default=2, choices=range(2, 7), help="Number of players (2-6)")
    parser.add_argument("--seed", type=int, help="Random seed for reproducible games")
    parser.add_argument("--names", nargs="+", help="Player names")
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument("--cli", action="store_true", help="Launch the text-based interface")
    mode_group.add_argument("--gui", action="store_true", help="Launch the graphical interface (default)")
    parser.add_argument(
        "--gui-framework",
        choices=["auto", "pyqt5", "tkinter"],
        default="auto",
        help="Select the GUI backend (default: auto, preferring PyQt5 when available).",
    )
    args = parser.parse_args()

    rng = None
    if args.seed is not None:
        rng = random.Random(args.seed)

    player_names = args.names if args.names else None
    game_kwargs = {"num_players": args.players, "player_names": player_names, "rng": rng}

    use_gui = args.gui or not args.cli

    if use_gui:
        try:
            run_gui, _ = load_run_gui("card_games.go_fish", args.gui_framework)
        except RuntimeError as exc:
            if args.gui_framework == "auto":
                print(f"{exc} Falling back to the CLI interface.")
                use_gui = False
            else:
                raise RuntimeError(str(exc)) from exc
        else:
            game = GoFishGame(**game_kwargs)
            result = run_gui(game=game)
            if isinstance(result, int) and result != 0:
                import sys

                sys.exit(result)
            return

    game = GoFishGame(**game_kwargs)
    game_loop(game)


if __name__ == "__main__":
    main()
