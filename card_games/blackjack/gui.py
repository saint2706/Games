"""Tkinter-powered graphical interface for the blackjack engine."""

from __future__ import annotations

import tkinter as tk
from typing import Optional

from card_games.blackjack.game import BlackjackGame, BlackjackHand, Outcome
from card_games.common.cards import Card, Suit

_TABLE_GREEN = "#0b5d1e"
_TABLE_ACCENT = "#145c2a"
_CARD_BORDER = "#f5f5f5"
_CARD_FACE = "#ffffff"
_CARD_BACK = "#1e3a5f"
_CARD_BACK_ACCENT = "#f7b733"
_TEXT_PRIMARY = "#f2f2f2"
_TEXT_MUTED = "#c8e6c9"
_TEXT_ALERT = "#ffdf6b"
_BUTTON_BG = "#f7c548"
_BUTTON_BG_ACTIVE = "#f9d976"
_BUTTON_DISABLED = "#b0b0b0"
_ACTION_BG = "#16532a"
_HIGHLIGHT = "#22a45d"
_CARD_WIDTH = 90
_CARD_HEIGHT = 130


class BlackjackApp(tk.Tk):
    """A complete blackjack table rendered with Tkinter."""

    def __init__(
        self,
        *,
        bankroll: int = 500,
        min_bet: int = 10,
        decks: int = 6,
        rng=None,
    ) -> None:
        super().__init__()
        self.title("Blackjack Table")
        self.configure(bg=_TABLE_GREEN)
        self.resizable(False, False)
        self.option_add("*Font", "Segoe UI 12")
        self.option_add("*Button.relief", "flat")
        self.option_add("*Label.background", _TABLE_GREEN)
        self.option_add("*Label.foreground", _TEXT_PRIMARY)

        self.game = BlackjackGame(bankroll=bankroll, min_bet=min_bet, decks=decks, rng=rng)
        self.round_active = False
        self.round_complete = False
        self.dealer_hidden = True
        self.current_hand_index: Optional[int] = None
        self._dealer_job: Optional[str] = None

        self.bet_var = tk.IntVar(value=self.game.min_bet)
        self.bankroll_var = tk.StringVar()
        self.shoe_var = tk.StringVar()
        self.message_var = tk.StringVar()

        self._build_layout()
        self._refresh_labels()
        self._render_table()
        self._update_buttons()

    # ------------------------------------------------------------------
    # Layout helpers
    # ------------------------------------------------------------------
    def _build_layout(self) -> None:
        header = tk.Frame(self, bg=_TABLE_GREEN)
        header.pack(fill="x", padx=24, pady=(24, 12))

        title = tk.Label(
            header,
            text="Blackjack",
            font=("Segoe UI", 26, "bold"),
            fg=_TEXT_ALERT,
        )
        title.pack(side="left")

        info_panel = tk.Frame(header, bg=_TABLE_GREEN)
        info_panel.pack(side="right")

        tk.Label(info_panel, text="Bankroll", font=("Segoe UI", 12, "bold"), fg=_TEXT_MUTED).pack(
            anchor="e"
        )
        tk.Label(info_panel, textvariable=self.bankroll_var, font=("Segoe UI", 18, "bold")).pack(
            anchor="e"
        )
        tk.Label(info_panel, textvariable=self.shoe_var, font=("Segoe UI", 10)).pack(anchor="e")

        controls = tk.Frame(self, bg=_TABLE_GREEN)
        controls.pack(fill="x", padx=24, pady=(0, 16))

        bet_panel = tk.Frame(controls, bg=_TABLE_GREEN)
        bet_panel.pack(side="left")

        tk.Label(bet_panel, text="Wager", font=("Segoe UI", 12, "bold"), fg=_TEXT_MUTED).pack(
            anchor="w"
        )
        spin = tk.Spinbox(
            bet_panel,
            from_=self.game.min_bet,
            to=max(self.game.min_bet, self.game.player.bankroll),
            increment=self.game.min_bet,
            textvariable=self.bet_var,
            width=6,
            justify="center",
            font=("Segoe UI", 14, "bold"),
            foreground="#1e272e",
        )
        spin.pack(side="left", padx=(0, 12))
        self.bet_spinbox = spin

        self.deal_button = tk.Button(
            controls,
            text="Deal",
            command=self.start_round,
            bg=_BUTTON_BG,
            activebackground=_BUTTON_BG_ACTIVE,
            fg="#1c1c1c",
            padx=18,
            pady=10,
            font=("Segoe UI", 12, "bold"),
        )
        self.deal_button.pack(side="left", padx=(0, 12))

        action_panel = tk.Frame(controls, bg=_TABLE_GREEN)
        action_panel.pack(side="right")

        self.hit_button = self._action_button(action_panel, "Hit", self.hit)
        self.stand_button = self._action_button(action_panel, "Stand", self.stand)
        self.double_button = self._action_button(action_panel, "Double", self.double_down)
        self.split_button = self._action_button(action_panel, "Split", self.split_hand)

        table = tk.Frame(self, bg=_TABLE_ACCENT, bd=6, relief="ridge")
        table.pack(fill="both", expand=True, padx=24, pady=(0, 16))

        dealer_section = tk.Frame(table, bg=_TABLE_ACCENT)
        dealer_section.pack(fill="x", pady=(16, 8))
        tk.Label(dealer_section, text="Dealer", font=("Segoe UI", 16, "bold")).pack()
        self.dealer_cards = tk.Frame(dealer_section, bg=_TABLE_ACCENT)
        self.dealer_cards.pack(pady=6)

        separator = tk.Canvas(table, height=2, bg=_TABLE_ACCENT, highlightthickness=0)
        separator.create_line(40, 1, 680, 1, fill=_TEXT_MUTED, width=2)
        separator.pack(fill="x", padx=24, pady=6)

        player_section = tk.Frame(table, bg=_TABLE_ACCENT)
        player_section.pack(fill="both", expand=True, pady=(8, 16))
        tk.Label(player_section, text="Player", font=("Segoe UI", 16, "bold")).pack()
        self.player_hands = tk.Frame(player_section, bg=_TABLE_ACCENT)
        self.player_hands.pack(pady=8)

        footer = tk.Frame(self, bg=_TABLE_GREEN)
        footer.pack(fill="x", padx=24, pady=(0, 18))
        self.message_label = tk.Label(
            footer,
            textvariable=self.message_var,
            font=("Segoe UI", 12),
            anchor="w",
            justify="left",
            wraplength=600,
        )
        self.message_label.pack(fill="x")

    def _action_button(self, parent: tk.Widget, text: str, command) -> tk.Button:
        button = tk.Button(
            parent,
            text=text,
            command=command,
            bg=_ACTION_BG,
            activebackground=_HIGHLIGHT,
            fg=_TEXT_PRIMARY,
            padx=16,
            pady=9,
            font=("Segoe UI", 12, "bold"),
        )
        button.pack(side="left", padx=6)
        return button

    # ------------------------------------------------------------------
    # UI update helpers
    # ------------------------------------------------------------------
    def _refresh_labels(self) -> None:
        bankroll = self.game.player.bankroll
        self.bankroll_var.set(f"${bankroll:,}")
        cards_remaining = len(self.game.shoe.cards)
        decks = self.game.shoe.decks
        self.shoe_var.set(f"Shoe: {cards_remaining} cards · {decks} decks")

        maximum = max(self.game.min_bet, bankroll)
        self.bet_spinbox.configure(to=maximum)
        if not self.game.can_continue():
            self.bet_var.set(self.game.player.bankroll)

    def _render_table(self) -> None:
        for widget in self.dealer_cards.winfo_children():
            widget.destroy()
        for widget in self.player_hands.winfo_children():
            widget.destroy()

        dealer_hand = self.game.dealer_hand if self.game.dealer.hands else None
        if dealer_hand:
            self._render_hand_cards(self.dealer_cards, dealer_hand, hide_hole=self.dealer_hidden)
            info = self._hand_summary(dealer_hand, dealer=True, hide_hole=self.dealer_hidden)
            tk.Label(
                self.dealer_cards,
                text=info,
                font=("Segoe UI", 11),
                fg=_TEXT_MUTED,
            ).pack(pady=(6, 0))

        for index, hand in enumerate(self.game.player.hands):
            highlight = index == self.current_hand_index and self.round_active
            container = tk.Frame(
                self.player_hands,
                bg=_HIGHLIGHT if highlight else _ACTION_BG,
                bd=4,
                relief="ridge",
            )
            container.pack(side="left", padx=8, pady=8, ipadx=6, ipady=6)

            header = tk.Frame(container, bg=container["background"])
            header.pack(fill="x")
            label = "Hand {}".format(index + 1) if len(self.game.player.hands) > 1 else "Your hand"
            tk.Label(
                header,
                text=label,
                font=("Segoe UI", 13, "bold"),
                fg=_TEXT_PRIMARY,
            ).pack(side="left")
            tk.Label(
                header,
                text=f"Bet ${hand.bet:,}",
                font=("Segoe UI", 11),
                fg=_TEXT_ALERT,
            ).pack(side="right")

            cards_frame = tk.Frame(container, bg=container["background"])
            cards_frame.pack(pady=4)
            self._render_hand_cards(cards_frame, hand, hide_hole=False)

            tk.Label(
                container,
                text=self._hand_summary(hand, dealer=False),
                font=("Segoe UI", 11),
                fg=_TEXT_MUTED,
            ).pack(pady=(4, 0))

    def _hand_summary(
        self,
        hand: BlackjackHand,
        *,
        dealer: bool = False,
        hide_hole: bool = False,
    ) -> str:
        if hide_hole:
            visible = BlackjackHand(cards=[hand.cards[0]])
            total = visible.best_total()
            return f"Showing {total}"

        parts: list[str] = []
        if hand.is_blackjack():
            parts.append("Blackjack!")
        elif hand.is_bust():
            parts.append("Bust")
        else:
            parts.append(f"Total {hand.best_total()}")
            if hand.is_soft() and hand.best_total() <= 21:
                parts.append("Soft")
        if hand.doubled:
            parts.append("Doubled")
        if hand.split_from is not None:
            parts.append("Split")
        if dealer and hand.stood and not hand.is_bust():
            parts.append("Stood")
        return " · ".join(parts)

    def _render_hand_cards(self, parent: tk.Widget, hand: BlackjackHand, *, hide_hole: bool) -> None:
        cards = list(hand.cards)
        for idx, card in enumerate(cards):
            hidden = hide_hole and idx == 1
            widget = self._card_widget(parent, card, hidden=hidden)
            widget.pack(side="left", padx=6)

    def _card_widget(self, parent: tk.Widget, card: Card, *, hidden: bool) -> tk.Canvas:
        canvas = tk.Canvas(
            parent,
            width=_CARD_WIDTH,
            height=_CARD_HEIGHT,
            bg=_ACTION_BG,
            highlightthickness=0,
        )
        if hidden:
            canvas.create_rectangle(
                6,
                6,
                _CARD_WIDTH - 6,
                _CARD_HEIGHT - 6,
                outline=_CARD_BORDER,
                width=3,
                fill=_CARD_BACK,
            )
            canvas.create_line(10, 10, _CARD_WIDTH - 10, _CARD_HEIGHT - 10, fill=_CARD_BACK_ACCENT, width=3)
            canvas.create_line(10, _CARD_HEIGHT - 10, _CARD_WIDTH - 10, 10, fill=_CARD_BACK_ACCENT, width=3)
            canvas.create_text(
                _CARD_WIDTH / 2,
                _CARD_HEIGHT / 2,
                text="★",
                font=("Segoe UI", 30),
                fill=_TEXT_PRIMARY,
            )
        else:
            suit = card.suit
            rank_display = "10" if card.rank == "T" else card.rank
            fill_color = _CARD_FACE
            outline_color = _CARD_BORDER
            suit_color = "#d32f2f" if suit in (Suit.HEARTS, Suit.DIAMONDS) else "#1c1c1c"
            canvas.create_rectangle(
                6,
                6,
                _CARD_WIDTH - 6,
                _CARD_HEIGHT - 6,
                outline=outline_color,
                width=3,
                fill=fill_color,
            )
            canvas.create_text(
                16,
                20,
                text=rank_display,
                fill=suit_color,
                font=("Segoe UI", 18, "bold"),
                anchor="nw",
            )
            canvas.create_text(
                _CARD_WIDTH - 16,
                _CARD_HEIGHT - 20,
                text=rank_display,
                fill=suit_color,
                font=("Segoe UI", 18, "bold"),
                anchor="se",
            )
            canvas.create_text(
                _CARD_WIDTH / 2,
                _CARD_HEIGHT / 2,
                text=suit.value,
                fill=suit_color,
                font=("Segoe UI Symbol", 32),
            )
        return canvas

    def _update_buttons(self) -> None:
        if self.round_active:
            self.deal_button.configure(state="disabled", bg=_BUTTON_DISABLED)
            for button in (self.hit_button, self.stand_button, self.double_button, self.split_button):
                button.configure(state="disabled", bg=_ACTION_BG)

            hand = self._current_hand()
            if hand is None:
                return

            actions = self.game.player_actions(hand)
            if "hit" in actions:
                self._enable_button(self.hit_button)
            if "stand" in actions:
                self._enable_button(self.stand_button)
            if "double" in actions:
                self._enable_button(self.double_button)
            if "split" in actions:
                self._enable_button(self.split_button)
        else:
            deal_state = tk.NORMAL if self.game.can_continue() else tk.DISABLED
            self.deal_button.configure(
                state=deal_state,
                text="Deal next hand" if self.round_complete else "Deal",
                bg=_BUTTON_BG if deal_state == tk.NORMAL else _BUTTON_DISABLED,
            )
            for button in (self.hit_button, self.stand_button, self.double_button, self.split_button):
                button.configure(state=tk.DISABLED, bg=_ACTION_BG)

    def _enable_button(self, button: tk.Button) -> None:
        button.configure(state=tk.NORMAL, bg=_HIGHLIGHT)

    def _current_hand(self) -> Optional[BlackjackHand]:
        if self.current_hand_index is None:
            return None
        if self.current_hand_index >= len(self.game.player.hands):
            return None
        return self.game.player.hands[self.current_hand_index]

    # ------------------------------------------------------------------
    # Game flow handlers
    # ------------------------------------------------------------------
    def start_round(self) -> None:
        if self.round_active:
            return
        if self.round_complete:
            self.game.reset()
            self.round_complete = False
        if not self.game.can_continue():
            self.message_var.set("Insufficient bankroll to place the minimum bet.")
            return

        bankroll = self.game.player.bankroll
        bet = max(self.game.min_bet, int(self.bet_var.get()))
        if bet > bankroll:
            bet = bankroll
            self.bet_var.set(bet)
        try:
            self.game.start_round(bet)
        except ValueError as exc:
            self.message_var.set(str(exc))
            return

        self.round_active = True
        self.dealer_hidden = True
        self.current_hand_index = 0
        self.message_var.set("Cards dealt. Make your move!")
        self._refresh_labels()
        self._render_table()
        self._update_buttons()

        player_hand = self.game.player.hands[0]
        dealer_blackjack = self.game.dealer_hand.is_blackjack()
        player_blackjack = player_hand.is_blackjack()

        if dealer_blackjack or player_blackjack:
            self.current_hand_index = None
            self.round_active = True
            self.dealer_hidden = False
            if dealer_blackjack and player_blackjack:
                self.message_var.set("Both player and dealer have blackjack!")
            elif player_blackjack:
                self.message_var.set("Blackjack! Awaiting dealer check...")
            else:
                self.message_var.set("Dealer reveals a blackjack.")
            self._render_table()
            self._update_buttons()
            self.after(800, self.finish_round)
            return

        if player_hand.best_total() == 21:
            player_hand.stood = True
            self.after(600, self._advance_hand)

    def hit(self) -> None:
        hand = self._current_hand()
        if hand is None:
            return
        card = self.game.hit(hand)
        self.message_var.set(f"Hit: drew {card}.")
        self._render_table()
        if hand.is_bust():
            hand.stood = True
            self.message_var.set("Bust! Hand is out of play.")
            self.after(500, self._advance_hand)
        elif hand.best_total() == 21:
            hand.stood = True
            self.message_var.set("21! Standing automatically.")
            self.after(500, self._advance_hand)
        else:
            self._update_buttons()

    def stand(self) -> None:
        hand = self._current_hand()
        if hand is None:
            return
        self.game.stand(hand)
        self.message_var.set("Stand. Dealer to play once all hands acted.")
        self._render_table()
        self.after(400, self._advance_hand)

    def double_down(self) -> None:
        hand = self._current_hand()
        if hand is None:
            return
        try:
            card = self.game.double_down(hand)
        except ValueError as exc:
            self.message_var.set(str(exc))
            return
        self.message_var.set(f"Double down! Drew {card} and standing on {hand.best_total()}.")
        self._refresh_labels()
        self._render_table()
        self.after(500, self._advance_hand)

    def split_hand(self) -> None:
        hand = self._current_hand()
        if hand is None:
            return
        try:
            self.game.split(hand)
        except ValueError as exc:
            self.message_var.set(str(exc))
            return
        self.message_var.set("Split successful — play each hand in turn.")
        self._refresh_labels()
        self._render_table()
        self._update_buttons()

    def _advance_hand(self) -> None:
        if not self.round_active:
            return

        next_index = None
        for idx, hand in enumerate(self.game.player.hands):
            if hand.is_bust() or hand.is_blackjack() or hand.stood:
                continue
            next_index = idx
            break

        self.current_hand_index = next_index
        if next_index is None:
            self._begin_dealer_turn()
        else:
            self._render_table()
            self._update_buttons()

    def _begin_dealer_turn(self) -> None:
        self.current_hand_index = None
        self.dealer_hidden = False
        self._render_table()
        self._update_buttons()

        if all(hand.is_bust() for hand in self.game.player.hands):
            self.after(600, self.finish_round)
            return

        dealer_hand = self.game.dealer_hand
        dealer_hand.stood = False
        self._dealer_job = self.after(600, self._dealer_draw_step)

    def _dealer_draw_step(self) -> None:
        hand = self.game.dealer_hand
        if hand.best_total() < 17 or (hand.best_total() == 17 and hand.is_soft()):
            card = self.game.hit(hand)
            self.message_var.set(f"Dealer draws {card}.")
            self._render_table()
            self._dealer_job = self.after(700, self._dealer_draw_step)
        else:
            hand.stood = True
            self.message_var.set("Dealer stands.")
            self._render_table()
            self._dealer_job = None
            self.after(700, self.finish_round)

    def finish_round(self) -> None:
        if not self.round_active:
            return
        if self._dealer_job is not None:
            self.after_cancel(self._dealer_job)
            self._dealer_job = None

        outcomes = self.game.settle_round()
        messages: list[str] = []
        for idx, (hand, outcome) in enumerate(zip(self.game.player.hands, outcomes), start=1):
            descriptor = self._describe_outcome(hand, outcome)
            if len(self.game.player.hands) > 1:
                messages.append(f"Hand {idx}: {descriptor}")
            else:
                messages.append(descriptor)
        summary = " | ".join(messages)
        text = f"{summary} Bankroll now ${self.game.player.bankroll:,}."
        if not self.game.can_continue():
            text += " Buy back in to keep playing."
        self.message_var.set(text)

        self.round_active = False
        self.round_complete = True
        self.current_hand_index = None
        self._refresh_labels()
        self._render_table()
        self._update_buttons()

    def _describe_outcome(self, hand: BlackjackHand, outcome: Outcome) -> str:
        mapping = {
            Outcome.PLAYER_BLACKJACK: "Blackjack pays 3:2!",
            Outcome.PLAYER_WIN: "Win",
            Outcome.DEALER_BUST: "Dealer busts — win",
            Outcome.PUSH: "Push",
            Outcome.PLAYER_LOSS: "Lost",
            Outcome.PLAYER_BUST: "Busted",
        }
        base = mapping.get(outcome, outcome.value.replace("_", " ").title())
        if outcome in {Outcome.PLAYER_WIN, Outcome.DEALER_BUST, Outcome.PLAYER_BLACKJACK}:
            base = f"{base} (+${hand.bet:,})"
        elif outcome == Outcome.PUSH:
            base = f"{base} (stake returned)"
        else:
            base = f"{base} (-${hand.bet:,})"
        return base


def run_app(
    *,
    bankroll: int = 500,
    min_bet: int = 10,
    decks: int = 6,
    rng=None,
) -> None:
    """Launch the blackjack GUI."""

    app = BlackjackApp(bankroll=bankroll, min_bet=min_bet, decks=decks, rng=rng)
    app.mainloop()


__all__ = ["BlackjackApp", "run_app"]
