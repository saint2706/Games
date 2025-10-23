"""PyScript bootstrap helpers exposing launcher data and game runners."""

from __future__ import annotations

import uuid
from typing import Dict, List, MutableMapping

from games_collection.core.challenges import get_default_challenge_manager
from games_collection.core.daily_challenges import DailyChallengeScheduler
from games_collection.core.profile_service import ProfileService, get_profile_service
from games_collection.web import CooperativeGameRunner, GameEvent, build_web_launcher_snapshot, get_catalogue_payload

__all__ = [
    "get_launcher_payload",
    "get_catalogue_payload",
    "start_game",
    "send_input",
    "poll_events",
    "close_game",
]


_PROFILE_SERVICE: ProfileService = get_profile_service()
_SCHEDULER = DailyChallengeScheduler(get_default_challenge_manager())
_RUNNERS: MutableMapping[str, CooperativeGameRunner] = {}


def get_launcher_payload() -> Dict[str, object]:
    """Return the launcher snapshot as a mapping."""

    snapshot = build_web_launcher_snapshot(_PROFILE_SERVICE, _SCHEDULER)
    return snapshot.to_payload()


def start_game(slug: str) -> Dict[str, object]:
    """Start ``slug`` and return the session identifier plus initial events."""

    session_id = str(uuid.uuid4())
    runner = CooperativeGameRunner(slug)
    _RUNNERS[session_id] = runner
    return {"session_id": session_id, "events": _drain_events(session_id)}


def send_input(session_id: str, value: str) -> List[Dict[str, object]]:
    """Deliver ``value`` to the active runner identified by ``session_id``."""

    runner = _RUNNERS.get(session_id)
    if runner is None:
        raise KeyError(f"Unknown session '{session_id}'")
    runner.send_input(value)
    return _drain_events(session_id)


def poll_events(session_id: str) -> List[Dict[str, object]]:
    """Return accumulated events for ``session_id`` and close finished sessions."""

    return _drain_events(session_id)


def close_game(session_id: str) -> None:
    """Stop and dispose the runner identified by ``session_id``."""

    runner = _RUNNERS.pop(session_id, None)
    if runner is not None:
        runner.close()


def _drain_events(session_id: str) -> List[Dict[str, object]]:
    runner = _RUNNERS.get(session_id)
    if runner is None:
        return []
    events = [_event_to_mapping(event) for event in runner.drain_events()]
    if runner.finished:
        runner.close()
        _RUNNERS.pop(session_id, None)
    return events


def _event_to_mapping(event: GameEvent) -> Dict[str, object]:
    return {"kind": event.kind, "payload": event.payload}
