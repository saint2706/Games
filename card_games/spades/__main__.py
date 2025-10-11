"""Entry point for Spades card game."""

from card_games.spades.cli import game_loop


def main() -> None:
    """Main entry point for Spades game."""
    game_loop()


if __name__ == "__main__":
    main()
