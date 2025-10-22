"""Compatibility wrapper for the legacy ``scripts.launcher`` import path."""

from __future__ import annotations

from importlib import import_module
from typing import Any

_launcher = import_module("games_collection.launcher")

__all__ = [name for name in dir(_launcher) if not name.startswith("_")]

globals().update({name: getattr(_launcher, name) for name in __all__})


def __getattr__(name: str) -> Any:
    """Forward attribute access to :mod:`games_collection.launcher`."""

    return getattr(_launcher, name)


def __dir__() -> list[str]:
    """Return attributes provided by the wrapped launcher module."""

    return sorted(__all__)


if __name__ == "__main__":  # pragma: no cover - exercised by smoke tests
    raise SystemExit(_launcher.main())
