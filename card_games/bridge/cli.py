"""Command-line interface for Bridge."""

from __future__ import annotations

from card_games.bridge.game import BidSuit, BridgeGame, BridgePlayer
from card_games.common.cards import format_cards, parse_card


def display_hand(player: BridgePlayer) -> None:
    """Display player's hand."""
    print(f"\n{player.name} ({player.position}): {format_cards(player.hand)}")


def game_loop() -> None:
    """Main game loop for Bridge (simplified demo)."""
    print("\nWELCOME TO BRIDGE")
    print("=" * 60)
    print("Simplified Contract Bridge implementation")
    print("=" * 60)

    player_name = input("\nEnter your name (you are South): ").strip() or "Player"

    players = [
        BridgePlayer(name="North AI", is_ai=True),
        BridgePlayer(name="East AI", is_ai=True),
        BridgePlayer(name="South " + player_name, is_ai=False),
        BridgePlayer(name="West AI", is_ai=True),
    ]

    game = BridgeGame(players)

    print("\n" + "=" * 60)
    print("DEALING CARDS")
    print("=" * 60)

    game.deal_cards()

    for player in players:
        if not player.is_ai:
            display_hand(player)
            hcp = game.evaluate_hand(player)
            print(f"High Card Points: {hcp}")

    print("\n" + "=" * 60)
    print("BIDDING PHASE")
    print("=" * 60)
    print("(Automated bidding)")

    contract = game.conduct_bidding()

    if not contract:
        print("\nAll players passed. No contract.")
        return

    print(f"\nContract: {contract.bid.level}{contract.bid.suit.name} by {contract.declarer.name}")

    # Set trump suit
    if contract.bid.suit != BidSuit.NO_TRUMP:
        from card_games.common.cards import Suit

        suit_map = {
            BidSuit.CLUBS: Suit.CLUBS,
            BidSuit.DIAMONDS: Suit.DIAMONDS,
            BidSuit.HEARTS: Suit.HEARTS,
            BidSuit.SPADES: Suit.SPADES,
        }
        game.trump_suit = suit_map[contract.bid.suit]

    print("\n" + "=" * 60)
    print("PLAYING PHASE")
    print("=" * 60)

    # Play 13 tricks
    current_player_idx = 0

    for trick_num in range(13):
        print(f"\n--- Trick {trick_num + 1} ---")

        for i in range(4):
            player = game.players[(current_player_idx + i) % 4]

            if player.is_ai:
                card = game.select_card_to_play(player)
            else:
                display_hand(player)
                print("\nCurrent trick:")
                for p, c in game.current_trick:
                    print(f"  {p.position}: {c}")

                valid = game.get_valid_plays(player)
                print(f"\nValid cards: {format_cards(valid)}")

                while True:
                    try:
                        card_code = input("Enter card to play: ").strip().upper()
                        card = parse_card(card_code)
                        if card in valid:
                            break
                        print("Invalid play")
                    except (ValueError, KeyError):
                        print("Invalid card")

            game.play_card(player, card)
            print(f"{player.position} plays {card}")

        winner = game.complete_trick()
        print(f"{winner.position} wins the trick")
        current_player_idx = game.players.index(winner)

    # Scoring
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)

    declarer = contract.declarer
    partner = game.players[declarer.partner_index]
    declarer_tricks = declarer.tricks_won + partner.tricks_won

    print(f"\nDeclarer partnership ({declarer.position}-{partner.position}): {declarer_tricks} tricks")
    print(f"Defender partnership: {13 - declarer_tricks} tricks")

    required = 6 + contract.bid.level
    print(f"\nContract required: {required} tricks")

    scores = game.calculate_score()

    if declarer_tricks >= required:
        print(f"✓ Contract MADE by {declarer.position}")
        print(f"Declarer score: {scores['declarer']} points")
    else:
        print("✗ Contract FAILED")
        print(f"Defender score: {scores['defenders']} points")
