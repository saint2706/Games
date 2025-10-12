"""CLI for Lights Out."""

from __future__ import annotations

from .lights_out import LightsOutGame


def main() -> None:
    """Run Lights Out."""
    print("LIGHTS OUT".center(50, "="))
    print("\nTurn all lights off! (O = on, . = off)")

    game = LightsOutGame(size=5)
    game.state = game.state.IN_PROGRESS

    while not game.is_game_over():
        print(f"\nMoves: {game.moves}")
        print("  " + " ".join(str(i) for i in range(game.size)))
        for r, row in enumerate(game.grid):
            cells = ["O" if cell else "." for cell in row]
            print(f"{r} " + " ".join(cells))

        try:
            r = int(input("\nRow: "))
            c = int(input("Col: "))

            if not game.make_move((r, c)):
                print("Invalid position!")
        except ValueError:
            print("Enter valid numbers!")

    print(f"\nSolved in {game.moves} moves!")


if __name__ == "__main__":
    main()
