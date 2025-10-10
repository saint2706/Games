"""Modern Texas hold'em engine with both CLI and GUI front-ends."""

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
    """Enumeration of player actions available during betting."""

    FOLD = "fold"
    CHECK = "check"
    CALL = "call"
    BET = "bet"
    RAISE = "raise"
    ALL_IN = "all-in"


@dataclass(frozen=True)
class Action:
    """Representation of a betting decision."""

    kind: ActionType
    target_bet: int = 0


@dataclass
class Player:
    """Representation of a player seated at the table."""

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
        self.hole_cards.clear()
        self.folded = False
        self.all_in = False
        self.current_bet = 0
        self.total_invested = 0
        self.last_action = "waiting"
        self.last_wager = 0

    def receive_cards(self, cards: Iterable[Card]) -> None:
        self.hole_cards.extend(cards)

    def __str__(self) -> str:  # pragma: no cover - debug helper
        return f"{self.name} ({self.chips} chips)"


@dataclass(frozen=True)
class BotSkill:
    """Tuning parameters that describe how confidently a bot plays."""

    name: str
    tightness: float
    aggression: float
    bluff: float
    mistake_rate: float
    simulations: int


FULL_DECK: tuple[Card, ...] = tuple(Deck().cards)


def fresh_deck(rng: random.Random | None = None) -> Deck:
    deck = Deck()
    deck.shuffle(rng=rng)
    return deck


DIFFICULTIES: dict[str, BotSkill] = {
    "Noob": BotSkill("Noob", tightness=0.32, aggression=0.10, bluff=0.30, mistake_rate=0.25, simulations=80),
    "Easy": BotSkill("Easy", tightness=0.37, aggression=0.16, bluff=0.26, mistake_rate=0.18, simulations=120),
    "Medium": BotSkill("Medium", tightness=0.43, aggression=0.22, bluff=0.22, mistake_rate=0.12, simulations=160),
    "Hard": BotSkill("Hard", tightness=0.48, aggression=0.3, bluff=0.18, mistake_rate=0.07, simulations=220),
    "Insane": BotSkill("Insane", tightness=0.54, aggression=0.42, bluff=0.14, mistake_rate=0.03, simulations=320),
}


class PokerBot:
    """Decision engine that picks an action for a non-user player."""

    def __init__(self, player: Player, skill: BotSkill, rng: random.Random) -> None:
        self.player = player
        self.skill = skill
        self.rng = rng

    def decide(self, table: "PokerTable") -> Action:
        stage = table.stage
        player = self.player
        to_call = table.current_bet - player.current_bet

        if player.chips == 0:
            return Action(ActionType.CHECK)

        win_rate = estimate_win_rate(
            hero=player,
            players=[p for p in table.players if not p.folded],
            community_cards=table.community_cards,
            simulations=self.skill.simulations,
            rng=self.rng,
        )

        if self.rng.random() < self.skill.mistake_rate:
            return self._random_legal_action(table, to_call)

        stage_adjustment = {
            "pre-flop": -0.08,
            "flop": 0.0,
            "turn": 0.04,
            "river": 0.08,
        }[stage]

        call_threshold = max(0.08, self.skill.tightness + stage_adjustment)
        strong_threshold = min(0.95, call_threshold + 0.25)

        if to_call == 0:
            if win_rate >= strong_threshold and player.chips > 0:
                if self.rng.random() < self.skill.aggression:
                    target = self._bet_target(table, pot_factor=0.65)
                    return Action(ActionType.BET, target_bet=target)
            if win_rate >= call_threshold or self.rng.random() < self.skill.bluff:
                return Action(ActionType.CHECK)
            if player.chips > 0:
                target = self._bet_target(table, pot_factor=0.35)
                return Action(ActionType.BET, target_bet=target)
            return Action(ActionType.CHECK)

        # Facing a bet
        call_amount = min(to_call, player.chips)
        pot_odds = call_amount / max(table.pot + call_amount, 1)

        if win_rate < call_threshold and win_rate < pot_odds and self.rng.random() > self.skill.bluff:
            return Action(ActionType.FOLD)

        if win_rate >= strong_threshold and player.chips > call_amount and self.rng.random() < self.skill.aggression:
            target = self._raise_target(table, pot_factor=0.8)
            return Action(ActionType.RAISE, target_bet=target)

        if call_amount >= player.chips:
            return Action(ActionType.ALL_IN, target_bet=player.current_bet + player.chips)

        return Action(ActionType.CALL, target_bet=table.current_bet)

    def _bet_target(self, table: "PokerTable", *, pot_factor: float) -> int:
        min_total = max(table.min_raise_amount, table.big_blind)
        pot_sized = max(min_total, int((table.pot or table.big_blind) * pot_factor))
        target = self.player.current_bet + min(self.player.chips, pot_sized)
        return target

    def _raise_target(self, table: "PokerTable", *, pot_factor: float) -> int:
        increment = max(table.min_raise_amount, int((table.pot or table.big_blind) * pot_factor))
        target = max(table.current_bet + increment, table.current_bet + table.min_raise_amount)
        target = min(self.player.current_bet + self.player.chips, target)
        if target <= self.player.current_bet:
            return self.player.current_bet + self.player.chips
        return target

    def _random_legal_action(self, table: "PokerTable", to_call: int) -> Action:
        player = self.player
        options: list[Action] = []
        if to_call == 0:
            options.append(Action(ActionType.CHECK))
            if player.chips > 0:
                target = player.current_bet + min(player.chips, max(table.big_blind, table.min_raise_amount))
                options.append(Action(ActionType.BET, target))
        else:
            options.append(Action(ActionType.CALL, table.current_bet))
            options.append(Action(ActionType.FOLD))
            if player.chips + player.current_bet > table.current_bet + table.min_raise_amount:
                target = self._raise_target(table, pot_factor=self.rng.uniform(0.2, 0.8))
                options.append(Action(ActionType.RAISE, target))
            else:
                options.append(Action(ActionType.ALL_IN, player.current_bet + player.chips))
        return self.rng.choice(options)


class PokerTable:
    """Stateful representation of a single Texas hold'em hand."""

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
        self.dealer_index = (self.dealer_index + 1) % len(self.players)

    def start_hand(self) -> None:
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

        for player in self.players:
            player.receive_cards(self.deck.deal(2))

        for player in self.players:
            if player.chips == 0:
                player.folded = True
                player.all_in = True

        self._post_blinds()
        self.current_player_index = self._first_to_act_index()

    def _post_blinds(self) -> None:
        sb_index = (self.dealer_index + 1) % len(self.players)
        bb_index = (self.dealer_index + 2) % len(self.players)
        sb_player = self.players[sb_index]
        bb_player = self.players[bb_index]
        self._commit(sb_player, sb_player.current_bet + min(self.small_blind, sb_player.chips))
        self._commit(bb_player, bb_player.current_bet + min(self.big_blind, bb_player.chips))
        self.current_bet = bb_player.current_bet
        self.min_raise_amount = self.big_blind
        self._players_who_acted = set()

    def _first_to_act_index(self) -> int:
        index = (self.dealer_index + 3) % len(self.players)
        return self._next_index(index - 1)

    def _next_index(self, start: int) -> int:
        index = (start + 1) % len(self.players)
        visited = 0
        while visited < len(self.players):
            player = self.players[index]
            if not player.folded and not player.all_in:
                return index
            index = (index + 1) % len(self.players)
            visited += 1
        return index

    def _commit(self, player: Player, target_bet: int) -> None:
        amount = max(0, target_bet - player.current_bet)
        if amount == 0:
            return
        contribution = min(amount, player.chips)
        player.chips -= contribution
        player.current_bet += contribution
        player.total_invested += contribution
        self.pot += contribution
        if player.chips == 0:
            player.all_in = True

    def valid_actions(self, player: Player) -> list[ActionType]:
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
            target = action.target_bet
            if target < player.current_bet:
                raise ValueError("Target bet cannot decrease commitment")
            if target > player.current_bet + player.chips:
                target = player.current_bet + player.chips

            before_bet = player.current_bet
            if action.kind is ActionType.CALL:
                if target != self.current_bet:
                    target = self.current_bet
            elif action.kind is ActionType.BET:
                if to_call > 0:
                    raise ValueError("Cannot bet when facing a wager; must call or raise")
                min_total = player.current_bet + max(self.min_raise_amount, self.big_blind)
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

        if action.kind in {ActionType.FOLD, ActionType.CHECK, ActionType.CALL, ActionType.ALL_IN}:
            self._players_who_acted.add(id(player))

        self.last_actions.append(f"{player.name} {action.kind.value}{self._action_suffix(player, previous_high)}")

        if self._active_player_count() <= 1:
            return
        if not self.players_can_act():
            return

        self.current_player_index = self._next_index(self.current_player_index)

    def _action_suffix(self, player: Player, previous_high: int) -> str:
        if player.folded:
            return ""
        if player.last_action == "check":
            return ""
        if player.last_action == "fold":
            return ""
        if player.last_action == ActionType.CALL.value:
            return f" ({player.last_wager} chips)"
        if player.last_action == ActionType.ALL_IN.value:
            return f" for {player.current_bet} total"
        if player.last_action in {ActionType.RAISE.value, ActionType.BET.value}:
            return f" to {player.current_bet}"
        return ""

    def betting_round_complete(self) -> bool:
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
        contenders = [player for player in self.players if not player.folded]
        rankings = [(player, best_hand(player.hole_cards + self.community_cards)) for player in contenders]
        rankings.sort(key=lambda item: item[1], reverse=True)
        return rankings

    def distribute_pot(self) -> dict[str, int]:
        payouts = {player.name: 0 for player in self.players}
        if self._active_player_count() == 1:
            winner = next(player for player in self.players if not player.folded)
            winner.chips += self.pot
            payouts[winner.name] = self.pot
            self.pot = 0
            return payouts

        contributions = sorted({player.total_invested for player in self.players if player.total_invested > 0})
        previous_level = 0
        remaining_pot = self.pot
        for level in contributions:
            eligible = [player for player in self.players if player.total_invested >= level]
            slice_amount = (level - previous_level) * len(eligible)
            slice_amount = min(slice_amount, remaining_pot)
            if slice_amount <= 0:
                continue
            contenders = [player for player in eligible if not player.folded]
            if contenders:
                ranked_contenders = [
                    (player, best_hand(player.hole_cards + self.community_cards))
                    for player in contenders
                ]
                best_rank = max(rank for _, rank in ranked_contenders)
                winners = [player for player, rank in ranked_contenders if rank == best_rank]
            else:
                winners = eligible
            share = slice_amount // len(winners)
            remainder = slice_amount % len(winners)
            for player in winners:
                player.chips += share
                payouts[player.name] += share
            for index, player in enumerate(winners[:remainder]):
                player.chips += 1
                payouts[player.name] += 1
            remaining_pot -= slice_amount
            previous_level = level

        if remaining_pot:
            richest = max(self.players, key=lambda p: p.chips)
            richest.chips += remaining_pot
            payouts[richest.name] += remaining_pot
        self.pot = 0
        for player in self.players:
            player.total_invested = 0
        return payouts

    def _burn(self) -> None:
        self.deck.deal(1)

    def _active_player_count(self) -> int:
        return sum(1 for player in self.players if not player.folded)

    def players_can_act(self) -> bool:
        return any(not player.folded and not player.all_in for player in self.players)


def estimate_win_rate(
    *,
    hero: Player,
    players: Sequence[Player],
    community_cards: Sequence[Card],
    simulations: int,
    rng: random.Random,
) -> float:
    """Monte Carlo estimate of the hero's equity against the table."""

    active_opponents = [player for player in players if player is not hero and not player.folded]
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
        opponent_holes = [list(itertools.islice(iterator, 2)) for _ in range(opponent_count)]
        board_completion = list(community_cards) + list(itertools.islice(iterator, needed_board))

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
    """Summary of a completed hand."""

    stage: str
    community_cards: list[Card]
    showdown: list[tuple[str, HandRank]]
    payouts: dict[str, int]
    log: list[str]


class PokerMatch:
    """High level controller that manages multiple hands."""

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
        self.bots = [Player(name=f"{difficulty.name} Bot {index+1}", chips=starting_chips) for index in range(3)]
        self.players = [self.user, *self.bots]
        self.table = PokerTable(self.players, rng=self.rng)
        self.bot_controllers = [PokerBot(bot, difficulty, self.rng) for bot in self.bots]
        self.hand_number = 0

    def reset(self) -> None:
        for player in self.players:
            player.chips = max(player.chips, 0)
        self.table.dealer_index = 0
        self.hand_number = 0

    def play_cli(self) -> None:
        print(
            "Welcome to a fully interactive table of Texas hold'em!",
            f"You're playing {self.rounds} hand{'s' if self.rounds != 1 else ''} against three {self.difficulty.name} bots.",
        )
        print()

        for round_number in range(1, self.rounds + 1):
            if self.user.chips <= 0:
                print("You are out of chips. Match ends early.")
                break
            if all(bot.chips <= 0 for bot in self.bots):
                print("All opponents are broke. Congratulations!")
                break
            print(f"=== Hand {round_number} ===")
            result = self.play_hand_cli()
            self._display_hand_result(result)
            print(self._stack_summary())
            print()
            self.table.rotate_dealer()

        print("Match complete! Final chip counts:")
        print(self._stack_summary())

    def play_hand_cli(self) -> MatchResult:
        table = self.table
        table.start_hand()
        table.last_actions.clear()
        log: list[str] = []

        print(f"Your hole cards: {format_cards(self.user.hole_cards)}")

        while True:
            player = table.players[table.current_player_index]
            if not table.players_can_act():
                log.extend(table.last_actions)
                table.last_actions.clear()
                if table.stage != "river":
                    table.proceed_to_next_stage()
                    print(f"Board: {format_cards(table.community_cards)}")
                    continue
                break
            if table._active_player_count() <= 1:
                log.extend(table.last_actions)
                break

            if player.is_user and not player.folded and not player.all_in:
                action = self._prompt_user_action(table, player)
            elif player.folded or player.all_in:
                table.current_player_index = table._next_index(table.current_player_index)
                continue
            else:
                controller = self.bot_controllers[self.bots.index(player)]
                action = controller.decide(table)

            table.apply_action(player, action)
            print(table.last_actions[-1])

            if table.betting_round_complete():
                log.extend(table.last_actions)
                table.last_actions.clear()
                if table.stage == "river":
                    break
                table.proceed_to_next_stage()
                if table.stage != "pre-flop":
                    print(f"Board: {format_cards(table.community_cards)}")

        if table._active_player_count() == 1:
            payouts = table.distribute_pot()
            showdown: list[tuple[str, HandRank]] = []
        else:
            rankings = table.showdown()
            for player, rank in rankings:
                print(f"{player.name}: {format_cards(player.hole_cards)} -> {rank.describe()}")
            payouts = table.distribute_pot()
            showdown = [(player.name, rank) for player, rank in rankings]

        return MatchResult(
            stage=table.stage,
            community_cards=list(table.community_cards),
            showdown=showdown,
            payouts=payouts,
            log=log,
        )

    def _prompt_user_action(self, table: PokerTable, player: Player) -> Action:
        to_call = table.current_bet - player.current_bet
        print(f"Pot: {table.pot} | To call: {to_call} | Stack: {player.chips}")
        if table.community_cards:
            print(f"Board: {format_cards(table.community_cards)}")
        options = table.valid_actions(player)
        prompt_parts = []
        if ActionType.CHECK in options:
            prompt_parts.append("check")
        if ActionType.CALL in options:
            call_amount = min(to_call, player.chips)
            prompt_parts.append(f"call ({call_amount})")
        if ActionType.BET in options or ActionType.RAISE in options:
            prompt_parts.append("bet <amount>")
            prompt_parts.append("raise <amount>")
        if ActionType.ALL_IN in options:
            prompt_parts.append("all-in")
        if ActionType.FOLD in options:
            prompt_parts.append("fold")

        while True:
            choice = input(f"Choose action [{', '.join(prompt_parts)}]: ").strip().lower()
            if choice in {"check", "c"} and ActionType.CHECK in options:
                return Action(ActionType.CHECK)
            if choice in {"fold", "f"} and ActionType.FOLD in options:
                return Action(ActionType.FOLD)
            if choice in {"call"} and ActionType.CALL in options:
                return Action(ActionType.CALL, target_bet=table.current_bet)
            if choice in {"all-in", "allin", "a"} and ActionType.ALL_IN in options:
                return Action(ActionType.ALL_IN, target_bet=player.current_bet + player.chips)
            if choice.startswith("bet") and ActionType.BET in options:
                amount = self._parse_amount(choice[3:], default=table.min_raise_amount)
                target = player.current_bet + max(amount, table.min_raise_amount)
                return Action(ActionType.BET, target_bet=target)
            if choice.startswith("raise") and ActionType.RAISE in options:
                amount = self._parse_amount(choice[5:], default=table.min_raise_amount)
                target = table.current_bet + max(amount, table.min_raise_amount)
                return Action(ActionType.RAISE, target_bet=target)
            if choice.startswith("call") and ActionType.CALL in options:
                return Action(ActionType.CALL, target_bet=table.current_bet)
            print("Invalid response. Please choose a legal action.")

    @staticmethod
    def _parse_amount(raw: str, *, default: int) -> int:
        try:
            raw = raw.strip()
            if not raw:
                return default
            return max(default, int(raw))
        except ValueError as exc:
            raise ValueError("Invalid wager amount") from exc

    def _display_hand_result(self, result: MatchResult) -> None:
        for name, payout in result.payouts.items():
            if payout:
                print(f"{name} wins {payout} chips")

    def _stack_summary(self) -> str:
        lines = ["Chip stacks:"]
        for player in self.players:
            lines.append(f"  {player.name}: {player.chips}")
        return "\n".join(lines)


def parse_arguments(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--difficulty",
        choices=DIFFICULTIES.keys(),
        default="Noob",
        help="Bot skill level to face.",
    )
    parser.add_argument(
        "--rounds",
        type=int,
        default=3,
        help="Number of hands to play (default: 3)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Optional random seed for deterministic play",
    )
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Launch the graphical interface instead of the CLI",
    )
    return parser.parse_args(argv)


def run_cli(argv: Sequence[str] | None = None) -> None:
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

