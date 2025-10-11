"""Command-line interface for Gin Rummy."""

from __future__ import annotations

from card_games.common.cards import format_cards, parse_card
from card_games.gin_rummy.game import GinRummyGame, GinRummyPlayer


def display_hand(player: GinRummyPlayer, game: GinRummyGame) -> None:
    """Display player's hand and deadwood."""
    print(f"\n{player.name}'s hand: {format_cards(player.hand)}")
    deadwood = game.calculate_deadwood(player)
    print(f"Deadwood: {deadwood} points")


def play_turn(player: GinRummyPlayer, game: GinRummyGame) -> bool:
    """Play one turn. Returns True if player knocks/gins."""
    print(f"\n{'='*60}")
    print(f"{player.name}'s turn")
    print("=" * 60)

    display_hand(player, game)

    if game.discard_pile:
        top_discard = game.discard_pile[-1]
        print(f"\nTop of discard pile: {top_discard}")

    # Draw phase
    if player.is_ai:
        # AI decides whether to draw from discard
        if game.discard_pile:
            card = game.draw_from_stock()
        else:
            card = game.draw_from_stock()
    else:
        choice = input("Draw from (s)tock or (d)iscard? ").strip().lower()
        if choice == "d" and game.discard_pile:
            card = game.draw_from_discard()
        else:
            card = game.draw_from_stock()

    player.hand.append(card)
    player.hand.sort(key=lambda c: (c.suit.value, c.value))
    print(f"Drew: {card}")

    display_hand(player, game)

    # Check for gin
    if game.has_gin(player):
        print(f"\n🎉 {player.name} has GIN! 🎉")
        return True

    # Check if can knock
    can_knock = game.can_knock(player)
    if can_knock:
        if player.is_ai:
            # AI knocks if deadwood <= 5
            if game.calculate_deadwood(player) <= 5:
                print(f"{player.name} knocks!")
                return True
        else:
            print("\nYou can knock! (deadwood <= 10)")
            knock = input("Do you want to knock? (y/n) ").strip().lower()
            if knock == "y":
                return True

    # Discard phase
    if player.is_ai:
        discard_card = game.suggest_discard(player)
    else:
        print("\nChoose a card to discard:")
        while True:
            try:
                card_code = input("Card: ").strip().upper()
                discard_card = parse_card(card_code)
                if discard_card in player.hand:
                    break
                print("Card not in hand")
            except (ValueError, KeyError):
                print("Invalid card")

    player.hand.remove(discard_card)
    game.discard(discard_card)
    print(f"{player.name} discards {discard_card}")

    return False


def game_loop() -> None:
    """Main game loop for Gin Rummy."""
    print("\nWELCOME TO GIN RUMMY")
    print("=" * 60)

    player_name = input("Enter your name: ").strip() or "Player"
    players = [
        GinRummyPlayer(name=player_name, is_ai=False),
        GinRummyPlayer(name="AI", is_ai=True),
    ]

    game = GinRummyGame(players)
    round_num = 0

    while not game.is_game_over():
        round_num += 1
        print(f"\n{'='*60}")
        print(f"ROUND {round_num}")
        print("=" * 60)

        game.deal_cards()
        game.current_player_idx = 0

        # Play until someone knocks or gins
        while True:
            player = game.players[game.current_player_idx]
            knocked = play_turn(player, game)

            if knocked:
                # Calculate scores
                knocker = player
                opponent = game.players[1 - game.current_player_idx]

                print(f"\n{'='*60}")
                print("ROUND RESULTS")
                print("=" * 60)

                print(f"\n{knocker.name}'s hand: {format_cards(knocker.hand)}")
                print(f"Deadwood: {game.calculate_deadwood(knocker)}")

                print(f"\n{opponent.name}'s hand: {format_cards(opponent.hand)}")
                print(f"Deadwood: {game.calculate_deadwood(opponent)}")

                round_scores = game.calculate_round_score(knocker, opponent)

                for p in game.players:
                    p.score += round_scores[p.name]
                    print(f"\n{p.name}: +{round_scores[p.name]} points (total: {p.score})")

                break

            game.current_player_idx = 1 - game.current_player_idx

        if not game.is_game_over():
            input("\nPress Enter for next round...")

    # Game over
    winner = game.get_winner()
    print("\n" + "=" * 60)
    print("GAME OVER!")
    print("=" * 60)
    print(f"\nWinner: {winner.name} with {winner.score} points!")
