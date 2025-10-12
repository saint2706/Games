"""Command-line interface for the War card game."""

from __future__ import annotations

import time

from card_games.war.game import WarGame


def display_game(game: WarGame) -> None:
    """Display the current game state.

    Args:
        game: The War game instance
    """
    summary = game.get_state_summary()
    print("\n" + "=" * 60)
    print(f"WAR - Round {summary['rounds_played']}")
    print("=" * 60)
    print(f"Player 1: {summary['player1_cards']} cards")
    print(f"Player 2: {summary['player2_cards']} cards")
    if summary["wars_fought"] > 0:
        print(f"Wars fought: {summary['wars_fought']}")
    print("=" * 60)


def display_round_result(result: dict[str, any]) -> None:
    """Display the result of a round.

    Args:
        result: Round result dictionary from play_round()
    """
    if result.get("game_over"):
        print(f"\n🎉 GAME OVER! Player {result.get('final_winner', result.get('winner'))} wins!")
        return

    print("\nCards played:")
    print(f"  Player 1: {result['player1_card']}")
    print(f"  Player 2: {result['player2_card']}")

    if result["round_type"] == "war":
        print("\n⚔️  WAR! Cards are equal!")
        if "reason" in result:
            print(f"   Player {3 - result['winner']} doesn't have enough cards for war!")
        elif "war_card1" in result:
            print("   Each player places 3 cards face down...")
            print(f"   War cards: Player 1: {result['war_card1']}, Player 2: {result['war_card2']}")
            if result.get("nested_war"):
                print("   ⚔️  ANOTHER WAR!")

    print(f"\n✓ Player {result['winner']} wins {result['cards_won']} cards!")


def game_loop(game: WarGame, auto_play: bool = False, delay: float = 0.5) -> None:
    """Main game loop for War.

    Args:
        game: The War game instance
        auto_play: If True, automatically play all rounds
        delay: Delay between rounds in auto-play mode (seconds)
    """
    print("\n" + "=" * 60)
    print("WELCOME TO WAR!")
    print("=" * 60)
    print("\nRules:")
    print("* Each player gets half the deck")
    print("* Both players reveal their top card each round")
    print("* Higher card wins both cards")
    print("* On a tie, WAR! Players place 3 cards down, then 1 up")
    print("* Winner of war takes all cards")
    print("* Game ends when one player has all cards")
    print("=" * 60)

    if not auto_play:
        input("\nPress Enter to start the game...")

    while not game.is_game_over():
        display_game(game)

        if not auto_play:
            user_input = input("\nPress Enter to play a round (or 'q' to quit): ").strip().lower()
            if user_input == "q":
                print("\nThanks for playing!")
                return

        result = game.play_round()
        display_round_result(result)

        if auto_play and not result.get("game_over"):
            time.sleep(delay)

    # Final summary
    summary = game.get_state_summary()
    print("\n" + "=" * 60)
    print("GAME STATISTICS")
    print("=" * 60)
    print(f"Total rounds played: {summary['rounds_played']}")
    print(f"Wars fought: {summary['wars_fought']}")
    print(f"Winner: Player {summary['winner']}")
    print("=" * 60)
