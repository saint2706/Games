"""Tests covering the GUI launcher dispatcher and bootstrap helpers."""

from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Optional

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from games_collection import launcher
from games_collection import launcher_gui
from games_collection.core.profile_service import RecentlyPlayedEntry


class DummyAchievementManager:
    """Minimal achievement manager used for snapshot construction."""

    def get_unlocked_count(self) -> int:
        """Return zero unlocked achievements for test profiles."""

        return 0

    def get_total_count(self) -> int:
        """Return zero total achievements for test profiles."""

        return 0

    def get_total_points(self) -> int:
        """Return zero achievement points."""

        return 0


class DummyDailyProgress:
    """Stub daily challenge progress supporting snapshot computations."""

    def is_completed(self, *_: object) -> bool:
        """Return ``False`` to mark challenges as pending."""

        return False

    @property
    def current_streak(self) -> int:
        """Return the current streak length."""

        return 0

    @property
    def best_streak(self) -> int:
        """Return the best streak length."""

        return 0

    @property
    def total_completed(self) -> int:
        """Return the total number of completed challenges."""

        return 0


class DummyProfile:
    """Profile stub exposing the attributes used by the launcher."""

    player_id = "default"
    display_name = "Default"
    level = 1
    experience = 0
    achievement_manager = DummyAchievementManager()
    daily_challenge_progress = DummyDailyProgress()

    def experience_to_next_level(self) -> int:
        """Return the remaining experience until the next level."""

        return 100


class DummyScheduler:
    """Scheduler stub that always returns the same challenge summary."""

    def __init__(self, *_: object, **__: object) -> None:
        self._selection = SimpleNamespace(summary=self._summary, target_date=object())

    def _summary(self) -> str:
        """Return a static summary string."""

        return "Demo Challenge"

    def get_challenge_for_date(self) -> SimpleNamespace:
        """Return a predictable daily challenge selection."""

        return self._selection


class DummyProfileService:
    """Profile service stub that tracks save calls."""

    def __init__(self, profile_dir):
        self.profile_dir = profile_dir
        self.active_profile = DummyProfile()
        self._saved = 0
        self._recently_played_limit: Optional[int] = None
        self._favorites: list[str] = []
        self._quick_launches: dict[str, str] = {}

    def save_active_profile(self) -> None:
        """Record that the profile would be saved."""

        self._saved += 1

    def summary(self) -> str:
        """Return a lightweight profile summary."""

        return "Profile summary"

    def get_recently_played(self, limit: int = 5):  # noqa: D401 - simple stub
        """Return an empty recently played list while capturing the requested limit."""

        self._recently_played_limit = limit
        return []

    def get_favorites(self):  # noqa: D401 - simple stub
        """Return the stubbed favorites list."""

        return list(self._favorites)

    def is_favorite(self, slug: str) -> bool:
        """Return whether ``slug`` is in the favorites list."""

        return slug in self._favorites

    def mark_favorite(self, slug: str) -> bool:
        """Append ``slug`` to the favorites list when absent."""

        if slug in self._favorites:
            return False
        self._favorites.append(slug)
        return True

    def unmark_favorite(self, slug: str) -> bool:
        """Remove ``slug`` from the favorites list when present."""

        if slug not in self._favorites:
            return False
        self._favorites = [entry for entry in self._favorites if entry != slug]
        return True

    def toggle_favorite(self, slug: str) -> bool:
        """Toggle membership of ``slug`` returning the new state."""

        if self.unmark_favorite(slug):
            return False
        self.mark_favorite(slug)
        return True

    def get_quick_launch_aliases(self) -> dict[str, str]:
        """Return configured quick-launch aliases."""

        return dict(self._quick_launches)

    def resolve_quick_launch_alias(self, alias: str) -> Optional[str]:
        """Resolve ``alias`` to a configured slug."""

        return self._quick_launches.get(alias)


def test_run_launcher_gui_invokes_preferred_framework(monkeypatch):
    """``run_launcher_gui`` delegates to ``launch_preferred_gui`` with PyQt."""

    calls: dict[str, object] = {}

    def fake_build(service, scheduler):  # noqa: ANN001
        def launcher_callable() -> None:
            calls["invoked"] = True

        calls["service"] = service
        calls["scheduler"] = scheduler
        return launcher_callable

    monkeypatch.setattr(launcher_gui, "_build_pyqt_launcher", fake_build)

    def fake_launch_preferred_gui(*, preferred, tkinter_launcher, pyqt_launcher):  # noqa: ANN001
        calls["preferred"] = preferred
        assert tkinter_launcher is None
        assert callable(pyqt_launcher)
        pyqt_launcher()
        return True, "pyqt5"

    monkeypatch.setattr(launcher_gui, "launch_preferred_gui", fake_launch_preferred_gui)

    result = launcher_gui.run_launcher_gui(object(), object(), preferred_framework="pyqt5")

    assert result is True
    assert calls["preferred"] == "pyqt5"
    assert calls["invoked"] is True


def test_main_launches_gui_when_requested(monkeypatch, tmp_path):
    """The CLI dispatcher hands off control to the GUI when requested."""

    args = SimpleNamespace(
        game=None,
        gui_framework="pyqt5",
        smoke_test=False,
        profile=None,
        profile_display_name=None,
        profile_rename=None,
        profile_reset=False,
        profile_summary=False,
        ui="gui",
        quick=None,
    )

    monkeypatch.setattr(launcher, "parse_args", lambda: args)

    profile_service = DummyProfileService(tmp_path / "profiles")
    profile_service.profile_dir.mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr(launcher, "get_profile_service", lambda: profile_service)
    monkeypatch.setattr(launcher, "get_default_challenge_manager", lambda: object())

    dummy_scheduler = DummyScheduler()
    monkeypatch.setattr(launcher, "DailyChallengeScheduler", lambda *_, **__: dummy_scheduler)

    gui_calls: dict[str, object] = {}

    def fake_run_launcher_gui(service, scheduler, preferred_framework=None):  # noqa: ANN001
        gui_calls["service"] = service
        gui_calls["scheduler"] = scheduler
        gui_calls["preferred"] = preferred_framework
        return True

    monkeypatch.setattr(launcher_gui, "run_launcher_gui", fake_run_launcher_gui)

    def fail_print(*_args, **_kwargs):  # noqa: ANN001
        raise AssertionError("CLI loop should not run when GUI is available")

    monkeypatch.setattr(launcher, "print_header", fail_print)
    monkeypatch.setattr(launcher, "print_menu", fail_print)
    monkeypatch.setattr("builtins.input", fail_print)

    launcher.main()

    assert gui_calls["service"] is profile_service
    assert gui_calls["scheduler"] is dummy_scheduler
    assert gui_calls["preferred"] == "pyqt5"
    assert profile_service._saved == 1


def test_build_pyqt_launcher_handles_missing_dependencies(monkeypatch):
    """``_build_pyqt_launcher`` returns ``None`` when PyQt5 is unavailable."""

    monkeypatch.setattr(launcher_gui, "PYQT5_AVAILABLE", False)

    result = launcher_gui._build_pyqt_launcher(object(), object())

    assert result is None


def test_print_menu_renders_favorites_and_recently_played(monkeypatch, capsys):
    """The CLI menu highlights favorites and the recently played section."""

    monkeypatch.setattr(launcher, "HAS_COLORAMA", False)

    class StubService:
        def __init__(self) -> None:
            self.requested_limit: Optional[int] = None
            self.favorites_requested = False
            self.quick_aliases = {"speed": "tic_tac_toe"}

        def get_favorites(self):  # noqa: D401 - simple stub
            """Return a deterministic favorites list."""

            self.favorites_requested = True
            return ["tic_tac_toe"]

        def get_recently_played(self, limit: int = 5):  # noqa: D401 - simple stub
            """Return a deterministic recently played entry."""

            self.requested_limit = limit
            return [RecentlyPlayedEntry(game_id="tic_tac_toe", last_played="2024-05-01T12:30:00")]

        def get_quick_launch_aliases(self):  # noqa: D401 - simple stub
            """Return a deterministic quick-launch alias mapping."""

            return dict(self.quick_aliases)

    service = StubService()

    launcher.print_menu(service)  # type: ignore[arg-type]
    output = capsys.readouterr().out

    assert service.requested_limit == 5
    assert service.favorites_requested is True
    assert "Favorite Games:" in output
    assert "★ Tic-Tac-Toe" in output
    assert "Recently Played:" in output
    assert "Tic-Tac-Toe" in output
    assert "2024-05-01 12:30" in output
    assert "Configuration:" in output
    assert "Manage game settings" in output
    assert "Quick Launch Shortcuts:" in output
    assert "!speed" in output


def test_launch_game_supports_favorite_toggle(monkeypatch, capsys):
    """The CLI dispatcher supports toggling favorites via the FAV command."""

    monkeypatch.setattr(launcher, "HAS_COLORAMA", False)

    class StubService:
        def __init__(self) -> None:
            self.favorites: set[str] = set()

        def is_favorite(self, slug: str) -> bool:
            return slug in self.favorites

        def toggle_favorite(self, slug: str) -> bool:
            if slug in self.favorites:
                self.favorites.remove(slug)
                return False
            self.favorites.add(slug)
            return True

    service = StubService()
    monkeypatch.setattr("builtins.input", lambda *_args, **_kwargs: "")

    assert launcher.launch_game("fav tic_tac_toe", service, object()) is True
    add_output = capsys.readouterr().out
    assert "Marked Tic-Tac-Toe as a favorite." in add_output

    assert launcher.launch_game("fav tic_tac_toe", service, object()) is True
    remove_output = capsys.readouterr().out
    assert "Removed Tic-Tac-Toe from favorites." in remove_output


def test_launch_game_supports_quick_alias(monkeypatch, capsys):
    """The CLI dispatcher resolves quick-launch aliases prefixed with !."""

    monkeypatch.setattr(launcher, "HAS_COLORAMA", False)

    calls: list[dict[str, object] | None] = []

    def fake_get_game_entry(identifier):  # noqa: ANN001
        assert identifier == "tic_tac_toe"
        return ("tic_tac_toe", lambda payload=None: calls.append(payload))

    monkeypatch.setattr(launcher, "get_game_entry", fake_get_game_entry)
    monkeypatch.setattr(launcher, "prepare_launcher_settings", lambda slug, manager: {})

    class StubService:
        def resolve_quick_launch_alias(self, alias: str) -> str | None:
            return {"speed": "tic_tac_toe"}.get(alias)

        def get_quick_launch_aliases(self):  # noqa: D401 - simple stub
            """Return no aliases for menu rendering."""

            return {}

    result = launcher.launch_game("!speed", StubService(), object())
    assert result is True
    assert calls == [None]


def test_launch_game_configuration_command(monkeypatch):
    """The configuration command opens the settings manager."""

    triggered: list[bool] = []
    monkeypatch.setattr(launcher, "run_configuration_cli", lambda _manager: triggered.append(True))

    class StubService:
        def get_quick_launch_aliases(self):  # noqa: D401 - minimal stub
            """Return no aliases."""

            return {}

    result = launcher.launch_game("g", StubService(), object())
    assert result is True
    assert triggered == [True]


def test_launch_game_passes_settings_payload(monkeypatch, capsys):
    """Launching a game forwards the prepared settings payload to the entry point."""

    payloads: list[dict[str, object] | None] = []
    monkeypatch.setattr(launcher, "prepare_launcher_settings", lambda slug, manager: {"bankroll": 900})
    monkeypatch.setitem(launcher.GAME_MAP, "blackjack", ("blackjack", lambda payload=None: payloads.append(payload)))

    assert launcher.launch_game("blackjack", object(), object()) is True
    assert payloads == [{"bankroll": 900}]
    assert "Launching" in capsys.readouterr().out


def test_main_supports_quick_alias(monkeypatch, tmp_path):
    """The launcher entry point resolves and launches quick aliases."""

    args = SimpleNamespace(
        game=None,
        gui_framework=None,
        smoke_test=False,
        profile=None,
        profile_display_name=None,
        profile_rename=None,
        profile_reset=False,
        profile_summary=False,
        ui="cli",
        quick="speed",
    )

    monkeypatch.setattr(launcher, "parse_args", lambda: args)

    class QuickAliasService:
        def __init__(self, root: Path) -> None:
            self.profile_dir = root
            self.profile_dir.mkdir(parents=True, exist_ok=True)
            self.active_profile = DummyProfile()
            self._aliases = {"speed": "tic_tac_toe"}
            self.saved = 0

        def resolve_quick_launch_alias(self, alias: str) -> str | None:
            return self._aliases.get(alias)

        def save_active_profile(self) -> None:
            self.saved += 1

        def summary(self) -> str:  # noqa: D401 - simple stub
            """Return a deterministic summary."""

            return "summary"

    service = QuickAliasService(tmp_path / "profiles")

    monkeypatch.setattr(launcher, "get_profile_service", lambda: service)
    monkeypatch.setattr(launcher, "get_default_challenge_manager", lambda: object())
    monkeypatch.setattr(launcher, "DailyChallengeScheduler", lambda *_, **__: object())

    launched: list[str] = []

    def fake_get_game_entry(identifier):  # noqa: ANN001
        assert identifier == "tic_tac_toe"
        return (identifier, lambda payload=None: launched.append(identifier))

    monkeypatch.setattr(launcher, "get_game_entry", fake_get_game_entry)

    launcher.main()

    assert launched == ["tic_tac_toe"]
    assert service.saved == 1
