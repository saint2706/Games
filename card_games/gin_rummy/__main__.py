"""Entry point for Gin Rummy card game."""

from card_games.gin_rummy.cli import game_loop


def main() -> None:
    """Main entry point for Gin Rummy game."""
    game_loop()


if __name__ == "__main__":
    main()
