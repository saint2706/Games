"""Battleship implementation with full fleets and a hunting AI opponent."""

from __future__ import annotations

import random
from collections import deque
from dataclasses import dataclass, field
from typing import Deque, Dict, Iterable, List, Optional, Sequence, Set, Tuple

Coordinate = Tuple[int, int]


@dataclass
class Ship:
    """Representation of a single ship on the board."""

    name: str
    length: int
    coordinates: Set[Coordinate]
    hits: Set[Coordinate] = field(default_factory=set)

    def register_hit(self, coord: Coordinate) -> None:
        self.hits.add(coord)

    @property
    def is_sunk(self) -> bool:
        return len(self.hits) == len(self.coordinates)


class Board:
    """Board that tracks ships, shots, and rendering."""

    def __init__(self, size: int) -> None:
        if size < 4:
            raise ValueError("Board must be at least 4x4.")
        self.size = size
        self.ships: List[Ship] = []
        self.occupied: Set[Coordinate] = set()
        self.shots: Dict[Coordinate, str] = {}

    def in_bounds(self, coord: Coordinate) -> bool:
        row, col = coord
        return 0 <= row < self.size and 0 <= col < self.size

    def place_ship(self, name: str, length: int, start: Coordinate, orientation: str) -> None:
        orientation = orientation.lower()
        if orientation not in {"h", "v"}:
            raise ValueError("Orientation must be 'h' or 'v'.")
        row, col = start
        if orientation == "h":
            coords = {(row, col + offset) for offset in range(length)}
        else:
            coords = {(row + offset, col) for offset in range(length)}
        if not all(self.in_bounds(coord) for coord in coords):
            raise ValueError("Ship placement is out of bounds.")
        if any(coord in self.occupied for coord in coords):
            raise ValueError("Ships cannot overlap.")
        ship = Ship(name=name, length=length, coordinates=coords)
        self.ships.append(ship)
        self.occupied.update(coords)

    def randomly_place_ships(self, ships: Sequence[Tuple[str, int]], rng: random.Random) -> None:
        for name, length in ships:
            placed = False
            attempts = 0
            while not placed:
                attempts += 1
                if attempts > 1000:
                    raise RuntimeError("Failed to place ships without overlap.")
                orientation = rng.choice(["h", "v"])
                row = rng.randrange(self.size)
                col = rng.randrange(self.size)
                try:
                    self.place_ship(name, length, (row, col), orientation)
                except ValueError:
                    continue
                placed = True

    def receive_shot(self, coord: Coordinate) -> Tuple[str, Optional[str]]:
        if not self.in_bounds(coord):
            raise ValueError("Shot outside the board.")
        if coord in self.shots:
            raise ValueError("Coordinate has already been targeted.")
        for ship in self.ships:
            if coord in ship.coordinates:
                ship.register_hit(coord)
                result = "sunk" if ship.is_sunk else "hit"
                self.shots[coord] = result
                return result, ship.name
        self.shots[coord] = "miss"
        return "miss", None

    def all_sunk(self) -> bool:
        return all(ship.is_sunk for ship in self.ships)

    def render(self, *, show_ships: bool = False) -> str:
        header = "   " + " ".join(f"{col:2}" for col in range(self.size))
        rows = [header]
        for row in range(self.size):
            cells: List[str] = []
            for col in range(self.size):
                coord = (row, col)
                if coord in self.shots:
                    marker = self.shots[coord]
                    if marker == "miss":
                        cells.append("o")
                    elif marker == "hit":
                        cells.append("X")
                    else:  # sunk
                        cells.append("X")
                elif show_ships and coord in self.occupied:
                    cells.append("█")
                else:
                    cells.append("~")
            rows.append(f"{row:2} " + "  ".join(cells))
        return "\n".join(rows)


DEFAULT_FLEET: Tuple[Tuple[str, int], ...] = (
    ("Carrier", 5),
    ("Battleship", 4),
    ("Cruiser", 3),
    ("Submarine", 3),
    ("Destroyer", 2),
)


class BattleshipGame:
    """Full Battleship game against a computer opponent."""

    def __init__(
        self,
        *,
        size: int = 10,
        fleet: Sequence[Tuple[str, int]] = DEFAULT_FLEET,
        rng: Optional[random.Random] = None,
    ) -> None:
        self.rng = rng or random.Random()
        self.size = size
        self.fleet = tuple(fleet)
        self.player_board = Board(size)
        self.opponent_board = Board(size)
        coords = [(r, c) for r in range(size) for c in range(size)]
        self.rng.shuffle(coords)
        self._ai_hunt_even: List[Coordinate] = [
            coord for coord in coords if (coord[0] + coord[1]) % 2 == 0
        ]
        self._ai_hunt_odd: List[Coordinate] = [
            coord for coord in coords if (coord[0] + coord[1]) % 2 == 1
        ]
        self._ai_targets: Deque[Coordinate] = deque()

    def setup_random(self) -> None:
        self.player_board.randomly_place_ships(self.fleet, self.rng)
        self.opponent_board.randomly_place_ships(self.fleet, self.rng)

    def setup_player_ships(
        self,
        placements: Iterable[Tuple[str, int, Coordinate, str]],
    ) -> None:
        for name, length in self.fleet:
            matching = [p for p in placements if p[0] == name]
            if not matching:
                raise ValueError(f"Placement missing for ship '{name}'.")
            ship_name, ship_length, start, orientation = matching[0]
            if ship_length != length:
                raise ValueError(f"Incorrect length for ship '{name}'.")
            self.player_board.place_ship(ship_name, ship_length, start, orientation)
        self.opponent_board.randomly_place_ships(self.fleet, self.rng)

    def player_shoot(self, coord: Coordinate) -> Tuple[str, Optional[str]]:
        result, ship_name = self.opponent_board.receive_shot(coord)
        return result, ship_name

    def ai_shoot(self) -> Tuple[Coordinate, str, Optional[str]]:
        while self._ai_targets:
            target = self._ai_targets.popleft()
            if target in self.player_board.shots:
                continue
            break
        else:
            if self._ai_hunt_even:
                target = self._ai_hunt_even.pop()
            elif self._ai_hunt_odd:
                target = self._ai_hunt_odd.pop()
            else:
                raise RuntimeError("AI has no available shots left.")
        result, ship_name = self.player_board.receive_shot(target)
        if result in {"hit", "sunk"}:
            self._enqueue_targets(target)
        if result == "sunk":
            self._flush_invalid_targets()
        return target, result, ship_name

    def _enqueue_targets(self, coord: Coordinate) -> None:
        row, col = coord
        neighbors = [
            (row - 1, col),
            (row + 1, col),
            (row, col - 1),
            (row, col + 1),
        ]
        for neighbor in neighbors:
            if (
                self.player_board.in_bounds(neighbor)
                and neighbor not in self.player_board.shots
                and neighbor not in self._ai_targets
            ):
                self._ai_targets.append(neighbor)

    def _flush_invalid_targets(self) -> None:
        self._ai_targets = deque(
            coord for coord in self._ai_targets if coord not in self.player_board.shots
        )

    def render(self) -> str:
        player = self.player_board.render(show_ships=True)
        opponent = self.opponent_board.render(show_ships=False)
        divider = "\n" + "=" * (self.size * 3) + "\n"
        return f"Your Fleet:\n{player}{divider}Enemy Waters:\n{opponent}"

    def player_has_lost(self) -> bool:
        return self.player_board.all_sunk()

    def opponent_has_lost(self) -> bool:
        return self.opponent_board.all_sunk()


def _prompt_orientation() -> str:
    orientation = input("Orientation (h for horizontal, v for vertical): ").strip().lower()
    if orientation not in {"h", "v"}:
        raise ValueError("Orientation must be 'h' or 'v'.")
    return orientation


def _prompt_coordinate(prompt: str) -> Coordinate:
    raw = input(prompt).split()
    if len(raw) != 2:
        raise ValueError("Enter row and column, separated by a space.")
    row, col = map(int, raw)
    return row, col


def play() -> None:
    """Interactive Battleship session."""

    game = BattleshipGame()
    print("Welcome to Battleship!")
    manual = input("Would you like to place your ships manually? (y/n): ").strip().lower()
    if manual.startswith("y"):
        print("Enter the starting coordinate for each ship.")
        for name, length in game.fleet:
            placed = False
            while not placed:
                print(f"\nPlacing {name} (length {length})")
                print(game.player_board.render(show_ships=True))
                try:
                    start = _prompt_coordinate("Starting coordinate (row col): ")
                    orientation = _prompt_orientation()
                    game.player_board.place_ship(name, length, start, orientation)
                    placed = True
                except ValueError as exc:
                    print(f"Cannot place ship: {exc}")
        game.opponent_board.randomly_place_ships(game.fleet, game.rng)
    else:
        game.setup_random()

    while True:
        print("\n" + game.render())
        try:
            target = _prompt_coordinate("Fire at (row col): ")
            result, ship_name = game.player_shoot(target)
        except ValueError as exc:
            print(f"Invalid shot: {exc}")
            continue
        if result == "miss":
            print("You splashed into the sea.")
        elif result == "hit":
            print("Direct hit!")
        else:
            print(f"You sank the enemy {ship_name}!")
        if game.opponent_has_lost():
            print("All enemy ships destroyed. You win!")
            break

        coord, ai_result, ship_name = game.ai_shoot()
        row, col = coord
        if ai_result == "miss":
            print(f"Enemy fires at ({row}, {col}) and misses.")
        elif ai_result == "hit":
            print(f"Enemy hits your ship at ({row}, {col})!")
        else:
            print(f"Enemy sinks your {ship_name} at ({row}, {col})!")
        if game.player_has_lost():
            print("Your fleet has been destroyed. You lose.")
            break


__all__ = [
    "BattleshipGame",
    "Board",
    "Ship",
    "DEFAULT_FLEET",
    "play",
]


if __name__ == "__main__":
    play()
