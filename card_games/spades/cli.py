"""Command-line interface for Spades."""

from __future__ import annotations

from card_games.common.cards import Card, format_cards, parse_card
from card_games.spades.game import SpadesGame, SpadesPlayer


def display_hand(player: SpadesPlayer) -> None:
    """Display a player's hand."""
    print(f"\n{player.name}'s hand: {format_cards(player.hand)}")


def get_bid(player: SpadesPlayer, game: SpadesGame) -> int:
    """Get bid from player."""
    if player.is_ai:
        return game.suggest_bid(player)

    display_hand(player)
    while True:
        try:
            bid_str = input("Enter your bid (0-13, 0 = nil): ").strip()
            bid = int(bid_str)
            if 0 <= bid <= 13:
                return bid
            print("Bid must be between 0 and 13")
        except ValueError:
            print("Invalid input")


def get_card_to_play(player: SpadesPlayer, game: SpadesGame) -> Card:
    """Get card from player to play."""

    if player.is_ai:
        return game.select_card_to_play(player)

    valid_plays = game.get_valid_plays(player)
    display_hand(player)
    print("\nCurrent trick:")
    for p, c in game.current_trick:
        print(f"  {p.name}: {c}")
    print(f"\nValid plays: {format_cards(valid_plays)}")

    while True:
        try:
            card_code = input("Enter card to play: ").strip().upper()
            card = parse_card(card_code)
            if card in valid_plays:
                return card
            print("Invalid play")
        except (ValueError, KeyError):
            print("Invalid card")


def game_loop() -> None:
    """Main game loop for Spades."""
    print("\nWELCOME TO SPADES")
    print("=" * 60)

    player_name = input("Enter your name: ").strip() or "Player"
    players = [
        SpadesPlayer(name=player_name, is_ai=False),
        SpadesPlayer(name="AI 1", is_ai=True),
        SpadesPlayer(name="Partner", is_ai=True),
        SpadesPlayer(name="AI 2", is_ai=True),
    ]

    game = SpadesGame(players)
    round_num = 0

    while not game.is_game_over():
        round_num += 1
        print(f"\n{'='*60}")
        print(f"ROUND {round_num}")
        print("=" * 60)

        game.deal_cards()
        game.spades_broken = False

        # Bidding phase
        print("\nBIDDING PHASE")
        for player in game.players:
            bid = get_bid(player, game)
            player.bid = bid
            print(f"{player.name} bids {bid}")

        # Play 13 tricks
        current_player_idx = 0

        for trick_num in range(13):
            print(f"\n--- Trick {trick_num + 1} ---")

            for i in range(4):
                player = game.players[(current_player_idx + i) % 4]
                card = get_card_to_play(player, game)
                game.play_card(player, card)
                print(f"{player.name} plays {card}")

            winner = game.complete_trick()
            print(f"{winner.name} wins the trick!")
            current_player_idx = game.players.index(winner)

        # Scoring
        print("\n" + "=" * 60)
        print("ROUND RESULTS")
        print("=" * 60)

        for player in game.players:
            bid_str = "nil" if player.bid == 0 else str(player.bid)
            print(f"{player.name}: bid {bid_str}, won {player.tricks_won} tricks")

        round_scores = game.calculate_round_score()

        # Update partnership scores
        game.players[0].score += round_scores[0]
        game.players[2].score = game.players[0].score
        game.players[1].score += round_scores[1]
        game.players[3].score = game.players[1].score

        print(f"\nPartnership 1 ({game.players[0].name} & {game.players[2].name}): {game.players[0].score} points, {game.bags[0]} bags")
        print(f"Partnership 2 ({game.players[1].name} & {game.players[3].name}): {game.players[1].score} points, {game.bags[1]} bags")

        if not game.is_game_over():
            input("\nPress Enter to continue...")

    # Game over
    winner_partnership = game.get_winner()
    print("\n" + "=" * 60)
    print("GAME OVER!")
    print("=" * 60)
    if winner_partnership == 0:
        print(f"Winners: {game.players[0].name} & {game.players[2].name}")
    else:
        print(f"Winners: {game.players[1].name} & {game.players[3].name}")
