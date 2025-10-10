"""Utility helpers for ranking poker hands from concise card codes.

Example
-------
>>> evaluate_hand(["As", "Kd", "Qh", "Jc", "Tc"])
'Straight (A♠ K♦ Q♥ J♣ T♣)'
"""

from __future__ import annotations

from typing import Iterable, Sequence

from ..common.cards import format_cards, parse_card
from .poker_core import HandRank, best_hand


def evaluate_hand(card_codes: Sequence[str]) -> HandRank:
    """Return a :class:`HandRank` for the provided ``card_codes``.

    Parameters
    ----------
    card_codes:
        Sequence of two character codes such as ``"As"`` for Ace of spades or
        ``"Td"`` for ten of diamonds.
    """

    cards = [parse_card(code) for code in card_codes]
    return best_hand(cards)


def describe_hand(card_codes: Sequence[str]) -> str:
    """Return a human friendly description of ``card_codes``."""

    rank = evaluate_hand(card_codes)
    return f"{rank.describe()} from {format_cards(parse_card(code) for code in card_codes)}"


def main(card_codes: Iterable[str]) -> None:  # pragma: no cover - convenience
    rank = evaluate_hand(list(card_codes))
    print(rank.describe())


if __name__ == "__main__":  # pragma: no cover - simple demo
    import sys

    if len(sys.argv) <= 1:
        print("Usage: python -m card_games.poker.poker_hand_evaluator <card> [<card> ...]")
        sys.exit(1)

    main(sys.argv[1:])
