"""Entry point for Crossword."""

from __future__ import annotations

from typing import Sequence

from .cli import main as cli_main


def main(argv: Sequence[str] | None = None, *, settings: dict[str, object] | None = None) -> None:
    """Launch the crossword CLI entry point."""

    cli_main(argv=argv, settings=settings)


if __name__ == "__main__":
    main()
