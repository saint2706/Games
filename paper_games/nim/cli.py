"""Command-line interface for playing Nim.

This module provides the terminal-based interactive experience for playing
Nim against the computer. It handles user input, game setup, and announcing
the winner.
"""

from __future__ import annotations

from .nim import NimGame


def play() -> None:
    """Run a terminal-based Nim match against the computer."""

    print("Welcome to Nim! Remove sticks; whoever takes the last wins by default.")
    print("You may optionally switch to misère rules where taking the last stick loses.")

    # Get the heap sizes from the user.
    while True:
        heap_input = input("Enter heap sizes separated by spaces (press Enter for the classic 3 4 5): ").strip()
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

    # Get the game rules from the user.
    misere_choice = input("Play misère Nim (last move loses)? [y/N]: ").strip().lower()
    misere = misere_choice == "y"
    first_choice = input("Do you want to move first? [Y/n]: ").strip().lower()
    human_turn = first_choice != "n"

    game = NimGame(heaps=heaps, misere=misere)
    last_mover: str | None = None
    print("\nStarting heaps: " + ", ".join(str(heap) for heap in game.heaps) + (" (misère rules)" if misere else " (normal rules)"))

    # Main game loop.
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

    # Determine the winner based on the game rules.
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
