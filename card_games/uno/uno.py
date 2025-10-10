"""Command line and GUI-capable Uno implementation."""

from __future__ import annotations

import argparse
import random
import textwrap
from dataclasses import dataclass
from typing import Iterable, List, Optional, Protocol, Sequence

from colorama import Fore, Style, init as colorama_init

colorama_init(autoreset=True)

COLORS = ("red", "yellow", "green", "blue")
NUMBER_VALUES = tuple(str(n) for n in range(10))
ACTION_VALUES = ("skip", "reverse", "+2")
WILD_VALUES = ("wild", "+4")

COLOR_STYLE_MAP = {
    "red": Fore.RED,
    "yellow": Fore.YELLOW,
    "green": Fore.GREEN,
    "blue": Fore.BLUE,
}


def colorize_color(color: str) -> str:
    color = color.lower()
    style = COLOR_STYLE_MAP.get(color, Fore.WHITE)
    return f"{style}{color.capitalize()}{Style.RESET_ALL}"


def format_card(card: "UnoCard", *, emphasize: bool = False) -> str:
    base = card.label()
    if card.color is None:
        style = Fore.MAGENTA if card.value == "+4" else Fore.WHITE
    else:
        style = COLOR_STYLE_MAP.get(card.color, Fore.WHITE)
    weight = Style.BRIGHT if emphasize else ""
    return f"{weight}{style}{base}{Style.RESET_ALL}"


def format_highlight(message: str, color: str, *, style: str = "") -> str:
    return f"{style}{color}{message}{Style.RESET_ALL}"


def format_section_heading(message: str) -> str:
    return format_highlight(message, Fore.CYAN, style=Style.BRIGHT)


@dataclass(frozen=True)
class UnoCard:
    """Representation of a single Uno card."""

    color: Optional[str]
    value: str

    def is_wild(self) -> bool:
        return self.color is None

    def is_action(self) -> bool:
        return self.value in ACTION_VALUES or self.value in WILD_VALUES

    def matches(self, active_color: str, active_value: str) -> bool:
        if self.is_wild():
            return True
        return self.color == active_color or self.value == active_value

    def label(self) -> str:
        if self.color is None:
            if self.value == "+4":
                return "Wild +4"
            return "Wild"
        color_name = self.color.capitalize()
        if self.value in {"skip", "reverse"}:
            return f"{color_name} {self.value.capitalize()}"
        return f"{color_name} {self.value}"

    def __str__(self) -> str:  # pragma: no cover - simple display helper
        if self.color is None:
            return self.label()
        color_code = self.color[0].upper()
        return f"{color_code}-{self.value.upper()}"


class UnoDeck:
    """Mutable Uno deck that can be shuffled and drawn from."""

    def __init__(self, *, rng: Optional[random.Random] = None) -> None:
        self._rng = rng or random.Random()
        self.cards: List[UnoCard] = []
        self.populate()
        self.shuffle()

    def populate(self) -> None:
        self.cards.clear()
        for color in COLORS:
            self.cards.append(UnoCard(color, "0"))
            for value in NUMBER_VALUES[1:] + ACTION_VALUES:
                self.cards.append(UnoCard(color, value))
                self.cards.append(UnoCard(color, value))
        for _ in range(4):
            self.cards.append(UnoCard(None, "wild"))
            self.cards.append(UnoCard(None, "+4"))

    def shuffle(self) -> None:
        self._rng.shuffle(self.cards)

    def draw(self) -> UnoCard:
        if not self.cards:
            raise RuntimeError("The deck is empty")
        return self.cards.pop()

    def extend(self, cards: Iterable[UnoCard]) -> None:
        self.cards.extend(cards)
        self.shuffle()

    def __len__(self) -> int:  # pragma: no cover - trivial helper
        return len(self.cards)


class UnoPlayer:
    """Representation of a human or bot Uno player."""

    def __init__(self, name: str, *, is_human: bool = False, personality: str = "balanced") -> None:
        self.name = name
        self.is_human = is_human
        self.personality = personality
        self.hand: List[UnoCard] = []
        self.pending_uno = False

    def draw_cards(self, deck: UnoDeck, count: int) -> List[UnoCard]:
        drawn: List[UnoCard] = []
        for _ in range(count):
            drawn_card = deck.draw()
            self.hand.append(drawn_card)
            drawn.append(drawn_card)
        self.pending_uno = False
        return drawn

    def take_card(self, card: UnoCard) -> None:
        self.hand.append(card)
        self.pending_uno = False

    def pop_card(self, index: int) -> UnoCard:
        card = self.hand.pop(index)
        if len(self.hand) != 1:
            self.pending_uno = False
        return card

    def has_cards(self) -> bool:
        return bool(self.hand)

    def playable_cards(
        self,
        active_color: str,
        active_value: str,
        *,
        penalty_value: Optional[str] = None,
    ) -> List[int]:
        if penalty_value == "+2":
            return [index for index, card in enumerate(self.hand) if card.value == "+2"]
        if penalty_value == "+4":
            return [index for index, card in enumerate(self.hand) if card.value == "+4"]
        return [
            index
            for index, card in enumerate(self.hand)
            if card.matches(active_color, active_value)
        ]

    def choose_card(
        self,
        playable: Sequence[int],
        active_color: str,
    ) -> Optional[int]:
        if not playable:
            return None

        def score(card: UnoCard) -> float:
            base = 0.0
            if card.color == active_color:
                base += 2.0
            if card.value in {"skip", "reverse"}:
                base += 1.0
            if card.value == "+2":
                base += 2.5
            if card.value == "+4":
                base += 3.0
            if card.value == "wild":
                base += 1.5
            if card.color:
                color_count = sum(1 for c in self.hand if c.color == card.color)
                base += color_count / 10
            if self.personality == "easy":
                base -= 0.5 if card.is_action() else 0.0
            elif self.personality == "aggressive":
                base += 0.75 if card.is_action() else 0.0
            return base

        best_index = max(playable, key=lambda idx: score(self.hand[idx]))
        return best_index

    def preferred_color(self) -> str:
        color_counts = {color: 0 for color in COLORS}
        for card in self.hand:
            if card.color in color_counts:
                color_counts[card.color] += 1
        max_count = max(color_counts.values()) if color_counts else 0
        top_colors = [color for color, count in color_counts.items() if count == max_count]
        return random.choice(top_colors) if top_colors else random.choice(COLORS)

    def __str__(self) -> str:  # pragma: no cover - simple helper
        return self.name


@dataclass
class PlayerDecision:
    action: str
    card_index: Optional[int] = None
    declare_uno: bool = False
    chosen_color: Optional[str] = None


class UnoInterface(Protocol):
    """Interface abstraction so the game can run in the console or a GUI."""

    def show_heading(self, message: str) -> None:
        ...

    def show_message(self, message: str, *, color: str = Fore.WHITE, style: str = "") -> None:
        ...

    def show_hand(self, player: UnoPlayer, formatted_cards: Sequence[str]) -> None:
        ...

    def choose_action(
        self,
        game: "UnoGame",
        player: UnoPlayer,
        playable: Sequence[int],
        penalty_active: bool,
    ) -> PlayerDecision:
        ...

    def handle_drawn_card(self, game: "UnoGame", player: UnoPlayer, card: UnoCard) -> PlayerDecision:
        ...

    def choose_color(self, player: UnoPlayer) -> str:
        ...

    def prompt_challenge(
        self,
        challenger: UnoPlayer,
        target: UnoPlayer,
        *,
        bluff_possible: bool,
    ) -> bool:
        ...

    def notify_uno_called(self, player: UnoPlayer) -> None:
        ...

    def notify_uno_penalty(self, player: UnoPlayer) -> None:
        ...

    def announce_winner(self, winner: UnoPlayer) -> None:
        ...

    def update_status(self, game: "UnoGame") -> None:
        ...

    def render_card(self, card: UnoCard, *, emphasize: bool = False) -> str:
        ...

    def render_color(self, color: str) -> str:
        ...


class ConsoleUnoInterface(UnoInterface):
    """Console-based interaction helpers."""

    def show_heading(self, message: str) -> None:
        print(format_section_heading(message))

    def show_message(self, message: str, *, color: str = Fore.WHITE, style: str = "") -> None:
        print(format_highlight(message, color, style=style))

    def show_hand(self, player: UnoPlayer, formatted_cards: Sequence[str]) -> None:
        print(format_section_heading("Your hand:"))
        for index, card in enumerate(formatted_cards, start=1):
            print(f"  {index}) {card}")

    def choose_action(
        self,
        game: "UnoGame",
        player: UnoPlayer,
        playable: Sequence[int],
        penalty_active: bool,
    ) -> PlayerDecision:
        while True:
            if penalty_active:
                prompt = (
                    "Stack a penalty card by number or type 'accept' to draw the required cards: "
                )
            elif playable:
                prompt = "Choose card number to play or type 'draw': "
            else:
                prompt = "No playable cards, type 'draw' to draw a card: "
            choice = input(prompt).strip()
            tokens = [token for token in choice.replace("-", " ").split() if token]
            declared_uno = False
            tokens_lower = [token.lower() for token in tokens]
            if "uno" in tokens_lower:
                declared_uno = True
                tokens = [token for token in tokens if token.lower() != "uno"]
                tokens_lower = [token.lower() for token in tokens]
            if not tokens:
                if declared_uno:
                    print("Declare UNO alongside the card number you wish to play.")
                continue
            token = tokens_lower[0]
            if penalty_active and token in {"accept", "draw"}:
                return PlayerDecision(action="accept_penalty")
            if token in {"draw", "d"}:
                return PlayerDecision(action="draw")
            if token.isdigit():
                index = int(token) - 1
                return PlayerDecision(action="play", card_index=index, declare_uno=declared_uno)
            self.show_message("Invalid selection. Try again.", color=Fore.RED)

    def handle_drawn_card(self, game: "UnoGame", player: UnoPlayer, card: UnoCard) -> PlayerDecision:
        if card.matches(game.active_color, game.active_value):
            while True:
                response = (
                    input("Play the drawn card? Enter 'y' to play, 'n' to keep it: ")
                    .strip()
                    .lower()
                )
                if response in {"y", "yes"}:
                    declare = (
                        input("Declare UNO with this play? [y/N]: ").strip().lower()
                        in {"y", "yes"}
                        if len(player.hand) == 2
                        else False
                    )
                    return PlayerDecision(action="play", card_index=len(player.hand) - 1, declare_uno=declare)
                if response in {"n", "no", ""}:
                    break
                self.show_message("Please answer with 'y' or 'n'.", color=Fore.RED)
        return PlayerDecision(action="skip")

    def choose_color(self, player: UnoPlayer) -> str:
        while True:
            choice = input("Choose a color (red, yellow, green, blue): ").strip().lower()
            if choice in COLORS:
                return choice
            self.show_message(
                "Invalid color. Please choose red, yellow, green, or blue.",
                color=Fore.RED,
            )

    def prompt_challenge(
        self,
        challenger: UnoPlayer,
        target: UnoPlayer,
        *,
        bluff_possible: bool,
    ) -> bool:
        if bluff_possible:
            prompt = f"{challenger.name}, challenge {target.name}'s +4? [y/N]: "
        else:
            prompt = f"{challenger.name}, challenge {target.name}'s +4? (unlikely to help) [y/N]: "
        response = input(prompt).strip().lower()
        return response in {"y", "yes"}

    def notify_uno_called(self, player: UnoPlayer) -> None:
        self.show_message(
            f"{player.name} calls UNO!",
            color=Fore.CYAN,
            style=Style.BRIGHT,
        )

    def notify_uno_penalty(self, player: UnoPlayer) -> None:
        self.show_message(
            f"{player.name} failed to call UNO and must draw two cards!",
            color=Fore.RED,
            style=Style.BRIGHT,
        )

    def announce_winner(self, winner: UnoPlayer) -> None:
        if winner.is_human:
            self.show_message(
                f"\n{winner.name} wins the game! Congratulations!",
                color=Fore.CYAN,
                style=Style.BRIGHT,
            )
        else:
            self.show_message(
                f"\n{winner.name} wins the game! Better luck next time.",
                color=Fore.CYAN,
                style=Style.BRIGHT,
            )

    def update_status(self, game: "UnoGame") -> None:
        # The console interface updates inline as events occur.
        return None

    def render_card(self, card: UnoCard, *, emphasize: bool = False) -> str:
        return format_card(card, emphasize=emphasize)

    def render_color(self, color: str) -> str:
        return colorize_color(color)


class UnoGame:
    """Manage and play an Uno game."""

    def __init__(
        self,
        *,
        players: Sequence[UnoPlayer],
        rng: Optional[random.Random] = None,
        interface: Optional[UnoInterface] = None,
    ) -> None:
        if len(players) < 2:
            raise ValueError("Uno requires at least two players")
        self.players: List[UnoPlayer] = list(players)
        self.rng = rng or random.Random()
        self.deck = UnoDeck(rng=self.rng)
        self.discard_pile: List[UnoCard] = []
        self.current_index = 0
        self.direction = 1
        self.active_color = ""
        self.active_value = ""
        self.penalty_value: Optional[str] = None
        self.penalty_amount = 0
        self.plus4_challenge: Optional[dict] = None
        self.interface = interface or ConsoleUnoInterface()
        self.event_log: List[tuple[str, str, str]] = []

    def setup(self, *, starting_hand: int = 7) -> None:
        for player in self.players:
            player.hand.clear()
            player.pending_uno = False
            player.draw_cards(self.deck, starting_hand)
        first_card = self._draw_start_card()
        self.discard_pile.append(first_card)
        self.active_color = first_card.color or self.rng.choice(COLORS)
        self.active_value = first_card.value
        skip_next = False
        if first_card.value in {"skip", "reverse"}:
            skip_next = self._apply_action_card(first_card, initializing=True)
        elif first_card.value in {"+2", "+4"}:
            self.penalty_value = first_card.value
            self.penalty_amount = 2 if first_card.value == "+2" else 4
            if first_card.value == "+4":
                self.plus4_challenge = {
                    "player": None,
                    "illegal": False,
                }
        if skip_next:
            self.current_index = self._next_index(1)
        self.interface.update_status(self)

    def _draw_start_card(self) -> UnoCard:
        while True:
            card = self.deck.draw()
            if card.value in {"wild", "+4"}:
                return card
            return card

    def _reshuffle_if_needed(self) -> None:
        if self.deck.cards:
            return
        if len(self.discard_pile) <= 1:
            raise RuntimeError("No cards left to reshuffle into the deck")
        top = self.discard_pile[-1]
        rest = self.discard_pile[:-1]
        self.discard_pile = [top]
        self.deck.extend(rest)

    def _next_index(self, steps: int = 1) -> int:
        total = len(self.players)
        return (self.current_index + steps * self.direction) % total

    def _advance_turn(self, *, skip_next: bool = False) -> None:
        step = 1 + (1 if skip_next else 0)
        self.current_index = self._next_index(step)

    def _apply_action_card(
        self,
        card: UnoCard,
        *,
        player: Optional[UnoPlayer] = None,
        initializing: bool = False,
        illegal_plus4: bool = False,
    ) -> bool:
        skip_next = False
        if card.value == "skip" and not initializing:
            self.penalty_value = None
            self.penalty_amount = 0
            self.plus4_challenge = None
            actor = player.name if player else "A player"
            self._log(f"{actor} skips the next player!", Fore.MAGENTA)
            skip_next = True
        elif card.value == "reverse":
            self.penalty_value = None
            self.penalty_amount = 0
            self.plus4_challenge = None
            self.direction *= -1
            direction_label = "clockwise" if self.direction == 1 else "counter-clockwise"
            self._log(
                f"Play order reverses and is now {direction_label}!",
                Fore.MAGENTA,
            )
            if len(self.players) == 2 and not initializing:
                skip_next = True
        elif card.value == "+2":
            self.penalty_value = "+2"
            self.penalty_amount += 2
            self.plus4_challenge = None
        elif card.value == "+4":
            self.penalty_value = "+4"
            self.penalty_amount += 4
            self.plus4_challenge = {
                "player": player,
                "illegal": illegal_plus4,
            }
        else:
            self.penalty_value = None
            self.penalty_amount = 0
            self.plus4_challenge = None
        return skip_next

    def _draw_cards(self, player: UnoPlayer, count: int) -> List[UnoCard]:
        drawn: List[UnoCard] = []
        for _ in range(count):
            self._reshuffle_if_needed()
            card = self.deck.draw()
            player.take_card(card)
            drawn.append(card)
        self.interface.update_status(self)
        return drawn

    def _log(self, message: str, color: str = Fore.WHITE, *, style: str = "") -> None:
        self.event_log.append((message, color, style))
        self.interface.show_message(message, color=color, style=style)

    def _render_hand(self, player: UnoPlayer) -> List[str]:
        return [self.interface.render_card(card) for card in player.hand]

    def _has_color_match(self, player: UnoPlayer, color: str, *, ignore_index: Optional[int] = None) -> bool:
        for index, card in enumerate(player.hand):
            if ignore_index is not None and index == ignore_index:
                continue
            if card.color == color:
                return True
        return False

    def _check_uno_penalties(self, current_player: UnoPlayer) -> None:
        for player in self.players:
            if player is current_player:
                continue
            if player.pending_uno and len(player.hand) == 1:
                self.interface.notify_uno_penalty(player)
                self._draw_cards(player, 2)
                player.pending_uno = False

    def _resolve_plus4_challenge(self, challenger: UnoPlayer) -> bool:
        if not self.plus4_challenge or self.penalty_value != "+4":
            return False
        target = self.plus4_challenge["player"]
        illegal = self.plus4_challenge["illegal"]
        if target is None:
            # Opening +4 cannot be challenged.
            return False
        should_challenge = (
            self.interface.prompt_challenge(
                challenger,
                target,
                bluff_possible=illegal,
            )
            if challenger.is_human
            else self._bot_should_challenge(challenger)
        )
        if not should_challenge:
            return False
        if illegal:
            self._log(
                f"{challenger.name} challenges successfully! {target.name} draws four cards.",
                Fore.MAGENTA,
                style=Style.BRIGHT,
            )
            self._draw_cards(target, 4)
            self.penalty_value = None
            self.penalty_amount = 0
            self.plus4_challenge = None
            self.interface.update_status(self)
            return True
        self._log(
            f"{challenger.name} challenges incorrectly and must draw six cards!",
            Fore.RED,
            style=Style.BRIGHT,
        )
        self._draw_cards(challenger, 6)
        self.penalty_value = None
        self.penalty_amount = 0
        self.plus4_challenge = None
        self._advance_turn()
        return True

    def _bot_should_challenge(self, challenger: UnoPlayer) -> bool:
        if self.plus4_challenge is None:
            return False
        illegal = self.plus4_challenge["illegal"]
        if challenger.personality == "aggressive":
            threshold = 0.4
        elif challenger.personality == "easy":
            threshold = 0.15
        else:
            threshold = 0.25
        modifier = 0.3 if illegal else -0.05
        return self.rng.random() < max(0.0, min(0.95, threshold + modifier))

    def _accept_penalty(self, player: UnoPlayer) -> None:
        if self.penalty_amount == 0:
            return
        penalty_desc = "+4" if self.penalty_value == "+4" else "+2"
        self._log(
            f"{player.name} draws {self.penalty_amount} cards from a {penalty_desc} stack.",
            Fore.YELLOW,
        )
        self._draw_cards(player, self.penalty_amount)
        self.penalty_amount = 0
        self.penalty_value = None
        self.plus4_challenge = None
        self._advance_turn()

    def _execute_play(
        self,
        player: UnoPlayer,
        card_index: int,
        *,
        declare_uno: bool = False,
        chosen_color: Optional[str] = None,
    ) -> Optional[UnoPlayer]:
        card = player.hand[card_index]
        illegal_plus4 = False
        if card.value == "+4" and self.active_color:
            illegal_plus4 = self._has_color_match(player, self.active_color, ignore_index=card_index)
        card = player.pop_card(card_index)
        self.discard_pile.append(card)
        previous_color = self.active_color
        self.active_value = card.value
        if card.color:
            self.active_color = card.color
        if card.color is None:
            chosen_color = chosen_color or (
                self.interface.choose_color(player)
                if player.is_human
                else player.preferred_color()
            )
            self.active_color = chosen_color
            self._log(
                f"Active color is now {self.interface.render_color(self.active_color)}.",
                Fore.CYAN,
            )
        if card.value in {"skip", "reverse", "+2", "+4"}:
            skip_next = self._apply_action_card(
                card,
                player=player,
                illegal_plus4=illegal_plus4,
            )
        else:
            skip_next = False
            self.penalty_value = None
            self.penalty_amount = 0
            self.plus4_challenge = None
        if card.color is None and card.value == "+4" and previous_color:
            self._log(
                f"{player.name} plays {self.interface.render_card(card)} and changes color to {self.interface.render_color(self.active_color)}.",
                Fore.GREEN,
            )
        else:
            self._log(
                f"{player.name} plays {self.interface.render_card(card)}.",
                Fore.GREEN,
            )
        if not player.has_cards():
            self.interface.announce_winner(player)
            return player
        if len(player.hand) == 1:
            if declare_uno or not player.is_human:
                player.pending_uno = False
                self.interface.notify_uno_called(player)
            else:
                player.pending_uno = True
        else:
            player.pending_uno = False
        self.interface.update_status(self)
        self._advance_turn(skip_next=skip_next)
        return None

    def _bot_take_turn(self, player: UnoPlayer, playable: Sequence[int], penalty_active: bool) -> Optional[UnoPlayer]:
        if self.penalty_value == "+4" and self.plus4_challenge:
            if self._resolve_plus4_challenge(player):
                return None
        if penalty_active and not playable:
            self._accept_penalty(player)
            return None
        if playable:
            chosen_index = player.choose_card(playable, self.active_color)
            declare = len(player.hand) == 2
            return self._execute_play(player, chosen_index, declare_uno=declare)
        drawn_card = self._draw_cards(player, 1)[0]
        self._log(f"{player.name} draws a card.", Fore.YELLOW)
        if drawn_card.matches(self.active_color, self.active_value):
            should_play = True
            if drawn_card.value in {"wild", "+4"}:
                should_play = True
            elif drawn_card.value in {"skip", "reverse", "+2"}:
                should_play = player.personality != "easy"
            else:
                should_play = True
            if should_play:
                index = len(player.hand) - 1
                declare = len(player.hand) == 1
                return self._execute_play(player, index, declare_uno=declare)
        self._advance_turn()
        return None

    def play(self) -> UnoPlayer:
        """Run the main game loop. Returns the winner."""

        while True:
            player = self.players[self.current_index]
            self._check_uno_penalties(player)
            top_card = self.discard_pile[-1]
            heading = (
                "Top card: "
                + self.interface.render_card(top_card, emphasize=True)
                + " | Active color: "
                + self.interface.render_color(self.active_color)
            )
            self.interface.show_heading(heading)
            if self.penalty_amount:
                self._log(
                    f"Pending penalty: draw {self.penalty_amount} (must stack {self.penalty_value}).",
                    Fore.YELLOW,
                )
            playable = player.playable_cards(
                self.active_color, self.active_value, penalty_value=self.penalty_value
            )
            penalty_active = self.penalty_amount > 0
            if player.is_human:
                self.interface.show_hand(player, self._render_hand(player))
                if self.penalty_value == "+4" and self.plus4_challenge and self.penalty_amount:
                    if self._resolve_plus4_challenge(player):
                        if self.penalty_value is None:
                            continue
                        else:
                            # Turn advanced during failed challenge.
                            continue
                while True:
                    decision = self.interface.choose_action(
                        self, player, playable, penalty_active
                    )
                    if penalty_active and not playable and decision.action != "accept_penalty":
                        self._log(
                            "You must accept the penalty since you cannot stack a matching card.",
                            Fore.RED,
                        )
                        continue
                    if decision.action == "accept_penalty":
                        self._accept_penalty(player)
                        break
                    if decision.action == "draw":
                        drawn_card = self._draw_cards(player, 1)[0]
                        self._log(
                            f"You drew {self.interface.render_card(drawn_card, emphasize=True)}.",
                            Fore.GREEN,
                        )
                        if drawn_card.matches(self.active_color, self.active_value):
                            follow_up = self.interface.handle_drawn_card(
                                self, player, drawn_card
                            )
                            if follow_up.action == "play":
                                result = self._execute_play(
                                    player,
                                    follow_up.card_index or (len(player.hand) - 1),
                                    declare_uno=follow_up.declare_uno,
                                    chosen_color=follow_up.chosen_color,
                                )
                                if result:
                                    return result
                                break
                        self._advance_turn()
                        break
                    if decision.action == "play" and decision.card_index is not None:
                        if decision.card_index < 0 or decision.card_index >= len(player.hand):
                            self._log("That card number is out of range.", Fore.RED)
                            continue
                        if decision.card_index not in playable:
                            self._log(
                                "You cannot play that card right now.",
                                Fore.RED,
                            )
                            continue
                        card = player.hand[decision.card_index]
                        chosen_color = decision.chosen_color
                        if card.color is None and chosen_color is None:
                            chosen_color = self.interface.choose_color(player)
                        result = self._execute_play(
                            player,
                            decision.card_index,
                            declare_uno=decision.declare_uno,
                            chosen_color=chosen_color,
                        )
                        if result:
                            return result
                        break
                    self._log("Invalid action. Try again.", Fore.RED)
                else:
                    continue
            else:
                result = self._bot_take_turn(player, playable, penalty_active)
                if result:
                    return result
                continue

    def interface_summary(self) -> List[str]:
        return [f"{p.name}: {len(p.hand)} cards" for p in self.players]


def build_players(total: int, *, bots: int, bot_skill: str) -> List[UnoPlayer]:
    if total < 2:
        raise ValueError("At least two players are required")
    if bots > total - 1:
        raise ValueError("Number of bots cannot exceed total players minus one human")
    players: List[UnoPlayer] = []
    players.append(UnoPlayer("You", is_human=True))
    bot_names = ["Watson", "SkyNet", "Hal", "Cortana", "Jarvis", "GLaDOS"]
    for index in range(bots):
        name = bot_names[index % len(bot_names)]
        players.append(UnoPlayer(name, personality=bot_skill))
    while len(players) < total:
        name = bot_names[len(players) % len(bot_names)]
        players.append(UnoPlayer(name, personality=bot_skill))
    return players


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Play a round of Uno against computer opponents.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """
            Controls:
              • Enter the card number from your hand to play it (include 'UNO' in the same line to declare UNO).
              • Type 'draw' to draw a card when you have no playable options or prefer not to play.
              • After drawing a playable card you may immediately play it by answering 'y'.
              • When playing a wild card choose the new color when prompted.
              • Type 'accept' when under a +2/+4 penalty to draw the required number of cards.
            """
        ),
    )
    parser.add_argument("--players", type=int, default=4, help="Total number of players (2-6).")
    parser.add_argument(
        "--bots",
        type=int,
        default=3,
        help="Number of computer opponents (defaults to 3).",
    )
    parser.add_argument(
        "--bot-skill",
        choices=["easy", "balanced", "aggressive"],
        default="balanced",
        help="Bot personality which influences how aggressively they play action cards.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for reproducible shuffles and bot decisions.",
    )
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Launch the graphical interface instead of the console version.",
    )
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> None:
    args = parse_args(argv)
    total_players = max(2, min(6, args.players))
    bots = max(1, min(total_players - 1, args.bots))
    if args.gui:
        try:
            from .gui import launch_uno_gui
        except Exception as exc:  # pragma: no cover - runtime import handling
            raise SystemExit(f"GUI launch failed: {exc}")
        launch_uno_gui(total_players, bots=bots, bot_skill=args.bot_skill, seed=args.seed)
        return
    rng = random.Random(args.seed)
    players = build_players(total_players, bots=bots, bot_skill=args.bot_skill)
    game = UnoGame(players=players, rng=rng)
    game.setup()
    winner = game.play()
    if winner.is_human:
        print("Congratulations! You outplayed the bots.")
    else:
        print("Better luck next time.")


__all__ = [
    "UnoCard",
    "UnoDeck",
    "UnoGame",
    "ConsoleUnoInterface",
    "PlayerDecision",
    "build_players",
    "main",
]
