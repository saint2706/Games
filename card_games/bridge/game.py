"""Bridge game engine.

Contract Bridge is a trick-taking game played by four players in two partnerships.
The game consists of bidding to determine the contract, and then playing to fulfill it.
This is a simplified implementation focusing on basic bidding and trick-taking.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from card_games.common.cards import Card, Deck, Suit


class BidSuit(Enum):
    """Bid suits in Bridge (ordered by rank)."""

    CLUBS = 1
    DIAMONDS = 2
    HEARTS = 3
    SPADES = 4
    NO_TRUMP = 5


@dataclass
class Bid:
    """Represents a bid in Bridge."""

    level: int  # 1-7
    suit: BidSuit

    def score(self) -> int:
        """Get bid score for comparison."""
        return self.level * 10 + self.suit.value


@dataclass
class Contract:
    """Represents the final contract."""

    bid: Bid
    declarer: BridgePlayer
    doubled: bool = False
    redoubled: bool = False


@dataclass
class BridgePlayer:
    """Represents a player in Bridge."""

    name: str
    hand: list[Card] = field(default_factory=list)
    tricks_won: int = 0
    is_ai: bool = False
    partner_index: Optional[int] = None
    position: str = ""  # N, S, E, W


class BridgeGame:
    """Main engine for Contract Bridge."""

    def __init__(self, players: list[BridgePlayer], *, rng=None):
        """Initialize a Bridge game."""
        if len(players) != 4:
            raise ValueError("Bridge requires exactly 4 players")

        self.players = players
        # Set up partnerships and positions
        positions = ["N", "S", "E", "W"]
        for i, player in enumerate(self.players):
            player.position = positions[i]
            player.partner_index = (i + 2) % 4  # N-S, E-W partnerships

        self.rng = rng
        self.deck = Deck()
        self.contract: Optional[Contract] = None
        self.current_trick: list[tuple[BridgePlayer, Card]] = []
        self.lead_suit: Optional[Suit] = None
        self.trump_suit: Optional[Suit] = None

    def deal_cards(self) -> None:
        """Deal 13 cards to each player."""
        self.deck = Deck()
        if self.rng:
            self.deck.shuffle(rng=self.rng)
        else:
            self.deck.shuffle()

        for player in self.players:
            player.hand = []
            player.tricks_won = 0

        for _ in range(13):
            for player in self.players:
                player.hand.append(self.deck.deal(1)[0])

        for player in self.players:
            player.hand.sort(key=lambda c: (c.suit.value, c.value))

    def evaluate_hand(self, player: BridgePlayer) -> int:
        """Calculate high card points (HCP) for a hand."""
        hcp = 0
        for card in player.hand:
            if card.rank == "A":
                hcp += 4
            elif card.rank == "K":
                hcp += 3
            elif card.rank == "Q":
                hcp += 2
            elif card.rank == "J":
                hcp += 1
        return hcp

    def suggest_bid(self, player: BridgePlayer, current_bid: Optional[Bid]) -> Optional[Bid]:
        """AI logic to suggest a bid (simplified)."""
        hcp = self.evaluate_hand(player)

        # Pass if less than 12 HCP
        if hcp < 12:
            return None

        # Find longest suit
        from collections import Counter

        suit_counts = Counter(card.suit for card in player.hand)
        longest_suit, count = suit_counts.most_common(1)[0]

        # Determine level
        if hcp >= 20:
            level = 3
        elif hcp >= 16:
            level = 2
        else:
            level = 1

        # Map Suit to BidSuit
        suit_map = {
            Suit.CLUBS: BidSuit.CLUBS,
            Suit.DIAMONDS: BidSuit.DIAMONDS,
            Suit.HEARTS: BidSuit.HEARTS,
            Suit.SPADES: BidSuit.SPADES,
        }

        bid_suit = suit_map[longest_suit]
        bid = Bid(level, bid_suit)

        # Must be higher than current bid
        if current_bid and bid.score() <= current_bid.score():
            # Try to raise
            if current_bid.level < 7:
                bid = Bid(current_bid.level + 1, bid_suit)
            else:
                return None  # Pass

        return bid

    def conduct_bidding(self) -> Optional[Contract]:
        """Conduct simplified bidding phase."""
        # Start with dealer (player 0)
        bids: list[Optional[Bid]] = []
        passes = 0
        last_bidder = None
        last_bid = None

        player_idx = 0

        # Simplified: 4 consecutive passes or 3 passes after a bid
        while passes < 4:
            player = self.players[player_idx]
            bid = self.suggest_bid(player, last_bid)

            if bid:
                bids.append(bid)
                last_bid = bid
                last_bidder = player
                passes = 0
            else:
                bids.append(None)
                passes += 1

            player_idx = (player_idx + 1) % 4

            # Stop after 3 passes following a bid
            if last_bid and passes >= 3:
                break

        if last_bid and last_bidder:
            return Contract(last_bid, last_bidder)

        return None  # All passed

    def is_valid_play(self, player: BridgePlayer, card: Card) -> bool:
        """Check if a card play is valid."""
        if card not in player.hand:
            return False

        if not self.current_trick:
            return True

        # Must follow suit if possible
        if self.lead_suit:
            has_suit = any(c.suit == self.lead_suit for c in player.hand)
            if has_suit:
                return card.suit == self.lead_suit

        return True

    def play_card(self, player: BridgePlayer, card: Card) -> None:
        """Play a card to the current trick."""
        if not self.is_valid_play(player, card):
            raise ValueError("Invalid play")

        player.hand.remove(card)
        self.current_trick.append((player, card))

        if len(self.current_trick) == 1:
            self.lead_suit = card.suit

    def complete_trick(self) -> BridgePlayer:
        """Complete the trick and determine winner."""
        if len(self.current_trick) != 4:
            raise RuntimeError("Trick is not complete")

        # Trump cards win
        if self.trump_suit:
            trump_cards = [(p, c) for p, c in self.current_trick if c.suit == self.trump_suit]
            if trump_cards:
                winner, _ = max(trump_cards, key=lambda x: x[1].value)
                winner.tricks_won += 1
                self.current_trick = []
                self.lead_suit = None
                return winner

        # Highest card of lead suit wins
        lead_cards = [(p, c) for p, c in self.current_trick if c.suit == self.lead_suit]
        winner, _ = max(lead_cards, key=lambda x: x[1].value)

        winner.tricks_won += 1
        self.current_trick = []
        self.lead_suit = None

        return winner

    def calculate_score(self) -> dict[str, int]:
        """Calculate score for the contract (simplified)."""
        if not self.contract:
            return {}

        declarer = self.contract.declarer
        partner = self.players[declarer.partner_index]
        tricks_won = declarer.tricks_won + partner.tricks_won

        level = self.contract.bid.level
        required_tricks = 6 + level

        scores = {}

        if tricks_won >= required_tricks:
            # Made contract
            base_score = level * 20
            if self.contract.bid.suit in (BidSuit.HEARTS, BidSuit.SPADES):
                base_score = level * 30
            elif self.contract.bid.suit == BidSuit.NO_TRUMP:
                base_score = level * 30 + 10

            overtricks = tricks_won - required_tricks
            score = base_score + (overtricks * 20)

            scores["declarer"] = score
            scores["defenders"] = 0
        else:
            # Failed contract
            undertricks = required_tricks - tricks_won
            scores["declarer"] = 0
            scores["defenders"] = undertricks * 50

        return scores

    def get_valid_plays(self, player: BridgePlayer) -> list[Card]:
        """Get all valid cards a player can play."""
        return [card for card in player.hand if self.is_valid_play(player, card)]

    def select_card_to_play(self, player: BridgePlayer) -> Card:
        """AI logic to select a card (simplified)."""
        valid_cards = self.get_valid_plays(player)

        if len(valid_cards) == 1:
            return valid_cards[0]

        # Simple strategy: play high if leading, try to win if following
        if not self.current_trick:
            # Lead with highest card
            return max(valid_cards, key=lambda c: c.value)

        # Try to win the trick
        return max(valid_cards, key=lambda c: c.value)
