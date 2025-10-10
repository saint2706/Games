"""Realistic bluff (Cheat) card game logic with both CLI and GUI hooks."""

from __future__ import annotations

import argparse
import random
from collections import Counter, deque
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Deque, Dict, Iterable, List, Optional, Sequence

from ..common.cards import RANKS, Card, Deck, Suit


class Phase(Enum):
    """High-level phases of the bluff game lifecycle."""

    TURN = auto()
    CHALLENGE = auto()
    COMPLETE = auto()


@dataclass(frozen=True)
class DifficultyLevel:
    """Configuration bucket for bluff bot personalities."""

    name: str
    bot_count: int
    deck_count: int
    honesty: float
    boldness: float
    challenge: float


@dataclass(frozen=True)
class PlayerProfile:
    """Traits that drive a bot's bluffing and challenge behaviour."""

    honesty: float
    boldness: float
    challenge: float
    memory: float


@dataclass
class PlayerState:
    """Runtime information about a seated player."""

    name: str
    is_user: bool
    profile: PlayerProfile
    rng: random.Random
    hand: list[Card] = field(default_factory=list)
    truths: int = 0
    lies: int = 0
    caught: int = 0
    challenge_attempts: int = 0
    challenge_successes: int = 0
    last_caught_turn: Optional[int] = None

    def record_claim(self, truthful: bool) -> None:
        if truthful:
            self.truths += 1
        else:
            self.lies += 1

    def record_caught(self, turn_index: int) -> None:
        self.caught += 1
        self.last_caught_turn = turn_index

    def record_challenge(self, success: bool) -> None:
        self.challenge_attempts += 1
        if success:
            self.challenge_successes += 1

    def card_counts(self) -> Counter[str]:
        return Counter(card.rank for card in self.hand)


@dataclass
class Claim:
    """Representation of a single facedown card entering the pile."""

    claimant: PlayerState
    card: Card
    claimed_rank: str
    truthful: bool


@dataclass
class ChallengeResult:
    """Outcome information from evaluating a pending challenge."""

    resolved: bool
    messages: list[str]


DIFFICULTIES: Dict[str, DifficultyLevel] = {
    "Noob": DifficultyLevel(
        "Noob", bot_count=1, deck_count=1, honesty=0.65, boldness=0.25, challenge=0.2
    ),
    "Easy": DifficultyLevel(
        "Easy", bot_count=2, deck_count=1, honesty=0.6, boldness=0.3, challenge=0.25
    ),
    "Medium": DifficultyLevel(
        "Medium", bot_count=2, deck_count=2, honesty=0.58, boldness=0.35, challenge=0.3
    ),
    "Hard": DifficultyLevel(
        "Hard", bot_count=3, deck_count=2, honesty=0.55, boldness=0.4, challenge=0.35
    ),
    "Insane": DifficultyLevel(
        "Insane", bot_count=4, deck_count=3, honesty=0.52, boldness=0.45, challenge=0.4
    ),
}


class BluffGame:
    """Rules engine for a realistic multi-player game of Cheat/Bluff."""

    def __init__(
        self,
        difficulty: DifficultyLevel,
        *,
        rounds: int = 5,
        rng: random.Random | None = None,
    ) -> None:
        if rounds <= 0:
            raise ValueError("rounds must be a positive integer")

        self.difficulty = difficulty
        self.max_turns = rounds * (difficulty.bot_count + 1)
        self._rng = rng or random.Random()

        self.players: list[PlayerState] = []
        self._pile_cards: list[Card] = []
        self._pile_claims: list[Claim] = []
        self._challenge_queue: Deque[PlayerState] = deque()
        self._claim_in_progress: Claim | None = None
        self._phase = Phase.TURN
        self._turns_played = 0
        self._winner: PlayerState | None = None

        self._setup_players()
        self._deal_initial_hands()

    # ------------------------------------------------------------------
    # Initialisation helpers
    # ------------------------------------------------------------------
    def _setup_players(self) -> None:
        user_profile = PlayerProfile(honesty=0.62, boldness=0.28, challenge=0.3, memory=0.6)
        self.players.append(
            PlayerState(name="You", is_user=True, profile=user_profile, rng=self._rng)
        )

        for index in range(self.difficulty.bot_count):
            base = self.difficulty
            variance = self._rng.uniform(-0.05, 0.05)
            profile = PlayerProfile(
                honesty=max(0.2, min(0.95, base.honesty + variance)),
                boldness=max(0.05, min(0.9, base.boldness + variance * 1.5)),
                challenge=max(0.05, min(0.9, base.challenge + variance)),
                memory=max(0.2, min(0.95, 0.55 + variance * 2)),
            )
            bot = PlayerState(
                name=f"{self.difficulty.name} Bot {index + 1}",
                is_user=False,
                profile=profile,
                rng=self._rng,
            )
            self.players.append(bot)

    def _build_multi_deck(self, deck_count: int) -> Deck:
        cards: list[Card] = []
        for _ in range(deck_count):
            cards.extend(Card(rank, suit) for suit in Suit for rank in RANKS)
        return Deck(cards=cards)

    def _deal_initial_hands(self) -> None:
        deck = self._build_multi_deck(self.difficulty.deck_count)
        deck.shuffle(rng=self._rng)
        player_index = 0
        while deck.cards:
            self.players[player_index].hand.append(deck.deal(1)[0])
            player_index = (player_index + 1) % len(self.players)

        self._current_player_index = 0
        self._phase = Phase.TURN
        self._turns_played = 0
        self._pile_cards.clear()
        self._pile_claims.clear()
        self._challenge_queue.clear()
        self._winner = None
        self._claim_in_progress = None

    # ------------------------------------------------------------------
    # Properties and state helpers
    # ------------------------------------------------------------------
    @property
    def phase(self) -> Phase:
        return self._phase

    @property
    def winner(self) -> PlayerState | None:
        return self._winner

    @property
    def finished(self) -> bool:
        return self._phase == Phase.COMPLETE

    @property
    def current_player(self) -> PlayerState:
        return self.players[self._current_player_index]

    @property
    def pile_size(self) -> int:
        return len(self._pile_cards)

    @property
    def claim_in_progress(self) -> Claim | None:
        return self._claim_in_progress

    @property
    def current_challenger(self) -> PlayerState | None:
        return self._challenge_queue[0] if self._challenge_queue else None

    def public_state(self) -> Dict[str, object]:
        """Expose a serialisable snapshot for UIs."""

        return {
            "phase": self._phase.name,
            "pile_size": len(self._pile_cards),
            "turns_played": self._turns_played,
            "max_turns": self.max_turns,
            "players": [
                {
                    "name": player.name,
                    "is_user": player.is_user,
                    "card_count": len(player.hand),
                    "truths": player.truths,
                    "lies": player.lies,
                    "calls": player.challenge_attempts,
                    "correct_calls": player.challenge_successes,
                }
                for player in self.players
            ],
            "claim": None
            if not self._claim_in_progress
            else {
                "claimant": self._claim_in_progress.claimant.name,
                "claimed_rank": self._claim_in_progress.claimed_rank,
                "truthful": self._claim_in_progress.truthful,
            },
        }

    # ------------------------------------------------------------------
    # Turn handling
    # ------------------------------------------------------------------
    def play_user_turn(self, card_index: int, claimed_rank: str) -> Claim:
        player = self.current_player
        if not player.is_user:
            raise RuntimeError("It is not the user's turn.")
        return self._play_turn(player, card_index, claimed_rank)

    def play_bot_turn(self) -> tuple[Claim, list[str]]:
        player = self.current_player
        if player.is_user:
            raise RuntimeError("It is not a bot's turn.")

        hand_counts = player.card_counts()
        truthful_bias = player.profile.honesty

        if player.last_caught_turn is not None and self._turns_played - player.last_caught_turn < 3:
            truthful_bias += 0.12

        # Larger piles encourage daring plays
        truthful_bias -= min(0.2, len(self._pile_cards) * 0.02 * player.profile.boldness)

        truthful = self._rng.random() < max(0.1, min(0.95, truthful_bias))
        claimed_rank: str
        chosen_card: Card

        if truthful and hand_counts:
            ranked = hand_counts.most_common()
            weights = [count for _, count in ranked]
            chosen_rank = self._rng.choices([rank for rank, _ in ranked], weights=weights)[0]
            chosen_card = next(card for card in player.hand if card.rank == chosen_rank)
            claimed_rank = chosen_rank
        else:
            chosen_card = self._rng.choice(player.hand)
            owned_ranks = set(card.rank for card in player.hand)
            bluff_options = [rank for rank in RANKS if rank not in owned_ranks and rank != chosen_card.rank]
            if not bluff_options:
                bluff_options = [rank for rank in RANKS if rank != chosen_card.rank]
            claimed_rank = self._rng.choice(bluff_options)
            truthful = chosen_card.rank == claimed_rank
            if truthful:
                # Ensure this remains a bluff by nudging to a different rank
                alternatives = [rank for rank in RANKS if rank != chosen_card.rank]
                claimed_rank = self._rng.choice(alternatives)
                truthful = False

        claim = self._play_turn(player, player.hand.index(chosen_card), claimed_rank)

        if truthful:
            message = f"{player.name} calmly slides a card forward claiming it is a {claimed_rank}."
        else:
            message = (
                f"{player.name} hesitates ever so slightly before declaring their card to be a {claimed_rank}."
            )
        return claim, [message]

    def _play_turn(self, player: PlayerState, card_index: int, claimed_rank: str) -> Claim:
        if self._phase != Phase.TURN:
            raise RuntimeError("Cannot play a turn while a challenge is unresolved.")
        if not 0 <= card_index < len(player.hand):
            raise ValueError("card_index out of range")
        if claimed_rank not in RANKS:
            raise ValueError("claimed_rank must be a valid rank symbol")

        card = player.hand.pop(card_index)
        truthful = card.rank == claimed_rank
        player.record_claim(truthful)

        claim = Claim(claimant=player, card=card, claimed_rank=claimed_rank, truthful=truthful)
        self._claim_in_progress = claim
        self._pile_cards.append(card)
        self._pile_claims.append(claim)

        self._challenge_queue = deque(self._iter_other_players_from(player))
        self._phase = Phase.CHALLENGE

        return claim

    def _iter_other_players_from(self, player: PlayerState) -> List[PlayerState]:
        start = self.players.index(player)
        ordering: list[PlayerState] = []
        for offset in range(1, len(self.players)):
            ordering.append(self.players[(start + offset) % len(self.players)])
        return ordering

    # ------------------------------------------------------------------
    # Challenge resolution
    # ------------------------------------------------------------------
    def evaluate_challenge(self, decision: bool) -> ChallengeResult:
        if self._phase != Phase.CHALLENGE:
            raise RuntimeError("There is no claim waiting to be challenged.")
        if not self._claim_in_progress:
            raise RuntimeError("No active claim is registered.")

        messages: list[str] = []
        if not self._challenge_queue:
            # No one left to challenge; finalise quietly.
            return self._finalise_uncontested()

        challenger = self._challenge_queue[0]
        if not decision:
            self._challenge_queue.popleft()
            if challenger.is_user:
                messages.append("You decide to let the claim stand.")
            else:
                messages.append(f"{challenger.name} chooses not to make a scene.")
            if not self._challenge_queue:
                follow_up = self._finalise_uncontested()
                messages.extend(follow_up.messages)
                return ChallengeResult(resolved=follow_up.resolved, messages=messages)
            return ChallengeResult(resolved=False, messages=messages)

        # Challenge is happening
        self._challenge_queue.popleft()
        claim = self._claim_in_progress
        challenger.record_challenge(success=not claim.truthful)
        messages.append(f"{challenger.name} slams a hand down and calls the bluff!")

        if claim.truthful:
            collector = challenger
            collector.hand.extend(self._pile_cards)
            collector.rng.shuffle(collector.hand)
            self._pile_cards.clear()
            self._pile_claims.clear()
            messages.append(
                f"The card really was {claim.card}. {collector.name} must scoop up the entire pile."
            )
            result = self._complete_turn(challenge_made=True, liar_caught=False, collector=collector)
            messages.extend(result.messages)
            return ChallengeResult(resolved=True, messages=messages)

        # Challenger was correct – claimant collects the pile
        collector = claim.claimant
        collector.record_caught(self._turns_played)
        collector.hand.extend(self._pile_cards)
        collector.rng.shuffle(collector.hand)
        self._pile_cards.clear()
        self._pile_claims.clear()
        messages.append(f"{claim.claimant.name} was caught! Their card was actually {claim.card}.")
        result = self._complete_turn(challenge_made=True, liar_caught=True, collector=collector)
        messages.extend(result.messages)
        return ChallengeResult(resolved=True, messages=messages)

    def _finalise_uncontested(self) -> ChallengeResult:
        claim = self._claim_in_progress
        if not claim:
            raise RuntimeError("There is no claim to finalise.")

        messages = ["No one dares to challenge. The table tension rises."]
        result = self._complete_turn(challenge_made=False, liar_caught=False, collector=None)
        messages.extend(result.messages)
        return ChallengeResult(resolved=True, messages=messages)

    def _complete_turn(
        self,
        *,
        challenge_made: bool,
        liar_caught: bool,
        collector: PlayerState | None,
    ) -> ChallengeResult:
        assert self._claim_in_progress is not None
        claimant = self._claim_in_progress.claimant
        messages: list[str] = []

        if liar_caught:
            messages.append(f"{claimant.name} drags the pile back and their hand grows to {len(claimant.hand)} cards.")
        elif challenge_made and collector is not None:
            messages.append(
                f"{collector.name} adds the pile to their hand, now holding {len(collector.hand)} cards."
            )

        self._claim_in_progress = None
        self._challenge_queue.clear()
        self._phase = Phase.TURN
        self._turns_played += 1

        if not claimant.hand:
            self._winner = claimant
            self._phase = Phase.COMPLETE
            messages.append(f"{claimant.name} has shed every card and wins the table!")
            return ChallengeResult(resolved=True, messages=messages)

        if self._turns_played >= self.max_turns:
            messages.extend(self._close_by_card_count())
            return ChallengeResult(resolved=True, messages=messages)

        self._current_player_index = (self.players.index(claimant) + 1) % len(self.players)
        self._advance_to_next_player_with_cards()
        return ChallengeResult(resolved=True, messages=messages)

    def _advance_to_next_player_with_cards(self) -> None:
        start = self._current_player_index
        for offset in range(len(self.players)):
            candidate = self.players[(start + offset) % len(self.players)]
            if candidate.hand:
                self._current_player_index = self.players.index(candidate)
                return
        # Everyone is out of cards (should not happen without winner). End the game defensively.
        self._phase = Phase.COMPLETE

    def _close_by_card_count(self) -> list[str]:
        standings = sorted(self.players, key=lambda player: (len(player.hand), player.is_user))
        best_count = len(standings[0].hand)
        winners = [player for player in standings if len(player.hand) == best_count]
        if len(winners) == 1:
            self._winner = winners[0]
            self._phase = Phase.COMPLETE
            return [
                "Maximum rounds reached.",
                f"{winners[0].name} holds the fewest cards ({best_count}) and is declared the winner.",
            ]

        self._winner = None
        self._phase = Phase.COMPLETE
        tied_names = ", ".join(player.name for player in winners)
        return [
            "Maximum rounds reached with a tie.",
            f"Players with the fewest cards ({best_count}): {tied_names}.",
        ]

    # ------------------------------------------------------------------
    # Bot challenge logic
    # ------------------------------------------------------------------
    def bot_should_challenge(self, challenger: PlayerState) -> bool:
        if not self._claim_in_progress:
            return False

        claim = self._claim_in_progress
        claimant = claim.claimant
        history_total = claimant.truths + claimant.lies
        lie_rate = (claimant.lies + 1) / (history_total + 2)
        call_rate = challenger.profile.challenge
        if claimant.last_caught_turn is not None:
            distance = self._turns_played - claimant.last_caught_turn
            if distance <= 1:
                lie_rate += 0.25
            elif distance <= 3:
                lie_rate += 0.1

        owned = challenger.card_counts()[claim.claimed_rank]
        ownership_pressure = 0.0
        if owned >= 3:
            ownership_pressure += 0.25
        elif owned == 2:
            ownership_pressure += 0.15
        elif owned == 0:
            ownership_pressure -= 0.08

        pile_pressure = min(0.35, len(self._pile_cards) * 0.025)
        tendency = call_rate + lie_rate * challenger.profile.memory + ownership_pressure + pile_pressure
        tendency = max(0.05, min(0.9, tendency))

        # Bots with few cards become more cautious
        if len(challenger.hand) <= 2:
            tendency -= 0.2
        elif len(challenger.hand) >= 10:
            tendency += 0.1

        return challenger.rng.random() < tendency

    # ------------------------------------------------------------------
    # CLI helpers
    # ------------------------------------------------------------------
    def scoreboard(self) -> str:
        rows = ["Current card counts:"]
        for player in self.players:
            rows.append(
                f"- {player.name}: {len(player.hand)} cards | Truths: {player.truths} | Lies: {player.lies} | Calls: {player.challenge_successes}/{player.challenge_attempts}"
            )
        rows.append(f"Pile size: {len(self._pile_cards)}")
        rows.append(f"Turn {self._turns_played + 1} of {self.max_turns}")
        return "\n".join(rows)


# ----------------------------------------------------------------------
# CLI orchestration
# ----------------------------------------------------------------------


def parse_arguments(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--difficulty",
        choices=DIFFICULTIES.keys(),
        default="Noob",
        help="Which AI difficulty to face.",
    )
    parser.add_argument(
        "--rounds",
        type=int,
        default=5,
        help="Number of table rotations before the match is adjudicated (default: 5).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Optional random seed for deterministic sessions.",
    )
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Launch the Tkinter interface instead of the CLI.",
    )
    return parser.parse_args(argv)


def run_cli(argv: Sequence[str] | None = None) -> None:
    args = parse_arguments(argv)
    rng = random.Random(args.seed) if args.seed is not None else random.Random()
    difficulty = DIFFICULTIES[args.difficulty]

    if args.gui:
        from .gui import run_gui

        run_gui(difficulty, rounds=args.rounds, seed=args.seed)
        return

    game = BluffGame(difficulty, rounds=args.rounds, rng=rng)

    print(
        "Welcome to Bluff! Each player discards one card facedown, claiming its rank."
        " If someone challenges and the card was truthful, the challenger collects the"
        " whole pile. If it was a bluff, the liar takes the pile. First to empty their"
        " hand wins."
    )
    print(f"Difficulty: {difficulty.name} | Opponents: {difficulty.bot_count}\n")

    while not game.finished:
        player = game.current_player
        print(game.scoreboard())
        print()
        if player.is_user:
            print("Your hand:")
            for idx, card in enumerate(player.hand):
                print(f"  [{idx}] {card} ({card.rank})")

            chosen_index = _prompt_card_index(len(player.hand))
            claimed_rank = _prompt_claim_rank(player.hand[chosen_index])
            claim = game.play_user_turn(chosen_index, claimed_rank)
            print(f"You slide forward {claim.card} and claim it is a {claim.claimed_rank}.")
        else:
            claim, messages = game.play_bot_turn()
            for message in messages:
                print(message)

        while game.phase == Phase.CHALLENGE and not game.finished:
            challenger = game.current_challenger
            if challenger is None:
                break
            if challenger.is_user:
                decision = _prompt_user_challenge(claim.claimant.name, game.pile_size)
            else:
                decision = game.bot_should_challenge(challenger)
                if decision:
                    print(f"{challenger.name} eyes the pile and prepares to challenge...")
                else:
                    print(f"{challenger.name} stays quiet.")
            result = game.evaluate_challenge(decision)
            for line in result.messages:
                print(line)

        print()

    print("Match complete!\n")
    if game.winner is not None:
        if game.winner.is_user:
            print("Congratulations, you outmaneuvered the table!")
        else:
            print(f"{game.winner.name} claims victory this time.")
    else:
        print("It's a draw—multiple players share the honours.")


def _prompt_card_index(hand_size: int) -> int:
    while True:
        choice = input("Select the index of the card you want to play: ").strip()
        if choice.isdigit():
            index = int(choice)
            if 0 <= index < hand_size:
                return index
        print("Please enter a valid index from your hand.")


def _prompt_claim_rank(card: Card) -> str:
    while True:
        rank = input(
            "Declare your card's rank (e.g. 'A', 'K', '7'). You may bluff by stating a different rank: "
        ).strip().upper()
        if rank in RANKS:
            return rank
        print("Unknown rank. Valid options are: " + ", ".join(RANKS))


def _prompt_user_challenge(claimant_name: str, pile_size: int) -> bool:
    while True:
        choice = input(
            f"Do you want to challenge {claimant_name}'s claim? (call/trust) [pile has {pile_size} cards]: "
        ).strip().lower()
        if choice in {"call", "c"}:
            return True
        if choice in {"trust", "t", "pass", "p"}:
            return False
        print("Please answer with 'call' or 'trust'.")


def main(argv: Iterable[str] | None = None) -> None:  # pragma: no cover - convenience
    run_cli(argv)


if __name__ == "__main__":  # pragma: no cover - script entry point
    main()
