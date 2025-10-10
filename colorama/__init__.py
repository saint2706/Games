"""Minimal subset of the colorama API for environments without the dependency."""

__all__ = ["Fore", "Style", "init"]

RESET_ALL = "\033[0m"
BRIGHT = "\033[1m"


class _Fore:
    """Namespace object matching the real Colorama ``Fore`` constants."""

    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"


class _Style:
    """Namespace object matching the real Colorama ``Style`` constants."""

    RESET_ALL = RESET_ALL
    BRIGHT = BRIGHT


Fore = _Fore()
Style = _Style()


def init(*, autoreset: bool = True) -> None:  # pragma: no cover - no-op shim
    # The real colorama installs console hooks on Windows; for ANSI-capable
    # environments we can safely do nothing.
    return None
