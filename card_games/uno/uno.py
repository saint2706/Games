"""Command line Uno implementation inspired by the original project."""

from __future__ import annotations

import argparse
import random
import textwrap
from dataclasses import dataclass
from typing import Iterable, List, Optional, Sequence

COLORS = ("red", "yellow", "green", "blue")
NUMBER_VALUES = tuple(str(n) for n in range(10))
ACTION_VALUES = ("skip", "reverse", "+2")
WILD_VALUES = ("wild", "+4")


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
            # One zero per color
            self.cards.append(UnoCard(color, "0"))
            # Two of each number 1-9 and action card per color
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

    def draw_cards(self, deck: UnoDeck, count: int) -> List[UnoCard]:
        drawn: List[UnoCard] = []
        for _ in range(count):
            drawn.append(deck.draw())
            self.hand.append(drawn[-1])
        return drawn

    def take_card(self, card: UnoCard) -> None:
        self.hand.append(card)

    def remove_card(self, card: UnoCard) -> None:
        self.hand.remove(card)

    def has_cards(self) -> bool:
        return bool(self.hand)

    def playable_cards(
        self,
        active_color: str,
        active_value: str,
        *,
        penalty_value: Optional[str] = None,
    ) -> List[UnoCard]:
        """Return the cards that may legally be played."""

        if penalty_value == "+2":
            return [card for card in self.hand if card.value == "+2"]
        if penalty_value == "+4":
            return [card for card in self.hand if card.value == "+4"]
        return [card for card in self.hand if card.matches(active_color, active_value)]

    def choose_card(
        self,
        playable: Sequence[UnoCard],
        active_color: str,
    ) -> Optional[UnoCard]:
        if not playable:
            return None
        if self.is_human:
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

        best = max(playable, key=score)
        return best

    def preferred_color(self) -> str:
        color_counts = {color: 0 for color in COLORS}
        for card in self.hand:
            if card.color in color_counts:
                color_counts[card.color] += 1
        max_count = max(color_counts.values())
        top_colors = [color for color, count in color_counts.items() if count == max_count]
        return random.choice(top_colors) if top_colors else random.choice(COLORS)

    def __str__(self) -> str:  # pragma: no cover - simple helper
        return self.name


class UnoGame:
    """Manage and play an Uno game."""

    def __init__(
        self,
        *,
        players: Sequence[UnoPlayer],
        rng: Optional[random.Random] = None,
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

    def setup(self, *, starting_hand: int = 7) -> None:
        for player in self.players:
            player.hand.clear()
            player.draw_cards(self.deck, starting_hand)
        first_card = self._draw_start_card()
        self.discard_pile.append(first_card)
        self.active_color = first_card.color or self.rng.choice(COLORS)
        self.active_value = first_card.value
        skip_next = False
        if first_card.value in {"skip", "reverse"}:
            skip_next = self._apply_action_card(first_card)
        elif first_card.value in {"+2", "+4"}:
            self.penalty_value = first_card.value
            self.penalty_amount = 2 if first_card.value == "+2" else 4
        if skip_next:
            self.current_index = self._next_index(1)

    def _draw_start_card(self) -> UnoCard:
        while True:
            card = self.deck.draw()
            if card.value in {"wild", "+4"}:
                # Wild starts are legal but we need an active color.
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
    ) -> bool:
        """Apply the effects of an action card.

        Returns ``True`` when the next player should be skipped because of the
        effect (skip card or reverse in a two-player match).
        """

        skip_next = False
        if card.value == "skip" and not initializing:
            self.penalty_value = None
            self.penalty_amount = 0
            actor = player.name if player else "A player"
            print(f"{actor} skips the next player!")
            skip_next = True
        elif card.value == "reverse":
            self.penalty_value = None
            self.penalty_amount = 0
            self.direction *= -1
            direction_label = "clockwise" if self.direction == 1 else "counter-clockwise"
            print(f"Play order reverses and is now {direction_label}!")
            if len(self.players) == 2 and not initializing:
                skip_next = True
        elif card.value == "+2":
            self.penalty_value = "+2"
            self.penalty_amount += 2
        elif card.value == "+4":
            self.penalty_value = "+4"
            self.penalty_amount += 4
        return skip_next

    def _play_card(self, player: UnoPlayer, card: UnoCard, chosen_color: Optional[str] = None) -> None:
        player.remove_card(card)
        self.discard_pile.append(card)
        self.active_value = card.value
        if card.color:
            self.active_color = card.color
        if card.color is None:
            self.active_color = chosen_color or player.preferred_color()
            print(f"Active color is now {self.active_color.capitalize()}.")
        skip_next = False
        if card.value in {"skip", "reverse", "+2", "+4"}:
            skip_next = self._apply_action_card(card, player=player)
        else:
            self.penalty_value = None
            self.penalty_amount = 0
        return skip_next

    def _handle_draw_penalty(self, player: UnoPlayer) -> bool:
        if self.penalty_amount == 0:
            return False
        playable = player.playable_cards(self.active_color, self.active_value, penalty_value=self.penalty_value)
        if playable:
            return False
        print(
            f"{player.name} must draw {self.penalty_amount} cards due to a {self.penalty_value}."
        )
        self._draw_cards(player, self.penalty_amount)
        self.penalty_amount = 0
        self.penalty_value = None
        self._advance_turn()
        return True

    def _draw_cards(self, player: UnoPlayer, count: int) -> List[UnoCard]:
        drawn: List[UnoCard] = []
        for _ in range(count):
            self._reshuffle_if_needed()
            card = self.deck.draw()
            player.take_card(card)
            drawn.append(card)
        return drawn

    def _display_hand(self, player: UnoPlayer) -> None:
        print("Your hand:")
        for index, card in enumerate(player.hand, start=1):
            print(f"  {index}) {card.label()}")

    def play(self) -> UnoPlayer:
        """Run the main game loop. Returns the winner."""

        while True:
            player = self.players[self.current_index]
            print("\n" + "-" * 60)
            print(
                f"Top card: {self.discard_pile[-1].label()} | Active color: {self.active_color.capitalize()}"
            )
            if self.penalty_amount:
                print(
                    f"Pending penalty: draw {self.penalty_amount} (must stack {self.penalty_value})."
                )

            if self._handle_draw_penalty(player):
                continue

            playable = player.playable_cards(
                self.active_color, self.active_value, penalty_value=self.penalty_value
            )
            penalty_active = self.penalty_amount > 0

            chosen_card: Optional[UnoCard] = None
            chosen_color: Optional[str] = None
            took_penalty = False

            if player.is_human:
                self._display_hand(player)
                while True:
                    if penalty_active:
                        choice = input(
                            "Stack a + card by number or type 'draw' to accept the penalty: "
                        ).strip()
                    elif playable:
                        choice = input(
                            "Choose card number to play or type 'draw': "
                        ).strip()
                    else:
                        choice = "draw"
                    if choice.lower() == "draw":
                        if penalty_active:
                            print(f"You accept the penalty of {self.penalty_amount} cards.")
                            self._draw_cards(player, self.penalty_amount)
                            self.penalty_amount = 0
                            self.penalty_value = None
                            took_penalty = True
                        else:
                            drawn_cards = self._draw_cards(player, 1)
                            drawn_card = drawn_cards[0]
                            print(f"You drew {drawn_card.label()}.")
                            if drawn_card.matches(self.active_color, self.active_value):
                                while True:
                                    play_now = input("Play the drawn card? [y/N]: ").strip().lower()
                                    if play_now in {"y", "yes"}:
                                        chosen_card = drawn_card
                                        if drawn_card.is_wild():
                                            chosen_color = self._prompt_color()
                                        break
                                    if play_now in {"", "n", "no"}:
                                        break
                        break
                    else:
                        if not playable:
                            print("You have no playable cards. You must draw.")
                            continue
                        if not choice.isdigit():
                            print("Please choose a card number or 'draw'.")
                            continue
                        index = int(choice) - 1
                        if not 0 <= index < len(player.hand):
                            print("Invalid card selection.")
                            continue
                        candidate = player.hand[index]
                        if candidate not in playable:
                            print("That card cannot be played right now.")
                            continue
                        chosen_card = candidate
                        if candidate.is_wild():
                            chosen_color = self._prompt_color()
                        break
            else:
                if not playable:
                    drawn_card = self._draw_cards(player, 1)[0]
                    print(f"{player.name} draws a card.")
                    if drawn_card.matches(self.active_color, self.active_value):
                        chosen_card = drawn_card
                        if drawn_card.is_wild():
                            chosen_color = player.preferred_color()
                            print(
                                f"{player.name} plays the drawn {drawn_card.label()} and sets color to {chosen_color}."
                            )
                        else:
                            print(f"{player.name} plays the drawn {drawn_card.label()}.")
                    else:
                        print(f"{player.name} keeps the drawn card.")
                else:
                    chosen_card = player.choose_card(playable, self.active_color)
                    if chosen_card is None:
                        chosen_card = playable[0]
                    if chosen_card.is_wild():
                        chosen_color = player.preferred_color()
                        print(
                            f"{player.name} plays {chosen_card.label()} and changes color to {chosen_color}."
                        )
                    else:
                        print(f"{player.name} plays {chosen_card.label()}.")

            if took_penalty:
                self._advance_turn()
                continue

            if chosen_card:
                skip_next = self._play_card(player, chosen_card, chosen_color)
                if not player.has_cards():
                    print(f"\n{player.name} wins the game!")
                    return player
                if len(player.hand) == 1:
                    print(f"{player.name} calls UNO!")
                self._advance_turn(skip_next=skip_next)
            else:
                self._advance_turn()

    def _prompt_color(self) -> str:
        while True:
            choice = input("Choose a color (red, yellow, green, blue): ").strip().lower()
            if choice in COLORS:
                return choice
            print("Invalid color. Please choose red, yellow, green, or blue.")


def _build_players(total: int, *, bots: int, bot_skill: str) -> List[UnoPlayer]:
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
              • Enter the card number from your hand to play it.
              • Type 'draw' to draw a card when you have no playable options or prefer not to play.
              • After drawing a playable card you may immediately play it by answering 'y'.
              • When playing a wild card choose the new color when prompted.
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
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> None:
    args = parse_args(argv)
    total_players = max(2, min(6, args.players))
    bots = max(1, min(total_players - 1, args.bots))
    rng = random.Random(args.seed)
    players = _build_players(total_players, bots=bots, bot_skill=args.bot_skill)
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
    "main",
]
