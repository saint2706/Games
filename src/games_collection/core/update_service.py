from __future__ import annotations

import logging
import os
import platform
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Sequence

import requests
from importlib import metadata
from importlib.metadata import PackageNotFoundError
from packaging.version import InvalidVersion, Version

from games_collection.core.architecture.settings import SettingsManager
from games_collection.core.configuration import (
    APPLICATION_SLUG,
    get_auto_update_preference as _configuration_get_auto_update_preference,
    get_launcher_settings,
    get_settings_manager,
    save_settings,
    set_auto_update_preference as _configuration_set_auto_update_preference,
)

get_auto_update_preference = _configuration_get_auto_update_preference
set_auto_update_preference = _configuration_set_auto_update_preference

LOGGER = logging.getLogger(__name__)

DEFAULT_PACKAGE_NAME = "games-collection"
DEFAULT_REPOSITORY = "saint2706/Games"
DEFAULT_RELEASE_ENDPOINT = "https://api.github.com/repos/{repository}/releases/latest"
DEFAULT_DOWNLOAD_DIR_NAME = "games_collection_updates"
REQUEST_TIMEOUT = 8.0
DOWNLOAD_TIMEOUT = 30.0
DEFAULT_CHUNK_SIZE = 64 * 1024


@dataclass(frozen=True)
class ReleaseAsset:
    """Metadata describing a downloadable asset attached to a release."""

    name: str
    download_url: str
    size: int
    content_type: str | None


@dataclass(frozen=True)
class ReleaseInfo:
    """Information about the latest GitHub release."""

    version: str
    tag_name: str
    name: str
    html_url: str | None
    published_at: str | None
    assets: tuple[ReleaseAsset, ...]


@dataclass(frozen=True)
class UpdateCheckResult:
    """Aggregate outcome of an update check."""

    installed_version: str | None
    release: ReleaseInfo | None
    update_available: bool


def _normalise_version_label(label: str) -> str:
    """Strip common prefixes such as ``v`` from version tags."""

    return label.strip().lstrip("v")


def _parse_version(label: str) -> Version | None:
    """Return a :class:`Version` object for ``label`` when possible."""

    normalised = _normalise_version_label(label)
    if not normalised:
        return None
    try:
        return Version(normalised)
    except InvalidVersion:
        LOGGER.debug("Unable to parse version label '%s'.", label)
        return None


def _default_platform_tags() -> tuple[str, ...]:
    """Return search tokens matching the current operating system."""

    system = sys.platform.lower()
    tags: list[str] = []
    if system.startswith("win"):
        tags.extend(("windows", "win64", "win32", "win"))
    elif system.startswith("darwin") or system == "mac" or system == "macos":
        tags.extend(("macos", "mac", "osx"))
    else:
        tags.extend(("linux", "gnu", "x86_64"))

    architecture = platform.machine().lower()
    if architecture:
        tags.append(architecture)
    return tuple(tags)


def detect_bundle() -> str | None:
    """Best-effort detection of the active bundle flavour."""

    if getattr(sys, "frozen", False):
        if hasattr(sys, "_MEIPASS"):
            return "pyinstaller"
        if "__compiled__" in globals() or os.environ.get("NUITKA_PYTHON"):
            return "nuitka"
        return "frozen"
    return None


def _ensure_download_dir(target_dir: Optional[Path]) -> Path:
    """Return a directory suitable for storing downloaded assets."""

    if target_dir is None:
        base = Path(tempfile.gettempdir()) / DEFAULT_DOWNLOAD_DIR_NAME
    else:
        base = target_dir
    base.mkdir(parents=True, exist_ok=True)
    return base


def _select_asset(
    assets: Sequence[ReleaseAsset],
    *,
    bundle_hint: Optional[str],
    platform_tags: Sequence[str],
) -> ReleaseAsset:
    """Return the best matching asset for the current platform and bundle."""

    if not assets:
        raise ValueError("No release assets are available for download.")

    scored: list[tuple[int, ReleaseAsset]] = []
    bundle_tokens: tuple[str, ...] = ()
    if bundle_hint:
        bundle_lower = bundle_hint.lower()
        bundle_tokens = (bundle_lower,)

    for asset in assets:
        name = asset.name.lower()
        score = 0
        for token in platform_tags:
            if token and token in name:
                score += 2
        for token in bundle_tokens:
            if token and token in name:
                score += 3
        if "pyinstaller" in name and bundle_hint is None:
            score += 1
        scored.append((score, asset))

    scored.sort(key=lambda item: (item[0], item[1].name))
    selected_score, selected_asset = scored[-1]
    if selected_score == 0:
        LOGGER.debug("No asset matched platform/bundle hints; using %s", selected_asset.name)
    return selected_asset


def get_installed_version(
    package_name: str = DEFAULT_PACKAGE_NAME,
    *,
    manager: Optional[SettingsManager] = None,
) -> str | None:
    """Return the installed package version and persist it for display."""

    settings_manager = manager or get_settings_manager()
    settings = get_launcher_settings(settings_manager)
    try:
        detected = metadata.version(package_name)
    except PackageNotFoundError:
        detected = None
    if detected:
        settings.set("detected_version", detected)
    else:
        settings.remove("detected_version")
    save_settings(APPLICATION_SLUG, settings, settings_manager)
    return detected


def fetch_latest_release(
    repository: str = DEFAULT_REPOSITORY,
    *,
    session: Optional[requests.Session] = None,
    manager: Optional[SettingsManager] = None,
    timeout: float = REQUEST_TIMEOUT,
) -> ReleaseInfo | None:
    """Return metadata about the latest GitHub release if reachable."""

    url = DEFAULT_RELEASE_ENDPOINT.format(repository=repository)
    http = session or requests.Session()
    try:
        response = http.get(url, headers={"Accept": "application/vnd.github+json"}, timeout=timeout)
    except requests.RequestException as exc:
        LOGGER.debug("Failed to contact GitHub releases API: %s", exc)
        if session is None:
            http.close()
        return None

    if response.status_code >= 400:
        LOGGER.debug("GitHub releases API responded with %s", response.status_code)
        if session is None:
            http.close()
        return None

    try:
        payload = response.json()
    except ValueError as exc:
        LOGGER.debug("Failed to decode GitHub response: %s", exc)
        if session is None:
            http.close()
        return None
    finally:
        if session is None:
            http.close()

    tag_name = str(payload.get("tag_name") or payload.get("name") or "").strip()
    version_label = _normalise_version_label(tag_name or str(payload.get("name") or ""))
    assets_data = payload.get("assets") or []
    assets: list[ReleaseAsset] = []
    for raw in assets_data:
        name = raw.get("name")
        download_url = raw.get("browser_download_url")
        if not name or not download_url:
            continue
        assets.append(
            ReleaseAsset(
                name=str(name),
                download_url=str(download_url),
                size=int(raw.get("size") or 0),
                content_type=raw.get("content_type"),
            )
        )

    release = ReleaseInfo(
        version=version_label or tag_name,
        tag_name=tag_name or version_label,
        name=str(payload.get("name") or tag_name or version_label or "Latest release"),
        html_url=payload.get("html_url"),
        published_at=payload.get("published_at"),
        assets=tuple(assets),
    )

    settings_manager = manager or get_settings_manager()
    settings = get_launcher_settings(settings_manager)
    settings.set("latest_release_version", release.version)
    settings.set("latest_release_tag", release.tag_name)
    save_settings(APPLICATION_SLUG, settings, settings_manager)

    return release


def is_update_available(installed_version: str | None, release: ReleaseInfo | None) -> bool:
    """Return ``True`` when ``release`` is newer than ``installed_version``."""

    if release is None:
        return False
    release_version = _parse_version(release.version) or _parse_version(release.tag_name)
    if installed_version is None:
        return release_version is not None or bool(release.version)

    installed = _parse_version(installed_version)
    if release_version is None or installed is None:
        return bool(release.version) and release.version != installed_version
    return release_version > installed


def check_for_updates(
    package_name: str = DEFAULT_PACKAGE_NAME,
    repository: str = DEFAULT_REPOSITORY,
    *,
    session: Optional[requests.Session] = None,
    manager: Optional[SettingsManager] = None,
) -> UpdateCheckResult:
    """Return the combined result of querying the installed and latest versions."""

    installed = get_installed_version(package_name, manager=manager)
    release = fetch_latest_release(repository, session=session, manager=manager)
    return UpdateCheckResult(installed_version=installed, release=release, update_available=is_update_available(installed, release))


def download_release_asset(
    release: ReleaseInfo,
    *,
    bundle_hint: Optional[str] = None,
    platform_tags: Optional[Sequence[str]] = None,
    target_dir: Optional[Path] = None,
    session: Optional[requests.Session] = None,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    timeout: float = DOWNLOAD_TIMEOUT,
) -> Path:
    """Download the most appropriate release asset and return its path."""

    tags = tuple(platform_tags) if platform_tags is not None else _default_platform_tags()
    asset = _select_asset(release.assets, bundle_hint=bundle_hint, platform_tags=tags)

    download_dir = _ensure_download_dir(target_dir)
    target_path = download_dir / asset.name

    http = session or requests.Session()
    try:
        with http.get(asset.download_url, stream=True, timeout=timeout) as response:
            response.raise_for_status()
            with target_path.open("wb") as handle:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        handle.write(chunk)
    except requests.RequestException as exc:
        LOGGER.debug("Failed to download release asset %s: %s", asset.name, exc)
        if target_path.exists():
            target_path.unlink(missing_ok=True)
        raise RuntimeError(f"Unable to download update asset: {exc}") from exc
    finally:
        if session is None:
            http.close()

    if not os.access(target_path, os.X_OK) and target_path.suffix in {"", ".bin", ".run", ".appimage", ".exe"}:
        target_path.chmod(target_path.stat().st_mode | 0o111)

    return target_path


__all__ = [
    "ReleaseAsset",
    "ReleaseInfo",
    "UpdateCheckResult",
    "DEFAULT_PACKAGE_NAME",
    "DEFAULT_REPOSITORY",
    "get_installed_version",
    "fetch_latest_release",
    "is_update_available",
    "check_for_updates",
    "download_release_asset",
    "detect_bundle",
    "get_auto_update_preference",
    "set_auto_update_preference",
]
