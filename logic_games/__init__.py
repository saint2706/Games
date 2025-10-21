"""Compatibility shim exposing logic game packages at the legacy import path."""

from __future__ import annotations

from importlib import import_module
from types import ModuleType
from typing import Iterable

import games_collection.games.logic as _logic_package

__all__ = tuple(getattr(_logic_package, "__all__", ()))


def __getattr__(name: str) -> ModuleType:
    """Defer attribute access to :mod:`games_collection.games.logic`."""

    return getattr(_logic_package, name)


def __dir__() -> Iterable[str]:
    """Return the available attributes for the compatibility package."""

    return sorted(set(__all__) | set(globals()) | set(dir(_logic_package)))


__path__ = list(getattr(_logic_package, "__path__", ()))
__spec__ = getattr(_logic_package, "__spec__", None)
