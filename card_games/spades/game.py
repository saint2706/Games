"""Spades game engine.

Spades is a trick-taking card game where spades are always trump. Players bid on
how many tricks they expect to win, and partnerships try to meet their combined bid.
Special bids include "nil" (zero tricks) for bonus points.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from card_games.common.cards import Card, Deck, Suit


@dataclass
class SpadesPlayer:
    """Represents a player in Spades."""

    name: str
    hand: list[Card] = field(default_factory=list)
    tricks_won: int = 0
    bid: Optional[int] = None
    score: int = 0
    is_ai: bool = False
    partner_index: Optional[int] = None

    def has_suit(self, suit: Suit) -> bool:
        """Check if player has any cards of the given suit."""
        return any(card.suit == suit for card in self.hand)


class SpadesGame:
    """Main engine for the Spades card game."""

    def __init__(self, players: list[SpadesPlayer], *, rng=None):
        """Initialize a Spades game."""
        if len(players) != 4:
            raise ValueError("Spades requires exactly 4 players")
        self.players = players
        self.players[0].partner_index = 2
        self.players[2].partner_index = 0
        self.players[1].partner_index = 3
        self.players[3].partner_index = 1
        self.rng = rng
        self.deck = Deck()
        self.spades_broken = False
        self.current_trick: list[tuple[SpadesPlayer, Card]] = []
        self.lead_suit: Optional[Suit] = None
        self.bags = [0, 0]

    def deal_cards(self) -> None:
        """Deal all 52 cards evenly to 4 players."""
        self.deck = Deck()
        if self.rng:
            self.deck.shuffle(rng=self.rng)
        else:
            self.deck.shuffle()
        for player in self.players:
            player.hand = []
            player.tricks_won = 0
            player.bid = None
        for _ in range(13):
            for player in self.players:
                player.hand.append(self.deck.deal(1)[0])
        for player in self.players:
            player.hand.sort(key=lambda c: (c.suit.value, c.value))

    def is_valid_play(self, player: SpadesPlayer, card: Card) -> bool:
        """Check if a card play is valid."""
        if card not in player.hand:
            return False
        if not self.current_trick:
            if card.suit == Suit.SPADES:
                return self.spades_broken or all(c.suit == Suit.SPADES for c in player.hand)
            return True
        if self.lead_suit and player.has_suit(self.lead_suit):
            return card.suit == self.lead_suit
        return True

    def play_card(self, player: SpadesPlayer, card: Card) -> None:
        """Play a card to the current trick."""
        if not self.is_valid_play(player, card):
            raise ValueError(f"Invalid play")
        player.hand.remove(card)
        self.current_trick.append((player, card))
        if len(self.current_trick) == 1:
            self.lead_suit = card.suit
        if card.suit == Suit.SPADES:
            self.spades_broken = True

    def complete_trick(self) -> SpadesPlayer:
        """Complete the current trick and determine winner."""
        if len(self.current_trick) != 4:
            raise RuntimeError("Trick is not complete")
        spades_played = [(p, c) for p, c in self.current_trick if c.suit == Suit.SPADES]
        if spades_played:
            winner, _ = max(spades_played, key=lambda x: x[1].value)
        else:
            lead_cards = [(p, c) for p, c in self.current_trick if c.suit == self.lead_suit]
            winner, _ = max(lead_cards, key=lambda x: x[1].value)
        winner.tricks_won += 1
        self.current_trick = []
        self.lead_suit = None
        return winner

    def calculate_round_score(self) -> dict[int, int]:
        """Calculate scores for the round."""
        scores = {0: 0, 1: 0}
        for partnership_idx in [0, 1]:
            if partnership_idx == 0:
                team = [self.players[0], self.players[2]]
            else:
                team = [self.players[1], self.players[3]]
            nil_bonuses = 0
            non_nil_bid = 0
            non_nil_tricks = 0
            for player in team:
                if player.bid == 0:
                    if player.tricks_won == 0:
                        nil_bonuses += 100
                    else:
                        nil_bonuses -= 100
                else:
                    non_nil_bid += player.bid or 0
                    non_nil_tricks += player.tricks_won
            total_bid = non_nil_bid
            total_tricks = non_nil_tricks
            if total_tricks >= total_bid:
                scores[partnership_idx] = total_bid * 10
                overtricks = total_tricks - total_bid
                scores[partnership_idx] += overtricks
                self.bags[partnership_idx] += overtricks
                if self.bags[partnership_idx] >= 10:
                    scores[partnership_idx] -= 100
                    self.bags[partnership_idx] -= 10
            else:
                scores[partnership_idx] = -total_bid * 10
            scores[partnership_idx] += nil_bonuses
        return scores

    def get_valid_plays(self, player: SpadesPlayer) -> list[Card]:
        """Get all valid cards a player can play."""
        return [card for card in player.hand if self.is_valid_play(player, card)]

    def suggest_bid(self, player: SpadesPlayer) -> int:
        """AI logic to suggest a bid."""
        bid = 0
        for suit in [Suit.SPADES, Suit.HEARTS, Suit.DIAMONDS, Suit.CLUBS]:
            suit_cards = [c for c in player.hand if c.suit == suit]
            if not suit_cards:
                continue
            high_cards = sum(1 for c in suit_cards if c.rank in ("A", "K", "Q"))
            if suit == Suit.SPADES:
                if len(suit_cards) >= 4:
                    bid += len(suit_cards) - 2
                elif len(suit_cards) >= 2:
                    bid += 1
                bid += high_cards
            else:
                if len(suit_cards) >= 4:
                    bid += 1
                bid += high_cards
        return min(bid, 13)

    def select_card_to_play(self, player: SpadesPlayer) -> Card:
        """AI logic to select a card to play."""
        valid_cards = self.get_valid_plays(player)
        if len(valid_cards) == 1:
            return valid_cards[0]
        if not self.current_trick:
            non_spades = [c for c in valid_cards if c.suit != Suit.SPADES]
            if non_spades:
                return min(non_spades, key=lambda c: c.value)
            return min(valid_cards, key=lambda c: c.value)
        lead_suit_cards = [c for c in valid_cards if c.suit == self.lead_suit]
        if lead_suit_cards:
            return max(lead_suit_cards, key=lambda c: c.value)
        non_spades = [c for c in valid_cards if c.suit != Suit.SPADES]
        if non_spades:
            return max(non_spades, key=lambda c: c.value)
        return min(valid_cards, key=lambda c: c.value)
