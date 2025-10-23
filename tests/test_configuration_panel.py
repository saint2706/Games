"""Tests covering the configuration profiles and CLI helpers."""

from __future__ import annotations

from pathlib import Path

from games_collection.configuration_cli import run_configuration_cli
from games_collection.core.architecture.settings import SettingsManager
from games_collection.core.configuration import load_settings, prepare_launcher_settings, save_settings


def test_prepare_launcher_settings_returns_defaults(tmp_path: Path) -> None:
    """The launcher payload merges defaults with any stored overrides."""

    manager = SettingsManager(config_dir=tmp_path)
    settings = load_settings("spades", manager)
    settings.set("backend", "tk")
    save_settings("spades", settings, manager)

    payload = prepare_launcher_settings("spades", manager)
    assert payload["backend"] == "tk"
    assert payload["theme"] == "dark"
    assert payload["enable_sounds"] is True


def test_run_configuration_cli_updates_settings(tmp_path: Path) -> None:
    """Interactive editing updates persisted configuration values."""

    manager = SettingsManager(config_dir=tmp_path)
    entries = iter(["1", "1", "750", "s", "b", ""])

    def fake_input(prompt: str = "") -> str:
        try:
            return next(entries)
        except StopIteration:  # pragma: no cover - defensive guard
            raise AssertionError("Configuration CLI requested more input than expected")

    run_configuration_cli(manager, input_func=fake_input, output_func=lambda _text: None)

    settings = load_settings("blackjack", manager)
    assert settings.get("bankroll") == 750
