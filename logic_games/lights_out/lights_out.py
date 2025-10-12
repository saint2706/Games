"""Lights Out game engine."""

from __future__ import annotations

import random
from typing import List, Tuple

from common.game_engine import GameEngine, GameState


class LightsOutGame(GameEngine[Tuple[int, int], int]):
    """Lights Out toggle puzzle game."""

    def __init__(self, size: int = 5) -> None:
        """Initialize game."""
        self.size = size
        self.reset()

    def reset(self) -> None:
        """Reset game."""
        self.state = GameState.NOT_STARTED
        self.grid = [[random.choice([True, False]) for _ in range(self.size)] 
                     for _ in range(self.size)]
        self.moves = 0

    def is_game_over(self) -> bool:
        """Check if all lights off."""
        return all(not cell for row in self.grid for cell in row)

    def get_current_player(self) -> int:
        """Get current player."""
        return 0

    def get_valid_moves(self) -> List[Tuple[int, int]]:
        """Get valid moves (all cells)."""
        return [(r, c) for r in range(self.size) for c in range(self.size)]

    def make_move(self, move: Tuple[int, int]) -> bool:
        """Toggle cell and neighbors."""
        if self.state == GameState.NOT_STARTED:
            self.state = GameState.IN_PROGRESS
        
        r, c = move
        if not (0 <= r < self.size and 0 <= c < self.size):
            return False
        
        # Toggle cell and neighbors
        for dr, dc in [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.size and 0 <= nc < self.size:
                self.grid[nr][nc] = not self.grid[nr][nc]
        
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
