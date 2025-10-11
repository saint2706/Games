"""Entry point for Hearts card game."""

from card_games.hearts.cli import game_loop


def main() -> None:
    """Main entry point for Hearts game."""
    game_loop()


if __name__ == "__main__":
    main()
