"""Core engine for a Texas Hold'em poker game.

This module provides the main classes and logic for running a game of Texas Hold'em,
including the game state management, player actions, bot AI, and hand evaluation.
It is designed to be used by different front-ends, such as a CLI or a GUI.

Key components:
- ``ActionType``, ``Action``: Represent player decisions (fold, check, bet, etc.).
- ``Player``: Stores the state of a single player (chips, cards, status).
- ``BotSkill``, ``PokerBot``: Define the AI for computer-controlled players.
- ``PokerTable``: Manages the state of a single hand, including betting rounds,
  community cards, and pot management.
- ``PokerMatch``: Orchestrates a series of hands between a user and bot opponents.
- ``estimate_win_rate``: A Monte Carlo simulation to estimate a hand's equity.
"""

from __future__ import annotations

import argparse
import itertools
import random
from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable, Sequence

from ..common.cards import Card, Deck, format_cards
from .poker_core import HandRank, best_hand


class ActionType(str, Enum):
    """Enumeration of the types of actions a player can take during a betting round."""

    FOLD = "fold"
    CHECK = "check"
    CALL = "call"
    BET = "bet"
    RAISE = "raise"
    ALL_IN = "all-in"


@dataclass(frozen=True)
class Action:
    """Represents a single betting decision made by a player.

    Attributes:
        kind (ActionType): The type of action taken.
        target_bet (int): The total amount the player is betting or raising to.
    """

    kind: ActionType
    target_bet: int = 0


@dataclass
class Player:
    """Represents a single player at the poker table.

    This class stores all state related to a player, including their name, chip stack,
    hole cards, and their status within the current hand (e.g., folded, all-in).
    """

    name: str
    chips: int = 1_000
    is_user: bool = False
    hole_cards: list[Card] = field(default_factory=list)
    folded: bool = False
    all_in: bool = False
    current_bet: int = 0
    total_invested: int = 0
    last_action: str = "waiting"
    last_wager: int = 0

    def reset_for_hand(self) -> None:
        """Resets the player's state for the start of a new hand."""
        self.hole_cards.clear()
        self.folded = False
        self.all_in = False
        self.current_bet = 0
        self.total_invested = 0
        self.last_action = "waiting"
        self.last_wager = 0

    def receive_cards(self, cards: Iterable[Card]) -> None:
        """Adds cards to the player's hand."""
        self.hole_cards.extend(cards)

    def __str__(self) -> str:  # pragma: no cover - debug helper
        return f"{self.name} ({self.chips} chips)"


@dataclass(frozen=True)
class BotSkill:
    """Defines the personality and skill level of a poker bot.

    These parameters control the bot's decision-making process, such as how
    often it bluffs, how aggressively it bets, and how accurately it assesses
    its hand strength.
    """

    name: str
    tightness: float  # How selective the bot is with starting hands.
    aggression: float  # How often the bot bets or raises with strong hands.
    bluff: float  # How often the bot bluffs.
    mistake_rate: float  # The probability of making a random, unoptimal move.
    simulations: (
        int  # The number of Monte Carlo simulations to run for equity estimation.
    )


# A pre-shuffled, full deck of cards for use in simulations.
FULL_DECK: tuple[Card, ...] = tuple(Deck().cards)


def fresh_deck(rng: random.Random | None = None) -> Deck:
    """Creates and shuffles a new deck of cards."""
    deck = Deck()
    deck.shuffle(rng=rng)
    return deck


# Pre-defined difficulty levels for the poker bots.
DIFFICULTIES: dict[str, BotSkill] = {
    "Noob": BotSkill(
        "Noob",
        tightness=0.32,
        aggression=0.10,
        bluff=0.30,
        mistake_rate=0.25,
        simulations=80,
    ),
    "Easy": BotSkill(
        "Easy",
        tightness=0.37,
        aggression=0.16,
        bluff=0.26,
        mistake_rate=0.18,
        simulations=120,
    ),
    "Medium": BotSkill(
        "Medium",
        tightness=0.43,
        aggression=0.22,
        bluff=0.22,
        mistake_rate=0.12,
        simulations=160,
    ),
    "Hard": BotSkill(
        "Hard",
        tightness=0.48,
        aggression=0.3,
        bluff=0.18,
        mistake_rate=0.07,
        simulations=220,
    ),
    "Insane": BotSkill(
        "Insane",
        tightness=0.54,
        aggression=0.42,
        bluff=0.14,
        mistake_rate=0.03,
        simulations=320,
    ),
}


class PokerBot:
    """An AI decision engine for a non-user poker player.

    This class uses the player's ``BotSkill`` profile and a Monte Carlo
    simulation (`estimate_win_rate`) to choose an appropriate action in a given
    game state.
    """

    def __init__(self, player: Player, skill: BotSkill, rng: random.Random) -> None:
        self.player = player
        self.skill = skill
        self.rng = rng

    def decide(self, table: "PokerTable") -> Action:
        """Chooses an action for the bot based on its skill and the current table state."""
        stage = table.stage
        player = self.player
        to_call = table.current_bet - player.current_bet

        if player.chips == 0:
            return Action(ActionType.CHECK)

        # Estimate the probability of winning the hand.
        win_rate = estimate_win_rate(
            hero=player,
            players=[p for p in table.players if not p.folded],
            community_cards=table.community_cards,
            simulations=self.skill.simulations,
            rng=self.rng,
        )

        # Occasionally make a random mistake to simulate human-like imperfection.
        if self.rng.random() < self.skill.mistake_rate:
            return self._random_legal_action(table, to_call)

        # Adjust strategy based on the current stage of the hand.
        stage_adjustment = {
            "pre-flop": -0.08,
            "flop": 0.0,
            "turn": 0.04,
            "river": 0.08,
        }[stage]
        call_threshold = max(0.08, self.skill.tightness + stage_adjustment)
        strong_threshold = min(0.95, call_threshold + 0.25)

        # If there is no bet to call (the bot can check).
        if to_call == 0:
            if (
                win_rate >= strong_threshold
                and player.chips > 0
                and self.rng.random() < self.skill.aggression
            ):
                target = self._bet_target(table, pot_factor=0.65)
                return Action(ActionType.BET, target_bet=target)
            if win_rate >= call_threshold or self.rng.random() < self.skill.bluff:
                return Action(ActionType.CHECK)
            if player.chips > 0:
                target = self._bet_target(table, pot_factor=0.35)
                return Action(ActionType.BET, target_bet=target)
            return Action(ActionType.CHECK)

        # If facing a bet.
        call_amount = min(to_call, player.chips)
        pot_odds = call_amount / max(table.pot + call_amount, 1)

        # Fold if hand is weak and pot odds are not favorable.
        if (
            win_rate < call_threshold
            and win_rate < pot_odds
            and self.rng.random() > self.skill.bluff
        ):
            return Action(ActionType.FOLD)

        # Raise if hand is very strong.
        if (
            win_rate >= strong_threshold
            and player.chips > call_amount
            and self.rng.random() < self.skill.aggression
        ):
            target = self._raise_target(table, pot_factor=0.8)
            return Action(ActionType.RAISE, target_bet=target)

        if call_amount >= player.chips:
            return Action(
                ActionType.ALL_IN, target_bet=player.current_bet + player.chips
            )

        return Action(ActionType.CALL, target_bet=table.current_bet)

    def _bet_target(self, table: "PokerTable", *, pot_factor: float) -> int:
        """Calculate a target bet size, typically a fraction of the pot."""
        min_total = max(table.min_raise_amount, table.big_blind)
        pot_sized = max(min_total, int((table.pot or table.big_blind) * pot_factor))
        return self.player.current_bet + min(self.player.chips, pot_sized)

    def _raise_target(self, table: "PokerTable", *, pot_factor: float) -> int:
        """Calculate a target raise size."""
        increment = max(
            table.min_raise_amount, int((table.pot or table.big_blind) * pot_factor)
        )
        target = max(
            table.current_bet + increment, table.current_bet + table.min_raise_amount
        )
        target = min(self.player.current_bet + self.player.chips, target)
        return (
            target
            if target > self.player.current_bet
            else self.player.current_bet + self.player.chips
        )

    def _random_legal_action(self, table: "PokerTable", to_call: int) -> Action:
        """Return a randomly chosen legal action, used to simulate mistakes."""
        player = self.player
        options: list[Action] = []
        if to_call == 0:
            options.append(Action(ActionType.CHECK))
            if player.chips > 0:
                target = player.current_bet + min(
                    player.chips, max(table.big_blind, table.min_raise_amount)
                )
                options.append(Action(ActionType.BET, target))
        else:
            options.append(Action(ActionType.CALL, table.current_bet))
            options.append(Action(ActionType.FOLD))
            if (
                player.chips + player.current_bet
                > table.current_bet + table.min_raise_amount
            ):
                target = self._raise_target(
                    table, pot_factor=self.rng.uniform(0.2, 0.8)
                )
                options.append(Action(ActionType.RAISE, target))
            else:
                options.append(
                    Action(ActionType.ALL_IN, player.current_bet + player.chips)
                )
        return self.rng.choice(options)


class PokerTable:
    """Manages the state and progression of a single Texas Hold'em hand.

    This class handles the core game flow, including dealing cards, managing betting
    rounds, posting blinds, and distributing the pot.
    """

    def __init__(
        self,
        players: Sequence[Player],
        *,
        small_blind: int = 10,
        big_blind: int = 20,
        rng: random.Random | None = None,
    ) -> None:
        if len(players) < 2:
            raise ValueError("At least two players are required")
        self.players = list(players)
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.rng = rng or random.Random()
        self.deck: Deck = fresh_deck(self.rng)
        self.community_cards: list[Card] = []
        self.pot: int = 0
        self.dealer_index = 0
        self.current_player_index = 0
        self.stage: str = "pre-flop"
        self.current_bet: int = 0
        self.min_raise_amount: int = self.big_blind
        self.last_actions: list[str] = []
        self._players_who_acted: set[int] = set()

    def rotate_dealer(self) -> None:
        """Moves the dealer button to the next player."""
        self.dealer_index = (self.dealer_index + 1) % len(self.players)

    def start_hand(self) -> None:
        """Resets the table and player states to begin a new hand."""
        for player in self.players:
            player.reset_for_hand()

        self.deck = fresh_deck(self.rng)
        self.community_cards.clear()
        self.pot = 0
        self.stage = "pre-flop"
        self.current_bet = 0
        self.min_raise_amount = self.big_blind
        self._players_who_acted.clear()
        self.last_actions.clear()

        # Deal hole cards to each player.
        for player in self.players:
            player.receive_cards(self.deck.deal(2))

        # Players with no chips are marked as folded.
        for player in self.players:
            if player.chips == 0:
                player.folded = True
                player.all_in = True

        self._post_blinds()
        self.current_player_index = self._first_to_act_index()

    def _post_blinds(self) -> None:
        """Posts the small and big blinds."""
        sb_index = (self.dealer_index + 1) % len(self.players)
        bb_index = (self.dealer_index + 2) % len(self.players)
        sb_player = self.players[sb_index]
        bb_player = self.players[bb_index]
        self._commit(
            sb_player, sb_player.current_bet + min(self.small_blind, sb_player.chips)
        )
        self._commit(
            bb_player, bb_player.current_bet + min(self.big_blind, bb_player.chips)
        )
        self.current_bet = bb_player.current_bet
        self.min_raise_amount = self.big_blind
        self._players_who_acted = set()

    def _first_to_act_index(self) -> int:
        """Determines the index of the player who acts first in a betting round."""
        index = (self.dealer_index + 3) % len(self.players)  # UTG position
        return self._next_index(index - 1)

    def _next_index(self, start: int) -> int:
        """Finds the index of the next active player."""
        index = (start + 1) % len(self.players)
        for _ in range(len(self.players)):
            player = self.players[index]
            if not player.folded and not player.all_in:
                return index
            index = (index + 1) % len(self.players)
        return index

    def _commit(self, player: Player, target_bet: int) -> None:
        """Commits a player's chips to the pot up to the target amount."""
        amount_to_add = max(0, target_bet - player.current_bet)
        if amount_to_add == 0:
            return

        contribution = min(amount_to_add, player.chips)
        player.chips -= contribution
        player.current_bet += contribution
        player.total_invested += contribution
        self.pot += contribution
        if player.chips == 0:
            player.all_in = True

    def valid_actions(self, player: Player) -> list[ActionType]:
        """Returns a list of legal actions for the given player."""
        to_call = self.current_bet - player.current_bet
        options: list[ActionType] = []
        if to_call <= 0:
            options.append(ActionType.CHECK)
            if player.chips > 0:
                options.append(ActionType.BET)
        else:
            options.append(ActionType.FOLD)
            options.append(ActionType.CALL)
            if player.chips + player.current_bet > self.current_bet:
                options.append(ActionType.RAISE)
            if player.chips > 0:
                options.append(ActionType.ALL_IN)
        return options

    def apply_action(self, player: Player, action: Action) -> None:
        """Applies a player's action and updates the game state."""
        to_call = self.current_bet - player.current_bet
        previous_high = self.current_bet

        if action.kind is ActionType.FOLD:
            player.folded = True
            player.last_action = "fold"
            player.last_wager = 0
        elif action.kind is ActionType.CHECK:
            if to_call > 0:
                raise ValueError("Cannot check when facing a bet")
            player.last_action = "check"
            player.last_wager = 0
        else:
            # Handle bet, raise, call, all-in
            target = min(action.target_bet, player.current_bet + player.chips)

            before_bet = player.current_bet
            if action.kind is ActionType.CALL:
                target = self.current_bet
            elif action.kind is ActionType.BET:
                if to_call > 0:
                    raise ValueError(
                        "Cannot bet when facing a wager; must call or raise"
                    )
                min_total = player.current_bet + max(
                    self.min_raise_amount, self.big_blind
                )
                target = max(target, min_total)
            elif action.kind is ActionType.RAISE:
                if to_call <= 0:
                    raise ValueError("Cannot raise without a bet to match")
                min_total = self.current_bet + self.min_raise_amount
                target = max(target, min_total)
            elif action.kind is ActionType.ALL_IN:
                target = player.current_bet + player.chips

            self._commit(player, target)
            player.last_action = action.kind.value
            player.last_wager = player.current_bet - before_bet

            # If the bet was a raise, update the minimum raise amount.
            if player.current_bet > previous_high:
                raise_size = player.current_bet - previous_high
                if previous_high == 0:
                    self.min_raise_amount = max(raise_size, self.big_blind)
                elif raise_size >= self.min_raise_amount or player.all_in:
                    if not player.all_in:
                        self.min_raise_amount = raise_size
                else:
                    raise ValueError("Raise did not meet minimum size")
                self.current_bet = player.current_bet
                self._players_who_acted = {id(player)}

        self._players_who_acted.add(id(player))
        self.last_actions.append(
            f"{player.name} {action.kind.value}{self._action_suffix(player)}"
        )

        # Advance to the next player if the round is not over.
        if self._active_player_count() > 1 and self.players_can_act():
            self.current_player_index = self._next_index(self.current_player_index)

    def _action_suffix(self, player: Player) -> str:
        """Generates a descriptive suffix for an action, e.g., ' (100 chips)'."""
        if (
            player.folded
            or player.last_action == "check"
            or player.last_action == "fold"
        ):
            return ""
        if player.last_action == ActionType.CALL.value:
            return f" ({player.last_wager} chips)"
        if player.last_action == ActionType.ALL_IN.value:
            return f" for {player.current_bet} total"
        if player.last_action in {ActionType.RAISE.value, ActionType.BET.value}:
            return f" to {player.current_bet}"
        return ""

    def betting_round_complete(self) -> bool:
        """Checks if the current betting round is complete."""
        if self._active_player_count() <= 1:
            return True

        for player in self.players:
            if player.folded or player.all_in:
                continue
            if player.current_bet != self.current_bet:
                return False
            if id(player) not in self._players_who_acted:
                return False
        return True

    def proceed_to_next_stage(self) -> None:
        """Advances the game to the next stage (flop, turn, river)."""
        # Reset bets for the new round.
        for player in self.players:
            player.current_bet = 0
        self.current_bet = 0
        self.min_raise_amount = self.big_blind
        self._players_who_acted = set()

        if self.stage == "pre-flop":
            self._burn()
            self.community_cards.extend(self.deck.deal(3))
            self.stage = "flop"
        elif self.stage == "flop":
            self._burn()
            self.community_cards.extend(self.deck.deal(1))
            self.stage = "turn"
        elif self.stage == "turn":
            self._burn()
            self.community_cards.extend(self.deck.deal(1))
            self.stage = "river"
        else:
            raise RuntimeError("No further stage to proceed to")

        self.current_player_index = self._next_index(self.dealer_index)

    def showdown(self) -> list[tuple[Player, HandRank]]:
        """Determines the winner(s) at the end of a hand by comparing hand ranks."""
        contenders = [player for player in self.players if not player.folded]
        rankings = [
            (player, best_hand(player.hole_cards + self.community_cards))
            for player in contenders
        ]
        rankings.sort(key=lambda item: item[1], reverse=True)
        return rankings

    def distribute_pot(self) -> dict[str, int]:
        """Distributes the pot to the winner(s), handling side pots correctly."""
        payouts = {player.name: 0 for player in self.players}

        # If only one player remains, they win the whole pot.
        if self._active_player_count() == 1:
            winner = next(player for player in self.players if not player.folded)
            winner.chips += self.pot
            payouts[winner.name] = self.pot
            self.pot = 0
            return payouts

        # Handle side pots by processing contributions at different levels.
        contributions = sorted(
            {p.total_invested for p in self.players if p.total_invested > 0}
        )
        previous_level = 0
        remaining_pot = self.pot

        for level in contributions:
            eligible = [p for p in self.players if p.total_invested >= level]
            slice_amount = min((level - previous_level) * len(eligible), remaining_pot)
            if slice_amount <= 0:
                continue

            contenders = [p for p in eligible if not p.folded]
            if contenders:
                ranked_contenders = [
                    (p, best_hand(p.hole_cards + self.community_cards))
                    for p in contenders
                ]
                best_rank = max(rank for _, rank in ranked_contenders)
                winners = [p for p, rank in ranked_contenders if rank == best_rank]
            else:
                winners = eligible

            # Distribute the side pot among the winners.
            share = slice_amount // len(winners)
            for player in winners:
                player.chips += share
                payouts[player.name] += share

            # Distribute any remainder chips.
            for i, player in enumerate(winners[: slice_amount % len(winners)]):
                player.chips += 1
                payouts[player.name] += 1

            remaining_pot -= slice_amount
            previous_level = level

        if remaining_pot > 0:
            # Any leftover chips go to the player with the largest stack.
            richest = max(self.players, key=lambda p: p.chips)
            richest.chips += remaining_pot
            payouts[richest.name] += remaining_pot

        self.pot = 0
        for player in self.players:
            player.total_invested = 0
        return payouts

    def _burn(self) -> None:
        """Discards one card from the deck before dealing community cards."""
        self.deck.deal(1)

    def _active_player_count(self) -> int:
        """Returns the number of players who have not folded."""
        return sum(1 for player in self.players if not player.folded)

    def players_can_act(self) -> bool:
        """Checks if there are any players who can still make a move."""
        return any(not player.folded and not player.all_in for player in self.players)


def estimate_win_rate(
    *,
    hero: Player,
    players: Sequence[Player],
    community_cards: Sequence[Card],
    simulations: int,
    rng: random.Random,
) -> float:
    """Estimates the probability of a player winning using Monte Carlo simulation.

    This function simulates the remainder of the hand many times to estimate the
    hero's equity (win rate) against their opponents.

    Args:
        hero: The player whose win rate is being estimated.
        players: All active players at the table.
        community_cards: The cards currently on the board.
        simulations: The number of simulations to run.
        rng: The random number generator to use.

    Returns:
        The estimated win rate as a float between 0.0 and 1.0.
    """
    active_opponents = [p for p in players if p is not hero and not p.folded]
    if not active_opponents:
        return 1.0

    known_cards = set(hero.hole_cards) | set(community_cards)
    deck_pool = [card for card in FULL_DECK if card not in known_cards]
    wins = 0
    ties = 0

    needed_board = 5 - len(community_cards)
    opponent_count = len(active_opponents)

    for _ in range(max(simulations, 1)):
        rng.shuffle(deck_pool)
        iterator = iter(deck_pool)
        opponent_holes = [
            list(itertools.islice(iterator, 2)) for _ in range(opponent_count)
        ]
        board_completion = list(community_cards) + list(
            itertools.islice(iterator, needed_board)
        )

        hero_rank = best_hand(hero.hole_cards + board_completion)
        opponent_ranks = [best_hand(hole + board_completion) for hole in opponent_holes]
        best_opponent = max(opponent_ranks)

        if hero_rank > best_opponent:
            wins += 1
        elif hero_rank == best_opponent:
            ties += 1

    return (wins + ties / 2) / max(simulations, 1)


@dataclass
class MatchResult:
    """A data class to store the results of a completed poker hand."""

    stage: str
    community_cards: list[Card]
    showdown: list[tuple[str, HandRank]]
    payouts: dict[str, int]
    log: list[str]


class PokerMatch:
    """A high-level controller that manages a series of poker hands.

    This class orchestrates the entire match, from initialization to playing
    multiple hands and tracking player chip counts over time.
    """

    def __init__(
        self,
        difficulty: BotSkill,
        *,
        rounds: int = 3,
        starting_chips: int = 1_000,
        rng: random.Random | None = None,
    ) -> None:
        if rounds <= 0:
            raise ValueError("rounds must be a positive integer")
        self.difficulty = difficulty
        self.rounds = rounds
        self.rng = rng or random.Random()
        self.user = Player(name="You", is_user=True, chips=starting_chips)
        self.bots = [
            Player(name=f"{difficulty.name} Bot {i+1}", chips=starting_chips)
            for i in range(3)
        ]
        self.players = [self.user, *self.bots]
        self.table = PokerTable(self.players, rng=self.rng)
        self.bot_controllers = [
            PokerBot(bot, difficulty, self.rng) for bot in self.bots
        ]
        self.hand_number = 0

    def reset(self) -> None:
        """Resets the match to its initial state."""
        for player in self.players:
            player.chips = max(player.chips, 0)
        self.table.dealer_index = 0
        self.hand_number = 0

    def play_cli(self) -> None:
        """Runs the poker match using the command-line interface."""
        print(
            f"Welcome to Texas Hold'em! Playing {self.rounds} hands against {len(self.bots)} {self.difficulty.name} bots."
        )
        print()

        for round_num in range(1, self.rounds + 1):
            if self.user.chips <= 0:
                print("You are out of chips. Match over.")
                break
            if all(bot.chips <= 0 for bot in self.bots):
                print("All opponents are out of chips. You win!")
                break

            print(f"=== Hand {round_num} ===")
            result = self.play_hand_cli()
            self._display_hand_result(result)
            print(self._stack_summary())
            print()
            self.table.rotate_dealer()

        print("Match complete! Final chip counts:")
        print(self._stack_summary())

    def play_hand_cli(self) -> MatchResult:
        """Plays a single hand of poker in the CLI."""
        table = self.table
        table.start_hand()
        table.last_actions.clear()
        log: list[str] = []

        print(f"Your hole cards: {format_cards(self.user.hole_cards)}")

        while True:
            player = table.players[table.current_player_index]

            # Check if betting round or hand is over.
            if not table.players_can_act() or table._active_player_count() <= 1:
                log.extend(table.last_actions)
                if table.stage != "river" and table._active_player_count() > 1:
                    table.proceed_to_next_stage()
                    print(f"Board: {format_cards(table.community_cards)}")
                    continue
                break

            # Get action from user or bot.
            if player.is_user and not player.folded and not player.all_in:
                action = self._prompt_user_action(table, player)
            elif player.folded or player.all_in:
                table.current_player_index = table._next_index(
                    table.current_player_index
                )
                continue
            else:
                controller = next(c for c in self.bot_controllers if c.player is player)
                action = controller.decide(table)

            table.apply_action(player, action)
            print(table.last_actions[-1])

            # If betting round is complete, advance to the next stage.
            if table.betting_round_complete():
                log.extend(table.last_actions)
                table.last_actions.clear()
                if table.stage == "river":
                    break
                table.proceed_to_next_stage()
                if table.stage != "pre-flop":
                    print(f"Board: {format_cards(table.community_cards)}")

        # Determine winner and distribute pot.
        showdown = []
        if table._active_player_count() == 1:
            payouts = table.distribute_pot()
        else:
            rankings = table.showdown()
            for p, rank in rankings:
                print(f"{p.name}: {format_cards(p.hole_cards)} -> {rank.describe()}")
            payouts = table.distribute_pot()
            showdown = [(p.name, rank) for p, rank in rankings]

        return MatchResult(
            table.stage, list(table.community_cards), showdown, payouts, log
        )

    def _prompt_user_action(self, table: PokerTable, player: Player) -> Action:
        """Prompts the user for an action and returns the chosen action."""
        to_call = table.current_bet - player.current_bet
        print(f"Pot: {table.pot} | To call: {to_call} | Stack: {player.chips}")
        if table.community_cards:
            print(f"Board: {format_cards(table.community_cards)}")

        options = table.valid_actions(player)
        prompt_parts = [
            opt.value
            for opt in options
            if opt not in {ActionType.BET, ActionType.RAISE}
        ]
        if ActionType.BET in options or ActionType.RAISE in options:
            prompt_parts.append("bet/raise <amount>")

        while True:
            choice = (
                input(f"Choose action [{', '.join(prompt_parts)}]: ").strip().lower()
            )
            parts = choice.split()
            command = parts[0]

            if command in {"check", "c"} and ActionType.CHECK in options:
                return Action(ActionType.CHECK)
            if command in {"fold", "f"} and ActionType.FOLD in options:
                return Action(ActionType.FOLD)
            if command == "call" and ActionType.CALL in options:
                return Action(ActionType.CALL, target_bet=table.current_bet)
            if command in {"all-in", "allin", "a"} and ActionType.ALL_IN in options:
                return Action(ActionType.ALL_IN)

            if command == "bet" and ActionType.BET in options:
                amount = self._parse_amount(
                    parts[1] if len(parts) > 1 else "", default=table.big_blind
                )
                return Action(ActionType.BET, target_bet=player.current_bet + amount)
            if command == "raise" and ActionType.RAISE in options:
                amount = self._parse_amount(
                    parts[1] if len(parts) > 1 else "", default=table.min_raise_amount
                )
                return Action(ActionType.RAISE, target_bet=table.current_bet + amount)

            print("Invalid action. Please choose from the available options.")

    @staticmethod
    def _parse_amount(raw: str, *, default: int) -> int:
        """Parses a string into a valid bet/raise amount."""
        try:
            return max(default, int(raw.strip())) if raw.strip() else default
        except ValueError as exc:
            raise ValueError("Invalid amount specified") from exc

    def _display_hand_result(self, result: MatchResult) -> None:
        """Prints the results of a completed hand."""
        for name, payout in result.payouts.items():
            if payout > 0:
                print(f"{name} wins {payout} chips.")

    def _stack_summary(self) -> str:
        """Returns a string summarizing the current chip stacks of all players."""
        return "Chip stacks:\n" + "\n".join(
            f"  {p.name}: {p.chips}" for p in self.players
        )


def parse_arguments(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parses command-line arguments for the poker application."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--difficulty",
        choices=DIFFICULTIES.keys(),
        default="Noob",
        help="Bot skill level.",
    )
    parser.add_argument(
        "--rounds", type=int, default=3, help="Number of hands to play."
    )
    parser.add_argument(
        "--seed", type=int, help="Optional random seed for deterministic play."
    )
    parser.add_argument(
        "--gui", action="store_true", help="Launch the graphical interface."
    )
    return parser.parse_args(argv)


def run_cli(argv: Sequence[str] | None = None) -> None:
    """Runs the command-line interface for the poker match."""
    args = parse_arguments(argv)
    rng = random.Random(args.seed) if args.seed is not None else random.Random()
    difficulty = DIFFICULTIES[args.difficulty]
    match = PokerMatch(difficulty, rounds=args.rounds, rng=rng)

    if getattr(args, "gui", False):
        from .gui import launch_gui

        launch_gui(match, rng=rng)
    else:
        match.play_cli()


def main() -> None:  # pragma: no cover - convenience wrapper
    run_cli()


__all__ = [
    "Action",
    "ActionType",
    "BotSkill",
    "DIFFICULTIES",
    "MatchResult",
    "Player",
    "PokerMatch",
    "PokerTable",
    "estimate_win_rate",
    "parse_arguments",
    "run_cli",
]
