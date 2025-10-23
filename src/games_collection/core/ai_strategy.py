"""AI strategy pattern implementations for game opponents.

This module provides a flexible and extensible implementation of the strategy
pattern for AI decision-making. It allows different AI algorithms to be
encapsulated in separate classes and used interchangeably within a game,
without altering the core game logic.

The key components are:
- `AIStrategy`: An abstract base class that defines the common interface for
  all AI strategies.
- `RandomStrategy`: A simple strategy that selects moves randomly.
- `MinimaxStrategy`: A placeholder for a minimax-based strategy, suitable for
  perfect-play games.
- `HeuristicStrategy`: A strategy that uses a heuristic function to evaluate
  and select the best move.

This modular approach makes it easy to add new AI behaviors and to configure
different difficulty levels for computer-controlled opponents.
"""

from __future__ import annotations

import os
import random
import time
from abc import ABC, abstractmethod
from collections import OrderedDict
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from threading import Lock
from typing import Callable, Generator, Generic, Hashable, Iterable, List, Optional, Tuple, TypeVar

import cProfile
import pstats

PROFILE_ENV_FLAG = "GAMES_PROFILE_AI"
PROFILE_DIR_ENV = "GAMES_PROFILE_AI_DIR"

# Type variable for move representation, allowing for flexibility in how
# different games define a "move."
MoveType = TypeVar("MoveType")

# Type variable for game state representation, allowing strategies to work
# with various forms of game state information.
StateType = TypeVar("StateType")


def _profile_directory() -> Path:
    """Return the directory where profiling artefacts should be stored."""

    location = os.getenv(PROFILE_DIR_ENV, "profiling")
    path = Path(location).expanduser().resolve()
    path.mkdir(parents=True, exist_ok=True)
    return path


@contextmanager
def _profiling_session(label: str) -> Generator[None, None, None]:
    """Profile a block of code when profiling is enabled."""

    if not os.getenv(PROFILE_ENV_FLAG):
        yield
        return
    profiler = cProfile.Profile()
    profiler.enable()
    start = time.perf_counter()
    try:
        yield
    finally:
        profiler.disable()
        duration_ms = (time.perf_counter() - start) * 1000
        timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%S%f")
        output_file = _profile_directory() / f"{label}_{timestamp}.prof"
        stream = output_file.open("w", encoding="utf-8")
        with stream:
            stream.write(f"# Profiling stats for {label} ({duration_ms:.2f} ms)\n")
            stats = pstats.Stats(profiler, stream=stream).sort_stats("tottime")
            stats.print_stats(25)


class AIStrategy(ABC, Generic[MoveType, StateType]):
    """Abstract base class for AI strategies.

    This class defines the essential interface that all AI strategies must
    implement. It establishes a contract for how the game engine interacts
    with different AI decision-making algorithms, such as random selection,
    minimax, or heuristic-based approaches.

    Type Parameters:
        MoveType: The type used to represent a move in the game.
        StateType: The type used to represent the game's state.
    """

    def __init__(self, rng: Optional[random.Random] = None) -> None:
        """Initialize the AI strategy.

        Args:
            rng: An optional random number generator. Providing a seeded RNG
                 can be useful for creating deterministic and reproducible AI
                 behavior, which is especially valuable for testing.
        """
        self.rng = rng or random.Random()

    @contextmanager
    def profile_move(self, label: str) -> Generator[None, None, None]:
        """Profile a decision-making block when profiling is enabled."""

        with _profiling_session(label):
            yield

    @abstractmethod
    def select_move(
        self,
        valid_moves: List[MoveType],
        game_state: StateType,
    ) -> MoveType:
        """Select the best move based on the implemented strategy.

        This is the core method of the strategy, where the AI's "thinking"
        process takes place.

        Args:
            valid_moves: A list of all valid moves available to the AI.
            game_state: The current state of the game, which the AI can use
                        to make its decision.

        Returns:
            The move selected by the AI.

        Raises:
            ValueError: If `valid_moves` is empty, as there is no move to
                        select.
        """
        pass

    def evaluate_move(
        self,
        move: MoveType,
        game_state: StateType,
    ) -> float:
        """Evaluate the quality of a potential move.

        While not always required, this method can be implemented by
        strategies to provide a score for a given move. This is particularly
        useful for more advanced AI, such as those that need to compare
        multiple moves.

        Args:
            move: The move to evaluate.
            game_state: The current state of the game.

        Returns:
            A score representing the quality of the move. Higher scores
            typically indicate better moves. The default implementation
            returns 0.0.
        """
        return 0.0


class RandomStrategy(AIStrategy[MoveType, StateType]):
    """A simple AI strategy that selects moves randomly.

    This strategy is useful as a baseline for testing, for creating an "easy"
    difficulty level, or for games where randomness is a key element.
    """

    def select_move(
        self,
        valid_moves: List[MoveType],
        game_state: StateType,
    ) -> MoveType:
        """Select a random move from the list of valid moves.

        Args:
            valid_moves: A list of all valid moves to choose from.
            game_state: The current state of the game (unused by this
                        strategy).

        Returns:
            A randomly selected move from the `valid_moves` list.

        Raises:
            ValueError: If `valid_moves` is empty.
        """
        if not valid_moves:
            raise ValueError("No valid moves available")
        with self.profile_move("RandomStrategy.select_move"):
            return self.rng.choice(valid_moves)


class MinimaxStrategy(AIStrategy[MoveType, StateType]):
    """A minimax-based strategy for perfect play in two-player games.

    This strategy is intended to use the minimax algorithm, optionally enhanced
    with alpha-beta pruning, to find the optimal move in zero-sum games like
    Tic-Tac-Toe or Checkers.

    Note: The current implementation is a placeholder and selects moves
          randomly. It needs to be extended with the actual minimax logic.
    """

    def __init__(
        self,
        max_depth: int = 10,
        alpha_beta: bool = True,
        evaluation_fn: Optional[Callable[[StateType], float]] = None,
        *,
        transition_fn: Optional[Callable[[StateType, MoveType], StateType]] = None,
        move_generator: Optional[Callable[[StateType], Iterable[MoveType]]] = None,
        is_terminal_fn: Optional[Callable[[StateType], bool]] = None,
        state_key_fn: Optional[Callable[[StateType], Hashable]] = None,
        rng: Optional[random.Random] = None,
    ) -> None:
        """Initialize the minimax strategy.

        Args:
            max_depth: The maximum depth for the minimax search tree.
            alpha_beta: A flag to enable or disable alpha-beta pruning.
            evaluation_fn: An optional function to evaluate non-terminal
                           states, which is necessary for games that are too
                           complex to search to the end.
            rng: An optional random number generator for tie-breaking.
        """
        super().__init__(rng)
        self.max_depth = max_depth
        self.alpha_beta = alpha_beta
        self.evaluation_fn = evaluation_fn
        self.transition_fn = transition_fn
        self.move_generator = move_generator
        self.is_terminal_fn = is_terminal_fn
        self.state_key_fn = state_key_fn
        self._memo: dict[Tuple[Hashable, int, bool], float] = {}

    def select_move(
        self,
        valid_moves: List[MoveType],
        game_state: StateType,
    ) -> MoveType:
        """Select the best move using the minimax algorithm.

        Args:
            valid_moves: A list of all valid moves to choose from.
            game_state: The current state of the game.

        Returns:
            The move with the highest minimax value.

        Raises:
            ValueError: If `valid_moves` is empty.
        """
        if not valid_moves:
            raise ValueError("No valid moves available")

        self._memo.clear()
        scored_moves: List[Tuple[MoveType, float]] = []
        with self.profile_move("MinimaxStrategy.select_move"):
            for move in valid_moves:
                score = self._evaluate_branch(game_state, move)
                scored_moves.append((move, score))
        best_score = max(score for _, score in scored_moves)
        best_moves = [move for move, score in scored_moves if score == best_score]
        return self.rng.choice(best_moves)

    def _evaluate_branch(self, state: StateType, move: MoveType) -> float:
        next_state = self._transition(state, move)
        depth = max(self.max_depth - 1, 0)
        if depth == 0:
            return self._evaluate_state(next_state)
        return self._minimax(next_state, depth, float("-inf"), float("inf"), False)

    def _minimax(
        self,
        state: StateType,
        depth: int,
        alpha: float,
        beta: float,
        maximizing: bool,
    ) -> float:
        cache_key = self._cache_key(state, depth, maximizing)
        if cache_key is not None and cache_key in self._memo:
            return self._memo[cache_key]
        if depth == 0 or self._is_terminal(state):
            score = self._evaluate_state(state)
        elif maximizing:
            score = self._maximize(state, depth, alpha, beta)
        else:
            score = self._minimize(state, depth, alpha, beta)
        if cache_key is not None:
            self._memo[cache_key] = score
        return score

    def _maximize(self, state: StateType, depth: int, alpha: float, beta: float) -> float:
        moves = list(self._moves(state))
        if not moves:
            return self._evaluate_state(state)
        best = float("-inf")
        for move in moves:
            child = self._transition(state, move)
            score = self._minimax(child, depth - 1, alpha, beta, False)
            best = max(best, score)
            if self.alpha_beta:
                alpha = max(alpha, best)
                if beta <= alpha:
                    break
        return best

    def _minimize(self, state: StateType, depth: int, alpha: float, beta: float) -> float:
        moves = list(self._moves(state))
        if not moves:
            return self._evaluate_state(state)
        best = float("inf")
        for move in moves:
            child = self._transition(state, move)
            score = self._minimax(child, depth - 1, alpha, beta, True)
            best = min(best, score)
            if self.alpha_beta:
                beta = min(beta, best)
                if beta <= alpha:
                    break
        return best

    def _transition(self, state: StateType, move: MoveType) -> StateType:
        if self.transition_fn is not None:
            return self.transition_fn(state, move)
        if hasattr(state, "apply_move"):
            return getattr(state, "apply_move")(move)
        raise ValueError("MinimaxStrategy requires a transition_fn or state.apply_move")

    def _moves(self, state: StateType) -> Iterable[MoveType]:
        if self.move_generator is not None:
            return self.move_generator(state)
        if hasattr(state, "get_valid_moves"):
            return getattr(state, "get_valid_moves")()
        raise ValueError("MinimaxStrategy requires a move_generator or state.get_valid_moves")

    def _is_terminal(self, state: StateType) -> bool:
        if self.is_terminal_fn is not None:
            return self.is_terminal_fn(state)
        if hasattr(state, "is_terminal"):
            return bool(getattr(state, "is_terminal")())
        if hasattr(state, "is_game_over"):
            return bool(getattr(state, "is_game_over")())
        return False

    def _evaluate_state(self, state: StateType) -> float:
        if self.evaluation_fn is not None:
            return self.evaluation_fn(state)
        if hasattr(state, "evaluate"):
            return float(getattr(state, "evaluate")())
        return 0.0

    def _cache_key(self, state: StateType, depth: int, maximizing: bool) -> Optional[Tuple[Hashable, int, bool]]:
        if self.state_key_fn is None:
            return None
        return self.state_key_fn(state), depth, maximizing

    def evaluate_move(
        self,
        move: MoveType,
        game_state: StateType,
    ) -> float:
        """Evaluate a move using the provided evaluation function.

        If an evaluation function is provided, this method will use it to
        score the game state.

        Args:
            move: The move to evaluate.
            game_state: The current state of the game.

        Returns:
            The evaluation score for the move, or 0.0 if no evaluation
            function is set.
        """
        if self.evaluation_fn:
            return self.evaluation_fn(game_state)
        return 0.0


class HeuristicStrategy(AIStrategy[MoveType, StateType]):
    """A strategy that selects moves based on a heuristic evaluation.

    This strategy evaluates each possible move using a provided heuristic
    function and chooses the one with the highest score. It is well-suited for
    games where a full search is not feasible, but where a "rule of thumb" can
    guide the AI toward good moves.

    For performance-sensitive scenarios, it supports optional caching of
    heuristic scores to avoid recomputing them for the same game states.
    """

    def __init__(
        self,
        heuristic_fn: Callable[[MoveType, StateType], float],
        *,
        cache_key_fn: Optional[Callable[[MoveType, StateType], Hashable]] = None,
        cache_size: int = 128,
        rng: Optional[random.Random] = None,
    ) -> None:
        """Initialize the heuristic strategy.

        Args:
            heuristic_fn: A function that takes a move and a game state and
                          returns a score for that move.
            cache_key_fn: An optional function that generates a hashable cache
                          key from a move and game state. If provided,
                          heuristic results are memoized.
            cache_size: The maximum number of entries to store in the LRU
                        cache. This is only used if `cache_key_fn` is provided.
            rng: An optional random number generator for tie-breaking.

        Raises:
            ValueError: If `cache_size` is not a positive integer.
        """
        super().__init__(rng)
        self.heuristic_fn = heuristic_fn
        self.cache_key_fn = cache_key_fn
        if cache_size <= 0:
            raise ValueError("cache_size must be a positive integer")
        self.cache_size = cache_size
        self._cache: OrderedDict[Hashable, float] = OrderedDict()
        self._cache_lock = Lock()

    def select_move(
        self,
        valid_moves: List[MoveType],
        game_state: StateType,
    ) -> MoveType:
        """Select the move with the highest heuristic value.

        If multiple moves share the same highest score, one is chosen at
        random.

        Args:
            valid_moves: A list of all valid moves to choose from.
            game_state: The current state of the game.

        Returns:
            The move with the highest heuristic score.

        Raises:
            ValueError: If `valid_moves` is empty.
        """
        if not valid_moves:
            raise ValueError("No valid moves available")

        with self.profile_move("HeuristicStrategy.select_move"):
            scored_moves = [(move, self._score_move(move, game_state)) for move in valid_moves]
        max_score = max(score for _, score in scored_moves)
        best_moves = [move for move, score in scored_moves if score == max_score]
        return self.rng.choice(best_moves)

    def evaluate_move(
        self,
        move: MoveType,
        game_state: StateType,
    ) -> float:
        """Evaluate a move using the heuristic function, with caching.

        Args:
            move: The move to evaluate.
            game_state: The current state of the game.

        Returns:
            The heuristic score for the move.
        """
        return self._score_move(move, game_state)

    def clear_cache(self) -> None:
        """Clear any cached heuristic values.

        This can be useful when the game state changes in a way that would
        invalidate the cached scores.
        """
        if not self.cache_key_fn:
            return
        with self._cache_lock:
            self._cache.clear()

    def _score_move(self, move: MoveType, game_state: StateType) -> float:
        """Return the heuristic score for a move, using caching if available.

        This internal method handles the logic for checking the cache, calling
        the heuristic function if necessary, and updating the cache.

        Args:
            move: The move to score.
            game_state: The current state of the game.

        Returns:
            The heuristic score for the move.
        """
        if not self.cache_key_fn:
            # If no caching is configured, just call the heuristic function
            return self.heuristic_fn(move, game_state)

        cache_key = self.cache_key_fn(move, game_state)
        # Use a lock to ensure thread-safe access to the cache.
        with self._cache_lock:
            # Check if the score for the current state is already in the cache.
            cached_score = self._cache.get(cache_key)
            if cached_score is not None:
                # If the item is in the cache, move it to the end to mark it as
                # recently used. This is part of the LRU (Least Recently Used)
                # cache strategy.
                self._cache.move_to_end(cache_key)
                return cached_score

        # If the score is not in the cache, compute it using the heuristic function.
        score = self.heuristic_fn(move, game_state)
        with self._cache_lock:
            # Store the newly computed score in the cache.
            self._cache[cache_key] = score
            # If the cache has exceeded its maximum size, remove the least
            # recently used item (the one at the beginning of the OrderedDict).
            if len(self._cache) > self.cache_size:
                self._cache.popitem(last=False)
        return score
