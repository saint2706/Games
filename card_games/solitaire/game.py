"""Solitaire (Klondike) game engine.

This module implements the classic Klondike solitaire game. The game involves:
- Building four foundation piles (one per suit) from Ace to King
- Seven tableau piles where cards can be moved and stacked in descending order with alternating colors
- A stock pile from which cards are drawn
- A waste pile where drawn cards are placed

The goal is to move all cards to the foundation piles.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional

from card_games.common.cards import Card, Deck, Suit


class PileType(Enum):
    """Types of piles in Klondike solitaire."""

    FOUNDATION = auto()  # Four piles, built up by suit from Ace to King
    TABLEAU = auto()  # Seven piles, built down in alternating colors
    STOCK = auto()  # Draw pile
    WASTE = auto()  # Discard pile


@dataclass
class Pile:
    """Represents a pile of cards in solitaire.

    Attributes:
        pile_type: The type of pile (foundation, tableau, etc.)
        cards: List of cards in the pile (bottom to top)
        face_up_count: Number of face-up cards (for tableau piles)
    """

    pile_type: PileType
    cards: list[Card] = field(default_factory=list)
    face_up_count: int = 0

    def top_card(self) -> Optional[Card]:
        """Get the top card of the pile without removing it."""
        return self.cards[-1] if self.cards else None

    def can_add_to_foundation(self, card: Card) -> bool:
        """Check if a card can be added to this foundation pile."""
        if self.pile_type != PileType.FOUNDATION:
            return False

        if not self.cards:
            return card.rank == "A"

        top = self.top_card()
        if top and top.suit == card.suit:
            # Must be one rank higher
            rank_order = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"]
            return rank_order.index(card.rank) == rank_order.index(top.rank) + 1

        return False

    def can_add_to_tableau(self, card: Card) -> bool:
        """Check if a card can be added to this tableau pile."""
        if self.pile_type != PileType.TABLEAU:
            return False

        if not self.cards:
            return card.rank == "K"

        top = self.top_card()
        if top:
            # Must be opposite color and one rank lower
            rank_order = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"]
            is_opposite_color = self._is_opposite_color(card, top)
            is_one_rank_lower = rank_order.index(card.rank) == rank_order.index(top.rank) - 1
            return is_opposite_color and is_one_rank_lower

        return False

    @staticmethod
    def _is_opposite_color(card1: Card, card2: Card) -> bool:
        """Check if two cards are opposite colors."""
        red_suits = {Suit.HEARTS, Suit.DIAMONDS}
        black_suits = {Suit.CLUBS, Suit.SPADES}
        card1_red = card1.suit in red_suits
        card2_red = card2.suit in red_suits
        return card1_red != card2_red


class SolitaireGame:
    """Main engine for Klondike solitaire.

    This class manages the game state and provides methods for moving cards
    between piles according to solitaire rules.
    """

    def __init__(self, *, rng=None):
        """Initialize a new solitaire game.

        Args:
            rng: Optional random number generator for shuffling.
        """
        self.rng = rng
        self.deck = Deck()
        if rng:
            self.deck.shuffle(rng=rng)
        else:
            self.deck.shuffle()

        # Initialize piles
        self.foundations: list[Pile] = [Pile(PileType.FOUNDATION) for _ in range(4)]
        self.tableau: list[Pile] = [Pile(PileType.TABLEAU) for _ in range(7)]
        self.stock = Pile(PileType.STOCK)
        self.waste = Pile(PileType.WASTE)

        self._setup_game()

    def _setup_game(self) -> None:
        """Deal cards to tableau and stock piles."""
        # Deal to tableau: 1 card to first pile, 2 to second, etc.
        for i in range(7):
            for j in range(i + 1):
                card = self.deck.deal(1)[0]
                self.tableau[i].cards.append(card)
            # Only the top card is face up
            self.tableau[i].face_up_count = 1

        # Remaining cards go to stock
        self.stock.cards = self.deck.cards.copy()
        self.deck.cards.clear()

    def draw_from_stock(self) -> bool:
        """Draw a card from stock to waste.

        Returns:
            True if a card was drawn, False if stock is empty.
        """
        if self.stock.cards:
            card = self.stock.cards.pop()
            self.waste.cards.append(card)
            return True
        return False

    def reset_stock(self) -> bool:
        """Move all cards from waste back to stock.

        Returns:
            True if cards were moved, False if waste is empty.
        """
        if self.waste.cards:
            self.stock.cards = list(reversed(self.waste.cards))
            self.waste.cards.clear()
            return True
        return False

    def move_to_foundation(self, source_pile: Pile, foundation_index: int) -> bool:
        """Move top card from source pile to foundation.

        Args:
            source_pile: The pile to move from.
            foundation_index: Index of the foundation pile (0-3).

        Returns:
            True if move was successful, False otherwise.
        """
        if not source_pile.cards:
            return False

        card = source_pile.top_card()
        if card and self.foundations[foundation_index].can_add_to_foundation(card):
            self.foundations[foundation_index].cards.append(source_pile.cards.pop())

            # Update face-up count for tableau piles
            if source_pile.pile_type == PileType.TABLEAU and source_pile.cards:
                if source_pile.face_up_count > len(source_pile.cards):
                    source_pile.face_up_count = len(source_pile.cards)
                if source_pile.face_up_count == 0:
                    source_pile.face_up_count = 1

            return True
        return False

    def move_to_tableau(self, source_pile: Pile, tableau_index: int, num_cards: int = 1) -> bool:
        """Move cards from source pile to tableau.

        Args:
            source_pile: The pile to move from.
            tableau_index: Index of the tableau pile (0-6).
            num_cards: Number of cards to move (for tableau to tableau moves).

        Returns:
            True if move was successful, False otherwise.
        """
        if not source_pile.cards or num_cards > len(source_pile.cards):
            return False

        # For waste and foundation, can only move 1 card
        if source_pile.pile_type in (PileType.WASTE, PileType.FOUNDATION) and num_cards != 1:
            return False

        # For tableau, check face-up count
        if source_pile.pile_type == PileType.TABLEAU:
            if num_cards > source_pile.face_up_count:
                return False

        # Get the cards to move
        cards_to_move = source_pile.cards[-num_cards:]
        bottom_card = cards_to_move[0]

        # Check if the move is valid
        if self.tableau[tableau_index].can_add_to_tableau(bottom_card):
            # Move the cards
            self.tableau[tableau_index].cards.extend(cards_to_move)
            self.tableau[tableau_index].face_up_count += num_cards

            # Remove from source
            source_pile.cards = source_pile.cards[:-num_cards]

            # Update source face-up count
            if source_pile.pile_type == PileType.TABLEAU:
                source_pile.face_up_count -= num_cards
                # Turn over next card if needed
                if source_pile.cards and source_pile.face_up_count == 0:
                    source_pile.face_up_count = 1

            return True
        return False

    def is_won(self) -> bool:
        """Check if the game is won.

        Returns:
            True if all foundations have 13 cards (complete), False otherwise.
        """
        return all(len(foundation.cards) == 13 for foundation in self.foundations)

    def auto_move_to_foundation(self) -> bool:
        """Automatically move any valid cards to foundations.

        Returns:
            True if at least one card was moved, False otherwise.
        """
        moved = False

        # Try waste pile first
        if self.waste.cards:
            for i in range(4):
                if self.move_to_foundation(self.waste, i):
                    moved = True
                    break

        # Try tableau piles
        for tableau_pile in self.tableau:
            if tableau_pile.cards:
                for i in range(4):
                    if self.move_to_foundation(tableau_pile, i):
                        moved = True
                        break

        return moved

    def get_state_summary(self) -> dict:
        """Get a summary of the current game state.

        Returns:
            Dictionary containing counts and information about each pile type.
        """
        return {
            "stock": len(self.stock.cards),
            "waste": len(self.waste.cards),
            "foundations": [len(f.cards) for f in self.foundations],
            "tableau": [
                {
                    "total": len(t.cards),
                    "face_up": t.face_up_count,
                    "face_down": len(t.cards) - t.face_up_count,
                }
                for t in self.tableau
            ],
        }
