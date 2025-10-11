"""Hearts game engine.

Hearts is a trick-taking card game where the goal is to avoid taking hearts and
the Queen of Spades (which are worth penalty points). However, a player who takes
ALL the hearts and the Queen of Spades "shoots the moon" and instead gives 26 points
to all other players.

The game includes:
- Passing cards phase (3 cards passed in rotating directions)
- Trick-taking with hearts and Queen of Spades as penalty cards
- Shooting the moon detection and scoring
- AI that tries to avoid hearts
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional

from card_games.common.cards import Card, Deck, Suit


class PassDirection(Enum):
    """Direction to pass cards in Hearts."""

    LEFT = auto()
    RIGHT = auto()
    ACROSS = auto()
    NONE = auto()  # No passing on 4th hand


@dataclass
class HeartsPlayer:
    """Represents a player in Hearts.

    Attributes:
        name: Player's name
        hand: Cards currently in hand
        tricks_won: Cards won in tricks this round
        score: Total score across all rounds
        is_ai: Whether this is an AI player
    """

    name: str
    hand: list[Card] = field(default_factory=list)
    tricks_won: list[Card] = field(default_factory=list)
    score: int = 0
    is_ai: bool = False

    def has_suit(self, suit: Suit) -> bool:
        """Check if player has any cards of the given suit."""
        return any(card.suit == suit for card in self.hand)

    def has_only_hearts(self) -> bool:
        """Check if player has only hearts in hand."""
        return all(card.suit == Suit.HEARTS for card in self.hand)

    def calculate_round_points(self) -> int:
        """Calculate points for this round based on tricks won.

        Returns:
            Points (higher is worse in Hearts).
        """
        points = 0
        for card in self.tricks_won:
            if card.suit == Suit.HEARTS:
                points += 1
            elif card.suit == Suit.SPADES and card.rank == "Q":
                points += 13
        return points


class HeartsGame:
    """Main engine for the Hearts card game.

    This class manages the game flow including dealing, passing cards,
    trick-taking, and scoring.
    """

    def __init__(self, players: list[HeartsPlayer], *, rng=None):
        """Initialize a Hearts game.

        Args:
            players: List of 4 players
            rng: Optional random number generator
        """
        if len(players) != 4:
            raise ValueError("Hearts requires exactly 4 players")

        self.players = players
        self.rng = rng
        self.deck = Deck()
        self.round_number = 0
        self.hearts_broken = False
        self.current_trick: list[tuple[HeartsPlayer, Card]] = []
        self.lead_suit: Optional[Suit] = None

    def deal_cards(self) -> None:
        """Deal all 52 cards evenly to 4 players (13 each)."""
        self.deck = Deck()
        if self.rng:
            self.deck.shuffle(rng=self.rng)
        else:
            self.deck.shuffle()

        # Clear hands and tricks
        for player in self.players:
            player.hand = []
            player.tricks_won = []

        # Deal 13 cards to each player
        for _ in range(13):
            for player in self.players:
                player.hand.append(self.deck.deal(1)[0])

        # Sort hands by suit and rank
        for player in self.players:
            player.hand.sort(key=lambda c: (c.suit.value, c.value))

    def get_pass_direction(self) -> PassDirection:
        """Get the passing direction for the current round.

        Returns:
            PassDirection based on round number (cycles every 4 rounds).
        """
        directions = [PassDirection.LEFT, PassDirection.RIGHT, PassDirection.ACROSS, PassDirection.NONE]
        return directions[self.round_number % 4]

    def pass_cards(self, passes: dict[HeartsPlayer, list[Card]]) -> None:
        """Execute the card passing phase.

        Args:
            passes: Dictionary mapping each player to 3 cards they want to pass.
        """
        direction = self.get_pass_direction()

        if direction == PassDirection.NONE:
            return

        # Validate passes
        for player, cards in passes.items():
            if len(cards) != 3:
                raise ValueError(f"{player.name} must pass exactly 3 cards")
            for card in cards:
                if card not in player.hand:
                    raise ValueError(f"{player.name} doesn't have {card}")

        # Remove cards from hands
        temp_passes = {}
        for player, cards in passes.items():
            temp_passes[player] = cards
            for card in cards:
                player.hand.remove(card)

        # Give cards to recipients
        for i, player in enumerate(self.players):
            if direction == PassDirection.LEFT:
                recipient = self.players[(i + 1) % 4]
            elif direction == PassDirection.RIGHT:
                recipient = self.players[(i - 1) % 4]
            else:  # ACROSS
                recipient = self.players[(i + 2) % 4]

            recipient.hand.extend(temp_passes[player])

        # Sort hands again
        for player in self.players:
            player.hand.sort(key=lambda c: (c.suit.value, c.value))

    def find_starting_player(self) -> HeartsPlayer:
        """Find the player with the 2 of Clubs (starts the game).

        Returns:
            The player who has the 2 of Clubs.
        """
        two_of_clubs = Card("2", Suit.CLUBS)
        for player in self.players:
            if two_of_clubs in player.hand:
                return player
        raise RuntimeError("No player has 2 of Clubs")

    def is_valid_play(self, player: HeartsPlayer, card: Card) -> bool:
        """Check if a card play is valid.

        Args:
            player: The player attempting to play
            card: The card to play

        Returns:
            True if the play is valid, False otherwise.
        """
        if card not in player.hand:
            return False

        # First trick: must play 2 of Clubs if you have it
        if not any(p.tricks_won for p in self.players):
            if not self.current_trick:
                return card == Card("2", Suit.CLUBS)
            # Can't play hearts or Queen of Spades on first trick
            if card.suit == Suit.HEARTS:
                return False
            if card.suit == Suit.SPADES and card.rank == "Q":
                return False

        # Leading a trick
        if not self.current_trick:
            # Can't lead hearts unless hearts broken or only have hearts
            if card.suit == Suit.HEARTS:
                return self.hearts_broken or player.has_only_hearts()
            return True

        # Following a trick: must follow suit if possible
        if self.lead_suit and player.has_suit(self.lead_suit):
            return card.suit == self.lead_suit

        return True

    def play_card(self, player: HeartsPlayer, card: Card) -> None:
        """Play a card to the current trick.

        Args:
            player: The player playing the card
            card: The card to play
        """
        if not self.is_valid_play(player, card):
            raise ValueError(f"Invalid play: {player.name} cannot play {card}")

        player.hand.remove(card)
        self.current_trick.append((player, card))

        # Set lead suit for this trick
        if len(self.current_trick) == 1:
            self.lead_suit = card.suit

        # Break hearts if a heart is played
        if card.suit == Suit.HEARTS:
            self.hearts_broken = True

    def complete_trick(self) -> HeartsPlayer:
        """Complete the current trick and determine the winner.

        Returns:
            The player who won the trick.
        """
        if len(self.current_trick) != 4:
            raise RuntimeError("Trick is not complete")

        # Find highest card of lead suit
        winner = self.current_trick[0][0]
        winning_card = self.current_trick[0][1]

        for player, card in self.current_trick[1:]:
            if card.suit == self.lead_suit and card.value > winning_card.value:
                winner = player
                winning_card = card

        # Give all cards to winner
        for _, card in self.current_trick:
            winner.tricks_won.append(card)

        # Reset for next trick
        self.current_trick = []
        self.lead_suit = None

        return winner

    def calculate_scores(self) -> dict[str, int]:
        """Calculate scores for the round and check for shooting the moon.

        Returns:
            Dictionary mapping player names to their points for this round.
        """
        round_scores = {}
        for player in self.players:
            round_scores[player.name] = player.calculate_round_points()

        # Check for shooting the moon
        shooter = None
        for player in self.players:
            if round_scores[player.name] == 26:
                shooter = player
                break

        if shooter:
            # This player shot the moon!
            # Give 26 points to everyone else, 0 to shooter
            for player in self.players:
                if player == shooter:
                    round_scores[player.name] = 0
                    player.score += 0
                else:
                    round_scores[player.name] = 26
                    player.score += 26
        else:
            # Normal scoring
            for player in self.players:
                player.score += round_scores[player.name]

        return round_scores

    def is_game_over(self, target_score: int = 100) -> bool:
        """Check if the game is over.

        Args:
            target_score: Score at which game ends (default 100).

        Returns:
            True if any player has reached the target score.
        """
        return any(player.score >= target_score for player in self.players)

    def get_winner(self) -> HeartsPlayer:
        """Get the winner (player with lowest score).

        Returns:
            The winning player.
        """
        return min(self.players, key=lambda p: p.score)

    def get_valid_plays(self, player: HeartsPlayer) -> list[Card]:
        """Get all valid cards a player can play.

        Args:
            player: The player to check

        Returns:
            List of valid cards to play.
        """
        return [card for card in player.hand if self.is_valid_play(player, card)]

    def select_cards_to_pass(self, player: HeartsPlayer) -> list[Card]:
        """AI logic to select 3 cards to pass.

        Args:
            player: The player (AI) selecting cards

        Returns:
            List of 3 cards to pass.
        """
        # Strategy: pass high cards, especially Queen of Spades, King/Ace of hearts
        priority = []
        for card in player.hand:
            score = 0
            # Strongly prefer to pass Queen of Spades
            if card.suit == Suit.SPADES and card.rank == "Q":
                score += 100
            # Prefer high hearts
            if card.suit == Suit.HEARTS:
                score += card.value + 10
            # Prefer high cards in general
            if card.rank in ("A", "K"):
                score += 5
            priority.append((score, card))

        # Sort by priority (descending) and take top 3
        priority.sort(reverse=True, key=lambda x: x[0])
        return [card for _, card in priority[:3]]

    def select_card_to_play(self, player: HeartsPlayer) -> Card:
        """AI logic to select a card to play.

        Args:
            player: The player (AI) selecting a card

        Returns:
            The card to play.
        """
        valid_cards = self.get_valid_plays(player)

        if not valid_cards:
            raise RuntimeError(f"{player.name} has no valid plays")

        # If only one valid card, play it
        if len(valid_cards) == 1:
            return valid_cards[0]

        # Leading a trick: play low cards
        if not self.current_trick:
            # Avoid leading hearts if possible
            non_hearts = [c for c in valid_cards if c.suit != Suit.HEARTS]
            if non_hearts:
                return min(non_hearts, key=lambda c: c.value)
            return min(valid_cards, key=lambda c: c.value)

        # Following a trick
        lead_suit_cards = [c for c in valid_cards if c.suit == self.lead_suit]

        if lead_suit_cards:
            # Try to play low and not take the trick
            highest_so_far = max(card.value for _, card in self.current_trick if card.suit == self.lead_suit)

            # Play highest card that doesn't win
            safe_cards = [c for c in lead_suit_cards if c.value < highest_so_far]
            if safe_cards:
                return max(safe_cards, key=lambda c: c.value)

            # Must win - play lowest winning card
            return min(lead_suit_cards, key=lambda c: c.value)

        # Dumping: get rid of bad cards
        # Priority: Queen of Spades > High Hearts > High cards
        queen_of_spades = Card("Q", Suit.SPADES)
        if queen_of_spades in valid_cards:
            return queen_of_spades

        hearts = [c for c in valid_cards if c.suit == Suit.HEARTS]
        if hearts:
            return max(hearts, key=lambda c: c.value)

        return max(valid_cards, key=lambda c: c.value)
