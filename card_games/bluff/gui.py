"""Tkinter interface for the bluff (Cheat) card game."""

from __future__ import annotations

import random
import tkinter as tk
from tkinter import ttk
from typing import Optional

from .bluff import BluffGame, DifficultyLevel, Phase


class BluffGUI:
    """Interactive Tk interface for :class:`BluffGame`."""

    def __init__(self, root: tk.Tk, game: BluffGame) -> None:
        self.root = root
        self.game = game

        self.root.title("Card Games - Bluff")
        self.root.geometry("960x640")

        self.status_var = tk.StringVar(value="Welcome to Bluff! Shed every card to win.")
        self.pile_var = tk.StringVar(value="Pile: 0 cards")
        self.turn_var = tk.StringVar(value="Turn 1")

        self._selected_card: Optional[int] = None
        self._last_claim_text = tk.StringVar(value="No claim yet.")

        style = ttk.Style()
        style.configure("Card.TButton", font=("Consolas", 14), padding=8)
        style.configure(
            "SelectedCard.TButton",
            font=("Consolas", 14, "bold"),
            padding=8,
            background="#1f6aa5",
            foreground="#ffffff",
        )

        self._build_layout()
        self._update_scoreboard()
        self._update_user_hand()
        self._set_user_controls_state(enabled=False)
        self._set_challenge_controls_state(enabled=False)

        self.root.after(300, self.advance_game)

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------
    def _build_layout(self) -> None:
        root = self.root
        root.columnconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)
        root.rowconfigure(2, weight=1)

        header = ttk.Frame(root, padding=12)
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(0, weight=2)
        header.columnconfigure(1, weight=1)
        header.columnconfigure(2, weight=1)

        ttk.Label(header, textvariable=self.status_var, font=("Segoe UI", 14, "bold")).grid(
            row=0, column=0, sticky="w"
        )
        ttk.Label(header, textvariable=self.turn_var).grid(row=0, column=1, sticky="e")
        ttk.Label(header, textvariable=self.pile_var).grid(row=0, column=2, sticky="e")

        board = ttk.Frame(root, padding=10)
        board.grid(row=1, column=0, sticky="nsew")
        board.columnconfigure(0, weight=2)
        board.columnconfigure(1, weight=1)

        self.log = tk.Text(
            board,
            height=18,
            state="disabled",
            wrap="word",
            background="#101820",
            foreground="#E0E6ED",
        )
        self.log.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        sidebar = ttk.Frame(board, padding=10)
        sidebar.grid(row=0, column=1, sticky="nsew")
        sidebar.columnconfigure(0, weight=1)

        ttk.Label(sidebar, text="Table summary", font=("Segoe UI", 12, "bold")).grid(
            row=0, column=0, sticky="w"
        )
        self.summary = tk.Text(sidebar, height=12, state="disabled", wrap="word")
        self.summary.grid(row=1, column=0, sticky="nsew", pady=(4, 10))

        ttk.Label(sidebar, textvariable=self._last_claim_text, wraplength=220).grid(
            row=2, column=0, sticky="w"
        )

        controls = ttk.Frame(root, padding=12)
        controls.grid(row=2, column=0, sticky="nsew")
        controls.columnconfigure(0, weight=1)
        controls.columnconfigure(1, weight=1)
        controls.columnconfigure(2, weight=1)

        hand_frame = ttk.LabelFrame(controls, text="Your hand", padding=10)
        hand_frame.grid(row=0, column=0, columnspan=3, sticky="ew")
        hand_frame.columnconfigure(tuple(range(10)), weight=1)
        self.hand_frame = hand_frame

        claim_frame = ttk.Frame(controls, padding=(0, 10))
        claim_frame.grid(row=1, column=0, columnspan=3, sticky="ew")
        claim_frame.columnconfigure(1, weight=1)

        ttk.Label(claim_frame, text="Declare rank:").grid(row=0, column=0, sticky="w")
        self.claim_rank_var = tk.StringVar(value="A")
        self.claim_combo = ttk.Combobox(
            claim_frame,
            textvariable=self.claim_rank_var,
            values=list("23456789TJQKA"),
            state="readonly",
        )
        self.claim_combo.grid(row=0, column=1, sticky="ew", padx=6)

        self.submit_btn = ttk.Button(
            claim_frame,
            text="Play selected card",
            command=self.submit_claim,
        )
        self.submit_btn.grid(row=0, column=2, sticky="ew")

        challenge_frame = ttk.Frame(controls)
        challenge_frame.grid(row=2, column=0, columnspan=3, sticky="ew")
        challenge_frame.columnconfigure(0, weight=1)
        challenge_frame.columnconfigure(1, weight=1)

        self.call_btn = ttk.Button(
            challenge_frame,
            text="Call Bluff",
            command=lambda: self.resolve_user_challenge(True),
        )
        self.trust_btn = ttk.Button(
            challenge_frame,
            text="Trust Claim",
            command=lambda: self.resolve_user_challenge(False),
        )
        self.call_btn.grid(row=0, column=0, sticky="ew", padx=(0, 6))
        self.trust_btn.grid(row=0, column=1, sticky="ew")

    # ------------------------------------------------------------------
    # UI state updates
    # ------------------------------------------------------------------
    def _update_scoreboard(self) -> None:
        state = self.game.public_state()
        self.turn_var.set(f"Turn {state['turns_played'] + 1} / {state['max_turns']}")
        self.pile_var.set(f"Pile: {state['pile_size']} cards")

        text_lines = []
        for player in state["players"]:
            calls = player["calls"]
            correct = player["correct_calls"]
            call_text = f"Calls: {correct}/{calls}" if calls else "Calls: 0"
            line = (
                f"{player['name']}: {player['card_count']} cards | Truths {player['truths']} | "
                f"Lies {player['lies']} | {call_text}"
            )
            text_lines.append(line)

        self.summary.configure(state="normal")
        self.summary.delete("1.0", tk.END)
        self.summary.insert(tk.END, "\n".join(text_lines))
        self.summary.configure(state="disabled")

    def _update_user_hand(self) -> None:
        for widget in self.hand_frame.winfo_children():
            widget.destroy()

        user = self.game.players[0]
        for idx, card in enumerate(user.hand):
            style = "SelectedCard.TButton" if idx == self._selected_card else "Card.TButton"
            button = ttk.Button(
                self.hand_frame,
                text=str(card),
                style=style,
                command=lambda i=idx: self._select_card(i),
            )
            button.grid(row=0, column=idx, padx=4, pady=4, sticky="ew")

        if self._selected_card is not None and self._selected_card >= len(user.hand):
            self._selected_card = None

    def _select_card(self, index: int) -> None:
        self._selected_card = index
        user = self.game.players[0]
        if 0 <= index < len(user.hand):
            self.claim_rank_var.set(user.hand[index].rank)
        self._update_user_hand()

    def _set_user_controls_state(self, *, enabled: bool) -> None:
        state = "!disabled" if enabled else "disabled"
        for widget in self.hand_frame.winfo_children():
            widget.state([state])
        self.claim_combo.state([state])
        if enabled:
            self.claim_combo.configure(state="readonly")
        else:
            self.claim_combo.configure(state="disabled")
        self.submit_btn.state([state])

    def _set_challenge_controls_state(self, *, enabled: bool) -> None:
        state = "!disabled" if enabled else "disabled"
        self.call_btn.state([state])
        self.trust_btn.state([state])

    def _log(self, message: str) -> None:
        self.log.configure(state="normal")
        self.log.insert(tk.END, message + "\n")
        self.log.configure(state="disabled")
        self.log.see(tk.END)

    # ------------------------------------------------------------------
    # Game progression
    # ------------------------------------------------------------------
    def advance_game(self) -> None:
        self._update_scoreboard()
        self._update_user_hand()
        if self.game.finished:
            self._handle_game_end()
            return

        current = self.game.current_player
        if current.is_user:
            self.status_var.set("Your turn: choose a card and declare its rank.")
            self._last_claim_text.set("Awaiting your play.")
            self._set_user_controls_state(enabled=True)
            self._set_challenge_controls_state(enabled=False)
        else:
            self._set_user_controls_state(enabled=False)
            claim, messages = self.game.play_bot_turn()
            for msg in messages:
                self._log(msg)
            self._log(
                f"{current.name} claims their card is a {claim.claimed_rank}."
            )
            self._last_claim_text.set(
                f"Latest claim: {current.name} says {claim.claimed_rank}."
            )
            self._update_scoreboard()
            self.root.after(450, self._resolve_challenges)

    def submit_claim(self) -> None:
        if self.game.finished:
            return
        if self.game.current_player is not self.game.players[0]:
            return
        if self._selected_card is None:
            self.status_var.set("Select a card from your hand first.")
            return
        rank = self.claim_rank_var.get().upper()
        try:
            claim = self.game.play_user_turn(self._selected_card, rank)
        except ValueError as exc:
            self.status_var.set(str(exc))
            return
        except RuntimeError as exc:
            self.status_var.set(str(exc))
            return

        card = claim.card
        self._log(f"You play {card} while stating it's a {claim.claimed_rank}.")
        self._last_claim_text.set(f"Latest claim: You said {claim.claimed_rank}.")
        self._selected_card = None
        self._set_user_controls_state(enabled=False)
        self._update_scoreboard()
        self.root.after(200, self._resolve_challenges)

    def _resolve_challenges(self) -> None:
        if self.game.finished:
            self.advance_game()
            return

        while self.game.phase == Phase.CHALLENGE and not self.game.finished:
            challenger = self.game.current_challenger
            if challenger is None:
                break
            claimant = self.game.claim_in_progress.claimant if self.game.claim_in_progress else None
            if challenger.is_user:
                if claimant:
                    self.status_var.set(
                        f"{claimant.name} insists they played a {self.game.claim_in_progress.claimed_rank}. Challenge?"
                    )
                self._set_challenge_controls_state(enabled=True)
                return

            decision = self.game.bot_should_challenge(challenger)
            if decision:
                self._log(f"{challenger.name} challenges the claim!")
            else:
                self._log(f"{challenger.name} decides to wait.")
            outcome = self.game.evaluate_challenge(decision)
            for line in outcome.messages:
                self._log(line)
            self._update_scoreboard()

        if self.game.phase != Phase.CHALLENGE:
            self.root.after(450, self.advance_game)

    def resolve_user_challenge(self, decision: bool) -> None:
        if self.game.phase != Phase.CHALLENGE:
            return
        challenger = self.game.current_challenger
        if challenger is None or not challenger.is_user:
            return

        self._set_challenge_controls_state(enabled=False)
        outcome = self.game.evaluate_challenge(decision)
        for line in outcome.messages:
            self._log(line)
        self._update_scoreboard()

        if self.game.phase == Phase.CHALLENGE:
            self.root.after(350, self._resolve_challenges)
        else:
            self.root.after(450, self.advance_game)

    def _handle_game_end(self) -> None:
        self._set_user_controls_state(enabled=False)
        self._set_challenge_controls_state(enabled=False)
        if self.game.winner is None:
            self.status_var.set("The match ends in a tie.")
            self._log("The table shares the honours—no single winner.")
        elif self.game.winner.is_user:
            self.status_var.set("You emptied your hand! Victory is yours.")
            self._log("Congratulations, you outfoxed every bluff.")
        else:
            self.status_var.set(f"{self.game.winner.name} wins the match.")
            self._log(f"{self.game.winner.name} finishes with the fewest cards.")


def run_gui(difficulty: DifficultyLevel, *, rounds: int, seed: int | None = None) -> None:
    rng = random.Random(seed) if seed is not None else random.Random()
    game = BluffGame(difficulty, rounds=rounds, rng=rng)
    root = tk.Tk()
    BluffGUI(root, game)
    root.mainloop()
