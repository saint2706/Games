"""Tic-tac-toe game with a minimax-powered computer opponent."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Tuple


COORDINATES: Dict[str, int] = {
    "A1": 0,
    "A2": 1,
    "A3": 2,
    "B1": 3,
    "B2": 4,
    "B3": 5,
    "C1": 6,
    "C2": 7,
    "C3": 8,
}
INDEX_TO_COORD = {index: coord for coord, index in COORDINATES.items()}


@dataclass
class TicTacToeGame:
    """Play a game of tic-tac-toe against an optimal computer opponent."""

    human_symbol: str = "X"
    computer_symbol: str = "O"
    starting_symbol: Optional[str] = None

    def __post_init__(self) -> None:
        if self.human_symbol == self.computer_symbol:
            raise ValueError("Players must use distinct symbols.")
        self.board: List[str] = [" "] * 9
        self.reset(self.starting_symbol)

    def reset(self, starting_symbol: Optional[str] = None) -> None:
        if starting_symbol is not None:
            self.starting_symbol = starting_symbol
        if self.starting_symbol is None:
            self.starting_symbol = self.human_symbol
        if self.starting_symbol not in {self.human_symbol, self.computer_symbol}:
            raise ValueError("Starting symbol must belong to one of the players.")
        self.board = [" "] * 9
        self.current_turn = self.starting_symbol or self.human_symbol

    def available_moves(self) -> List[int]:
        return [i for i, value in enumerate(self.board) if value == " "]

    def make_move(self, position: int, symbol: str) -> bool:
        if position not in range(9):
            raise ValueError("Position must be between 0 and 8 inclusive.")
        if self.board[position] != " ":
            return False
        self.board[position] = symbol
        return True

    def winner(self) -> Optional[str]:
        lines = [
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),
            (0, 4, 8),
            (2, 4, 6),
        ]
        for a, b, c in lines:
            if (
                self.board[a] != " "
                and self.board[a] == self.board[b] == self.board[c]
            ):
                return self.board[a]
        return None

    def is_draw(self) -> bool:
        return " " not in self.board and self.winner() is None

    def minimax(
        self, is_maximizing: bool, depth: int = 0
    ) -> Tuple[int, Optional[int]]:
        winner = self.winner()
        if winner == self.computer_symbol:
            return 10 - depth, None
        if winner == self.human_symbol:
            return depth - 10, None
        if self.is_draw():
            return 0, None

        best_score = float("-inf") if is_maximizing else float("inf")
        best_move: Optional[int] = None
        symbol = self.computer_symbol if is_maximizing else self.human_symbol

        for move in self.available_moves():
            self.board[move] = symbol
            score, _ = self.minimax(not is_maximizing, depth + 1)
            self.board[move] = " "
            if is_maximizing:
                if score > best_score:
                    best_score = score
                    best_move = move
            else:
                if score < best_score:
                    best_score = score
                    best_move = move
        return int(best_score), best_move

    def computer_move(self) -> int:
        _, move = self.minimax(True)
        if move is None:
            move = self.available_moves()[0]
        self.make_move(move, self.computer_symbol)
        return move

    def human_move(self, position: int) -> bool:
        return self.make_move(position, self.human_symbol)

    def render(self, show_reference: bool = False) -> str:
        """Return a human-friendly board representation."""

        header = "    1   2   3"
        separator = "  +---+---+---"
        rows = []
        for row_index, row_label in enumerate("ABC"):
            start = row_index * 3
            cells = " | ".join(self.board[start : start + 3])
            rows.append(f"{row_label} | {cells}")
        board_render = "\n".join(
            [header, separator, rows[0], separator, rows[1], separator, rows[2]]
        )
        if not show_reference:
            return board_render
        reference_rows = []
        for row_index, row_label in enumerate("ABC"):
            start = row_index * 3
            coords = " | ".join(
                INDEX_TO_COORD[start + offset] for offset in range(3)
            )
            reference_rows.append(f"{row_label} | {coords}")
        reference = "\n".join(
            [
                "Reference:",
                "    1   2   3",
                "  +---+---+---",
                reference_rows[0],
                "  +---+---+---",
                reference_rows[1],
                "  +---+---+---",
                reference_rows[2],
            ]
        )
        return board_render + "\n\n" + reference

    def legal_coordinates(self) -> Iterable[str]:
        return (coord for coord, idx in COORDINATES.items() if self.board[idx] == " ")

    def parse_coordinate(self, text: str) -> int:
        text = text.strip().upper()
        if text not in COORDINATES:
            raise ValueError("Enter a coordinate like A1, B3, or C2.")
        return COORDINATES[text]

    def swap_turn(self) -> None:
        self.current_turn = (
            self.computer_symbol
            if self.current_turn == self.human_symbol
            else self.human_symbol
        )


def play() -> None:
    """Run the game loop in the terminal."""

    print("Welcome to Tic-Tac-Toe! Coordinates are letter-row + number-column (e.g. B2).")
    human_symbol = input("Choose your symbol (X or O) [X]: ").strip().upper() or "X"
    if human_symbol not in {"X", "O"}:
        print("Invalid symbol chosen. Defaulting to X.")
        human_symbol = "X"
    computer_symbol = "O" if human_symbol == "X" else "X"

    wants_first = input("Do you want to go first? [Y/n]: ").strip().lower()
    if wants_first in {"n", "no"}:
        starting_symbol = computer_symbol
    elif wants_first in {"y", "yes", ""}:
        starting_symbol = human_symbol
    else:
        starting_symbol = random.choice([human_symbol, computer_symbol])
        print(f"We'll toss a coin… {('You' if starting_symbol == human_symbol else 'Computer')} start(s)!")

    game = TicTacToeGame(
        human_symbol=human_symbol,
        computer_symbol=computer_symbol,
        starting_symbol=starting_symbol,
    )

    print("\nThe empty board looks like this:")
    print(game.render(show_reference=True))

    while True:
        print("\n" + game.render())
        if game.winner() or game.is_draw():
            break

        if game.current_turn == game.human_symbol:
            prompt = "Choose your move: "
            move_str = input(prompt)
            try:
                position = game.parse_coordinate(move_str)
            except ValueError as exc:
                print(exc)
                continue
            if not game.human_move(position):
                print("That square is already taken. Try again.")
                continue
        else:
            print("Computer is thinking…")
            comp_position = game.computer_move()
            print(f"Computer chooses {INDEX_TO_COORD[comp_position]}.")

        if game.winner() or game.is_draw():
            break
        game.swap_turn()

    print("\n" + game.render())
    winner = game.winner()
    if winner == game.human_symbol:
        print("You win! Congratulations.")
    elif winner == game.computer_symbol:
        print("Computer wins with perfect play.")
    else:
        print("It's a draw – a classic cat's game.")


if __name__ == "__main__":
    play()
