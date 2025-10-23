"""Compatibility shim that exposes the src-installed games_collection package."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

_SRC_ROOT = Path(__file__).resolve().parent.parent / "src" / "games_collection"
_SPEC = importlib.util.spec_from_file_location(__name__, _SRC_ROOT / "__init__.py")
if _SPEC is None or _SPEC.loader is None:  # pragma: no cover - defensive guard
    raise ImportError("Unable to load games_collection package from src directory")
_MODULE = importlib.util.module_from_spec(_SPEC)
sys.modules[__name__] = _MODULE
_SPEC.loader.exec_module(_MODULE)

globals().update(_MODULE.__dict__)
