"""Entry point for Bridge card game."""

from card_games.bridge.cli import game_loop


def main() -> None:
    """Main entry point for Bridge game."""
    game_loop()


if __name__ == "__main__":
    main()
