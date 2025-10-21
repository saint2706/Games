"""Command-line interface for playing tic-tac-toe.

This module provides the terminal-based interactive experience for playing
tic-tac-toe against an optimal minimax-based computer opponent. It handles
user input, game setup, and the main game loop, providing a complete
end-to-end gameplay experience in the console.

The CLI supports various features, including:
- **Customizable Board Size**: Players can choose to play on 3x3, 4x4, or 5x5 boards.
- **Variable Win Length**: The number of symbols in a row needed to win can be adjusted.
- **Themed Boards**: Players can select from a variety of symbol themes.
- **Game Statistics**: Tracks and displays player stats, such as wins, losses, and draws.
- **Undo Functionality**: Allows players to undo their last move.

Functions:
    play(): Runs the main game loop, handling user interaction and game flow.

Constants:
    STATS_FILE: The default file path for storing game statistics.
"""

from __future__ import annotations

import pathlib
import random
from typing import Dict, List

from games_collection.core.profile_service import get_profile_service

from .stats import GameStats
from .themes import get_theme, list_themes
from .tic_tac_toe import TicTacToeGame

# Default location for storing the user's game statistics.
STATS_FILE = pathlib.Path.home() / ".games" / "tic_tac_toe_stats.json"


def play() -> None:
    """Runs the main game loop for a terminal-based tic-tac-toe game.

    This function orchestrates the entire game flow, from welcoming the player
    to setting up the game, handling turns, and announcing the result. It
    interacts with the user to configure the game settings, such as board
    size, win length, and symbol theme.
    """
    print("Welcome to Tic-Tac-Toe! Coordinates are letter-row + number-column (e.g. B2).")

    # Load player statistics from the file system.
    stats = GameStats.load(STATS_FILE)
    profile_service = get_profile_service()

    # Offer to show statistics if there are any games played.
    if stats.games_played > 0:
        show_stats = input("View your statistics? [y/N]: ").strip().lower()
        if show_stats in {"y", "yes"}:
            print("\n" + stats.summary() + "\n")

    # Get the desired board size from the player.
    board_size_input = input("Choose board size (3, 4, or 5) [3]: ").strip()
    board_size = 3
    if board_size_input in {"3", "4", "5"}:
        board_size = int(board_size_input)
    elif board_size_input:
        print("Invalid board size. Defaulting to 3x3.")

    # Get the desired win length from the player.
    win_length_input = input(f"Choose win length (3 to {board_size}) [{board_size}]: ").strip()
    win_length = board_size
    if win_length_input:
        try:
            win_length = int(win_length_input)
            if win_length < 3 or win_length > board_size:
                print(f"Invalid win length. Defaulting to {board_size}.")
                win_length = board_size
        except ValueError:
            print(f"Invalid win length. Defaulting to {board_size}.")

    # Allow the player to choose a themed board or classic symbols.
    use_theme = input("Use a themed board? [y/N]: ").strip().lower()
    if use_theme in {"y", "yes"}:
        print("\n" + list_themes())
        theme_name = input("\nChoose a theme [classic]: ").strip().lower() or "classic"
        try:
            human_symbol, computer_symbol = get_theme(theme_name)
            print(f"Using theme: {theme_name} ({human_symbol} vs {computer_symbol})")
        except ValueError as e:
            print(f"Error: {e}. Using classic theme.")
            human_symbol, computer_symbol = "X", "O"
    else:
        # Let the player choose their symbol (X or O).
        human_symbol = input("Choose your symbol (X or O) [X]: ").strip().upper() or "X"
        if human_symbol not in {"X", "O"}:
            print("Invalid symbol chosen. Defaulting to X.")
            human_symbol = "X"
        computer_symbol = "O" if human_symbol == "X" else "X"

    # Determine who goes first.
    wants_first = input("Do you want to go first? [Y/n]: ").strip().lower()
    if wants_first in {"n", "no"}:
        starting_symbol = computer_symbol
    elif wants_first in {"y", "yes", ""}:
        starting_symbol = human_symbol
    else:
        # If the input is ambiguous, randomize the starting player.
        starting_symbol = random.choice([human_symbol, computer_symbol])
        print(f"We'll toss a coin… {('You' if starting_symbol == human_symbol else 'Computer')} start(s)!")

    # Initialize the game engine with the chosen settings.
    game = TicTacToeGame(
        human_symbol=human_symbol,
        computer_symbol=computer_symbol,
        starting_symbol=starting_symbol,
        board_size=board_size,
        win_length=win_length,
    )

    session = profile_service.start_session("tic_tac_toe")

    print("\nThe empty board looks like this:")
    print(game.render(show_reference=True))

    # Main game loop continues until there is a winner or a draw.
    while True:
        print("\n" + game.render())
        if game.winner() or game.is_draw():
            break

        if game.current_turn == game.human_symbol:
            prompt = "Choose your move (or 'undo' to undo last move): "
            move_str = input(prompt).strip().lower()

            # Handle the 'undo' command.
            if move_str == "undo":
                if game.can_undo():
                    # Undo the human's last move.
                    if game.undo_last_move():
                        print("Undid your last move.")
                        # If the computer made a move after, undo that too.
                        if game.can_undo():
                            game.undo_last_move()
                            print("Also undid computer's move.")
                        # Revert the turn back to the player.
                        game.swap_turn()
                        continue
                else:
                    print("No moves to undo.")
                    continue

            try:
                position = game.parse_coordinate(move_str)
            except ValueError as exc:
                print(exc)
                continue
            if not game.human_move(position):
                print("That square is already taken. Try again.")
                continue
        else:
            # Computer's turn.
            print("Computer is thinking…")
            comp_row, comp_col = game.computer_move()
            comp_position = comp_row * game.board_size + comp_col
            coords_map = game._generate_coordinates()
            print(f"Computer chooses {coords_map[comp_position]}.")

        if game.winner() or game.is_draw():
            break
        game.swap_turn()

    # Announce the final result of the game.
    print("\n" + game.render())
    winner = game.winner()
    if winner == game.human_symbol:
        print("You win! Congratulations.")
    elif winner == game.computer_symbol:
        print("Computer wins with perfect play.")
    else:
        print("It's a draw – a classic cat's game.")

    # Record the game result in the statistics.
    stats.record_game(winner, game.human_symbol, game.computer_symbol, game.board_size)
    stats.save(STATS_FILE)

    # Show the updated statistics summary.
    print("\n" + stats.summary())

    # Map the game result to a profile service outcome.
    result_map = {
        game.human_symbol: ("win", 120),
        game.computer_symbol: ("loss", 40),
        None: ("draw", 60),
    }
    result_key = winner if winner in result_map else None
    result, experience = result_map[result_key]

    # Prepare metadata for the profile service.
    metadata: Dict[str, object] = {
        "board_size": board_size,
        "win_length": win_length,
        "human_symbol": human_symbol,
        "computer_symbol": computer_symbol,
        "moves_played": sum(1 for cell in game.board if cell.strip()),
    }
    if winner == game.human_symbol and game.board.count(game.computer_symbol) == 0:
        metadata["perfect_game"] = True

    # Complete the profile session and check for unlocked achievements.
    unlocked = session.complete(result=result, experience=experience, metadata=metadata)
    if unlocked:
        manager = profile_service.active_profile.achievement_manager
        print("\nNew achievements unlocked:")
        formatted: List[str] = []
        for achievement_id in unlocked:
            achievement = manager.achievements.get(achievement_id)
            if achievement is not None:
                formatted.append(f"  • {achievement.name} (+{achievement.points} pts)")
            else:
                formatted.append(f"  • {achievement_id}")
        print("\n".join(formatted))
