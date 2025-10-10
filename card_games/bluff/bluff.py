"""Card game engine, AI, and CLI helpers for the game of Bluff (a.k.a. Cheat).

This module provides a comprehensive implementation of the card game "Bluff"
(also known as "Cheat" or "I Doubt It"). It includes the game engine, bot AI,
and hooks for both command-line and graphical user interfaces.

The game is structured around these key components:

* **Phases** – The :class:`Phase` enum models the three states of play
  (``TURN``, ``CHALLENGE``, and ``COMPLETE``) so the engine can react
  appropriately to user and AI choices.
* **Player representation** – :class:`PlayerState` tracks a player's hand, bot
  personality, and historical statistics that inform the AI's decision making.
* **Game state** – The :class:`BluffGame` class manages the deck, discard pile,
  pending challenges, and the overall flow of the match.
* **Bot AI** – Bot behaviour is parameterised by :class:`DifficultyLevel`
  objects, giving each difficulty setting a distinct "personality".
* **User interaction** – Helper functions at the bottom of the module wire the
  engine into an interactive CLI, while :mod:`card_games.bluff.gui` provides a
  Tkinter interface.

In addition to the public API, the module contains numerous helper functions
with richly documented behaviour intended to act as executable documentation for
the game's rules. These docstrings deliberately repeat concepts established in
other parts of the file so that each class or function can be understood in
isolation.
"""

from __future__ import annotations

import argparse
import random
from collections import Counter, deque
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Deque, Dict, Iterable, List, Optional, Sequence

from ..common.cards import RANKS, Card, Deck, Suit


class Phase(Enum):
    """High-level phases of the bluff game lifecycle.

    - ``TURN``: The current player is expected to make a claim.
    - ``CHALLENGE``: Other players have the opportunity to challenge the claim.
    - ``COMPLETE``: The game has ended, and a winner may be declared.
    """

    TURN = auto()
    CHALLENGE = auto()
    COMPLETE = auto()


@dataclass(frozen=True)
class DifficultyLevel:
    """Configuration bucket for bluff bot personalities and game rules.

    This dataclass defines the parameters for a game's difficulty, including
    the number of bots, decks, and the baseline AI characteristics.

    Attributes:
        name (str): The name of the difficulty level (e.g., "Easy", "Hard").
        bot_count (int): The number of bot opponents.
        deck_count (int): The number of standard 52-card decks to use.
        honesty (float): Baseline probability that a bot will play truthfully.
        boldness (float): Multiplier for how much the pile size encourages bluffing.
        challenge (float): Baseline probability that a bot will challenge a claim.
    """

    name: str
    bot_count: int
    deck_count: int
    honesty: float
    boldness: float
    challenge: float


@dataclass(frozen=True)
class PlayerProfile:
    """Traits that drive a bot's bluffing and challenge behaviour.

    Each bot player has a profile that fine-tunes its AI, adding variability
    and personality beyond the base difficulty level.

    Attributes:
        honesty (float): The bot's individual tendency to be truthful.
        boldness (float): How much the bot is influenced by the size of the pile.
        challenge (float): The bot's willingness to call out others.
        memory (float): How much the bot considers other players' history.
    """

    honesty: float
    boldness: float
    challenge: float
    memory: float


@dataclass
class PlayerState:
    """Runtime information about a seated player, including their hand and stats.

    Attributes:
        name (str): The player's display name.
        is_user (bool): True if this player is controlled by a human.
        profile (PlayerProfile): The AI profile for this player.
        rng (random.Random): The random number generator for this player.
        hand (list[Card]): The cards currently held by the player.
        truths (int): The number of truthful claims made.
        lies (int): The number of bluffs made.
        caught (int): The number of times this player was caught bluffing.
        challenge_attempts (int): The number of challenges made.
        challenge_successes (int): The number of successful challenges.
        last_caught_turn (Optional[int]): The turn index when the player was last caught.
    """

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
        """Update statistics based on a claim being truthful or a bluff."""
        if truthful:
            self.truths += 1
        else:
            self.lies += 1

    def record_caught(self, turn_index: int) -> None:
        """Record that the player was caught in a bluff."""
        self.caught += 1
        self.last_caught_turn = turn_index

    def record_challenge(self, success: bool) -> None:
        """Update statistics after making a challenge."""
        self.challenge_attempts += 1
        if success:
            self.challenge_successes += 1

    def card_counts(self) -> Counter[str]:
        """Return a count of cards for each rank in the player's hand."""
        return Counter(card.rank for card in self.hand)


@dataclass
class Claim:
    """Representation of a single facedown card played into the pile.

    A claim captures who played the card, the card itself, what rank they
    claimed it was, and whether that claim was truthful.
    """

    claimant: PlayerState
    card: Card
    claimed_rank: str
    truthful: bool


@dataclass
class ChallengeResult:
    """Outcome information from evaluating a pending challenge.

    Attributes:
        resolved (bool): True if the challenge phase is over.
        messages (list[str]): A list of messages describing the outcome.
    """

    resolved: bool
    messages: list[str]


# Pre-defined difficulty levels for the game.
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
    """Rules engine for a realistic multi-player game of Cheat/Bluff.

    This class manages the entire game lifecycle, from setup and dealing to
    turn processing, challenge resolution, and determining the winner.
    """

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

        # Game state attributes
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
        """Create the user and bot players based on the difficulty settings."""
        user_profile = PlayerProfile(
            honesty=0.62, boldness=0.28, challenge=0.3, memory=0.6
        )
        self.players.append(
            PlayerState(name="You", is_user=True, profile=user_profile, rng=self._rng)
        )

        for index in range(self.difficulty.bot_count):
            base = self.difficulty
            variance = self._rng.uniform(-0.05, 0.05)
            # Each bot inherits the base difficulty personality but receives a
            # small random variance so the table feels less predictable.
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
        """Create a deck composed of multiple standard 52-card decks."""
        cards: list[Card] = []
        for _ in range(deck_count):
            cards.extend(Card(rank, suit) for suit in Suit for rank in RANKS)
        return Deck(cards=cards)

    def _deal_initial_hands(self) -> None:
        """Shuffle the deck and deal cards to all players."""
        deck = self._build_multi_deck(self.difficulty.deck_count)
        deck.shuffle(rng=self._rng)

        # Deal cards one by one to each player
        player_index = 0
        while deck.cards:
            self.players[player_index].hand.append(deck.deal(1)[0])
            player_index = (player_index + 1) % len(self.players)

        # Reset game state for a new round
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
        """The current phase of the game."""
        return self._phase

    @property
    def winner(self) -> PlayerState | None:
        """The winning player, if the game is complete."""
        return self._winner

    @property
    def finished(self) -> bool:
        """True if the game has finished."""
        return self._phase == Phase.COMPLETE

    @property
    def current_player(self) -> PlayerState:
        """The player whose turn it is."""
        return self.players[self._current_player_index]

    @property
    def pile_size(self) -> int:
        """The number of cards in the central pile."""
        return len(self._pile_cards)

    @property
    def claim_in_progress(self) -> Claim | None:
        """The claim that is currently being challenged."""
        return self._claim_in_progress

    @property
    def current_challenger(self) -> PlayerState | None:
        """The player who is next in line to challenge."""
        return self._challenge_queue[0] if self._challenge_queue else None

    def public_state(self) -> Dict[str, object]:
        """Expose a serialisable snapshot of the game state for UIs."""
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
            "claim": (
                None
                if not self._claim_in_progress
                else {
                    "claimant": self._claim_in_progress.claimant.name,
                    "claimed_rank": self._claim_in_progress.claimed_rank,
                    "truthful": self._claim_in_progress.truthful,
                }
            ),
        }

    # ------------------------------------------------------------------
    # Turn handling
    # ------------------------------------------------------------------
    def play_user_turn(self, card_index: int, claimed_rank: str) -> Claim:
        """Process a turn for the human user."""
        player = self.current_player
        if not player.is_user:
            raise RuntimeError("It is not the user's turn.")
        return self._play_turn(player, card_index, claimed_rank)

    def play_bot_turn(self) -> tuple[Claim, list[str]]:
        """Determine and execute a bot's turn based on its AI profile."""
        player = self.current_player
        if player.is_user:
            raise RuntimeError("It is not a bot's turn.")

        hand_counts = player.card_counts()
        truthful_bias = player.profile.honesty

        # If recently caught, a bot becomes more honest
        if (
            player.last_caught_turn is not None
            and self._turns_played - player.last_caught_turn < 3
        ):
            truthful_bias += 0.12

        # Larger piles encourage more daring (less honest) plays
        truthful_bias -= min(
            0.2, len(self._pile_cards) * 0.02 * player.profile.boldness
        )

        # Clamp the bias into a sensible range so pathological bot settings
        # still result in believable behaviour.
        truthful = self._rng.random() < max(0.1, min(0.95, truthful_bias))
        claimed_rank: str
        chosen_card: Card

        if truthful and hand_counts:
            # Play truthfully: choose a rank the bot holds
            ranked = hand_counts.most_common()
            weights = [count for _, count in ranked]
            # Weighted sampling means the bot mirrors human tendencies—more
            # plentiful ranks are more likely to be played when honest.
            chosen_rank = self._rng.choices(
                [rank for rank, _ in ranked], weights=weights
            )[0]
            chosen_card = next(card for card in player.hand if card.rank == chosen_rank)
            claimed_rank = chosen_rank
        else:
            # Bluff: choose a card and claim it's a different rank
            chosen_card = self._rng.choice(player.hand)
            owned_ranks = set(card.rank for card in player.hand)
            bluff_options = [
                rank
                for rank in RANKS
                if rank not in owned_ranks and rank != chosen_card.rank
            ]
            if not bluff_options:
                bluff_options = [rank for rank in RANKS if rank != chosen_card.rank]

            claimed_rank = self._rng.choice(bluff_options)
            truthful = chosen_card.rank == claimed_rank
            if truthful:
                # This was supposed to be a bluff, but we accidentally chose a truthful rank.
                # Nudge it to a different rank to ensure it remains a bluff.
                alternatives = [rank for rank in RANKS if rank != chosen_card.rank]
                claimed_rank = self._rng.choice(alternatives)
                truthful = False

        claim = self._play_turn(player, player.hand.index(chosen_card), claimed_rank)

        if truthful:
            message = f"{player.name} calmly slides a card forward, claiming it is a {claimed_rank}."
        else:
            message = f"{player.name} hesitates before declaring their card to be a {claimed_rank}."
        return claim, [message]

    def _play_turn(
        self, player: PlayerState, card_index: int, claimed_rank: str
    ) -> Claim:
        """Core logic for playing a card and making a claim."""
        if self._phase != Phase.TURN:
            raise RuntimeError("Cannot play a turn while a challenge is unresolved.")
        if not 0 <= card_index < len(player.hand):
            raise ValueError("card_index out of range")
        if claimed_rank not in RANKS:
            raise ValueError("claimed_rank must be a valid rank symbol")

        # Create and record the claim
        card = player.hand.pop(card_index)
        truthful = card.rank == claimed_rank
        player.record_claim(truthful)

        claim = Claim(
            claimant=player, card=card, claimed_rank=claimed_rank, truthful=truthful
        )
        self._claim_in_progress = claim
        self._pile_cards.append(card)
        self._pile_claims.append(claim)

        # Transition to the challenge phase by lining up every other player so
        # they can decide whether to call the claim.
        self._challenge_queue = deque(self._iter_other_players_from(player))
        self._phase = Phase.CHALLENGE

        return claim

    def _iter_other_players_from(self, player: PlayerState) -> List[PlayerState]:
        """Return a list of other players in turn order, starting from the given player."""
        start = self.players.index(player)
        ordering: list[PlayerState] = []
        for offset in range(1, len(self.players)):
            ordering.append(self.players[(start + offset) % len(self.players)])
        return ordering

    # ------------------------------------------------------------------
    # Challenge resolution
    # ------------------------------------------------------------------
    def evaluate_challenge(self, decision: bool) -> ChallengeResult:
        """Evaluate the current player's decision to challenge or not."""
        if self._phase != Phase.CHALLENGE:
            raise RuntimeError("There is no claim waiting to be challenged.")
        if not self._claim_in_progress:
            raise RuntimeError("No active claim is registered.")

        messages: list[str] = []
        if not self._challenge_queue:
            # No one left to challenge; finalize the turn.
            return self._finalise_uncontested()

        # Evaluate challengers in the order they queued up during the turn.
        challenger = self._challenge_queue.popleft()
        if not decision:
            # Player chooses not to challenge
            if challenger.is_user:
                messages.append("You decide to let the claim stand.")
            else:
                messages.append(f"{challenger.name} chooses not to make a scene.")

            if not self._challenge_queue:
                # No one else can challenge, so finalize the turn
                follow_up = self._finalise_uncontested()
                messages.extend(follow_up.messages)
                return ChallengeResult(resolved=True, messages=messages)

            return ChallengeResult(resolved=False, messages=messages)

        # A challenge has been made
        claim = self._claim_in_progress
        # Record the attempt so bot AI can adapt to success/failure later.
        challenger.record_challenge(success=not claim.truthful)
        messages.append(f"{challenger.name} slams a hand down and calls the bluff!")

        if claim.truthful:
            # The claim was true; challenger picks up the pile
            collector = challenger
            # Shuffle the enlarged hand so future draws do not reveal pile order.
            collector.hand.extend(self._pile_cards)
            collector.rng.shuffle(collector.hand)
            self._pile_cards.clear()
            self._pile_claims.clear()
            messages.append(
                f"The card really was a {claim.card.rank}. {collector.name} must scoop up the entire pile."
            )
            result = self._complete_turn(
                challenge_made=True, liar_caught=False, collector=collector
            )
            messages.extend(result.messages)
            return ChallengeResult(resolved=True, messages=messages)
        else:
            # The claim was a bluff; claimant picks up the pile
            collector = claim.claimant
            collector.record_caught(self._turns_played)
            # The claimant inherits every facedown card to keep them honest in
            # future rounds.
            collector.hand.extend(self._pile_cards)
            collector.rng.shuffle(collector.hand)
            self._pile_cards.clear()
            self._pile_claims.clear()
            messages.append(
                f"{claim.claimant.name} was caught! Their card was actually a {claim.card.rank}."
            )
            result = self._complete_turn(
                challenge_made=True, liar_caught=True, collector=collector
            )
            messages.extend(result.messages)
            return ChallengeResult(resolved=True, messages=messages)

    def _finalise_uncontested(self) -> ChallengeResult:
        """Finalize a turn where no one challenged the claim."""
        if not self._claim_in_progress:
            raise RuntimeError("There is no claim to finalise.")

        messages = ["No one dares to challenge. The table tension rises."]
        result = self._complete_turn(
            challenge_made=False, liar_caught=False, collector=None
        )
        messages.extend(result.messages)
        return ChallengeResult(resolved=True, messages=messages)

    def _complete_turn(
        self,
        *,
        challenge_made: bool,
        liar_caught: bool,
        collector: PlayerState | None,
    ) -> ChallengeResult:
        """Finalize the turn, check for a winner, and advance to the next player."""
        assert self._claim_in_progress is not None
        claimant = self._claim_in_progress.claimant
        messages: list[str] = []

        if liar_caught and collector:
            messages.append(
                f"{collector.name} drags the pile back, their hand growing to {len(collector.hand)} cards."
            )
        elif challenge_made and collector:
            messages.append(
                f"{collector.name} adds the pile to their hand, now holding {len(collector.hand)} cards."
            )

        # Reset for the next turn
        self._claim_in_progress = None
        self._challenge_queue.clear()
        self._phase = Phase.TURN
        self._turns_played += 1

        # Check for a winner
        if not claimant.hand:
            self._winner = claimant
            self._phase = Phase.COMPLETE
            messages.append(f"{claimant.name} has shed every card and wins the table!")
            return ChallengeResult(resolved=True, messages=messages)

        # Check if the game should end due to reaching the max turn limit
        if self._turns_played >= self.max_turns:
            messages.extend(self._close_by_card_count())
            return ChallengeResult(resolved=True, messages=messages)

        # Advance to the next player, skipping anyone who just emptied their hand.
        self._current_player_index = (self.players.index(claimant) + 1) % len(
            self.players
        )
        self._advance_to_next_player_with_cards()
        return ChallengeResult(resolved=True, messages=messages)

    def _advance_to_next_player_with_cards(self) -> None:
        """Find the next player in turn order who still has cards to play."""
        start = self._current_player_index
        for offset in range(len(self.players)):
            candidate_index = (start + offset) % len(self.players)
            if self.players[candidate_index].hand:
                self._current_player_index = candidate_index
                return

        # If no players have cards, the game is over.
        self._phase = Phase.COMPLETE

    def _close_by_card_count(self) -> list[str]:
        """End the game and determine the winner by the lowest card count."""
        # Sort players by card count (ascending), with user as tie-breaker
        standings = sorted(self.players, key=lambda p: (len(p.hand), p.is_user))
        best_count = len(standings[0].hand)
        winners = [p for p in standings if len(p.hand) == best_count]

        if len(winners) == 1:
            self._winner = winners[0]
            self._phase = Phase.COMPLETE
            return [
                "Maximum rounds reached.",
                f"{winners[0].name} holds the fewest cards ({best_count}) and is declared the winner.",
            ]

        # Handle a tie
        self._winner = None
        self._phase = Phase.COMPLETE
        # Multiple players share the title, so enumerate them for the match log.
        tied_names = ", ".join(p.name for p in winners)
        return [
            "Maximum rounds reached with a tie.",
            f"Players with the fewest cards ({best_count}): {tied_names}.",
        ]

    # ------------------------------------------------------------------
    # Bot challenge logic
    # ------------------------------------------------------------------
    def bot_should_challenge(self, challenger: PlayerState) -> bool:
        """Determine if a bot should challenge a claim, based on its profile and game state."""
        if not self._claim_in_progress:
            return False

        claim = self._claim_in_progress
        claimant = claim.claimant

        # Base tendency to challenge from profile
        tendency = challenger.profile.challenge

        # Factor in the claimant's history of lying
        history_total = claimant.truths + claimant.lies
        lie_rate = (claimant.lies + 1) / (
            history_total + 2
        )  # +1/+2 to avoid division by zero
        tendency += lie_rate * challenger.profile.memory

        # Adjust based on how recently the claimant was caught
        if claimant.last_caught_turn is not None:
            distance = self._turns_played - claimant.last_caught_turn
            if distance <= 1:
                tendency += 0.25
            elif distance <= 3:
                tendency += 0.1

        # Check if the challenger holds cards of the claimed rank
        owned = challenger.card_counts()[claim.claimed_rank]
        ownership_pressure = 0.0
        if owned >= 3:
            ownership_pressure += 0.25  # High suspicion
        elif owned == 2:
            ownership_pressure += 0.15
        elif owned == 0:
            ownership_pressure -= 0.08  # Lower suspicion

        # The size of the pile can make challenging more tempting
        pile_pressure = min(0.35, len(self._pile_cards) * 0.025)

        tendency += ownership_pressure + pile_pressure
        tendency = max(0.05, min(0.9, tendency))  # Clamp probability

        # Bots with few cards become more cautious to avoid picking up the pile
        if len(challenger.hand) <= 2:
            tendency -= 0.2
        elif len(challenger.hand) >= 10:
            tendency += 0.1

        return challenger.rng.random() < tendency

    # ------------------------------------------------------------------
    # CLI helpers
    # ------------------------------------------------------------------
    def scoreboard(self) -> str:
        """Generate a string with the current game scores and stats."""
        rows = ["Current card counts:"]
        for player in self.players:
            rows.append(
                f"- {player.name}: {len(player.hand)} cards | "
                f"Truths: {player.truths} | Lies: {player.lies} | "
                f"Calls: {player.challenge_successes}/{player.challenge_attempts}"
            )
        rows.append(f"Pile size: {len(self._pile_cards)}")
        rows.append(f"Turn {self._turns_played + 1} of {self.max_turns}")
        return "\n".join(rows)


# ----------------------------------------------------------------------
# CLI orchestration
# ----------------------------------------------------------------------


def parse_arguments(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Return parsed command-line arguments for a Bluff session.

    The CLI supports both human-vs-bot matches and a Tkinter-powered GUI.  This
    helper centralises argument parsing so that :func:`run_cli` and the module's
    ``__main__`` entry point share the exact same behaviour.

    Args:
        argv: Optional sequence of command-line arguments. Passing ``None``
            allows :func:`argparse.ArgumentParser.parse_args` to consume
            arguments directly from :data:`sys.argv`.

    Returns:
        argparse.Namespace: A namespace containing the chosen difficulty,
        number of rounds, optional random seed, and whether the GUI was
        requested.
    """

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
    """Run an interactive Bluff match in the terminal.

    This function wires together :func:`parse_arguments`, the
    :class:`~card_games.bluff.BluffGame` engine, and the text prompts defined
    below.  The implementation doubles as living documentation for the game
    flow—reading the code explains precisely when the player is prompted, how
    challenges are resolved, and under which conditions the match concludes.

    Args:
        argv: Optional command-line arguments to parse. ``None`` means the
            function should read directly from :data:`sys.argv`.
    """

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
            print(
                f"You slide forward {claim.card} and claim it is a {claim.claimed_rank}."
            )
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
                    print(
                        f"{challenger.name} eyes the pile and prepares to challenge..."
                    )
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
    """Prompt the user to select a card index from their hand.

    The helper loops until a valid integer within the bounds of the player's
    hand is supplied. It intentionally avoids raising exceptions so that the
    user receives human-friendly feedback for invalid input.

    Args:
        hand_size: The number of cards currently held by the user.

    Returns:
        int: The zero-based index corresponding to the chosen card.
    """

    while True:
        choice = input("Select the index of the card you want to play: ").strip()
        if choice.isdigit():
            index = int(choice)
            if 0 <= index < hand_size:
                return index
        print("Please enter a valid index from your hand.")


def _prompt_claim_rank(card: Card) -> str:
    """Prompt the user to declare the rank of the card being played.

    For honesty they may repeat the actual rank, but bluffing is as simple as
    naming a different value from :data:`card_games.common.cards.RANKS`.  The
    prompting loop doubles as in-game documentation by reminding the user which
    ranks are legal.

    Args:
        card: The actual card about to be placed on the pile. The card is not
            modified—only its rank is used for the optional prompt text.

    Returns:
        str: A single-character rank chosen from ``RANKS``.
    """

    while True:
        rank = (
            input(
                "Declare your card's rank (e.g. 'A', 'K', '7'). You may bluff by stating a different rank: "
            )
            .strip()
            .upper()
        )
        if rank in RANKS:
            return rank
        print("Unknown rank. Valid options are: " + ", ".join(RANKS))


def _prompt_user_challenge(claimant_name: str, pile_size: int) -> bool:
    """Ask the human player whether they wish to challenge the current claim.

    The decision matters: calling a bluff risks collecting the entire pile if
    the claimant was truthful, but refusing allows the next player in the
    challenge queue to decide.  The function keeps prompting until a recognised
    response is entered, providing in-line documentation for the accepted
    commands (``call``/``trust`` and their short aliases).

    Args:
        claimant_name: The name of the player who made the claim.
        pile_size: The number of facedown cards currently in the pile. This is
            shown to help the user gauge the risk/reward of challenging.

    Returns:
        bool: ``True`` if the user wants to challenge, ``False`` otherwise.
    """

    while True:
        choice = (
            input(
                f"Do you want to challenge {claimant_name}'s claim? (call/trust) [pile has {pile_size} cards]: "
            )
            .strip()
            .lower()
        )
        if choice in {"call", "c"}:
            return True
        if choice in {"trust", "t", "pass", "p"}:
            return False
        print("Please answer with 'call' or 'trust'.")


def main(argv: Iterable[str] | None = None) -> None:  # pragma: no cover - convenience
    run_cli(argv)


if __name__ == "__main__":  # pragma: no cover - script entry point
    main()
