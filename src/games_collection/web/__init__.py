"""Utilities for adapting the launcher to a web/PyScript environment."""

from __future__ import annotations

from .context import WebLauncherSnapshot, build_web_launcher_snapshot, get_catalogue_payload
from .game_runner import CooperativeGameRunner, GameEvent

__all__ = [
    "WebLauncherSnapshot",
    "build_web_launcher_snapshot",
    "get_catalogue_payload",
    "CooperativeGameRunner",
    "GameEvent",
]
