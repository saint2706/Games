"""Tests for common base classes and utilities.

This module tests the abstract base classes and utility functions provided
in the common module.
"""

import unittest
from typing import List, Optional

from common import AIStrategy, GameEngine, GameState, HeuristicStrategy, RandomStrategy


class SimpleTestGame(GameEngine[int, str]):
    """A simple test game implementation for testing the GameEngine base class."""

    def __init__(self) -> None:
        """Initialize the test game."""
        self.board: List[str] = [" "] * 9
        self.current_player_val: str = "X"
        self.state: GameState = GameState.IN_PROGRESS

    def reset(self) -> None:
        """Reset the game."""
        self.board = [" "] * 9
        self.current_player_val = "X"
        self.state = GameState.IN_PROGRESS

    def is_game_over(self) -> bool:
        """Check if game is over."""
        return self.state == GameState.FINISHED

    def get_current_player(self) -> str:
        """Get current player."""
        return self.current_player_val

    def get_valid_moves(self) -> List[int]:
        """Get valid moves."""
        return [i for i, cell in enumerate(self.board) if cell == " "]

    def make_move(self, move: int) -> bool:
        """Make a move."""
        if move not in self.get_valid_moves():
            return False
        self.board[move] = self.current_player_val
        self.current_player_val = "O" if self.current_player_val == "X" else "X"
        # Check if board is full
        if not self.get_valid_moves():
            self.state = GameState.FINISHED
        return True

    def get_winner(self) -> Optional[str]:
        """Get winner (simplified - just checks if game is over)."""
        if self.is_game_over():
            return None  # Draw
        return None

    def get_game_state(self) -> GameState:
        """Get game state."""
        return self.state


class TestGameEngine(unittest.TestCase):
    """Tests for GameEngine base class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.game = SimpleTestGame()

    def test_initial_state(self) -> None:
        """Test initial game state."""
        self.assertEqual(self.game.get_current_player(), "X")
        self.assertFalse(self.game.is_game_over())
        self.assertEqual(self.game.get_game_state(), GameState.IN_PROGRESS)
        self.assertEqual(len(self.game.get_valid_moves()), 9)

    def test_make_move(self) -> None:
        """Test making moves."""
        self.assertTrue(self.game.make_move(0))
        self.assertEqual(self.game.board[0], "X")
        self.assertEqual(self.game.get_current_player(), "O")

    def test_invalid_move(self) -> None:
        """Test invalid move handling."""
        self.game.make_move(0)
        self.assertFalse(self.game.make_move(0))  # Same position

    def test_is_valid_move(self) -> None:
        """Test move validation."""
        self.assertTrue(self.game.is_valid_move(0))
        self.game.make_move(0)
        self.assertFalse(self.game.is_valid_move(0))

    def test_reset(self) -> None:
        """Test game reset."""
        self.game.make_move(0)
        self.game.make_move(1)
        self.game.reset()
        self.assertEqual(len(self.game.get_valid_moves()), 9)
        self.assertEqual(self.game.get_current_player(), "X")

    def test_game_over(self) -> None:
        """Test game over state."""
        # Fill the board
        for i in range(9):
            self.game.make_move(i)
        self.assertTrue(self.game.is_game_over())
        self.assertEqual(self.game.get_game_state(), GameState.FINISHED)


class TestRandomStrategy(unittest.TestCase):
    """Tests for RandomStrategy."""

    def test_select_move(self) -> None:
        """Test random move selection."""
        strategy = RandomStrategy()
        valid_moves = [0, 1, 2, 3, 4]
        game_state = None

        # Test multiple selections
        for _ in range(10):
            move = strategy.select_move(valid_moves, game_state)
            self.assertIn(move, valid_moves)

    def test_no_valid_moves(self) -> None:
        """Test behavior with no valid moves."""
        strategy = RandomStrategy()
        with self.assertRaises(ValueError):
            strategy.select_move([], None)

    def test_single_move(self) -> None:
        """Test with single valid move."""
        strategy = RandomStrategy()
        valid_moves = [5]
        move = strategy.select_move(valid_moves, None)
        self.assertEqual(move, 5)


class TestHeuristicStrategy(unittest.TestCase):
    """Tests for HeuristicStrategy."""

    def test_select_best_move(self) -> None:
        """Test selection of best move based on heuristic."""

        def simple_heuristic(move: int, state: None) -> float:
            # Prefer higher numbers
            return float(move)

        strategy = HeuristicStrategy(heuristic_fn=simple_heuristic)
        valid_moves = [1, 2, 3, 4, 5]
        move = strategy.select_move(valid_moves, None)
        self.assertEqual(move, 5)  # Highest score

    def test_tie_breaking(self) -> None:
        """Test random selection among equal-score moves."""

        def constant_heuristic(move: int, state: None) -> float:
            # All moves have same score
            return 1.0

        strategy = HeuristicStrategy(heuristic_fn=constant_heuristic)
        valid_moves = [1, 2, 3, 4, 5]
        move = strategy.select_move(valid_moves, None)
        self.assertIn(move, valid_moves)

    def test_evaluate_move(self) -> None:
        """Test move evaluation."""

        def scoring_heuristic(move: int, state: None) -> float:
            return move * 2.0

        strategy = HeuristicStrategy(heuristic_fn=scoring_heuristic)
        score = strategy.evaluate_move(3, None)
        self.assertEqual(score, 6.0)


if __name__ == "__main__":
    unittest.main()
