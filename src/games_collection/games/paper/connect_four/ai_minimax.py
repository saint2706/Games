"""Minimax-based AI strategy for Connect Four."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence, Tuple

from games_collection.core.ai_strategy import MinimaxStrategy
from games_collection.games.paper.connect_four.connect_four import ConnectFourMove


BoardMatrix = Tuple[Tuple[int, ...], ...]


@dataclass(frozen=True)
class ConnectFourPosition:
    """Immutable representation of a Connect Four board."""

    board: BoardMatrix
    current_player: int
    connect_length: int = 4

    @property
    def rows(self) -> int:
        return len(self.board)

    @property
    def columns(self) -> int:
        return len(self.board[0]) if self.board else 0

    def drop(self, column: int) -> "ConnectFourPosition | None":
        for row in range(self.rows - 1, -1, -1):
            if self.board[row][column] == 0:
                new_board = [list(r) for r in self.board]
                new_board[row][column] = self.current_player
                next_player = 2 if self.current_player == 1 else 1
                return ConnectFourPosition(tuple(tuple(r) for r in new_board), next_player, self.connect_length)
        return None

    def valid_moves(self) -> Iterable[ConnectFourMove]:
        for column in range(self.columns):
            if self.board[0][column] == 0:
                yield ConnectFourMove(column)

    def is_terminal(self) -> bool:
        return self._has_winner(1) or self._has_winner(2) or all(self.board[0][column] != 0 for column in range(self.columns))

    def score(self, player: int) -> float:
        return self._line_score(player) - self._line_score(2 if player == 1 else 1)

    def _line_score(self, player: int) -> float:
        score = 0.0
        for window in self._windows():
            marks = window.count(player)
            empties = window.count(0)
            if marks and marks + empties == self.connect_length:
                score += marks ** 2
        return score

    def _has_winner(self, player: int) -> bool:
        return any(window.count(player) == self.connect_length for window in self._windows())

    def _windows(self) -> Iterable[Sequence[int]]:
        for row in range(self.rows):
            for column in range(self.columns - self.connect_length + 1):
                yield self.board[row][column : column + self.connect_length]
        for column in range(self.columns):
            for row in range(self.rows - self.connect_length + 1):
                yield tuple(self.board[row + offset][column] for offset in range(self.connect_length))
        for row in range(self.rows - self.connect_length + 1):
            for column in range(self.columns - self.connect_length + 1):
                yield tuple(self.board[row + offset][column + offset] for offset in range(self.connect_length))
        for row in range(self.connect_length - 1, self.rows):
            for column in range(self.columns - self.connect_length + 1):
                yield tuple(self.board[row - offset][column + offset] for offset in range(self.connect_length))


class ConnectFourMinimaxStrategy(MinimaxStrategy[ConnectFourMove, ConnectFourPosition]):
    """Depth-limited minimax strategy tuned for Connect Four."""

    def __init__(self, max_depth: int = 4) -> None:
        super().__init__(
            max_depth=max_depth,
            alpha_beta=True,
            transition_fn=self._transition,
            move_generator=self._moves,
            is_terminal_fn=lambda position: position.is_terminal(),
            state_key_fn=lambda position: (position.board, position.current_player),
        )
        self._root_player = 1

    def _transition(self, position: ConnectFourPosition, move: ConnectFourMove) -> ConnectFourPosition:
        next_position = position.drop(move.column)
        if next_position is None:
            return position
        return next_position

    def _moves(self, position: ConnectFourPosition) -> Iterable[ConnectFourMove]:
        return tuple(position.valid_moves())

    def select_move(
        self,
        valid_moves: list[ConnectFourMove],
        game_state: ConnectFourPosition,
    ) -> ConnectFourMove:
        self._root_player = game_state.current_player
        return super().select_move(valid_moves, game_state)

    def _evaluate_state(self, position: ConnectFourPosition) -> float:  # type: ignore[override]
        return position.score(self._root_player)
