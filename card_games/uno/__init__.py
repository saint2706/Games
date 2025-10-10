"""Uno game implementation with console and GUI front-ends."""

# Public re-exports make it easy for callers to discover the primary
# interfaces without digging through submodules.
from .gui import TkUnoInterface, launch_uno_gui
from .uno import (
    ConsoleUnoInterface,
    PlayerDecision,
    UnoCard,
    UnoDeck,
    UnoGame,
    build_players,
    main,
)

__all__ = [
    "ConsoleUnoInterface",
    "PlayerDecision",
    "TkUnoInterface",
    "UnoCard",
    "UnoDeck",
    "UnoGame",
    "build_players",
    "launch_uno_gui",
    "main",
]
