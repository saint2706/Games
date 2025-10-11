"""Gin Rummy game engine.

Gin Rummy is a two-player card game where players try to form melds (sets and runs)
and minimize deadwood (unmatched cards). Players can knock when their deadwood is
10 or less, or declare gin with no deadwood for bonus points.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto

from card_games.common.cards import Card, Deck


class MeldType(Enum):
    """Type of meld in Gin Rummy."""

    SET = auto()  # Three or four cards of same rank
    RUN = auto()  # Three or more consecutive cards of same suit


@dataclass
class Meld:
    """Represents a meld (set or run) in Gin Rummy."""

    meld_type: MeldType
    cards: list[Card]


@dataclass
class GinRummyPlayer:
    """Represents a player in Gin Rummy."""

    name: str
    hand: list[Card] = field(default_factory=list)
    score: int = 0
    is_ai: bool = False


class GinRummyGame:
    """Main engine for Gin Rummy."""

    def __init__(self, players: list[GinRummyPlayer], *, rng=None):
        """Initialize a Gin Rummy game."""
        if len(players) != 2:
            raise ValueError("Gin Rummy requires exactly 2 players")
        self.players = players
        self.rng = rng
        self.deck = Deck()
        self.discard_pile: list[Card] = []
        self.current_player_idx = 0

    def deal_cards(self) -> None:
        """Deal 10 cards to each player."""
        self.deck = Deck()
        if self.rng:
            self.deck.shuffle(rng=self.rng)
        else:
            self.deck.shuffle()

        for player in self.players:
            player.hand = []

        for _ in range(10):
            for player in self.players:
                player.hand.append(self.deck.deal(1)[0])

        # Start discard pile
        self.discard_pile = [self.deck.deal(1)[0]]

        for player in self.players:
            player.hand.sort(key=lambda c: (c.suit.value, c.value))

    def find_melds(self, cards: list[Card]) -> list[Meld]:
        """Find all possible melds in a set of cards."""
        melds: list[Meld] = []

        # Find sets (3-4 of same rank)
        from collections import defaultdict

        by_rank = defaultdict(list)
        for card in cards:
            by_rank[card.rank].append(card)

        for rank_cards in by_rank.values():
            if len(rank_cards) >= 3:
                melds.append(Meld(MeldType.SET, rank_cards[:4]))

        # Find runs (3+ consecutive of same suit)
        by_suit = defaultdict(list)
        for card in cards:
            by_suit[card.suit].append(card)

        for suit_cards in by_suit.values():
            suit_cards.sort(key=lambda c: c.value)

            i = 0
            while i < len(suit_cards):
                run = [suit_cards[i]]
                j = i + 1

                while j < len(suit_cards):
                    if suit_cards[j].value == run[-1].value + 1:
                        run.append(suit_cards[j])
                        j += 1
                    else:
                        break

                if len(run) >= 3:
                    melds.append(Meld(MeldType.RUN, run))

                i = j if j > i + 1 else i + 1

        return melds

    def calculate_deadwood(self, player: GinRummyPlayer) -> int:
        """Calculate deadwood points for a player."""
        melds = self.find_melds(player.hand)
        melded_cards = set()

        # Use greedy approach: use melds that minimize deadwood
        for meld in melds:
            if not any(c in melded_cards for c in meld.cards):
                melded_cards.update(meld.cards)

        deadwood = 0
        for card in player.hand:
            if card not in melded_cards:
                if card.rank == "A":
                    deadwood += 1
                elif card.rank in ("J", "Q", "K"):
                    deadwood += 10
                elif card.rank == "T":
                    deadwood += 10
                else:
                    deadwood += int(card.rank)

        return deadwood

    def can_knock(self, player: GinRummyPlayer) -> bool:
        """Check if player can knock (deadwood <= 10)."""
        return self.calculate_deadwood(player) <= 10

    def has_gin(self, player: GinRummyPlayer) -> bool:
        """Check if player has gin (no deadwood)."""
        return self.calculate_deadwood(player) == 0

    def draw_from_stock(self) -> Card:
        """Draw a card from stock."""
        if not self.deck.cards:
            # Reshuffle discard pile except top card
            top = self.discard_pile.pop()
            self.deck.cards = list(reversed(self.discard_pile))
            self.discard_pile = [top]
            if self.rng:
                self.deck.shuffle(rng=self.rng)
            else:
                self.deck.shuffle()
        return self.deck.deal(1)[0]

    def draw_from_discard(self) -> Card:
        """Draw a card from discard pile."""
        if not self.discard_pile:
            raise RuntimeError("Discard pile is empty")
        return self.discard_pile.pop()

    def discard(self, card: Card) -> None:
        """Discard a card."""
        self.discard_pile.append(card)

    def calculate_round_score(self, knocker: GinRummyPlayer, opponent: GinRummyPlayer) -> dict[str, int]:
        """Calculate scores for the round."""
        knocker_deadwood = self.calculate_deadwood(knocker)
        opponent_deadwood = self.calculate_deadwood(opponent)

        scores = {knocker.name: 0, opponent.name: 0}

        if knocker_deadwood == 0:
            # Gin bonus
            scores[knocker.name] = opponent_deadwood + 25
        elif opponent_deadwood <= knocker_deadwood:
            # Undercut bonus
            scores[opponent.name] = (knocker_deadwood - opponent_deadwood) + 25
        else:
            # Normal knock
            scores[knocker.name] = opponent_deadwood - knocker_deadwood

        return scores

    def is_game_over(self, target_score: int = 100) -> bool:
        """Check if game is over."""
        return any(player.score >= target_score for player in self.players)

    def get_winner(self) -> GinRummyPlayer:
        """Get the winner."""
        return max(self.players, key=lambda p: p.score)

    def suggest_discard(self, player: GinRummyPlayer) -> Card:
        """AI logic to suggest a card to discard."""
        # Simple strategy: discard highest deadwood card
        melds = self.find_melds(player.hand)
        melded_cards = {c for meld in melds for c in meld.cards}

        deadwood_cards = [c for c in player.hand if c not in melded_cards]
        if deadwood_cards:
            # Discard highest value card
            return max(deadwood_cards, key=lambda c: c.value)

        # All cards are melded, discard lowest
        return min(player.hand, key=lambda c: c.value)
