"""CLI for Crossword."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from .crossword import CrosswordGame, CrosswordPackManager


def build_parser() -> argparse.ArgumentParser:
    """Create a parser for crossword CLI options."""

    parser = argparse.ArgumentParser(description="Play or manage crossword packs.")
    parser.add_argument("--pack", type=Path, default=None, help="Import a crossword pack from the provided JSON file")
    parser.add_argument(
        "--export",
        type=Path,
        default=None,
        help="Write the active crossword pack to the specified JSON file",
    )
    return parser


def main(argv: Sequence[str] | None = None, *, settings: dict[str, object] | None = None) -> None:
    """Run Crossword game."""

    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

    print("CROSSWORD".center(50, "="))
    print("\nSolve the crossword puzzle or manage packs!")

    pack_path = args.pack
    allow_hints = True
    if settings:
        if pack_path is None:
            pack_setting = settings.get("pack")
            if pack_setting:
                candidate = Path(str(pack_setting)).expanduser()
                if candidate.exists():
                    pack_path = candidate
                else:
                    print(f"Configured pack '{pack_setting}' was not found. Using defaults.")
        if "allow_hints" in settings:
            allow_hints = bool(settings["allow_hints"])

    if pack_path is not None:
        clues = CrosswordPackManager.load(pack_path)
        print(f"\nLoaded crossword pack from {pack_path}")
    else:
        clues = None

    game = CrosswordGame(clues)
    game.state = game.state.IN_PROGRESS

    while not game.is_game_over():
        print(f"\nSolved: {len(game.solved)}/{len(game.get_clues())}")
        print("\nClues:")

        for cid, clue in game.get_clues().items():
            status = "✓" if cid in game.solved else " "
            direction = clue.direction.capitalize()
            location = f"(r{clue.row}, c{clue.column})"
            print(f"  [{status}] {cid}. {direction} {location}: {clue.clue}")

        prompt = input("\nClue number (or 'hint'): ").strip()
        if allow_hints and prompt.lower() == "hint":
            unsolved = next((cid for cid in game.get_clues() if cid not in game.solved), None)
            if unsolved is None:
                print("All clues are solved!")
            else:
                answer = game.get_clues()[unsolved].answer
                print(f"Try looking at clue {unsolved}: {answer[:1]}…")
            continue
        if not prompt:
            print("Please enter a clue number.")
            continue
        try:
            cid = int(prompt)
        except ValueError:
            print("Invalid input!")
            continue

        guess = input("Answer: ").strip()
        if not game.make_move((cid, guess)):
            print("Incorrect or already solved!")
        elif cid in game.solved:
            print("Nice work!")

    print("\nPuzzle complete!")

    if args.export is not None:
        CrosswordPackManager.dump(game.get_clues(), args.export)
        print(f"Pack exported to {args.export}")


if __name__ == "__main__":
    main()
