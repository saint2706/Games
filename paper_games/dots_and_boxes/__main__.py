"""Main entry point for the Dots and Boxes game."""

import argparse
import sys

from . import host_game, join_game, play, play_tournament
from common.gui_framework import load_run_gui

# This script allows the game to be run directly from the command line.
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Play Dots and Boxes against a chain-aware AI.")
    parser.add_argument(
        "--size",
        type=int,
        default=2,
        choices=[2, 3, 4, 5, 6],
        help="Board size (2x2 to 6x6). Default is 2.",
    )
    parser.add_argument("--gui", action="store_true", help="Launch the graphical interface instead of CLI.")
    parser.add_argument(
        "--gui-framework",
        choices=["auto", "pyqt5", "tkinter"],
        default="auto",
        help="Select the GUI backend (default: auto, preferring PyQt5 when available).",
    )
    parser.add_argument(
        "--hints",
        action="store_true",
        help="Enable move hints/suggestions (GUI only).",
    )
    parser.add_argument(
        "--tournament",
        type=int,
        metavar="N",
        help="Play a tournament of N games and track statistics.",
    )
    parser.add_argument(
        "--host",
        action="store_true",
        help="Host a network multiplayer game.",
    )
    parser.add_argument(
        "--join",
        type=str,
        metavar="HOST",
        help="Join a network multiplayer game at HOST address.",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=5555,
        help="Port for network multiplayer (default: 5555).",
    )
    parser.add_argument(
        "--name",
        type=str,
        default="Player",
        help="Your player name for network multiplayer.",
    )
    args = parser.parse_args()

    if args.host:
        host_game(size=args.size, port=args.port, player_name=args.name)
    elif args.join:
        join_game(host=args.join, port=args.port, player_name=args.name)
    elif args.tournament:
        play_tournament(size=args.size, num_games=args.tournament)
    elif args.gui:
        try:
            run_gui, _ = load_run_gui("paper_games.dots_and_boxes", args.gui_framework)
        except RuntimeError as exc:
            if args.gui_framework == "auto":
                print(f"{exc} Falling back to the CLI interface.", file=sys.stderr)
                play(size=args.size)
                return
            raise RuntimeError(str(exc)) from exc

        result = run_gui(size=args.size, show_hints=args.hints)
        if isinstance(result, int) and result != 0:
            sys.exit(result)
    else:
        play(size=args.size)
