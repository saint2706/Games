"""Utilities for discovering and loading GUI frameworks.

The helper functions in this module provide a consistent way to detect GUI
framework availability and to dynamically import GUI launchers for games. They
centralize the logic for preferring PyQt5 when it is available while keeping
support for Tkinter-based interfaces that still exist throughout the codebase.
"""

from __future__ import annotations

from importlib import import_module, util
from typing import Callable, Iterable, List, Optional, Tuple

FrameworkName = str

_FRAMEWORK_PACKAGE_MAP = {
    "pyqt5": "PyQt5",
    "tkinter": "tkinter",
}

_FRAMEWORK_MODULE_SUFFIX = {
    "pyqt5": "gui_pyqt",
    "tkinter": "gui",
}

_PREFERRED_ORDER: Tuple[FrameworkName, FrameworkName] = ("pyqt5", "tkinter")

_INSTALL_HINT = (
    "Install the 'games-collection[gui]' extra to add PyQt5 or ensure Tkinter is "
    "installed on your system."
)


def available_frameworks() -> List[FrameworkName]:
    """Return the GUI frameworks that can be imported in the current environment."""

    available: List[FrameworkName] = []
    for name, package in _FRAMEWORK_PACKAGE_MAP.items():
        if util.find_spec(package) is not None:
            available.append(name)
    return available


def _implemented_frameworks(module_base: str) -> List[FrameworkName]:
    """Return the frameworks that have a GUI module in the specified package."""

    implemented: List[FrameworkName] = []
    for name, suffix in _FRAMEWORK_MODULE_SUFFIX.items():
        if util.find_spec(f"{module_base}.{suffix}") is not None:
            implemented.append(name)
    return implemented


def _resolve_runner(module_name: str) -> Callable[..., object]:
    """Return the callable entry point exposed by the GUI module."""

    module = import_module(module_name)
    for attribute in ("run_app", "run_gui", "main"):
        runner = getattr(module, attribute, None)
        if callable(runner):
            return runner
    raise RuntimeError(f"Module '{module_name}' does not expose a GUI entry point.")


def _attempt_load(module_base: str, framework: FrameworkName) -> Optional[Callable[..., object]]:
    """Try importing the GUI module for the requested framework."""

    module_name = f"{module_base}.{_FRAMEWORK_MODULE_SUFFIX[framework]}"
    try:
        return _resolve_runner(module_name)
    except (ImportError, RuntimeError):
        return None


def _format_framework_list(items: Iterable[FrameworkName]) -> str:
    """Return a comma-separated list of frameworks or 'none'."""

    values = list(items)
    return ", ".join(values) if values else "none"


def _display_name(framework: FrameworkName) -> str:
    """Return a human-readable name for a framework."""

    return "PyQt5" if framework == "pyqt5" else "Tkinter"


def load_run_gui(module_base: str, framework: FrameworkName) -> Tuple[Callable[..., object], FrameworkName]:
    """Load the GUI launcher for a game module.

    Args:
        module_base: Dotted path to the game package (for example,
            ``"card_games.blackjack"``).
        framework: Requested GUI framework. Supported values are ``"auto"``,
            ``"pyqt5"``, and ``"tkinter"``.

    Returns:
        A tuple containing the callable that launches the GUI and the framework
        name that was used.

    Raises:
        RuntimeError: When the requested framework (or any framework in
            ``auto`` mode) cannot be loaded.
        ValueError: If an unsupported framework name is provided.
    """

    requested = framework.lower()
    if requested not in {"auto", "pyqt5", "tkinter"}:
        raise ValueError("framework must be one of: auto, pyqt5, tkinter")

    implemented = _implemented_frameworks(module_base)
    system_available = available_frameworks()

    if requested == "auto":
        for candidate in _PREFERRED_ORDER:
            runner = _attempt_load(module_base, candidate)
            if runner is not None:
                return runner, candidate

        if not system_available:
            raise RuntimeError(
                "No GUI frameworks are available (PyQt5 or Tkinter). " f"{_INSTALL_HINT}"
            )

        if not implemented:
            raise RuntimeError(
                f"The package '{module_base}' does not include PyQt5 or Tkinter GUIs. "
                f"Detected frameworks on this system: {_format_framework_list(system_available)}."
            )

        raise RuntimeError(
            "Unable to load a GUI for the available frameworks. "
            f"Implemented frameworks: {_format_framework_list(implemented)}. "
            f"Available in the environment: {_format_framework_list(system_available)}."
        )

    runner = _attempt_load(module_base, requested)
    if runner is not None:
        return runner, requested

    if requested not in implemented:
        alternative = "tkinter" if requested == "pyqt5" else "pyqt5"
        if alternative in implemented:
            raise RuntimeError(
                f"The package '{module_base}' does not provide a {_display_name(requested)} GUI yet. "
                f"Try --gui-framework {alternative}."
            )

    if requested not in system_available:
        raise RuntimeError(f"{_display_name(requested)} is not available in this environment. {_INSTALL_HINT}")

    raise RuntimeError(
        f"Failed to load the {_display_name(requested)} GUI for '{module_base}'. "
        f"Implemented frameworks: {_format_framework_list(implemented)}."
    )
