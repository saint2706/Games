"""Core poker domain models and hand evaluation utilities.

This module provides a modern, well tested friendly API for working with
standard playing cards.  It exposes a light-weight object model for hand
rankings that can be reused by the command line interface and other scripts.
The implementation intentionally avoids any global state so it is easy to test
and reuse.

The public entry point is :func:`best_hand` which accepts an iterable of cards
and returns the strongest five card hand that can be made from them.  The
result is returned as a :class:`HandRank` instance which can be compared using
standard ordering operators.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from itertools import combinations
from typing import Iterable, Sequence, Tuple

from ..common.cards import RANK_TO_VALUE, Card


class HandCategory(int, Enum):
    """Categories of poker hands ordered from weakest to strongest."""

    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    STRAIGHT = 4
    FLUSH = 5
    FULL_HOUSE = 6
    FOUR_OF_A_KIND = 7
    STRAIGHT_FLUSH = 8


@dataclass(order=True, frozen=True)
class HandRank:
    """Value object encapsulating the strength of a five card hand."""

    category: HandCategory
    tiebreaker: Tuple[int, ...]
    cards: Tuple[Card, ...] = field(compare=False)

    def describe(self) -> str:
        """Return a human friendly description of the ranked hand."""

        category_name = self.category.name.replace("_", " ").title()
        cards_str = " ".join(map(str, self.cards))
        return f"{category_name} ({cards_str})"


def best_hand(cards: Iterable[Card]) -> HandRank:
    """Return the best possible five-card hand from the provided cards."""

    card_list = list(cards)
    if len(card_list) < 5:
        raise ValueError("At least five cards are required to evaluate a hand")

    return max((rank_five_card_hand(combo) for combo in combinations(card_list, 5)))


def rank_five_card_hand(cards: Sequence[Card]) -> HandRank:
    """Evaluate a five card poker hand and return its :class:`HandRank`."""

    if len(cards) != 5:
        raise ValueError("Exactly five cards must be supplied")

    sorted_cards = tuple(sorted(cards, key=lambda card: card.value, reverse=True))
    values = tuple(card.value for card in sorted_cards)
    is_flush = len({card.suit for card in cards}) == 1

    unique_values = sorted(set(values), reverse=True)
    straight_values = _straight_values(values)
    is_straight = straight_values is not None

    counts: dict[int, int] = {value: values.count(value) for value in unique_values}
    sorted_counts = sorted(counts.items(), key=lambda item: (item[1], item[0]), reverse=True)

    if is_straight and is_flush:
        return HandRank(HandCategory.STRAIGHT_FLUSH, (straight_values,), sorted_cards)

    if sorted_counts[0][1] == 4:
        kicker = max(value for value in values if value != sorted_counts[0][0])
        return HandRank(HandCategory.FOUR_OF_A_KIND, (sorted_counts[0][0], kicker), sorted_cards)

    if sorted_counts[0][1] == 3 and sorted_counts[1][1] == 2:
        return HandRank(HandCategory.FULL_HOUSE, (sorted_counts[0][0], sorted_counts[1][0]), sorted_cards)

    if is_flush:
        return HandRank(HandCategory.FLUSH, values, sorted_cards)

    if is_straight:
        return HandRank(HandCategory.STRAIGHT, (straight_values,), sorted_cards)

    if sorted_counts[0][1] == 3:
        kickers = tuple(value for value in values if value != sorted_counts[0][0])
        return HandRank(HandCategory.THREE_OF_A_KIND, (sorted_counts[0][0],) + kickers, sorted_cards)

    if sorted_counts[0][1] == 2 and sorted_counts[1][1] == 2:
        pair_values = (sorted_counts[0][0], sorted_counts[1][0])
        kicker = max(value for value in values if value not in pair_values)
        return HandRank(HandCategory.TWO_PAIR, pair_values + (kicker,), sorted_cards)

    if sorted_counts[0][1] == 2:
        pair_value = sorted_counts[0][0]
        kickers = tuple(value for value in values if value != pair_value)
        return HandRank(HandCategory.ONE_PAIR, (pair_value,) + kickers, sorted_cards)

    return HandRank(HandCategory.HIGH_CARD, values, sorted_cards)


def _straight_values(values: Tuple[int, ...]) -> int | None:
    """Return the highest card in a straight or ``None`` if not a straight."""

    unique_values = sorted(set(values), reverse=True)
    if len(unique_values) != 5:
        # Can't be a straight if duplicates exist.
        return None

    # Handle the "wheel" straight: A-2-3-4-5.
    if unique_values == [12, 3, 2, 1, 0]:
        return 3

    high, *rest = unique_values
    expected = list(range(high, high - 5, -1))
    return high if unique_values == expected else None
