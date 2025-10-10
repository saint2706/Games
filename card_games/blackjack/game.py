"""Blackjack game engine and supporting data structures."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable, Optional

from card_games.common.cards import Card, Deck, format_cards


class Outcome(str, Enum):
    """Possible outcomes of a blackjack hand."""

    PLAYER_BLACKJACK = "player_blackjack"
    PLAYER_WIN = "player_win"
    PUSH = "push"
    PLAYER_LOSS = "player_loss"
    PLAYER_BUST = "player_bust"
    DEALER_BUST = "dealer_bust"


@dataclass
class BlackjackHand:
    """A blackjack hand belonging to either the dealer or a player."""

    cards: list[Card] = field(default_factory=list)
    bet: int = 0
    stood: bool = False
    doubled: bool = False
    split_from: Optional[Card] = None

    def add_card(self, card: Card) -> None:
        self.cards.append(card)

    def totals(self) -> list[int]:
        """Return all possible totals for the hand."""

        total = sum(self._card_value(card) for card in self.cards)
        aces = sum(1 for card in self.cards if card.rank == "A")
        totals = [total]
        # Treat some aces as 11 if it helps the hand without busting.
        for _ in range(aces):
            total -= 10
            totals.append(total)
        valid_totals = sorted({value for value in totals if value <= 21}, reverse=True)
        if valid_totals:
            return valid_totals
        return [min(totals)]

    def best_total(self) -> int:
        """Return the best (highest <= 21) total for the hand."""

        return self.totals()[0]

    def is_blackjack(self) -> bool:
        return (
            self.split_from is None
            and len(self.cards) == 2
            and sorted(self.totals(), reverse=True)[0] == 21
        )

    def is_bust(self) -> bool:
        return self.best_total() > 21

    def is_soft(self) -> bool:
        totals = self.totals()
        return len(totals) > 1 and totals[0] != totals[-1]

    def can_double(self, balance: int) -> bool:
        return not self.doubled and not self.stood and len(self.cards) == 2 and balance >= self.bet

    def can_split(self, balance: int) -> bool:
        return (
            len(self.cards) == 2
            and self.cards[0].rank == self.cards[1].rank
            and balance >= self.bet
        )

    def split(self) -> BlackjackHand:
        if not self.can_split(balance=self.bet):
            raise ValueError("Hand cannot be split")
        card = self.cards.pop()
        new_hand = BlackjackHand(cards=[card], bet=self.bet, split_from=card)
        self.split_from = self.cards[0]
        return new_hand

    def describe(self) -> str:
        return f"{format_cards(self.cards)} ({self.best_total()})"

    @staticmethod
    def _card_value(card: Card) -> int:
        if card.rank in {"J", "Q", "K", "T"}:
            return 10
        if card.rank == "A":
            return 11
        return int(card.rank)


class Shoe:
    """A blackjack shoe comprised of one or more standard decks."""

    def __init__(self, decks: int = 6, *, rng=None) -> None:
        if decks <= 0:
            raise ValueError("Number of decks must be positive")
        self.decks = decks
        self._rng = rng
        self.cards: list[Card] = []
        self._reshuffle()

    def _reshuffle(self) -> None:
        self.cards = []
        for _ in range(self.decks):
            self.cards.extend(Deck().cards)
        if self._rng is None:
            import random

            random.shuffle(self.cards)
        else:
            self._rng.shuffle(self.cards)

    def draw(self) -> Card:
        if len(self.cards) < max(20, self.decks * 52 // 4):
            self._reshuffle()
        if not self.cards:
            raise RuntimeError("The shoe is empty")
        return self.cards.pop()


@dataclass
class Player:
    """A blackjack player with a bankroll and hands."""

    name: str
    bankroll: int
    hands: list[BlackjackHand] = field(default_factory=list)

    def active_hands(self) -> Iterable[BlackjackHand]:
        return (hand for hand in self.hands if not hand.stood and not hand.is_bust())


class BlackjackGame:
    """Manages a game of blackjack for a single player against the dealer."""

    def __init__(
        self,
        *,
        bankroll: int = 500,
        min_bet: int = 10,
        decks: int = 6,
        rng=None,
    ) -> None:
        if bankroll <= 0:
            raise ValueError("bankroll must be positive")
        if min_bet <= 0:
            raise ValueError("min_bet must be positive")
        if min_bet > bankroll:
            raise ValueError("bankroll must cover at least one min bet")
        self.min_bet = min_bet
        self.player = Player("You", bankroll)
        self.dealer = Player("Dealer", bankroll=0)
        self.shoe = Shoe(decks, rng=rng)
        self.history: list[tuple[Outcome, BlackjackHand, BlackjackHand]] = []

    def can_continue(self) -> bool:
        return self.player.bankroll >= self.min_bet

    def start_round(self, bet: int) -> None:
        if bet < self.min_bet:
            raise ValueError(f"Bet must be at least {self.min_bet}")
        if bet > self.player.bankroll:
            raise ValueError("Insufficient bankroll for bet")
        self.player.bankroll -= bet
        player_hand = BlackjackHand(bet=bet)
        dealer_hand = BlackjackHand()
        self.player.hands = [player_hand]
        self.dealer.hands = [dealer_hand]
        for _ in range(2):
            player_hand.add_card(self.shoe.draw())
            dealer_hand.add_card(self.shoe.draw())

    @property
    def dealer_hand(self) -> BlackjackHand:
        return self.dealer.hands[0]

    def player_actions(self, hand: BlackjackHand) -> list[str]:
        actions = ["hit", "stand"]
        if hand.can_double(self.player.bankroll):
            actions.append("double")
        if hand.can_split(self.player.bankroll):
            actions.append("split")
        return actions

    def hit(self, hand: BlackjackHand) -> Card:
        card = self.shoe.draw()
        hand.add_card(card)
        return card

    def stand(self, hand: BlackjackHand) -> None:
        hand.stood = True

    def double_down(self, hand: BlackjackHand) -> Card:
        if not hand.can_double(self.player.bankroll):
            raise ValueError("Cannot double this hand")
        self.player.bankroll -= hand.bet
        hand.bet *= 2
        hand.doubled = True
        card = self.hit(hand)
        hand.stood = True
        return card

    def split(self, hand: BlackjackHand) -> BlackjackHand:
        if not hand.can_split(self.player.bankroll):
            raise ValueError("Cannot split this hand")
        self.player.bankroll -= hand.bet
        new_hand = hand.split()
        index = self.player.hands.index(hand)
        self.player.hands.insert(index + 1, new_hand)
        # Add one card to each split hand.
        for split_hand in (hand, new_hand):
            split_hand.add_card(self.shoe.draw())
        return new_hand

    def dealer_play(self) -> None:
        hand = self.dealer_hand
        hand.stood = False
        while hand.best_total() < 17 or (hand.best_total() == 17 and hand.is_soft()):
            self.hit(hand)
        hand.stood = True

    def resolve(self, hand: BlackjackHand) -> Outcome:
        dealer_total = self.dealer_hand.best_total()
        player_total = hand.best_total()
        if hand.is_blackjack() and not self.dealer_hand.is_blackjack():
            payout = int(hand.bet * 1.5)
            self.player.bankroll += hand.bet + payout
            outcome = Outcome.PLAYER_BLACKJACK
        elif hand.is_bust():
            outcome = Outcome.PLAYER_BUST
        elif self.dealer_hand.is_bust():
            self.player.bankroll += hand.bet * 2
            outcome = Outcome.DEALER_BUST
        elif self.dealer_hand.is_blackjack() and not hand.is_blackjack():
            outcome = Outcome.PLAYER_LOSS
        elif player_total > dealer_total:
            self.player.bankroll += hand.bet * 2
            outcome = Outcome.PLAYER_WIN
        elif player_total == dealer_total:
            self.player.bankroll += hand.bet
            outcome = Outcome.PUSH
        else:
            outcome = Outcome.PLAYER_LOSS
        self.history.append((outcome, hand, self.dealer_hand))
        return outcome

    def settle_round(self) -> list[Outcome]:
        outcomes: list[Outcome] = []
        for hand in self.player.hands:
            outcomes.append(self.resolve(hand))
        return outcomes

    def reset(self) -> None:
        self.player.hands.clear()
        self.dealer.hands.clear()

    def format_hand(self, hand: BlackjackHand) -> str:
        return hand.describe()


__all__ = [
    "BlackjackGame",
    "BlackjackHand",
    "Outcome",
]
