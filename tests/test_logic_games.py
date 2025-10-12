"""Tests for logic and puzzle games."""

from __future__ import annotations

import pytest

from logic_games import LightBulb, LightsOutGame, MinesweeperGame, PicrossGame, SlidingPuzzleGame, SokobanGame
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
        assert all(isinstance(cell, LightBulb) for row in game.grid for cell in row)

    def test_toggle_cell(self) -> None:
        """Test toggling a cell."""
        game = LightsOutGame(size=3)
        positions = [
            (1, 1),
            (0, 1),
            (2, 1),
            (1, 0),
            (1, 2),
        ]
        before = {
            (r, c): game.grid[r][c].is_on
            for r, c in positions
            if 0 <= r < game.size and 0 <= c < game.size
        }

        result = game.make_move((1, 1))
        assert result

        for (r, c), state in before.items():
            assert game.grid[r][c].is_on != state

    def test_win_condition(self) -> None:
        """Test win condition detection."""
        game = LightsOutGame(size=3)
        # Set all lights off
        for row in game.grid:
            for bulb in row:
                bulb.is_on = False
                bulb.brightness = 0.0
        assert game.is_game_over()

    def test_brightness_reflects_neighbors(self) -> None:
        """Bulb brightness should respond to neighbours."""
        game = LightsOutGame(size=3)
        for row in game.grid:
            for bulb in row:
                bulb.is_on = False
                bulb.brightness = 0.0

        game.grid[1][1].is_on = True
        game._recalculate_brightness()

        assert game.grid[1][1].brightness == game.on_brightness
        assert game.grid[0][1].brightness > 0

    def test_energy_tracking(self) -> None:
        """Energy tracking should increase with moves."""
        game = LightsOutGame(size=3)
        initial_energy = game.total_energy_kwh
        initial_time = game.total_time_seconds

        assert game.make_move((0, 0))

        assert game.total_energy_kwh > initial_energy
        assert game.total_time_seconds > initial_time

    def test_state_representation_contains_metrics(self) -> None:
        """Structured state representation should expose telemetry."""
        game = LightsOutGame(size=3)
        state = game.get_state_representation()

        assert "brightness" in state
        assert "power_draw_w" in state
        assert "total_energy_kwh" in state


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
