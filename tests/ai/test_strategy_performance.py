"""Regression benchmarks for AI strategy decision speed."""

from __future__ import annotations

from pathlib import Path
from time import perf_counter
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from games_collection.games.paper.connect_four.ai_minimax import (
    ConnectFourMinimaxStrategy,
    ConnectFourPosition,
)
from games_collection.games.paper.connect_four.connect_four import ConnectFourMove
from games_collection.games.paper.sudoku.ai_solver import SudokuBoard, SudokuMove, SudokuSolverStrategy


def test_connect_four_minimax_decision_time() -> None:
    board = (
        (0, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 2, 0, 0, 0),
        (0, 0, 2, 1, 0, 0, 0),
        (0, 2, 1, 1, 0, 0, 0),
        (2, 1, 1, 2, 0, 0, 0),
    )
    position = ConnectFourPosition(board=board, current_player=1)
    strategy = ConnectFourMinimaxStrategy(max_depth=4)
    valid_moves = list(position.valid_moves())

    start = perf_counter()
    move = strategy.select_move(valid_moves, position)
    duration = perf_counter() - start

    assert isinstance(move, ConnectFourMove)
    assert duration < 0.2, f"Minimax decision took {duration:.3f}s"


def test_sudoku_solver_decision_time() -> None:
    board = (
        (5, 3, 0, 0, 7, 0, 0, 0, 0),
        (6, 0, 0, 1, 9, 5, 0, 0, 0),
        (0, 9, 8, 0, 0, 0, 0, 6, 0),
        (8, 0, 0, 0, 6, 0, 0, 0, 3),
        (4, 0, 0, 8, 0, 3, 0, 0, 1),
        (7, 0, 0, 0, 2, 0, 0, 0, 6),
        (0, 6, 0, 0, 0, 0, 2, 8, 0),
        (0, 0, 0, 4, 1, 9, 0, 0, 5),
        (0, 0, 0, 0, 8, 0, 0, 7, 9),
    )
    sudoku_board = SudokuBoard(cells=board)
    strategy = SudokuSolverStrategy()
    valid_moves = list(sudoku_board.valid_moves())

    start = perf_counter()
    move = strategy.select_move(valid_moves, sudoku_board)
    duration = perf_counter() - start

    assert isinstance(move, SudokuMove)
    assert duration < 0.1, f"Sudoku decision took {duration:.3f}s"
