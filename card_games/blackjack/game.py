"""Blackjack game engine and supporting data structures.

This module contains the core logic for a game of Blackjack, including the
rules for hands, player actions, and game progression. It is designed to be
reusable and adaptable for different interfaces, such as a command-line or
graphical user interface.

The main components are:
- ``Outcome``: An ``Enum`` representing the possible results of a hand.
- ``BlackjackHand``: A class that manages the cards in a hand, calculates totals,
  and checks for conditions like blackjack or bust.
- ``Shoe``: Represents a collection of multiple decks of cards, from which
  cards are drawn during the game.
- ``Player``: A dataclass for players, managing their bankroll and hands.
- ``BlackjackGame``: The main game engine that orchestrates the game flow,
  manages player and dealer actions, and resolves outcomes.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable, Optional

from card_games.common.cards import Card, Deck, format_cards


class Outcome(str, Enum):
    """Enumeration of the possible outcomes for a single blackjack hand.

    Each member represents a specific result from the player's perspective.
    - ``PLAYER_BLACKJACK``: Player wins with a natural 21.
    - ``PLAYER_WIN``: Player's hand beats the dealer's.
    - ``PUSH``: The hand is a tie.
    - ``PLAYER_LOSS``: Player's hand loses to the dealer's.
    - ``PLAYER_BUST``: Player's hand exceeds 21.
    - ``DEALER_BUST``: Dealer's hand exceeds 21, and player wins.
    """

    PLAYER_BLACKJACK = "player_blackjack"
    PLAYER_WIN = "player_win"
    PUSH = "push"
    PLAYER_LOSS = "player_loss"
    PLAYER_BUST = "player_bust"
    DEALER_BUST = "dealer_bust"


@dataclass
class BlackjackHand:
    """A blackjack hand belonging to either the dealer or a player.

    This class manages the cards in a hand, calculates possible totals (especially
    with Aces), and tracks the hand's state, such as whether it has been stood,
    doubled, or split.

    Attributes:
        cards (list[Card]): The cards currently in the hand.
        bet (int): The wager placed on this hand.
        stood (bool): True if the player has chosen to "stand" on this hand.
        doubled (bool): True if the hand has been "doubled down".
        split_from (Optional[Card]): The card from which this hand was split, if any.
    """

    cards: list[Card] = field(default_factory=list)
    bet: int = 0
    stood: bool = False
    doubled: bool = False
    split_from: Optional[Card] = None

    def add_card(self, card: Card) -> None:
        """Add a card to the hand."""
        self.cards.append(card)

    def totals(self) -> list[int]:
        """Return all possible totals for the hand, accounting for Aces.

        Aces can be valued at 1 or 11. This method calculates all valid totals,
        with and without busting, and returns them in descending order.

        For example, a hand with an Ace and a 5 can be 6 or 16.
        A hand with two Aces and a 5 can be 7 or 17.

        Returns:
            list[int]: A sorted list of possible hand totals, with the best
                       (highest without busting) first. If all totals are over
                       21, it returns the lowest bust total.
        """
        num_aces = sum(1 for card in self.cards if card.rank == "A")
        base_total = sum(self._card_value(card) for card in self.cards)

        totals = {base_total}
        # Each Ace can be 1 or 11. The base total assumes 11.
        # Subtract 10 for each Ace to get the alternative values.
        for i in range(num_aces):
            base_total -= 10
            totals.add(base_total)

        valid_totals = sorted([t for t in totals if t <= 21], reverse=True)
        if valid_totals:
            return valid_totals

        # If all totals are a bust, return the smallest bust total.
        return [min(totals)]

    def best_total(self) -> int:
        """Return the best (highest non-busting) total for the hand."""
        return self.totals()[0]

    def is_blackjack(self) -> bool:
        """Check if the hand is a natural blackjack (2 cards totaling 21)."""
        return (
            self.split_from is None and len(self.cards) == 2 and self.best_total() == 21
        )

    def is_bust(self) -> bool:
        """Check if the hand's best total is over 21."""
        return self.best_total() > 21

    def is_soft(self) -> bool:
        """Check if the hand is "soft" (an Ace is counted as 11).

        A soft hand has multiple possible totals, meaning it contains an Ace
        that can be either 1 or 11 without busting.
        """
        totals = self.totals()
        return len(totals) > 1 and totals[0] <= 21

    def can_double(self, balance: int) -> bool:
        """Check if the hand can be doubled down.

        A player can double down on their initial two cards if they have
        sufficient balance to match their original bet.
        """
        return (
            not self.doubled
            and not self.stood
            and len(self.cards) == 2
            and balance >= self.bet
        )

    def can_split(self, balance: int) -> bool:
        """Check if the hand can be split.

        A player can split a hand if it consists of two cards of the same rank
        and they have enough balance to place an equal bet on the new hand.
        """
        return (
            len(self.cards) == 2
            and self.cards[0].rank == self.cards[1].rank
            and balance >= self.bet
        )

    def split(self) -> BlackjackHand:
        """Split the hand into two, returning the new hand.

        This method modifies the current hand by removing one card and creates
        a new hand with that card. Both hands are marked as having been split.

        Returns:
            BlackjackHand: The new hand created from the split.

        Raises:
            ValueError: If the hand is not splittable.
        """
        if not self.can_split(balance=self.bet):
            raise ValueError("Hand cannot be split")

        card = self.cards.pop()
        new_hand = BlackjackHand(cards=[card], bet=self.bet, split_from=card)
        self.split_from = self.cards[0]
        return new_hand

    def describe(self) -> str:
        """Return a string description of the hand, including cards and total."""
        return f"{format_cards(self.cards)} ({self.best_total()})"

    @staticmethod
    def _card_value(card: Card) -> int:
        """Calculate the blackjack value of a single card.

        Face cards (J, Q, K, T) are 10. Aces are 11. Other cards are their
        face value.
        """
        if card.rank in {"J", "Q", "K", "T"}:
            return 10
        if card.rank == "A":
            return 11
        return int(card.rank)


class Shoe:
    """A blackjack shoe comprised of one or more standard decks.

    A shoe is a container for multiple decks of cards, used in casino games to
    reduce the frequency of shuffling. This implementation automatically
    reshuffles when the number of remaining cards falls below a threshold.

    Attributes:
        decks (int): The number of decks in the shoe.
        cards (list[Card]): The list of cards currently in the shoe.
    """

    def __init__(self, decks: int = 6, *, rng=None) -> None:
        if decks <= 0:
            raise ValueError("Number of decks must be positive")
        self.decks = decks
        self._rng = rng
        self.cards: list[Card] = []
        self._reshuffle()

    def _reshuffle(self) -> None:
        """Reshuffle the shoe with a full set of cards."""
        self.cards = []
        for _ in range(self.decks):
            self.cards.extend(Deck().cards)

        # Use the provided RNG for shuffling, or the default `random` module.
        if self._rng is None:
            import random

            random.shuffle(self.cards)
        else:
            self._rng.shuffle(self.cards)

    def draw(self) -> Card:
        """Draw a single card from the shoe.

        If the number of cards is below the reshuffle threshold (typically 25%
        of the total), the shoe is reshuffled before drawing.
        """
        # Reshuffle if the shoe is getting low
        if len(self.cards) < max(20, self.decks * 52 // 4):
            self._reshuffle()

        if not self.cards:
            raise RuntimeError("The shoe is empty")

        return self.cards.pop()


@dataclass
class Player:
    """A blackjack player with a bankroll and a set of hands.

    Attributes:
        name (str): The player's name.
        bankroll (int): The player's current money balance.
        hands (list[BlackjackHand]): The list of hands the player is currently playing.
    """

    name: str
    bankroll: int
    hands: list[BlackjackHand] = field(default_factory=list)

    def active_hands(self) -> Iterable[BlackjackHand]:
        """Return an iterator over the player's hands that are still in play."""
        return (hand for hand in self.hands if not hand.stood and not hand.is_bust())


class BlackjackGame:
    """Manages a game of blackjack for a single player against the dealer.

    This class orchestrates the entire game flow, from starting a round and
    placing bets to handling player actions (hit, stand, double, split) and
    resolving the outcomes.

    Attributes:
        min_bet (int): The minimum allowed bet.
        player (Player): The human player.
        dealer (Player): The dealer.
        shoe (Shoe): The shoe of cards for the game.
        history (list): A log of outcomes from previous hands.
    """

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
        self.dealer = Player("Dealer", bankroll=0)  # Dealer has infinite bankroll
        self.shoe = Shoe(decks, rng=rng)
        self.history: list[tuple[Outcome, BlackjackHand, BlackjackHand]] = []

    def can_continue(self) -> bool:
        """Check if the player has enough money to continue playing."""
        return self.player.bankroll >= self.min_bet

    def start_round(self, bet: int) -> None:
        """Start a new round of blackjack.

        This involves taking the player's bet, dealing two cards to both the
        player and the dealer, and setting up their initial hands.

        Args:
            bet (int): The amount the player wishes to bet.
        """
        if bet < self.min_bet:
            raise ValueError(f"Bet must be at least {self.min_bet}")
        if bet > self.player.bankroll:
            raise ValueError("Insufficient bankroll for bet")

        self.player.bankroll -= bet
        player_hand = BlackjackHand(bet=bet)
        dealer_hand = BlackjackHand()

        self.player.hands = [player_hand]
        self.dealer.hands = [dealer_hand]

        # Deal two cards to both player and dealer
        for _ in range(2):
            player_hand.add_card(self.shoe.draw())
            dealer_hand.add_card(self.shoe.draw())

    @property
    def dealer_hand(self) -> BlackjackHand:
        """A convenience property to access the dealer's single hand."""
        return self.dealer.hands[0]

    def player_actions(self, hand: BlackjackHand) -> list[str]:
        """Return a list of valid actions for the player's current hand."""
        actions = ["hit", "stand"]
        if hand.can_double(self.player.bankroll):
            actions.append("double")
        if hand.can_split(self.player.bankroll):
            actions.append("split")
        return actions

    def hit(self, hand: BlackjackHand) -> Card:
        """Add a card to the specified hand (player's or dealer's)."""
        card = self.shoe.draw()
        hand.add_card(card)
        return card

    def stand(self, hand: BlackjackHand) -> None:
        """Mark the player's hand as "stood" (no more cards)."""
        hand.stood = True

    def double_down(self, hand: BlackjackHand) -> Card:
        """Double the player's bet, deal one more card, and stand."""
        if not hand.can_double(self.player.bankroll):
            raise ValueError("Cannot double this hand")

        self.player.bankroll -= hand.bet
        hand.bet *= 2
        hand.doubled = True

        card = self.hit(hand)
        hand.stood = True
        return card

    def split(self, hand: BlackjackHand) -> BlackjackHand:
        """Split the player's hand into two separate hands."""
        if not hand.can_split(self.player.bankroll):
            raise ValueError("Cannot split this hand")

        self.player.bankroll -= hand.bet
        new_hand = hand.split()

        # Insert the new hand immediately after the original
        index = self.player.hands.index(hand)
        self.player.hands.insert(index + 1, new_hand)

        # Add one card to each of the newly split hands
        for split_hand in (hand, new_hand):
            split_hand.add_card(self.shoe.draw())

        return new_hand

    def dealer_play(self) -> None:
        """Perform the dealer's turn according to standard casino rules.

        The dealer must hit on 16 or less and on a soft 17. They stand on a
        hard 17 or greater.
        """
        hand = self.dealer_hand
        hand.stood = False
        while hand.best_total() < 17 or (hand.best_total() == 17 and hand.is_soft()):
            self.hit(hand)
        hand.stood = True

    def resolve(self, hand: BlackjackHand) -> Outcome:
        """Resolve a single player hand against the dealer's hand.

        This method determines the outcome (win, loss, push) and adjusts the
        player's bankroll accordingly.

        Args:
            hand (BlackjackHand): The player's hand to be resolved.

        Returns:
            Outcome: The outcome of the hand.
        """
        dealer_total = self.dealer_hand.best_total()
        player_total = hand.best_total()

        if hand.is_blackjack() and not self.dealer_hand.is_blackjack():
            # Blackjack pays 3:2
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
            # Push: return the bet to the player
            self.player.bankroll += hand.bet
            outcome = Outcome.PUSH
        else:  # player_total < dealer_total
            outcome = Outcome.PLAYER_LOSS

        self.history.append((outcome, hand, self.dealer_hand))
        return outcome

    def settle_round(self) -> list[Outcome]:
        """Settle all of the player's hands at the end of a round."""
        outcomes: list[Outcome] = []
        for hand in self.player.hands:
            outcomes.append(self.resolve(hand))
        return outcomes

    def reset(self) -> None:
        """Clear the player's and dealer's hands for the next round."""
        self.player.hands.clear()
        self.dealer.hands.clear()

    def format_hand(self, hand: BlackjackHand) -> str:
        """Return a formatted string representation of a hand."""
        return hand.describe()


__all__ = [
    "BlackjackGame",
    "BlackjackHand",
    "Outcome",
]
