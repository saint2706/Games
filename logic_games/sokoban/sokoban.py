"""Sokoban game engine."""

from __future__ import annotations

from typing import List, Tuple

from common.game_engine import GameEngine, GameState


class SokobanGame(GameEngine[str, int]):
    """Sokoban box-pushing puzzle game."""

    # Simple level: # = wall, @ = player, $ = box, . = goal, * = box on goal
    LEVEL = ["######", "#.@ $#", "#  $.#", "######"]

    def __init__(self) -> None:
        """Initialize game."""
        self.reset()

    def reset(self) -> None:
        """Reset game."""
        self.state = GameState.NOT_STARTED
        self.grid = [list(row) for row in self.LEVEL]
        self.player_pos = self._find_player()
        self.moves = 0

    def _find_player(self) -> Tuple[int, int]:
        """Find player position."""
        for r, row in enumerate(self.grid):
            for c, cell in enumerate(row):
                if cell in "@+":
                    return (r, c)
        return (0, 0)

    def is_game_over(self) -> bool:
        """Check if all boxes on goals."""
        for row in self.grid:
            if "$" in row or "." in row:
                return False
        return True

    def get_current_player(self) -> int:
        """Get current player."""
        return 0

    def get_valid_moves(self) -> List[str]:
        """Get valid moves: u/d/l/r."""
        return ["u", "d", "l", "r"]

    def make_move(self, move: str) -> bool:
        """Move player."""
        if self.state == GameState.NOT_STARTED:
            self.state = GameState.IN_PROGRESS

        dr, dc = {"u": (-1, 0), "d": (1, 0), "l": (0, -1), "r": (0, 1)}.get(move, (0, 0))
        if dr == 0 and dc == 0:
            return False

        r, c = self.player_pos
        nr, nc = r + dr, c + dc
        nnr, nnc = nr + dr, nc + dc

        # Check bounds
        if nr < 0 or nr >= len(self.grid) or nc < 0 or nc >= len(self.grid[0]):
            return False

        next_cell = self.grid[nr][nc]

        # Hit wall
        if next_cell == "#":
            return False

        # Push box
        if next_cell in "$*":
            # Check if can push
            if nnr < 0 or nnr >= len(self.grid) or nnc < 0 or nnc >= len(self.grid[0]):
                return False
            beyond_cell = self.grid[nnr][nnc]
            if beyond_cell in "#$*":
                return False

            # Move box
            self.grid[nnr][nnc] = "*" if beyond_cell == "." else "$"
            self.grid[nr][nc] = "." if next_cell == "*" else " "

        # Move player
        current = self.grid[r][c]
        self.grid[r][c] = "." if current == "+" else " "
        self.grid[nr][nc] = "+" if next_cell in ".*" else "@"
        self.player_pos = (nr, nc)
        self.moves += 1

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
