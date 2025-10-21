"""Compatibility shim exposing shared utilities at the legacy :mod:`common` path."""

from __future__ import annotations

from importlib import import_module
from types import ModuleType
from typing import Iterable

import games_collection.core as _core_package

__all__ = tuple(getattr(_core_package, "__all__", ()))


def __getattr__(name: str) -> ModuleType:
    """Defer attribute access to :mod:`games_collection.core`."""

    return getattr(_core_package, name)


def __dir__() -> Iterable[str]:
    """Return the available attributes for the compatibility package."""

    return sorted(set(__all__) | set(globals()) | set(dir(_core_package)))


__path__ = list(getattr(_core_package, "__path__", ()))
__spec__ = getattr(_core_package, "__spec__", None)
