"""Mobile launchers that wrap the shared Games Collection services."""

from __future__ import annotations

from .kivy_launcher import MobileGameEntry, build_mobile_launcher_app, launch_mobile_launcher

__all__ = [
    "MobileGameEntry",
    "build_mobile_launcher_app",
    "launch_mobile_launcher",
]
