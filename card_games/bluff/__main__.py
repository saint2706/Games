"""Main entry point for running the Bluff card game.

This script serves as the executable entry point for the Bluff game, allowing
it to be run directly using the ``-m`` flag with Python. For example:

    python -m card_games.bluff --difficulty Hard

It simply imports and calls the ``main`` function from the ``bluff`` module.
"""

from .bluff import main


if __name__ == "__main__":  # pragma: no cover - script entry point
    main()
