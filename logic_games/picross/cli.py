"""CLI for Picross."""

from __future__ import annotations

from .picross import PicrossGame


def main() -> None:
    """Run Picross."""
    print("PICROSS".center(50, "="))
    print("\nFill cells based on hints!")

    game = PicrossGame()
    game.state = game.state.IN_PROGRESS

    print("\nRow hints:", game.row_hints)
    print("Col hints:", game.col_hints)

    while not game.is_game_over():
        print()
        for r, row in enumerate(game.grid):
            cells = []
            for cell in row:
                if cell is None:
                    cells.append("?")
                elif cell:
                    cells.append("█")
                else:
                    cells.append("·")
            print(f"{r} " + " ".join(cells))

        try:
            r = int(input("\nRow: "))
            c = int(input("Col: "))
            action = input("Action (f=fill, m=mark empty): ").strip().lower()

            action_name = "fill" if action == "f" else "mark"
            if not game.make_move((r, c, action_name)):
                print("Invalid move!")
        except (ValueError, IndexError):
            print("Invalid input!")

    print("\nPuzzle solved!")


if __name__ == "__main__":
    main()
