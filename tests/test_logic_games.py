"""Tests for logic and puzzle games."""

from __future__ import annotations

import pytest

from logic_games import LightsOutGame, MinesweeperGame, PicrossGame, SlidingPuzzleGame, SokobanGame
from logic_games.minesweeper.minesweeper import Difficulty


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
        game = SlidingPuzzleGame(size=4)
        assert len(game.board) == 16
        assert 0 in game.board  # Empty space
        assert game.size == 4
        assert not game.is_game_over()

    def test_valid_moves(self) -> None:
        """Test getting valid moves."""
        game = SlidingPuzzleGame(size=4)
        moves = game.get_valid_moves()
        assert len(moves) > 0
        assert all(m in ["u", "d", "l", "r"] for m in moves)

    def test_move_execution(self) -> None:
        """Test executing moves by direction and tile number."""
        game = SlidingPuzzleGame(size=4)
        moves = game.get_valid_moves()
        assert moves
        initial_moves = game.moves
        assert game.make_move(moves[0])
        assert game.moves == initial_moves + 1

        zero_idx = game.board.index(0)
        row, col = divmod(zero_idx, game.size)
        neighbor_indices = []
        if row > 0:
            neighbor_indices.append(zero_idx - game.size)
        if row < game.size - 1:
            neighbor_indices.append(zero_idx + game.size)
        if col > 0:
            neighbor_indices.append(zero_idx - 1)
        if col < game.size - 1:
            neighbor_indices.append(zero_idx + 1)
        tile_to_slide = next(game.board[idx] for idx in neighbor_indices if game.board[idx] != 0)
        assert tile_to_slide != 0
        assert game.make_move(str(tile_to_slide))


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
        assert len(game.row_hints) > 0
        assert len(game.col_hints) > 0
        assert game.size > 0

    def test_hints_generation(self) -> None:
        """Test hint generation."""
        game = PicrossGame()
        # Row with no filled cells should have hint [0]
        hints = game._get_hints([0, 0, 0])
        assert hints == [0]
        # Row with consecutive filled cells
        hints = game._get_hints([1, 1, 0, 1])
        assert hints == [2, 1]

    def test_make_move(self) -> None:
        """Test making a move."""
        game = PicrossGame()
        game.state = game.state.IN_PROGRESS
        result = game.make_move((0, 0, "fill"))
        assert result
        assert game.grid[0][0] is not None
