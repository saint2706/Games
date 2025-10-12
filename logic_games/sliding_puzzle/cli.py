"""CLI for Sliding Puzzle."""

from __future__ import annotations

from .sliding_puzzle import SlidingPuzzleGame


def main() -> None:
    """Run Sliding Puzzle."""
    print("SLIDING PUZZLE".center(50, "="))
    print("\nArrange tiles in order!")
    
    game = SlidingPuzzleGame(size=3)
    game.state = game.state.IN_PROGRESS
    
    while not game.is_game_over():
        print(f"\nMoves: {game.moves}")
        for i in range(game.size):
            row = []
            for j in range(game.size):
                val = game.board[i * game.size + j]
                row.append(f"{val:2}" if val else "  ")
            print(" ".join(row))
        
        move = input("\nMove (u/d/l/r, q=quit): ").strip().lower()
        if move == "q":
            break
        
        if not game.make_move(move):
            print("Invalid move!")
    
    if game.is_game_over():
        print(f"\nSolved in {game.moves} moves!")


if __name__ == "__main__":
    main()
