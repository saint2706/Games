"""Main entry point for the Tic-Tac-Toe game."""

import sys

from . import play
from .ultimate_cli import play_ultimate

# This script allows the game to be run directly from the command line.
if __name__ == "__main__":
    # Check if user wants ultimate variant
    if len(sys.argv) > 1 and sys.argv[1] in ["--ultimate", "-u"]:
        play_ultimate()
    else:
        # Show option for ultimate variant
        print("Tip: Run with --ultimate or -u for Ultimate Tic-Tac-Toe\n")
        play()
