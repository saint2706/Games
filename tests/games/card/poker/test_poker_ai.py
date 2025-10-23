"""Regression tests for the poker AI's Monte Carlo equity estimation."""

from __future__ import annotations

import os
import random
import time

import pytest

from games_collection.games.card.common.cards import Card, Suit
from games_collection.games.card.poker.poker import Player, estimate_win_rate


@pytest.fixture
def sample_players() -> tuple[Player, list[Player]]:
    """Provide a hero and a list of active opponents with deterministic cards."""

    hero = Player(name="Hero")
    hero.hole_cards = [Card("A", Suit.SPADES), Card("K", Suit.SPADES)]

    opponents = [Player(name="Villain1"), Player(name="Villain2")]
    for opponent in opponents:
        opponent.folded = False

    return hero, opponents


def test_parallel_matches_serial(sample_players: tuple[Player, list[Player]]) -> None:
    """Parallel estimation must match the serial estimator when seeded."""

    hero, opponents = sample_players
    community_cards = [Card("2", Suit.DIAMONDS), Card("7", Suit.CLUBS), Card("9", Suit.HEARTS)]

    serial_rng = random.Random(1337)
    parallel_rng = random.Random(1337)

    players = [hero] + opponents

    serial_equity = estimate_win_rate(
        hero=hero,
        players=players,
        community_cards=community_cards,
        simulations=256,
        rng=serial_rng,
        max_workers=1,
    )

    parallel_equity = estimate_win_rate(
        hero=hero,
        players=players,
        community_cards=community_cards,
        simulations=256,
        rng=parallel_rng,
        max_workers=4,
    )

    assert parallel_equity == pytest.approx(serial_equity, abs=1e-9)


@pytest.mark.skipif((os.cpu_count() or 1) < 2, reason="parallel benchmarks require multiple CPUs")
def test_parallel_speedup(sample_players: tuple[Player, list[Player]]) -> None:
    """Parallel estimation should be meaningfully faster on multi-core systems."""

    hero, opponents = sample_players
    community_cards = [Card("2", Suit.DIAMONDS), Card("7", Suit.CLUBS), Card("9", Suit.HEARTS)]

    serial_rng = random.Random(2024)
    parallel_rng = random.Random(2024)
    players = [hero] + opponents

    simulations = 1024
    worker_cap = min(4, os.cpu_count() or 2)

    serial_start = time.perf_counter()
    serial_equity = estimate_win_rate(
        hero=hero,
        players=players,
        community_cards=community_cards,
        simulations=simulations,
        rng=serial_rng,
        max_workers=1,
    )
    serial_duration = time.perf_counter() - serial_start

    parallel_start = time.perf_counter()
    parallel_equity = estimate_win_rate(
        hero=hero,
        players=players,
        community_cards=community_cards,
        simulations=simulations,
        rng=parallel_rng,
        max_workers=worker_cap,
    )
    parallel_duration = time.perf_counter() - parallel_start

    assert parallel_equity == pytest.approx(serial_equity, abs=1e-9)
    assert parallel_duration < serial_duration * 0.9
