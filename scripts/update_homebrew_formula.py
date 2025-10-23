from __future__ import annotations

"""Utilities for keeping the Homebrew formula in sync with GitHub releases."""

from dataclasses import dataclass
import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Iterable, Optional
from urllib.error import HTTPError
from urllib.request import Request, urlopen

FORMULA_FILENAME = "games-collection.rb"
DEFAULT_FORMULA_PATH = Path("packaging/homebrew") / FORMULA_FILENAME
DEFAULT_REPOSITORY = "saint2706/Games"


@dataclass(frozen=True)
class Asset:
    """Metadata describing the release asset that should back the formula."""

    url: str
    sha256: str
    version: str


class FormulaUpdateError(RuntimeError):
    """Raised when the formula cannot be updated from release metadata."""


def parse_args(argv: Optional[Iterable[str]] = None) -> argparse.Namespace:
    """Parse command line arguments for formula updates."""

    parser = argparse.ArgumentParser(description="Update the Homebrew formula from a GitHub release")
    parser.add_argument("--repository", default=DEFAULT_REPOSITORY, help="GitHub repository in owner/name format")
    parser.add_argument("--tag", help="Specific release tag to use. Defaults to the latest release when omitted.")
    parser.add_argument("--formula", type=Path, default=DEFAULT_FORMULA_PATH, help="Path to the Homebrew formula to update")
    parser.add_argument("--no-commit", action="store_true", help="Skip committing the updated formula")
    parser.add_argument("--tap-root", type=Path, default=DEFAULT_FORMULA_PATH.parent, help="Directory containing the formula")
    return parser.parse_args(list(argv) if argv is not None else None)


def _github_request(url: str, token: Optional[str]) -> dict:
    """Perform an authenticated GitHub API request."""

    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(url, headers=headers)
    with urlopen(request) as response:
        return json.loads(response.read().decode("utf-8"))


def load_release(repository: str, tag: Optional[str], token: Optional[str]) -> dict:
    """Load the GitHub release metadata for the provided tag or the latest release."""

    base_url = f"https://api.github.com/repos/{repository}/releases"
    url = f"{base_url}/tags/{tag}" if tag else f"{base_url}/latest"
    try:
        return _github_request(url, token)
    except HTTPError as exc:  # pragma: no cover - network failures handled at runtime
        raise FormulaUpdateError(f"Failed to load release metadata from {url}: {exc}") from exc


def select_asset(release: dict) -> Asset:
    """Select the best release asset (wheel preferred, otherwise source tarball)."""

    assets: list[dict] = release.get("assets", [])
    wheel = next((asset for asset in assets if asset.get("name", "").endswith(".whl")), None)
    download = wheel or next((asset for asset in assets if asset.get("name", "").endswith(".tar.gz")), None)

    if not download:
        tarball_url = release.get("tarball_url")
        if not tarball_url:
            raise FormulaUpdateError("Release does not contain downloadable assets")
        download_url = tarball_url
    else:
        download_url = download.get("browser_download_url")

    version = release.get("tag_name")
    if not version:
        raise FormulaUpdateError("Release tag is missing from metadata")

    checksum = compute_sha256(download_url)
    return Asset(url=download_url, sha256=checksum, version=version.lstrip("v"))


def compute_sha256(url: str) -> str:
    """Compute the SHA256 digest of the content located at the provided URL."""

    token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    headers = {}
    if token and url.startswith("https://api.github.com"):
        headers["Authorization"] = f"Bearer {token}"
    request = Request(url, headers=headers)
    digest = hashlib.sha256()
    with urlopen(request) as response:
        while chunk := response.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def update_formula_content(content: str, asset: Asset) -> str:
    """Return updated formula content with the latest release metadata injected."""

    replacements = {
        "url": f'  url "{asset.url}"',
        "sha256": f'  sha256 "{asset.sha256}"',
        "version": f'  version "{asset.version}"',
    }
    lines = content.splitlines()
    updated_lines: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("url "):
            updated_lines.append(replacements["url"])
        elif stripped.startswith("sha256 "):
            updated_lines.append(replacements["sha256"])
        elif stripped.startswith("version "):
            updated_lines.append(replacements["version"])
        else:
            updated_lines.append(line)
    return "\n".join(updated_lines) + "\n"


def write_formula(path: Path, content: str) -> None:
    """Write the updated formula content to disk."""

    path.write_text(content, encoding="utf-8")


def git_commit(paths: Iterable[Path], message: str) -> None:
    """Stage the provided paths and create a Git commit."""

    path_strings = [str(path) for path in paths]
    subprocess.run(["git", "add", *path_strings], check=True)
    subprocess.run(["git", "commit", "-m", message], check=True)


def main(argv: Optional[Iterable[str]] = None) -> int:
    """CLI entry point for refreshing the Homebrew formula."""

    args = parse_args(argv)
    token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    release = load_release(args.repository, args.tag, token)
    asset = select_asset(release)

    tap_root = args.tap_root if args.tap_root.is_absolute() else (Path.cwd() / args.tap_root).resolve()
    formula_path = args.formula if args.formula.is_absolute() else (Path.cwd() / args.formula).resolve()

    if not formula_path.exists():
        raise FormulaUpdateError(f"Formula path {formula_path} does not exist")

    try:
        formula_path.relative_to(tap_root)
    except ValueError as exc:
        raise FormulaUpdateError(
            f"Formula path {formula_path} must be contained in the tap root {tap_root}"
        ) from exc

    original_content = formula_path.read_text(encoding="utf-8")
    new_content = update_formula_content(original_content, asset)

    if new_content == original_content:
        print("Formula is already up to date.")
        return 0

    write_formula(formula_path, new_content)
    print(f"Updated {formula_path} to version {asset.version}")

    if not args.no_commit:
        message = f"chore(homebrew): update games-collection to v{asset.version}"
        git_commit([tap_root], message)
        print("Created git commit for formula update")

    return 0


if __name__ == "__main__":
    sys.exit(main())
