"""Game engine and logic for the mathematical game of Nim.

This module provides the core game logic for Nim, including the game state,
move validation, and an optimal computer opponent based on nim-sum calculations.
The computer player uses combinatorial game theory to find winning moves when
possible.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Iterable, List, Tuple


@dataclass
class NimGame:
    """Classic Nim with configurable rules and an optimal computer opponent."""

    heaps: List[int] = field(default_factory=lambda: [3, 4, 5])
    misere: bool = False  # In misere Nim, the player who takes the last object loses.
    rng: random.Random = field(default_factory=random.Random)

    def __post_init__(self) -> None:
        """Validates the initial game state after the dataclass is created."""
        if not self.heaps or any(heap <= 0 for heap in self.heaps):
            raise ValueError("Heaps must contain positive integers.")

    # ------------------------------------------------------------------
    # Game state helpers
    def is_over(self) -> bool:
        """Checks if the game is over (all heaps are empty)."""
        return all(heap == 0 for heap in self.heaps)

    def non_empty_heaps(self) -> Iterable[int]:
        """Returns an iterator over the non-empty heaps."""
        return (heap for heap in self.heaps if heap > 0)

    def player_move(self, heap_index: int, count: int) -> None:
        """Applies a player's move to the game state."""
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
        """Calculates the Nim-sum of the current heaps, a key concept in Nim strategy."""
        nim_sum = 0
        for heap in self.heaps:
            nim_sum ^= heap
        return nim_sum

    def _available_moves(self) -> List[Tuple[int, int]]:
        """Returns a list of all possible moves (heap_index, count)."""
        moves: List[Tuple[int, int]] = []
        for heap_index, heap in enumerate(self.heaps):
            if heap == 0:
                continue
            for take in range(1, heap + 1):
                moves.append((heap_index, take))
        return moves

    def _nim_sum_after_move(self, heap_index: int, remove: int) -> int:
        """Calculates what the Nim-sum would be after a given move."""
        new_heaps = list(self.heaps)
        new_heaps[heap_index] -= remove
        nim_sum = 0
        for heap in new_heaps:
            nim_sum ^= heap
        return nim_sum

    def _all_non_zero_heaps_are_singletons(self) -> bool:
        """Checks if all non-empty heaps have a size of 1."""
        return all(heap == 1 for heap in self.non_empty_heaps())

    # ------------------------------------------------------------------
    # Computer strategy
    def computer_move(self) -> tuple[int, int]:
        """Determines and applies the optimal computer move."""
        # Special case for misere Nim when all heaps are size 1.
        if self.misere and self._all_non_zero_heaps_are_singletons():
            heap_index = next(index for index, heap in enumerate(self.heaps) if heap > 0)
            remove = 1
            self.heaps[heap_index] -= remove
            return heap_index, remove

        current_nim_sum = self.nim_sum()
        if current_nim_sum == 0:
            # If the Nim-sum is 0, the current player is in a losing position.
            # The computer makes a random move as a fallback.
            heap_index, remove = self._fallback_move()
        else:
            # If the Nim-sum is non-zero, there is a winning move.
            # The computer finds a move that results in a Nim-sum of 0.
            winning_moves = [(heap_index, remove) for heap_index, remove in self._available_moves() if self._nim_sum_after_move(heap_index, remove) == 0]
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
        """A non-optimal move to make when no winning move is available."""
        heap_index = next(index for index, heap in enumerate(self.heaps) if heap > 0)
        return heap_index, 1

    # ------------------------------------------------------------------
    # Presentation helpers
    def render(self) -> str:
        """Renders the current state of the heaps as a string."""
        display_parts = []
        for i, heap in enumerate(self.heaps):
            sticks = "|" * min(heap, 12)
            if heap > 12:
                sticks += "…"
            display_parts.append(f"Heap {i + 1}: {sticks} ({heap})")
        return "  ".join(display_parts)
