"""Picross game engine."""

from __future__ import annotations

from typing import List, Tuple

from common.game_engine import GameEngine, GameState


class PicrossGame(GameEngine[Tuple[int, int, str], int]):
    """Picross/Nonogram picture logic puzzle."""

    # Simple 5x5 puzzle (1 = filled, 0 = empty)
    SOLUTION = [[0, 1, 1, 1, 0], [1, 0, 0, 0, 1], [1, 0, 0, 0, 1], [1, 0, 0, 0, 1], [0, 1, 1, 1, 0]]

    def __init__(self) -> None:
        """Initialize game."""
        self.size = len(self.SOLUTION)
        self.reset()

    def reset(self) -> None:
        """Reset game."""
        self.state = GameState.NOT_STARTED
        self.grid = [[None] * self.size for _ in range(self.size)]
        self.row_hints = [self._get_hints(row) for row in self.SOLUTION]
        self.col_hints = [self._get_hints([self.SOLUTION[r][c] for r in range(self.size)]) for c in range(self.size)]

    def _get_hints(self, line: List[int]) -> List[int]:
        """Get hints for a line."""
        hints = []
        count = 0
        for cell in line:
            if cell:
                count += 1
            elif count:
                hints.append(count)
                count = 0
        if count:
            hints.append(count)
        return hints or [0]

    def is_game_over(self) -> bool:
        """Check if solved."""
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] != bool(self.SOLUTION[r][c]):
                    return False
        return True

    def get_current_player(self) -> int:
        """Get current player."""
        return 0

    def get_valid_moves(self) -> List[Tuple[int, int, str]]:
        """Get valid moves: (row, col, action)."""
        moves = []
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] is None:
                    moves.append((r, c, "fill"))
                    moves.append((r, c, "mark"))
        return moves

    def make_move(self, move: Tuple[int, int, str]) -> bool:
        """Fill or mark cell."""
        if self.state == GameState.NOT_STARTED:
            self.state = GameState.IN_PROGRESS

        r, c, action = move
        if not (0 <= r < self.size and 0 <= c < self.size):
            return False

        if self.grid[r][c] is not None:
            return False

        self.grid[r][c] = action == "fill"

        if self.is_game_over():
            self.state = GameState.FINISHED

        return True

    def get_winner(self) -> int | None:
        """Get winner."""
        return 0 if self.is_game_over() else None

    def get_game_state(self) -> GameState:
        """Get current game state.

        Returns:
            Current state of the game
        """
        return self.state
