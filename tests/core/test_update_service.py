from __future__ import annotations

from pathlib import Path

import responses

from games_collection.core.architecture.settings import SettingsManager
from games_collection.core.configuration import APPLICATION_SLUG, load_settings
from games_collection.core.update_service import (
    ReleaseAsset,
    ReleaseInfo,
    UpdateCheckResult,
    download_release_asset,
    fetch_latest_release,
    get_installed_version,
    is_update_available,
)


@responses.activate
def test_fetch_latest_release_populates_settings(tmp_path: Path) -> None:
    manager = SettingsManager(config_dir=tmp_path)
    responses.add(
        responses.GET,
        "https://api.github.com/repos/saint2706/Games/releases/latest",
        json={
            "tag_name": "v2.3.4",
            "name": "2.3.4",
            "html_url": "https://example.com/release",
            "assets": [
                {
                    "name": "games-collection-2.3.4-pyinstaller-linux.tar.gz",
                    "browser_download_url": "https://downloads.example.com/linux",
                    "size": 1024,
                    "content_type": "application/gzip",
                }
            ],
        },
    )

    release = fetch_latest_release(manager=manager)
    assert release is not None
    assert release.version == "2.3.4"
    assert release.assets[0].download_url == "https://downloads.example.com/linux"

    stored = load_settings(APPLICATION_SLUG, manager)
    assert stored.get("latest_release_version") == "2.3.4"


def test_get_installed_version_persists_detected_value(tmp_path: Path, monkeypatch) -> None:
    manager = SettingsManager(config_dir=tmp_path)
    monkeypatch.setattr("games_collection.core.update_service.metadata.version", lambda _: "1.2.3")

    version = get_installed_version(manager=manager)
    assert version == "1.2.3"

    stored = load_settings(APPLICATION_SLUG, manager)
    assert stored.get("detected_version") == "1.2.3"


def test_is_update_available_handles_versions() -> None:
    release = ReleaseInfo(
        version="2.0.0",
        tag_name="v2.0.0",
        name="Games Collection 2.0.0",
        html_url=None,
        published_at=None,
        assets=(),
    )

    assert is_update_available("1.5.0", release)
    assert not is_update_available("2.0.0", release)
    assert is_update_available(None, release)


@responses.activate
def test_download_release_asset_selects_best_candidate(tmp_path: Path) -> None:
    asset_linux = ReleaseAsset(
        name="games-collection-3.0.0-pyinstaller-linux.tar.gz",
        download_url="https://downloads.example.com/linux",
        size=10,
        content_type="application/gzip",
    )
    asset_windows = ReleaseAsset(
        name="games-collection-3.0.0-nuitka-windows.zip",
        download_url="https://downloads.example.com/windows",
        size=10,
        content_type="application/zip",
    )
    release = ReleaseInfo(
        version="3.0.0",
        tag_name="v3.0.0",
        name="Games Collection 3.0.0",
        html_url=None,
        published_at=None,
        assets=(asset_linux, asset_windows),
    )

    responses.add(responses.GET, asset_linux.download_url, body=b"archive", status=200)

    path = download_release_asset(release, bundle_hint="pyinstaller", platform_tags=("linux",), target_dir=tmp_path)
    assert path.exists()
    assert path.read_bytes() == b"archive"


def test_update_check_result_structure() -> None:
    release = ReleaseInfo(
        version="2.5.0",
        tag_name="v2.5.0",
        name="Games Collection 2.5.0",
        html_url="https://example.com/notes",
        published_at="2024-01-01T00:00:00Z",
        assets=(),
    )
    result = UpdateCheckResult(installed_version="2.4.0", release=release, update_available=True)
    assert result.update_available
    assert result.release.version == "2.5.0"
