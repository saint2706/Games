"""Compatibility shim exposing word game packages at the legacy import path."""

from __future__ import annotations

from importlib import import_module
from types import ModuleType
from typing import Iterable

import games_collection.games.word as _word_package

__all__ = tuple(getattr(_word_package, "__all__", ()))


def __getattr__(name: str) -> ModuleType:
    """Defer attribute access to :mod:`games_collection.games.word`."""

    return getattr(_word_package, name)


def __dir__() -> Iterable[str]:
    """Return the available attributes for the compatibility package."""

    return sorted(set(__all__) | set(globals()) | set(dir(_word_package)))


__path__ = list(getattr(_word_package, "__path__", ()))
__spec__ = getattr(_word_package, "__spec__", None)
