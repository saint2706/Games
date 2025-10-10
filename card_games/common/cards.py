"""General representations of playing cards shared across games."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable, Iterator, Tuple


class Suit(str, Enum):
    """Enumeration of the four suits in a standard 52 card deck."""

    CLUBS = "♣"
    DIAMONDS = "♦"
    HEARTS = "♥"
    SPADES = "♠"


RANKS: Tuple[str, ...] = (
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "T",
    "J",
    "Q",
    "K",
    "A",
)

RANK_TO_VALUE = {rank: index for index, rank in enumerate(RANKS)}


@dataclass(frozen=True)
class Card:
    """Representation of a single playing card."""

    rank: str
    suit: Suit

    def __post_init__(self) -> None:
        if self.rank not in RANK_TO_VALUE:
            raise ValueError(f"Unsupported rank: {self.rank!r}")

    @property
    def value(self) -> int:
        """Integer value of the card used for comparisons."""

        return RANK_TO_VALUE[self.rank]

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"{self.rank}{self.suit.value}"


@dataclass
class Deck:
    """A mutable deck of playing cards."""

    cards: list[Card] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.cards:
            self.cards = [Card(rank, suit) for suit in Suit for rank in RANKS]

    def shuffle(self, *, rng=None) -> None:
        """Shuffle the deck in place."""

        if rng is None:
            import random

            rng = random

        rng.shuffle(self.cards)

    def deal(self, count: int = 1) -> list[Card]:
        """Remove and return ``count`` cards from the top of the deck."""

        if count < 0:
            raise ValueError("count must be positive")
        if count > len(self.cards):
            raise ValueError("Not enough cards remaining in the deck")
        dealt, self.cards = self.cards[:count], self.cards[count:]
        return dealt

    def __iter__(self) -> Iterator[Card]:  # pragma: no cover - trivial
        yield from self.cards


def parse_card(code: str) -> Card:
    """Parse a two character card code (e.g. ``"As"``) into a :class:`Card`."""

    if len(code) != 2:
        raise ValueError(f"Invalid card code: {code!r}")
    rank_code, suit_code = code[0].upper(), code[1].upper()

    suit_map = {"S": Suit.SPADES, "H": Suit.HEARTS, "D": Suit.DIAMONDS, "C": Suit.CLUBS}
    if suit_code not in suit_map:
        raise ValueError(f"Unknown suit code: {suit_code!r}")

    if rank_code == "A":
        rank = "A"
    elif rank_code == "K":
        rank = "K"
    elif rank_code == "Q":
        rank = "Q"
    elif rank_code == "J":
        rank = "J"
    elif rank_code in {"T", "1"}:
        rank = "T"
    elif rank_code in {"2", "3", "4", "5", "6", "7", "8", "9"}:
        rank = rank_code
    else:
        raise ValueError(f"Unknown rank code: {rank_code!r}")

    return Card(rank, suit_map[suit_code])


def format_cards(cards: Iterable[Card]) -> str:
    """Return a nicely formatted string representation of ``cards``."""

    return " ".join(str(card) for card in cards)


__all__ = [
    "Card",
    "Deck",
    "Suit",
    "RANKS",
    "RANK_TO_VALUE",
    "format_cards",
    "parse_card",
]
