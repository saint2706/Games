"""Tkinter powered graphical interface for the poker match."""

from __future__ import annotations

import random
import tkinter as tk
from tkinter import ttk
from typing import Optional

from ..common.cards import format_cards
from .poker import Action, ActionType, PokerMatch


class PokerGUI:
    """Interactive Tk interface that visualises the :class:`PokerMatch`."""

    def __init__(self, root: tk.Tk, match: PokerMatch, rng: random.Random | None = None) -> None:
        self.root = root
        self.match = match
        self.rng = rng or random.Random()
        self.awaiting_user = False
        self.completed_hands = 0

        self.root.title("Card Games - Poker")
        self.root.geometry("980x680")

        self.status_var = tk.StringVar(value="Welcome to the poker table!")
        self.pot_var = tk.StringVar(value="Pot: 0")
        self.stage_var = tk.StringVar(value="Stage: pre-flop")

        self._build_layout()
        self._update_stacks()
        self._update_board()

        self.start_hand()

    def _build_layout(self) -> None:
        root = self.root
        root.columnconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)

        header = ttk.Frame(root, padding=10)
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(0, weight=1)
        header.columnconfigure(1, weight=1)
        header.columnconfigure(2, weight=1)

        ttk.Label(header, textvariable=self.status_var, font=("Segoe UI", 14, "bold")).grid(row=0, column=0, sticky="w")
        ttk.Label(header, textvariable=self.stage_var).grid(row=0, column=1, sticky="n")
        ttk.Label(header, textvariable=self.pot_var, anchor="e").grid(row=0, column=2, sticky="e")

        self.board_frame = ttk.Frame(root, padding=10)
        self.board_frame.grid(row=1, column=0, sticky="nsew")
        self.board_frame.columnconfigure(tuple(range(5)), weight=1)

        self.player_frames: dict[str, ttk.Frame] = {}
        self.player_vars: dict[str, dict[str, tk.StringVar]] = {}

        players_container = ttk.Frame(root, padding=10)
        players_container.grid(row=2, column=0, sticky="ew")
        players_container.columnconfigure(tuple(range(len(self.match.players))), weight=1)

        for index, player in enumerate(self.match.players):
            frame = ttk.LabelFrame(players_container, text=player.name, padding=10)
            frame.grid(row=0, column=index, sticky="nsew", padx=5)
            frame.columnconfigure(0, weight=1)
            cards_var = tk.StringVar(value="??")
            chips_var = tk.StringVar(value=f"Chips: {player.chips}")
            action_var = tk.StringVar(value="Waiting")
            ttk.Label(frame, textvariable=cards_var, font=("Consolas", 16)).grid(row=0, column=0, sticky="n")
            ttk.Label(frame, textvariable=chips_var).grid(row=1, column=0, sticky="n")
            ttk.Label(frame, textvariable=action_var, foreground="#555").grid(row=2, column=0, sticky="n")
            self.player_frames[player.name] = frame
            self.player_vars[player.name] = {
                "cards": cards_var,
                "chips": chips_var,
                "action": action_var,
            }

        actions_frame = ttk.Frame(root, padding=(10, 0, 10, 10))
        actions_frame.grid(row=3, column=0, sticky="ew")
        actions_frame.columnconfigure(1, weight=1)

        self.log = tk.Text(actions_frame, height=10, state="disabled", wrap="word", background="#101820", foreground="#E0E6ED")
        self.log.grid(row=0, column=0, columnspan=4, sticky="nsew", pady=(0, 10))

        ttk.Label(actions_frame, text="Wager amount:").grid(row=1, column=0, sticky="w")
        self.amount_var = tk.StringVar()
        ttk.Entry(actions_frame, textvariable=self.amount_var).grid(row=1, column=1, sticky="ew", padx=5)

        self.btn_fold = ttk.Button(actions_frame, text="Fold", command=lambda: self.handle_user_action(ActionType.FOLD))
        self.btn_call = ttk.Button(actions_frame, text="Call/Check", command=self._handle_call_or_check)
        self.btn_raise = ttk.Button(actions_frame, text="Bet/Raise", command=lambda: self.handle_user_action(ActionType.RAISE))
        self.btn_all_in = ttk.Button(actions_frame, text="All-in", command=lambda: self.handle_user_action(ActionType.ALL_IN))

        self.btn_fold.grid(row=2, column=0, sticky="ew")
        self.btn_call.grid(row=2, column=1, sticky="ew", padx=5)
        self.btn_raise.grid(row=2, column=2, sticky="ew")
        self.btn_all_in.grid(row=2, column=3, sticky="ew", padx=5)

        self._set_action_buttons_state("disabled")

    def start_hand(self) -> None:
        table = self.match.table
        if self._match_complete():
            self.status_var.set("Match complete! Thanks for playing.")
            self._set_action_buttons_state("disabled")
            return

        self.completed_hands += 1
        self.status_var.set(f"Hand {self.completed_hands} of {self.match.rounds}")
        table.start_hand()
        table.last_actions.clear()
        self.amount_var.set(str(max(table.min_raise_amount, table.big_blind)))
        self._log(f"New hand begins. Your cards: {format_cards(self.match.user.hole_cards)}")
        self._update_board()
        self._update_stacks()
        self._update_player_cards(show_all=False)
        self._set_action_buttons_state("disabled")
        self.root.after(400, self._advance_until_user)

    def _match_complete(self) -> bool:
        if self.completed_hands >= self.match.rounds and self.match.rounds > 0:
            return True
        if self.match.user.chips <= 0:
            return True
        if all(bot.chips <= 0 for bot in self.match.bots):
            return True
        return False

    def _advance_until_user(self) -> None:
        table = self.match.table

        while True:
            if table._active_player_count() <= 1:
                self._finish_hand()
                return
            if not table.players_can_act():
                self._flush_action_log()
                if table.stage != "river":
                    table.proceed_to_next_stage()
                    self._log(f"Stage advances to {table.stage}. Board: {format_cards(table.community_cards)}")
                    self._update_board()
                    self._update_player_cards(show_all=False)
                    continue
                self._finish_hand()
                return
            if table.stage == "river" and table.betting_round_complete():
                self._finish_hand()
                return

            player = table.players[table.current_player_index]
            if player.is_user and not player.folded and not player.all_in:
                self.awaiting_user = True
                self._prepare_user_turn()
                return
            if player.folded or player.all_in:
                table.current_player_index = table._next_index(table.current_player_index)
                continue

            controller = self.match.bot_controllers[self.match.bots.index(player)]
            action = controller.decide(table)
            table.apply_action(player, action)
            self._flush_action_log()
            self._update_stacks()
            self._update_player_cards(show_all=False)

            if table.betting_round_complete():
                self._end_betting_round()
                if table.stage == "river":
                    self._finish_hand()
                    return
                table.proceed_to_next_stage()
                self._log(f"Stage advances to {table.stage}. Board: {format_cards(table.community_cards)}")
                self._update_board()
                self._update_player_cards(show_all=False)

    def _prepare_user_turn(self) -> None:
        table = self.match.table
        player = self.match.user
        to_call = table.current_bet - player.current_bet
        self.status_var.set(f"Your turn | Pot {table.pot} | To call {to_call}")
        self._set_action_buttons_state("normal")
        self._update_board()
        self._update_player_cards(show_all=False)
        options = table.valid_actions(player)
        self.btn_fold.configure(state="normal" if ActionType.FOLD in options else "disabled")
        if to_call <= 0 and ActionType.CHECK in options:
            self.btn_call.configure(text="Check")
        elif ActionType.CALL in options:
            self.btn_call.configure(text=f"Call ({min(to_call, player.chips)})")
        else:
            self.btn_call.configure(text="Call/Check", state="disabled")
        if ActionType.RAISE in options or ActionType.BET in options:
            self.btn_raise.configure(state="normal")
        else:
            self.btn_raise.configure(state="disabled")
        if ActionType.ALL_IN in options:
            self.btn_all_in.configure(state="normal")
        else:
            self.btn_all_in.configure(state="disabled")

    def _handle_call_or_check(self) -> None:
        table = self.match.table
        player = self.match.user
        to_call = table.current_bet - player.current_bet
        if to_call <= 0:
            self.handle_user_action(ActionType.CHECK)
        else:
            self.handle_user_action(ActionType.CALL)

    def handle_user_action(self, action_type: ActionType) -> None:
        if not self.awaiting_user:
            return
        table = self.match.table
        player = self.match.user
        to_call = table.current_bet - player.current_bet

        try:
            if action_type is ActionType.FOLD:
                action = Action(ActionType.FOLD)
            elif action_type is ActionType.CHECK:
                action = Action(ActionType.CHECK)
            elif action_type is ActionType.CALL:
                action = Action(ActionType.CALL, target_bet=table.current_bet)
            elif action_type is ActionType.ALL_IN:
                action = Action(ActionType.ALL_IN, target_bet=player.current_bet + player.chips)
            elif action_type in {ActionType.BET, ActionType.RAISE}:
                amount = self._parse_amount(self.amount_var.get(), default=table.min_raise_amount)
                if to_call <= 0:
                    target = player.current_bet + max(amount, table.min_raise_amount)
                    action = Action(ActionType.BET, target_bet=target)
                else:
                    target = table.current_bet + max(amount, table.min_raise_amount)
                    action = Action(ActionType.RAISE, target_bet=target)
            else:
                return
        except ValueError:
            self.status_var.set("Invalid amount. Please enter a positive integer.")
            return

        table.apply_action(player, action)
        self.awaiting_user = False
        self._set_action_buttons_state("disabled")
        self._flush_action_log()
        self._update_stacks()
        self._update_player_cards(show_all=False)

        if table.betting_round_complete():
            self._end_betting_round()
            if table.stage == "river":
                self._finish_hand()
                return
            table.proceed_to_next_stage()
            self._log(f"Stage advances to {table.stage}. Board: {format_cards(table.community_cards)}")
            self._update_board()
            self._update_player_cards(show_all=False)

        self.root.after(200, self._advance_until_user)

    def _finish_hand(self) -> None:
        table = self.match.table
        self._flush_action_log()

        if table._active_player_count() == 1:
            payouts = table.distribute_pot()
            for name, amount in payouts.items():
                if amount:
                    self._log(f"{name} wins the pot uncontested ({amount} chips)")
            self._update_player_cards(show_all=False)
        else:
            rankings = table.showdown()
            for player, rank in rankings:
                self._log(f"{player.name}: {format_cards(player.hole_cards)} -> {rank.describe()}")
            payouts = table.distribute_pot()
            for name, amount in payouts.items():
                if amount:
                    self._log(f"{name} collects {amount} chips")
            self._update_player_cards(show_all=True)

        self._update_stacks()
        self._update_board()
        self._set_action_buttons_state("disabled")

        if self._match_complete():
            self.status_var.set("Match complete! Close the window to exit.")
            return

        self.status_var.set("Preparing next hand...")
        self.match.table.rotate_dealer()
        self.root.after(2200, self.start_hand)

    def _end_betting_round(self) -> None:
        for line in self.match.table.last_actions:
            self._log(line)
        self.match.table.last_actions.clear()

    def _flush_action_log(self) -> None:
        for line in self.match.table.last_actions:
            self._log(line)
        self.match.table.last_actions.clear()

    def _update_board(self) -> None:
        table = self.match.table
        self.stage_var.set(f"Stage: {table.stage}")
        self.pot_var.set(f"Pot: {table.pot}")
        for widget in self.board_frame.winfo_children():
            widget.destroy()
        cards = table.community_cards
        for index in range(5):
            if index < len(cards):
                card_text = str(cards[index])
            else:
                card_text = "🂠"
            label = ttk.Label(self.board_frame, text=card_text, font=("Consolas", 24), padding=10)
            label.grid(row=0, column=index, padx=6)

    def _update_player_cards(self, *, show_all: bool) -> None:
        for player in self.match.players:
            vars = self.player_vars[player.name]
            if player.is_user or show_all or player.folded:
                if player.hole_cards:
                    vars["cards"].set(format_cards(player.hole_cards))
                else:
                    vars["cards"].set("--")
            else:
                vars["cards"].set("??")
            vars["action"].set(player.last_action.capitalize())

    def _update_stacks(self) -> None:
        for player in self.match.players:
            vars = self.player_vars[player.name]
            vars["chips"].set(f"Chips: {player.chips}")

    def _log(self, message: str) -> None:
        self.log.configure(state="normal")
        self.log.insert("end", message + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def _set_action_buttons_state(self, state: str) -> None:
        for button in (self.btn_fold, self.btn_call, self.btn_raise, self.btn_all_in):
            button.configure(state=state)

    @staticmethod
    def _parse_amount(raw: str, *, default: int) -> int:
        raw = raw.strip()
        if not raw:
            return default
        value = int(raw)
        if value <= 0:
            raise ValueError("Amount must be positive")
        return value


def launch_gui(match: PokerMatch, *, rng: Optional[random.Random] = None) -> None:
    """Entry point used by :func:`card_games.poker.poker.run_cli`."""

    root = tk.Tk()
    PokerGUI(root, match, rng=rng)
    root.mainloop()


__all__ = ["PokerGUI", "launch_gui"]

