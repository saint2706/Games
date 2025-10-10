"""Play the mathematical game of Nim."""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Iterable, List, Tuple


@dataclass
class NimGame:
    """Classic Nim with configurable rules and an optimal computer opponent."""

    heaps: List[int] = field(default_factory=lambda: [3, 4, 5])
    misere: bool = False
    rng: random.Random = field(default_factory=random.Random)

    def __post_init__(self) -> None:
        if not self.heaps or any(heap <= 0 for heap in self.heaps):
            raise ValueError("Heaps must contain positive integers.")

    # ------------------------------------------------------------------
    # Game state helpers
    def is_over(self) -> bool:
        return all(heap == 0 for heap in self.heaps)

    def non_empty_heaps(self) -> Iterable[int]:
        return (heap for heap in self.heaps if heap > 0)

    def player_move(self, heap_index: int, count: int) -> None:
        if heap_index not in range(len(self.heaps)):
            raise ValueError("Invalid heap index.")
        if count <= 0:
            raise ValueError("You must remove at least one object.")
        if count > self.heaps[heap_index]:
            raise ValueError("Cannot remove more objects than the heap contains.")
        self.heaps[heap_index] -= count

    # ------------------------------------------------------------------
    # Combinatorial analysis helpers
    def nim_sum(self) -> int:
        nim_sum = 0
        for heap in self.heaps:
            nim_sum ^= heap
        return nim_sum

    def _available_moves(self) -> List[Tuple[int, int]]:
        moves: List[Tuple[int, int]] = []
        for heap_index, heap in enumerate(self.heaps):
            if heap == 0:
                continue
            for take in range(1, heap + 1):
                moves.append((heap_index, take))
        return moves

    def _nim_sum_after_move(self, heap_index: int, remove: int) -> int:
        new_heaps = list(self.heaps)
        new_heaps[heap_index] -= remove
        nim_sum = 0
        for heap in new_heaps:
            nim_sum ^= heap
        return nim_sum

    def _all_non_zero_heaps_are_singletons(self) -> bool:
        return all(heap == 1 for heap in self.non_empty_heaps())

    # ------------------------------------------------------------------
    # Computer strategy
    def computer_move(self) -> tuple[int, int]:
        if self.misere and self._all_non_zero_heaps_are_singletons():
            heap_index = next(index for index, heap in enumerate(self.heaps) if heap > 0)
            remove = 1
            self.heaps[heap_index] -= remove
            return heap_index, remove

        current_nim_sum = self.nim_sum()
        if current_nim_sum == 0:
            heap_index, remove = self._fallback_move()
        else:
            winning_moves = [
                (heap_index, remove)
                for heap_index, remove in self._available_moves()
                if self._nim_sum_after_move(heap_index, remove) == 0
            ]
            if not winning_moves:
                heap_index, remove = self._fallback_move()
            else:
                heap_index, remove = min(
                    winning_moves,
                    key=lambda move: (self.heaps[move[0]] - move[1], move[0]),
                )
        self.heaps[heap_index] -= remove
        return heap_index, remove

    def _fallback_move(self) -> Tuple[int, int]:
        heap_index = next(index for index, heap in enumerate(self.heaps) if heap > 0)
        return heap_index, 1

    # ------------------------------------------------------------------
    # Presentation helpers
    def render(self) -> str:
        display_parts = []
        for i, heap in enumerate(self.heaps):
            sticks = "|" * min(heap, 12)
            if heap > 12:
                sticks += "…"
            display_parts.append(f"Heap {i + 1}: {sticks} ({heap})")
        return "  ".join(display_parts)


def play() -> None:
    """Run a terminal-based Nim match against the computer."""

    print("Welcome to Nim! Remove sticks; whoever takes the last wins by default.")
    print("You may optionally switch to misère rules where taking the last stick loses.")

    while True:
        heap_input = input(
            "Enter heap sizes separated by spaces (press Enter for the classic 3 4 5): "
        ).strip()
        if heap_input:
            try:
                heaps = [int(value) for value in heap_input.split() if value]
                if not heaps or any(value <= 0 for value in heaps):
                    raise ValueError
            except ValueError:
                print("Please provide positive integers like '1 3 5'.")
                continue
        else:
            heaps = [3, 4, 5]
        break

    misere_choice = input("Play misère Nim (last move loses)? [y/N]: ").strip().lower()
    misere = misere_choice == "y"
    first_choice = input("Do you want to move first? [Y/n]: ").strip().lower()
    human_turn = first_choice != "n"

    game = NimGame(heaps=heaps, misere=misere)
    last_mover: str | None = None
    print(
        "\nStarting heaps: "
        + ", ".join(str(heap) for heap in game.heaps)
        + (" (misère rules)" if misere else " (normal rules)")
    )

    while not game.is_over():
        print("\n" + game.render())
        if human_turn:
            move = input("Choose heap and amount (e.g., 2 3 to take 3 from heap 2): ").split()
            if len(move) != 2:
                print("Enter two numbers: heap index and count to remove.")
                continue
            try:
                heap_index = int(move[0]) - 1
                count = int(move[1])
                game.player_move(heap_index, count)
            except ValueError as exc:
                print(exc)
                continue
            last_mover = "human"
        else:
            heap_index, count = game.computer_move()
            print(f"Computer removes {count} from heap {heap_index + 1}.")
            last_mover = "computer"
        if not game.is_over():
            human_turn = not human_turn

    assert last_mover is not None
    if misere:
        winner = "human" if last_mover == "computer" else "computer"
        print("\nMisère scoring: whoever takes the last object loses!")
    else:
        winner = last_mover
        print("\nNormal scoring: taking the last object wins.")

    if winner == "human":
        print("You win! Congratulations.")
    else:
        print("Computer wins. Better luck next time!")


if __name__ == "__main__":
    play()
