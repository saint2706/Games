"""Helpers for running games cooperatively within a PyScript session."""

from __future__ import annotations

import builtins
import contextlib
import io
import inspect
import queue
import threading
import traceback
from dataclasses import dataclass
from importlib import import_module
from typing import Callable, Dict, Iterable, Literal, Optional

from games_collection.catalog.registry import GameMetadata, get_game_by_slug


@dataclass(frozen=True)
class GameEvent:
    """Event emitted by :class:`CooperativeGameRunner`."""

    kind: Literal["output", "prompt", "finished", "error"]
    payload: Optional[str] = None


class GameExecutionError(RuntimeError):
    """Raised when the cooperative runner cannot execute a game."""


class _QueueStream(io.TextIOBase):
    """Lightweight ``TextIOBase`` implementation that forwards writes to a queue."""

    def __init__(self, target: "queue.Queue[GameEvent]") -> None:
        super().__init__()
        self._target = target

    def write(self, data: str) -> int:  # type: ignore[override]
        if not data:
            return 0
        self._target.put(GameEvent(kind="output", payload=data))
        return len(data)

    def flush(self) -> None:  # type: ignore[override]
        return None


class CooperativeGameRunner:
    """Run a CLI game inside a worker thread while interacting via queues."""

    _STOP = object()

    def __init__(self, slug: str, settings: Optional[Dict[str, object]] = None) -> None:
        """Initialise the runner for ``slug`` and start the worker thread."""

        metadata = get_game_by_slug(slug)
        if metadata is None:
            raise GameExecutionError(f"Unknown game slug '{slug}'")

        self._settings = settings
        self._launcher = _resolve_entry_point(metadata)
        self._output_queue: "queue.Queue[GameEvent]" = queue.Queue()
        self._input_queue: "queue.Queue[object]" = queue.Queue()
        self._finished = threading.Event()
        self._thread = threading.Thread(target=self._run, name=f"{slug}-runner", daemon=True)
        self._thread.start()

    def send_input(self, value: str) -> None:
        """Deliver user input to the running game."""

        if self._finished.is_set():
            raise GameExecutionError("Cannot send input to a finished game.")
        self._input_queue.put(value)

    def drain_events(self) -> Iterable[GameEvent]:
        """Yield all queued events since the last call."""

        events: list[GameEvent] = []
        while True:
            try:
                events.append(self._output_queue.get_nowait())
            except queue.Empty:
                break
        return events

    def close(self) -> None:
        """Signal the worker to stop and wait for it to finish."""

        if not self._finished.is_set():
            self._input_queue.put(self._STOP)
        self._thread.join(timeout=1)

    @property
    def finished(self) -> bool:
        """Return ``True`` if the worker has completed execution."""

        return self._finished.is_set()

    def _run(self) -> None:
        stdout = _QueueStream(self._output_queue)

        def _cooperative_input(prompt: str = "") -> str:
            self._output_queue.put(GameEvent(kind="prompt", payload=prompt))
            token = self._input_queue.get()
            if token is self._STOP:
                self._finished.set()
                raise GameExecutionError("Game stopped by frontend")
            if not isinstance(token, str):
                raise GameExecutionError("Received unexpected token from input queue")
            return token

        try:
            with contextlib.ExitStack() as stack:
                stack.enter_context(contextlib.redirect_stdout(stdout))
                stack.enter_context(contextlib.redirect_stderr(stdout))
                stack.enter_context(_patched_input(_cooperative_input))
                try:
                    self._launcher(self._settings)
                except SystemExit:
                    pass
        except GameExecutionError as exc:
            self._output_queue.put(GameEvent(kind="error", payload=str(exc)))
        except Exception as exc:  # pragma: no cover - defensive, surfaced to UI
            details = "".join(traceback.format_exception(exc.__class__, exc, exc.__traceback__))
            self._output_queue.put(GameEvent(kind="error", payload=details))
        finally:
            self._finished.set()
            self._output_queue.put(GameEvent(kind="finished"))


def _patched_input(callback: Callable[[str], str]) -> contextlib.AbstractContextManager[None]:
    """Return a context manager that temporarily replaces :func:`input`."""

    class _InputPatch(contextlib.AbstractContextManager[None]):
        def __enter__(self) -> None:
            self._original = builtins.input

            def _wrapped(prompt: str = "", /) -> str:
                return callback(prompt)

            builtins.input = _wrapped

        def __exit__(self, exc_type, exc, exc_tb) -> None:
            builtins.input = self._original
            return None

    return _InputPatch()


def _resolve_entry_point(metadata: GameMetadata) -> Callable[[Optional[Dict[str, object]]], None]:
    """Return a callable that runs the game's registered entry point."""

    module_path, _, attribute = metadata.entry_point.partition(":")
    if not module_path or not attribute:
        raise GameExecutionError(f"Invalid entry point '{metadata.entry_point}' for '{metadata.slug}'")

    signature: Optional[inspect.Signature] = None
    accepts_kwargs = False
    accepts_settings_kw = False
    accepts_config_kw = False

    def _ensure_signature(target: Callable[..., object]) -> None:
        nonlocal signature, accepts_kwargs, accepts_settings_kw, accepts_config_kw
        if signature is not None:
            return
        try:
            signature = inspect.signature(target)
        except (TypeError, ValueError):  # pragma: no cover - builtin/extension entry points
            signature = inspect.Signature()  # type: ignore[assignment]
        accepts_kwargs = any(param.kind == inspect.Parameter.VAR_KEYWORD for param in signature.parameters.values())
        accepts_settings_kw = "settings" in signature.parameters
        accepts_config_kw = "config" in signature.parameters

    def _invoke(settings: Optional[Dict[str, object]] = None) -> None:
        module = import_module(module_path)
        target = getattr(module, attribute)
        _ensure_signature(target)
        kwargs: Dict[str, object] = {}
        if settings:
            if accepts_settings_kw or accepts_kwargs:
                kwargs["settings"] = settings
            elif accepts_config_kw or accepts_kwargs:
                kwargs["config"] = settings
        target(**kwargs)

    return _invoke
