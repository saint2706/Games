"""Command-line interface for playing Battleship.

This module provides the terminal-based interactive experience for playing
Battleship against an AI opponent that uses a hunting strategy.
"""

from __future__ import annotations

from .battleship import BattleshipGame, Coordinate


def _prompt_orientation() -> str:
    """Prompts the user for a ship orientation."""
    orientation = input("Orientation (h for horizontal, v for vertical): ").strip().lower()
    if orientation not in {"h", "v"}:
        raise ValueError("Orientation must be 'h' or 'v'.")
    return orientation


def _prompt_coordinate(prompt: str) -> Coordinate:
    """Prompts the user for a coordinate."""
    raw = input(prompt).split()
    if len(raw) != 2:
        raise ValueError("Enter row and column, separated by a space.")
    row, col = map(int, raw)
    return row, col


def play() -> None:
    """Interactive Battleship session."""

    game = BattleshipGame()
    print("Welcome to Battleship!")
    # Ask the user if they want to place their ships manually.
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

    # Main game loop.
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
