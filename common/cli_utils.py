"""Compatibility wrapper for legacy ``common.cli_utils`` imports."""

from __future__ import annotations

from games_collection.core.cli_utils import *  # noqa: F401,F403

# ``cli_utils`` in ``games_collection.core`` does not expose ``__all__`` so we
# derive it from the imported namespace to keep ``from common.cli_utils import *``
# semantics for downstream consumers that still rely on the legacy path.
__all__ = [name for name in globals() if not name.startswith("_")]
