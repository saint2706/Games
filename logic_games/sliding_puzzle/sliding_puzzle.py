"""Sliding Puzzle game engine."""

from __future__ import annotations

import random
from typing import List

from common.game_engine import GameEngine, GameState


class SlidingPuzzleGame(GameEngine[str, int]):
    """Sliding puzzle (15-puzzle) game."""

    def __init__(self, size: int = 3) -> None:
        """Initialize game."""
        self.size = size
        self.reset()

    def reset(self) -> None:
        """Reset game."""
        self.state = GameState.NOT_STARTED
        self.board = list(range(1, self.size * self.size)) + [0]
        self._shuffle()
        self.moves = 0

    def _shuffle(self) -> None:
        """Shuffle board with solvable configuration."""
        for _ in range(100):
            moves = self.get_valid_moves()
            if moves:
                random.choice(moves)
                self._slide(random.choice(moves))

    def _slide(self, direction: str) -> bool:
        """Slide tile in direction."""
        zero_idx = self.board.index(0)
        row, col = zero_idx // self.size, zero_idx % self.size

        dr, dc = {"u": (1, 0), "d": (-1, 0), "l": (0, 1), "r": (0, -1)}.get(direction, (0, 0))
        nr, nc = row + dr, col + dc

        if 0 <= nr < self.size and 0 <= nc < self.size:
            new_idx = nr * self.size + nc
            self.board[zero_idx], self.board[new_idx] = self.board[new_idx], self.board[zero_idx]
            return True
        return False

    def is_game_over(self) -> bool:
        """Check if solved."""
        return self.board == list(range(1, self.size * self.size)) + [0]

    def get_current_player(self) -> int:
        """Get current player."""
        return 0

    def get_valid_moves(self) -> List[str]:
        """Get valid moves."""
        zero_idx = self.board.index(0)
        row, col = zero_idx // self.size, zero_idx % self.size
        moves = []
        if row > 0:
            moves.append("u")
        if row < self.size - 1:
            moves.append("d")
        if col > 0:
            moves.append("l")
        if col < self.size - 1:
            moves.append("r")
        return moves

    def make_move(self, move: str) -> bool:
        """Make move."""
        if self.state == GameState.NOT_STARTED:
            self.state = GameState.IN_PROGRESS

        if move not in self.get_valid_moves():
            return False

        if self._slide(move):
            self.moves += 1
            if self.is_game_over():
                self.state = GameState.FINISHED
            return True
        return False

    def get_winner(self) -> int | None:
        """Get winner."""
        return 0 if self.is_game_over() else None

    def get_game_state(self) -> GameState:
        """Get current game state.

        Returns:
            Current state of the game
        """
        return self.state
