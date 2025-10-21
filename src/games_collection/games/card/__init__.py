"""A collection of interactive, text-based and GUI-based card game implementations.

This package provides a suite of classic card games, each with its own engine,
bot AI, and user interface. The games included are:
- Blackjack
- Bluff (also known as Cheat or I Doubt It)
- Poker (Texas Hold'em)
- Uno

Each game can be run as a standalone application from the command line.
"""

# Export the subpackages so compatibility shims and discovery helpers work
# without manual maintenance.
from games_collection.catalog.registry import iter_genre

__all__ = [metadata.slug for metadata in iter_genre("card")]
