"""Generate documentation pages from the central games registry."""

from __future__ import annotations

from pathlib import Path
from textwrap import dedent

from games_collection.catalog.registry import GENRES, iter_genre

GENRE_TITLES = {
    "card": "Card games",
    "paper": "Paper games",
    "dice": "Dice games",
    "logic": "Logic games",
    "word": "Word games",
}

DOCS_HEADER_RST = dedent(
    """
    Games Catalogue
    ===============

    This file is generated from :mod:`games_collection.catalog.registry`.
    The lists below group games by their importable package paths.
    """
).strip()

DOCS_FOOTER_RST = dedent(
    """
    Where to learn more
    -------------------

    Each package ships with its own README and inline docstrings that
    describe rules and command-line switches. For a bird's-eye view across the
    entire project, read ``overview`` and ``developers/architecture``.

    Detailed descriptions
    ---------------------

    .. include:: games_catalog_detail.rst
       :start-line: 0
    """
).strip()

MARKDOWN_HEADER = dedent(
    """
    # Games Catalog

    _This file is generated from `games_collection.catalog.registry`. Do not edit manually._
    """
).strip()


def _genre_entries(genre: str) -> list[tuple[str, str]]:
    metadata = iter_genre(genre)
    return [(entry.name, entry.package) for entry in metadata]


def _format_rst_section(genre: str) -> list[str]:
    entries = _genre_entries(genre)
    if not entries:
        return []

    title = f"{GENRE_TITLES.get(genre, genre.title())} ({len(entries)})"
    underline = "-" * len(title)
    lines = [title, underline, ""]
    for name, package in entries:
        lines.append(f"- :mod:`{package}`")
    lines.append("")
    return lines


def _format_markdown_section(genre: str) -> list[str]:
    entries = _genre_entries(genre)
    if not entries:
        return []

    title = f"## {GENRE_TITLES.get(genre, genre.title())} ({len(entries)})"
    lines = [title, ""]
    for name, package in entries:
        lines.append(f"- **{name}** (`{package}`)")
    lines.append("")
    return lines


def build_games_catalog_rst() -> str:
    lines: list[str] = [DOCS_HEADER_RST, ""]
    for genre in sorted(GENRES, key=lambda value: GENRE_TITLES.get(value, value)):
        lines.extend(_format_rst_section(genre))
    lines.append(DOCS_FOOTER_RST)
    return "\n".join(lines) + "\n"


def build_games_markdown() -> str:
    lines: list[str] = [MARKDOWN_HEADER, ""]
    for genre in sorted(GENRES, key=lambda value: GENRE_TITLES.get(value, value)):
        lines.extend(_format_markdown_section(genre))
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    rst_path = repo_root / "docs" / "source" / "players" / "games_catalog.rst"
    md_path = repo_root / "GAMES.md"

    rst_path.write_text(build_games_catalog_rst(), encoding="utf-8")
    md_path.write_text(build_games_markdown(), encoding="utf-8")


if __name__ == "__main__":
    main()
