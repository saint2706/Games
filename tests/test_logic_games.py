"""Tests for logic and puzzle games."""

from __future__ import annotations

import pytest

from logic_games import LightsOutGame, MinesweeperGame, PicrossGame, SlidingPuzzleGame, SokobanGame
from logic_games.minesweeper.minesweeper import Difficulty
from logic_games.picross.picross import CellState


class TestMinesweeper:
    """Test Minesweeper game."""

    def test_initialization_beginner(self) -> None:
        """Test beginner difficulty initialization."""
        game = MinesweeperGame(Difficulty.BEGINNER)
        assert game.rows == 9
        assert game.cols == 9
        assert game.num_mines == 10

    def test_initialization_intermediate(self) -> None:
        """Test intermediate difficulty initialization."""
        game = MinesweeperGame(Difficulty.INTERMEDIATE)
        assert game.rows == 16
        assert game.cols == 16
        assert game.num_mines == 40

    def test_first_click_safe(self) -> None:
        """Test first click is always safe."""
        game = MinesweeperGame()
        game.state = game.state.IN_PROGRESS
        # First click should place mines
        result = game.make_move((0, 0, "reveal"))
        assert result
        # Should not have hit mine
        assert not game.game_lost

    def test_flag_cell(self) -> None:
        """Test flagging a cell."""
        game = MinesweeperGame()
        game.state = game.state.IN_PROGRESS
        result = game.make_move((0, 0, "flag"))
        assert result
        assert (0, 0) in game.flagged_positions


class TestSokoban:
    """Test Sokoban game."""

    def test_initialization(self) -> None:
        """Test game initializes correctly."""
        game = SokobanGame()
        assert len(game.grid) > 0
        assert game.moves == 0

    def test_find_player(self) -> None:
        """Test finding player position."""
        game = SokobanGame()
        pos = game._find_player()
        assert isinstance(pos, tuple)
        assert len(pos) == 2


class TestSlidingPuzzle:
    """Test Sliding Puzzle game."""

    def test_initialization(self) -> None:
        """Test game initializes correctly."""
        game = SlidingPuzzleGame(size=3)
        assert len(game.board) == 9
        assert 0 in game.board  # Empty space
        assert game.size == 3

    def test_valid_moves(self) -> None:
        """Test getting valid moves."""
        game = SlidingPuzzleGame(size=3)
        moves = game.get_valid_moves()
        assert len(moves) > 0
        assert all(m in ["u", "d", "l", "r"] for m in moves)

    def test_move_execution(self) -> None:
        """Test executing a move."""
        game = SlidingPuzzleGame(size=3)
        # Make sure game isn't already solved
        if not game.is_game_over():
            game.state = game.state.IN_PROGRESS
            moves = game.get_valid_moves()
            if moves:
                initial_moves = game.moves
                result = game.make_move(moves[0])
                assert result
                assert game.moves == initial_moves + 1


class TestLightsOut:
    """Test Lights Out game."""

    def test_initialization(self) -> None:
        """Test game initializes correctly."""
        game = LightsOutGame(size=5)
        assert len(game.grid) == 5
        assert all(len(row) == 5 for row in game.grid)

    def test_toggle_cell(self) -> None:
        """Test toggling a cell."""
        game = LightsOutGame(size=3)
        game.state = game.state.IN_PROGRESS
        initial_state = game.grid[1][1]
        game.make_move((1, 1))
        # Center and neighbors should toggle
        assert game.grid[1][1] != initial_state

    def test_win_condition(self) -> None:
        """Test win condition detection."""
        game = LightsOutGame(size=3)
        # Set all lights off
        game.grid = [[False] * 3 for _ in range(3)]
        assert game.is_game_over()


class TestPicross:
    """Test Picross game."""

    def test_initialization(self) -> None:
        """Test game initializes correctly."""
        game = PicrossGame()
        assert game.size == 10
        assert len(game.row_hints) == 10
        assert len(game.col_hints) == 10
        assert all(cell == CellState.UNKNOWN for row in game.grid for cell in row)
        assert game.total_mistakes == 0

    def test_hints_generation(self) -> None:
        """Test hint generation."""
        # Row with no filled cells should have hint [0]
        hints = PicrossGame._get_hints([0, 0, 0])
        assert hints == [0]
        # Row with consecutive filled cells
        hints = PicrossGame._get_hints([1, 1, 0, 1])
        assert hints == [2, 1]

    def test_move_cycle_and_validation(self) -> None:
        """Test filling, toggling and clearing cells."""
        game = PicrossGame()
        assert game.make_move((0, 2, "fill"))
        assert game.grid[0][2] == CellState.FILLED
        assert game.is_cell_correct(0, 2)

        assert game.make_move((0, 2, "toggle"))
        assert game.grid[0][2] == CellState.EMPTY
        assert not game.is_cell_correct(0, 2)
        assert game.total_mistakes == 1
        assert (0, 2) in game.incorrect_cells

        assert game.make_move((0, 2, "clear"))
        assert game.grid[0][2] == CellState.UNKNOWN
        assert (0, 2) not in game.incorrect_cells

    def test_line_progress_tracks_segments(self) -> None:
        """Ensure line progress reflects placed groups."""
        game = PicrossGame()
        game.make_move((0, 2, "fill"))
        game.make_move((0, 3, "fill"))
        progress = game.get_line_progress(0, is_row=True)
        assert list(progress.segments) == [2]
        assert progress.expected_filled == sum(game.row_hints[0])
        assert not progress.is_satisfied

        game.make_move((0, 2, "clear"))
        progress_after_clear = game.get_line_progress(0, is_row=True)
        assert list(progress_after_clear.segments) == [1]

        game.make_move((0, 3, "clear"))
        progress_all_cleared = game.get_line_progress(0, is_row=True)
        assert list(progress_all_cleared.segments) == [0]

    def test_mistake_tracking(self) -> None:
        """Incorrect placements are counted once until cleared."""
        game = PicrossGame()
        assert game.make_move((0, 0, "fill"))  # incorrect cell
        assert (0, 0) in game.incorrect_cells
        assert game.total_mistakes == 1

        # Repeating the same incorrect action should not double count
        assert game.make_move((0, 0, "fill"))
        assert game.total_mistakes == 1

        # Clearing removes the mistake marker
        assert game.make_move((0, 0, "clear"))
        assert (0, 0) not in game.incorrect_cells
