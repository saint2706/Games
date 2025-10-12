"""Minesweeper game engine implementation.

This module implements the core logic for the classic Minesweeper game,
including board generation, mine placement, and reveal mechanics.
"""

from __future__ import annotations

import random
from enum import Enum
from typing import List, Set, Tuple

from common.game_engine import GameEngine, GameState


class CellState(Enum):
    """State of a minesweeper cell."""
    
    HIDDEN = "hidden"
    REVEALED = "revealed"
    FLAGGED = "flagged"


class Difficulty(Enum):
    """Minesweeper difficulty levels."""
    
    BEGINNER = (9, 9, 10)      # 9x9, 10 mines
    INTERMEDIATE = (16, 16, 40)  # 16x16, 40 mines
    EXPERT = (16, 30, 99)      # 16x30, 99 mines
    
    @property
    def rows(self) -> int:
        """Get number of rows."""
        return self.value[0]
    
    @property
    def cols(self) -> int:
        """Get number of columns."""
        return self.value[1]
    
    @property
    def mines(self) -> int:
        """Get number of mines."""
        return self.value[2]


class MinesweeperGame(GameEngine[Tuple[int, int, str], int]):
    """Minesweeper game engine.
    
    Classic mine detection game. Players reveal cells, using numbered hints
    to deduce mine locations. Game is won by revealing all non-mine cells.
    
    Move format: (row, col, action) where action is 'reveal' or 'flag'
    """

    def __init__(self, difficulty: Difficulty = Difficulty.BEGINNER) -> None:
        """Initialize Minesweeper game.
        
        Args:
            difficulty: Game difficulty level
        """
        self.difficulty = difficulty
        self.rows = difficulty.rows
        self.cols = difficulty.cols
        self.num_mines = difficulty.mines
        self.reset()

    def reset(self) -> None:
        """Reset the game to initial state."""
        self.state = GameState.NOT_STARTED
        self.board: List[List[bool]] = []  # True = mine
        self.cell_states: List[List[CellState]] = []
        self.numbers: List[List[int]] = []  # Adjacent mine counts
        self.revealed_count = 0
        self.flagged_positions: Set[Tuple[int, int]] = set()
        self.game_won = False
        self.game_lost = False
        self._initialize_board()

    def _initialize_board(self) -> None:
        """Initialize empty board."""
        self.board = [[False] * self.cols for _ in range(self.rows)]
        self.cell_states = [[CellState.HIDDEN] * self.cols for _ in range(self.rows)]
        self.numbers = [[0] * self.cols for _ in range(self.rows)]

    def _place_mines(self, first_row: int, first_col: int) -> None:
        """Place mines on board, avoiding first click.
        
        Args:
            first_row: Row of first click
            first_col: Column of first click
        """
        # Get all positions except first click and neighbors
        forbidden = {(first_row, first_col)}
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = first_row + dr, first_col + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    forbidden.add((nr, nc))
        
        available = [(r, c) for r in range(self.rows) for c in range(self.cols)
                     if (r, c) not in forbidden]
        
        # Place mines randomly
        mine_positions = random.sample(available, min(self.num_mines, len(available)))
        for row, col in mine_positions:
            self.board[row][col] = True
        
        # Calculate numbers
        for row in range(self.rows):
            for col in range(self.cols):
                if not self.board[row][col]:
                    self.numbers[row][col] = self._count_adjacent_mines(row, col)

    def _count_adjacent_mines(self, row: int, col: int) -> int:
        """Count mines adjacent to a cell.
        
        Args:
            row: Row index
            col: Column index
            
        Returns:
            Number of adjacent mines
        """
        count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row + dr, col + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    if self.board[nr][nc]:
                        count += 1
        return count

    def is_game_over(self) -> bool:
        """Check if game is over."""
        return self.game_won or self.game_lost

    def get_current_player(self) -> int:
        """Get current player (always 0 for single-player)."""
        return 0

    def get_valid_moves(self) -> List[Tuple[int, int, str]]:
        """Get all valid moves.
        
        Returns:
            List of (row, col, action) tuples
        """
        moves = []
        for row in range(self.rows):
            for col in range(self.cols):
                if self.cell_states[row][col] == CellState.HIDDEN:
                    moves.append((row, col, "reveal"))
                    moves.append((row, col, "flag"))
                elif self.cell_states[row][col] == CellState.FLAGGED:
                    moves.append((row, col, "unflag"))
        return moves

    def make_move(self, move: Tuple[int, int, str]) -> bool:
        """Execute a move.
        
        Args:
            move: Tuple of (row, col, action)
            
        Returns:
            True if move was valid
        """
        row, col, action = move
        
        # Validate position
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return False
        
        # First move: place mines
        if self.state == GameState.NOT_STARTED:
            self.state = GameState.IN_PROGRESS
            self._place_mines(row, col)
        
        cell_state = self.cell_states[row][col]
        
        if action == "reveal":
            if cell_state != CellState.HIDDEN:
                return False
            
            # Hit a mine - game over
            if self.board[row][col]:
                self.cell_states[row][col] = CellState.REVEALED
                self.game_lost = True
                self.state = GameState.FINISHED
                return True
            
            # Reveal cell and cascade if needed
            self._reveal_cell(row, col)
            
            # Check for win
            total_cells = self.rows * self.cols
            if self.revealed_count == total_cells - self.num_mines:
                self.game_won = True
                self.state = GameState.FINISHED
            
            return True
        
        elif action == "flag":
            if cell_state != CellState.HIDDEN:
                return False
            self.cell_states[row][col] = CellState.FLAGGED
            self.flagged_positions.add((row, col))
            return True
        
        elif action == "unflag":
            if cell_state != CellState.FLAGGED:
                return False
            self.cell_states[row][col] = CellState.HIDDEN
            self.flagged_positions.discard((row, col))
            return True
        
        return False

    def _reveal_cell(self, row: int, col: int) -> None:
        """Reveal a cell and cascade if it's a zero.
        
        Args:
            row: Row index
            col: Column index
        """
        if self.cell_states[row][col] != CellState.HIDDEN:
            return
        
        self.cell_states[row][col] = CellState.REVEALED
        self.revealed_count += 1
        
        # Cascade reveal if cell has no adjacent mines
        if self.numbers[row][col] == 0:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        self._reveal_cell(nr, nc)

    def get_winner(self) -> int | None:
        """Get winner if game is over."""
        if self.game_won:
            return 0
        return None

    def get_game_state(self) -> GameState:
        """Get current game state.
        
        Returns:
            Current state of the game
        """
        return self.state

    def get_cell_display(self, row: int, col: int) -> str:
        """Get display string for a cell.
        
        Args:
            row: Row index
            col: Column index
            
        Returns:
            String representation of the cell
        """
        state = self.cell_states[row][col]
        
        if state == CellState.HIDDEN:
            return "·"
        elif state == CellState.FLAGGED:
            return "F"
        elif state == CellState.REVEALED:
            if self.board[row][col]:
                return "*"  # Mine
            num = self.numbers[row][col]
            return str(num) if num > 0 else " "
        return "?"
