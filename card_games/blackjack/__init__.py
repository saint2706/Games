"""Blackjack game package."""

# Re-export core types so ``card_games.blackjack`` behaves like a facade for
# both the engine and the GUI helper functions.
from .game import BlackjackGame, BlackjackHand, Outcome
from .gui import BlackjackApp, run_app

__all__ = ["BlackjackGame", "BlackjackHand", "Outcome", "BlackjackApp", "run_app"]
