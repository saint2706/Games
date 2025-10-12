"""CLI for Sokoban."""

from __future__ import annotations

from .sokoban import SokobanGame


def main() -> None:
    """Run Sokoban game."""
    print("SOKOBAN".center(50, "="))
    print("\nPush boxes ($) onto goals (*)!")
    print("Controls: u=up, d=down, l=left, r=right, q=quit")
    
    game = SokobanGame()
    game.state = game.state.IN_PROGRESS
    
    while not game.is_game_over():
        print(f"\nMoves: {game.moves}")
        for row in game.grid:
            print("".join(row))
        
        move = input("\nMove: ").strip().lower()
        if move == "q":
            break
        
        if not game.make_move(move):
            print("Invalid move!")
    
    if game.is_game_over():
        print("\nPuzzle solved!")


if __name__ == "__main__":
    main()
