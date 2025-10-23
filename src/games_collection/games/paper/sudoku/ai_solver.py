"""Backtracking-friendly AI helpers for Sudoku solving."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence, Tuple

from games_collection.core.ai_strategy import AIStrategy


SudokuGrid = Tuple[Tuple[int, ...], ...]


@dataclass(frozen=True)
class SudokuMove:
    """Represents placing ``value`` at ``(row, column)``."""

    row: int
    column: int
    value: int


@dataclass(frozen=True)
class SudokuBoard:
    """Immutable snapshot of a Sudoku board."""

    cells: SudokuGrid

    @property
    def size(self) -> int:
        return len(self.cells)

    @property
    def block(self) -> int:
        return int(self.size ** 0.5)

    def valid_moves(self) -> Iterable[SudokuMove]:
        for row in range(self.size):
            for column in range(self.size):
                if self.cells[row][column] == 0:
                    for value in self._candidates(row, column):
                        yield SudokuMove(row, column, value)

    def signature(self) -> SudokuGrid:
        return self.cells

    def _candidates(self, row: int, column: int) -> Sequence[int]:
        taken = set(self.cells[row])
        taken.update(self.cells[index][column] for index in range(self.size))
        start_row = (row // self.block) * self.block
        start_column = (column // self.block) * self.block
        for r in range(start_row, start_row + self.block):
            for c in range(start_column, start_column + self.block):
                taken.add(self.cells[r][c])
        return [value for value in range(1, self.size + 1) if value not in taken]

    def conflict_cost(self, move: SudokuMove) -> int:
        row_values = self.cells[move.row]
        if move.value in row_values:
            return 10
        column_values = [self.cells[index][move.column] for index in range(self.size)]
        if move.value in column_values:
            return 10
        start_row = (move.row // self.block) * self.block
        start_column = (move.column // self.block) * self.block
        for r in range(start_row, start_row + self.block):
            for c in range(start_column, start_column + self.block):
                if self.cells[r][c] == move.value:
                    return 10
        return 0


class SudokuSolverStrategy(AIStrategy[SudokuMove, SudokuBoard]):
    """Select Sudoku moves using constraint heuristics."""

    def __init__(self) -> None:
        super().__init__()
        self._score_cache: Dict[Tuple[SudokuGrid, int, int, int], float] = {}

    def select_move(
        self,
        valid_moves: List[SudokuMove],
        game_state: SudokuBoard,
    ) -> SudokuMove:
        if not valid_moves:
            raise ValueError("No valid moves available")

        self._score_cache.clear()
        with self.profile_move("SudokuSolverStrategy.select_move"):
            scored = [(move, self._score_move(game_state, move)) for move in valid_moves]
        best_score = min(score for _, score in scored)
        best_moves = [move for move, score in scored if score == best_score]
        return self.rng.choice(best_moves)

    def _score_move(self, board: SudokuBoard, move: SudokuMove) -> float:
        key = (board.signature(), move.row, move.column, move.value)
        cached = self._score_cache.get(key)
        if cached is not None:
            return cached
        conflict_penalty = board.conflict_cost(move)
        entropy = self._remaining_entropy(board, move)
        score = conflict_penalty + entropy
        self._score_cache[key] = score
        return score

    def _remaining_entropy(self, board: SudokuBoard, move: SudokuMove) -> float:
        updated = self._apply_move(board, move)
        counts = [len(updated._candidates(row, column)) for row, column in self._empty_cells(updated)]
        return float(sum(counts))

    def _apply_move(self, board: SudokuBoard, move: SudokuMove) -> SudokuBoard:
        new_cells = [list(row) for row in board.cells]
        new_cells[move.row][move.column] = move.value
        return SudokuBoard(tuple(tuple(row) for row in new_cells))

    def _empty_cells(self, board: SudokuBoard) -> Iterable[Tuple[int, int]]:
        for row in range(board.size):
            for column in range(board.size):
                if board.cells[row][column] == 0:
                    yield row, column
