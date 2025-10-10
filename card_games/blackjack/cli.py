"""Command line interface helpers for the blackjack game."""

from __future__ import annotations

import argparse
from typing import Iterable

from card_games.blackjack.game import BlackjackGame, BlackjackHand
from card_games.common.cards import format_cards


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Play a game of blackjack against the dealer.")
    parser.add_argument("--bankroll", type=int, default=500, help="Starting bankroll (default: 500)")
    parser.add_argument("--min-bet", type=int, default=10, help="Minimum bet size (default: 10)")
    parser.add_argument("--decks", type=int, default=6, help="Number of decks in the shoe (default: 6)")
    parser.add_argument("--seed", type=int, help="Optional random seed for deterministic play")
    return parser


def render_hand(title: str, hand: BlackjackHand, *, hide_hole: bool = False) -> str:
    cards = hand.cards[:]
    if hide_hole and len(cards) >= 2:
        visible = [str(cards[0]), "??"]
        value = BlackjackHand(cards=[cards[0]]).best_total()
        return f"{title}: {' '.join(visible)} ({value}+?)"
    return f"{title}: {format_cards(cards)} ({hand.best_total()})"


def prompt_bet(game: BlackjackGame) -> int:
    while True:
        raw = input(f"Place your bet (min {game.min_bet}, bankroll {game.player.bankroll}): ").strip()
        if not raw:
            print("Bet cannot be empty.")
            continue
        if not raw.isdigit():
            print("Please enter a positive integer amount.")
            continue
        bet = int(raw)
        try:
            game.start_round(bet)
            return bet
        except ValueError as exc:
            print(exc)


def display_table(game: BlackjackGame, *, hide_dealer: bool = True) -> None:
    dealer = render_hand("Dealer", game.dealer_hand, hide_hole=hide_dealer)
    print("\n" + dealer)
    for index, hand in enumerate(game.player.hands, start=1):
        prefix = f"Hand {index}" if len(game.player.hands) > 1 else "Your hand"
        status = []
        if hand.is_blackjack():
            status.append("blackjack!")
        elif hand.is_bust():
            status.append("bust")
        elif hand.stood:
            status.append("stood")
        if hand.doubled:
            status.append("doubled")
        suffix = f" [{', '.join(status)}]" if status else ""
        print(f"{prefix}: {format_cards(hand.cards)} ({hand.best_total()}){suffix}")
    print()


def prompt_action(game: BlackjackGame, hand: BlackjackHand) -> str:
    action_map = {"h": "hit", "s": "stand", "d": "double", "p": "split"}
    while True:
        actions = game.player_actions(hand)
        available = {key: value for key, value in action_map.items() if value in actions}
        options = "/".join(key.upper() for key in available)
        choice = input(f"Choose action [{options}]: ").strip().lower()
        if not choice:
            print("Please choose an action.")
            continue
        key = choice[0]
        if key not in action_map:
            print("Unknown option, try again.")
            continue
        action = action_map[key]
        if action not in actions:
            print("That action is not currently available.")
            continue
        return action


def handle_player_turn(game: BlackjackGame) -> None:
    index = 0
    while index < len(game.player.hands):
        hand = game.player.hands[index]
        while not hand.stood and not hand.is_bust() and not hand.is_blackjack():
            display_table(game)
            action = prompt_action(game, hand)
            if action == "hit":
                card = game.hit(hand)
                print(f"You draw {card}.")
                if hand.is_bust():
                    print("You bust!")
            elif action == "stand":
                game.stand(hand)
                print("You stand.")
            elif action == "double":
                card = game.double_down(hand)
                print(f"Double down! You draw {card} and stand with {hand.best_total()}.")
            elif action == "split":
                game.split(hand)
                print("Hands split into two bets.")
                continue
        display_table(game)
        index += 1


def resolve_round(game: BlackjackGame) -> None:
    print("Dealer reveals their hand...")
    display_table(game, hide_dealer=False)
    if not all(hand.is_bust() for hand in game.player.hands):
        game.dealer_play()
        display_table(game, hide_dealer=False)
    for index, hand in enumerate(game.player.hands, start=1):
        outcome = game.resolve(hand)
        description = outcome.replace("_", " ").title()
        label = f"Hand {index}" if len(game.player.hands) > 1 else "Result"
        print(f"{label}: {description}. Bankroll: {game.player.bankroll}")
    print()


def game_loop(game: BlackjackGame) -> None:
    print("Welcome to Blackjack! Type Ctrl+C to quit at any time.\n")
    try:
        while game.can_continue():
            bet = prompt_bet(game)
            display_table(game)
            if not game.player.hands[0].is_blackjack():
                handle_player_turn(game)
            resolve_round(game)
            game.reset()
            if not game.can_continue():
                break
            cont = input("Play another hand? (Y/n): ").strip().lower()
            if cont and cont.startswith("n"):
                break
        print(f"Thanks for playing! Final bankroll: {game.player.bankroll}")
    except KeyboardInterrupt:
        print("\nGame interrupted. Thanks for playing!")


def main(argv: Iterable[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    rng = None
    if args.seed is not None:
        import random

        rng = random.Random(args.seed)
    game = BlackjackGame(bankroll=args.bankroll, min_bet=args.min_bet, decks=args.decks, rng=rng)
    game_loop(game)


__all__ = ["main", "game_loop", "build_parser"]
