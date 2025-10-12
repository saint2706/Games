"""Tests for logic and puzzle games."""

from __future__ import annotations

import pytest

from common.game_engine import GameState
from logic_games import LightsOutGame, MinesweeperGame, PicrossGame, SlidingPuzzleGame, SokobanGame
from logic_games.minesweeper.minesweeper import CellState, Difficulty


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
        game.state = GameState.IN_PROGRESS
        # First click should place mines
        result = game.make_move((0, 0, "reveal"))
        assert result
        # Should not have hit mine
        assert not game.game_lost

    def test_flag_cell(self) -> None:
        """Test flagging a cell."""
        game = MinesweeperGame()
        game.state = GameState.IN_PROGRESS
        result = game.make_move((0, 0, "flag"))
        assert result
        assert (0, 0) in game.flagged_positions

    def test_question_mark_cycle(self) -> None:
        """Test cycling through mark states."""
        game = MinesweeperGame()
        game.state = GameState.IN_PROGRESS

        assert game.make_move((0, 0, "question"))
        assert game.cell_states[0][0] == CellState.QUESTION

        assert game.make_move((0, 0, "flag"))
        assert game.cell_states[0][0] == CellState.FLAGGED
        assert (0, 0) in game.flagged_positions

        assert game.make_move((0, 0, "question"))
        assert game.cell_states[0][0] == CellState.QUESTION
        assert (0, 0) not in game.flagged_positions

        assert game.make_move((0, 0, "unflag"))
        assert game.cell_states[0][0] == CellState.HIDDEN

    def test_chord_reveals_neighbors(self) -> None:
        """Chord action should reveal adjacent hidden cells when flags match numbers."""

        game = MinesweeperGame()
        game.state = GameState.IN_PROGRESS
        game.board = [[False] * game.cols for _ in range(game.rows)]
        game.cell_states = [[CellState.HIDDEN] * game.cols for _ in range(game.rows)]
        game.numbers = [[0] * game.cols for _ in range(game.rows)]

        game.board[0][0] = True
        for row in range(3):
            for col in range(3):
                if not game.board[row][col]:
                    game.numbers[row][col] = game._count_adjacent_mines(row, col)

        assert game.make_move((1, 1, "reveal"))
        assert game.numbers[1][1] == 1
        assert game.cell_states[1][1] == CellState.REVEALED

        assert game.make_move((0, 0, "flag"))
        assert game.make_move((1, 1, "chord"))
        assert game.cell_states[2][2] == CellState.REVEALED

    def test_misflag_display_after_loss(self) -> None:
        """Misflagged cells should be indicated when the player loses."""

        game = MinesweeperGame()
        game.state = GameState.IN_PROGRESS
        game.board = [[False] * game.cols for _ in range(game.rows)]
        game.cell_states = [[CellState.HIDDEN] * game.cols for _ in range(game.rows)]
        game.numbers = [[0] * game.cols for _ in range(game.rows)]

        game.board[0][0] = True
        for row in range(2):
            for col in range(2):
                if not game.board[row][col]:
                    game.numbers[row][col] = game._count_adjacent_mines(row, col)

        assert game.make_move((0, 1, "flag"))
        assert game.make_move((0, 0, "reveal"))
        assert game.game_lost
        assert game.get_cell_display(0, 0) == "*"
        assert game.get_cell_display(0, 1) == "✗"


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
