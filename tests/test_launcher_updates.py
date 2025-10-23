from __future__ import annotations

import sys
from pathlib import Path

from games_collection.core.architecture.settings import SettingsManager
from games_collection.core.update_service import ReleaseInfo, UpdateCheckResult
from games_collection import launcher


def _make_release(version: str) -> ReleaseInfo:
    return ReleaseInfo(
        version=version,
        tag_name=f"v{version}",
        name=f"Games Collection {version}",
        html_url=None,
        published_at=None,
        assets=(),
    )


def test_cli_check_updates_reports_status(monkeypatch, tmp_path: Path, capsys) -> None:
    monkeypatch.setattr(launcher, "SETTINGS_MANAGER", SettingsManager(config_dir=tmp_path))
    monkeypatch.setattr(launcher, "HAS_COLORAMA", False)
    result = UpdateCheckResult(installed_version="2.0.0", release=_make_release("2.0.0"), update_available=False)
    monkeypatch.setattr(launcher, "_check_updates", lambda: result)
    monkeypatch.setattr(launcher, "_download_update_asset", lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError))

    monkeypatch.setenv("PYTHONIOENCODING", "utf-8")
    monkeypatch.setattr(sys, "argv", ["games-collection", "--check-updates"])

    launcher.main()
    captured = capsys.readouterr()
    assert "up to date" in captured.out.lower()


def test_cli_update_downloads_asset(monkeypatch, tmp_path: Path, capsys) -> None:
    monkeypatch.setattr(launcher, "SETTINGS_MANAGER", SettingsManager(config_dir=tmp_path))
    monkeypatch.setattr(launcher, "HAS_COLORAMA", False)
    release = _make_release("2.1.0")
    result = UpdateCheckResult(installed_version="2.0.0", release=release, update_available=True)
    monkeypatch.setattr(launcher, "_check_updates", lambda: result)

    downloaded: list[Path] = []

    def _fake_download(_release: ReleaseInfo, _bundle_hint: str | None) -> Path:
        path = tmp_path / "games-collection"
        path.write_text("binary")
        downloaded.append(path)
        print(f"Downloaded update to {path}")
        return path

    monkeypatch.setattr(launcher, "_download_update_asset", _fake_download)
    monkeypatch.setenv("PYTHONIOENCODING", "utf-8")
    monkeypatch.setattr(sys, "argv", ["games-collection", "--update"])

    launcher.main()
    captured = capsys.readouterr()
    assert "update available" in captured.out.lower()
    assert "downloaded update" in captured.out.lower()
    assert downloaded
