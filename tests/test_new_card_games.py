"""Tests for newly implemented card games."""

from __future__ import annotations

from card_games.bridge import BridgeGame, BridgePlayer
from card_games.gin_rummy import GinRummyGame, GinRummyPlayer
from card_games.hearts import HeartsGame, HeartsPlayer
from card_games.solitaire import SolitaireGame
from card_games.spades import SpadesGame, SpadesPlayer


class TestSolitaire:
    """Test Solitaire (Klondike) game."""

    def test_game_initialization(self):
        """Test that a solitaire game initializes correctly."""
        game = SolitaireGame()

        assert len(game.foundations) == 4
        assert len(game.tableau) == 7
        assert game.stock is not None
        assert game.waste is not None

    def test_tableau_setup(self):
        """Test that tableau is set up correctly."""
        game = SolitaireGame()

        # Verify tableau has correct number of cards
        for i, pile in enumerate(game.tableau):
            assert len(pile.cards) == i + 1
            assert pile.face_up_count == 1

    def test_draw_from_stock(self):
        """Test drawing from stock."""
        game = SolitaireGame()
        initial_stock = len(game.stock.cards)
        initial_waste = len(game.waste.cards)

        result = game.draw_from_stock()

        assert result is True
        assert len(game.stock.cards) == initial_stock - 1
        assert len(game.waste.cards) == initial_waste + 1

    def test_is_won(self):
        """Test win detection."""
        game = SolitaireGame()

        # Initially not won
        assert game.is_won() is False

        # Simulate winning condition
        from card_games.common.cards import Card, Suit

        for foundation in game.foundations:
            foundation.cards = [Card(r, Suit.HEARTS) for r in ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"]]

        assert game.is_won() is True


class TestHearts:
    """Test Hearts game."""

    def test_game_initialization(self):
        """Test that a hearts game initializes correctly."""
        players = [HeartsPlayer(f"Player {i}", is_ai=True) for i in range(4)]
        game = HeartsGame(players)

        assert len(game.players) == 4
        assert game.hearts_broken is False

    def test_deal_cards(self):
        """Test card dealing."""
        players = [HeartsPlayer(f"Player {i}", is_ai=True) for i in range(4)]
        game = HeartsGame(players)
        game.deal_cards()

        for player in players:
            assert len(player.hand) == 13

    def test_calculate_round_points(self):
        """Test round points calculation."""
        player = HeartsPlayer("Test", is_ai=True)
        from card_games.common.cards import Card, Suit

        # Add some hearts and queen of spades
        player.tricks_won = [
            Card("2", Suit.HEARTS),
            Card("3", Suit.HEARTS),
            Card("Q", Suit.SPADES),
        ]

        points = player.calculate_round_points()
        assert points == 15  # 2 hearts + 13 for queen

    def test_shooting_the_moon(self):
        """Test shooting the moon detection."""
        players = [HeartsPlayer(f"Player {i}", is_ai=True) for i in range(4)]
        game = HeartsGame(players)

        from card_games.common.cards import Card, Suit

        # Give one player all hearts and queen of spades
        players[0].tricks_won = [Card(r, Suit.HEARTS) for r in ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]]
        players[0].tricks_won.append(Card("Q", Suit.SPADES))

        # Before calculating scores, check points
        points_0 = players[0].calculate_round_points()
        assert points_0 == 26  # Shot the moon

        # Calculate scores
        game.calculate_scores()

        # Shooter gets 0, others get 26
        assert players[0].score == 0
        assert players[1].score == 26


class TestSpades:
    """Test Spades game."""

    def test_game_initialization(self):
        """Test that a spades game initializes correctly."""
        players = [SpadesPlayer(f"Player {i}", is_ai=True) for i in range(4)]
        game = SpadesGame(players)

        assert len(game.players) == 4
        assert game.spades_broken is False

        # Check partnerships
        assert game.players[0].partner_index == 2
        assert game.players[1].partner_index == 3

    def test_deal_cards(self):
        """Test card dealing."""
        players = [SpadesPlayer(f"Player {i}", is_ai=True) for i in range(4)]
        game = SpadesGame(players)
        game.deal_cards()

        for player in players:
            assert len(player.hand) == 13

    def test_suggest_bid(self):
        """Test AI bidding."""
        players = [SpadesPlayer(f"Player {i}", is_ai=True) for i in range(4)]
        game = SpadesGame(players)
        game.deal_cards()

        bid = game.suggest_bid(players[0])
        assert 0 <= bid <= 13


class TestGinRummy:
    """Test Gin Rummy game."""

    def test_game_initialization(self):
        """Test that a gin rummy game initializes correctly."""
        players = [GinRummyPlayer(f"Player {i}", is_ai=True) for i in range(2)]
        game = GinRummyGame(players)

        assert len(game.players) == 2

    def test_deal_cards(self):
        """Test card dealing."""
        players = [GinRummyPlayer(f"Player {i}", is_ai=True) for i in range(2)]
        game = GinRummyGame(players)
        game.deal_cards()

        for player in players:
            assert len(player.hand) == 10

        # Check discard pile has one card
        assert len(game.discard_pile) == 1

    def test_find_melds(self):
        """Test meld detection."""
        players = [GinRummyPlayer("Player", is_ai=True) for _ in range(2)]
        game = GinRummyGame(players)

        from card_games.common.cards import Card, Suit

        # Create a set of three
        cards = [
            Card("5", Suit.HEARTS),
            Card("5", Suit.DIAMONDS),
            Card("5", Suit.CLUBS),
        ]

        melds = game.find_melds(cards)
        assert len(melds) >= 1

    def test_calculate_deadwood(self):
        """Test deadwood calculation."""
        players = [GinRummyPlayer("Player", is_ai=True) for _ in range(2)]
        game = GinRummyGame(players)

        from card_games.common.cards import Card, Suit

        players[0].hand = [
            Card("A", Suit.HEARTS),
            Card("2", Suit.HEARTS),
        ]

        deadwood = game.calculate_deadwood(players[0])
        assert deadwood == 3  # Ace=1, 2=2


class TestBridge:
    """Test Bridge game."""

    def test_game_initialization(self):
        """Test that a bridge game initializes correctly."""
        players = [BridgePlayer(f"Player {i}", is_ai=True) for i in range(4)]
        game = BridgeGame(players)

        assert len(game.players) == 4

        # Check positions
        positions = [p.position for p in game.players]
        assert positions == ["N", "S", "E", "W"]

        # Check partnerships
        assert game.players[0].partner_index == 2  # N-S
        assert game.players[1].partner_index == 3  # E-W

    def test_deal_cards(self):
        """Test card dealing."""
        players = [BridgePlayer(f"Player {i}", is_ai=True) for i in range(4)]
        game = BridgeGame(players)
        game.deal_cards()

        for player in players:
            assert len(player.hand) == 13

    def test_evaluate_hand(self):
        """Test HCP calculation."""
        players = [BridgePlayer("Player", is_ai=True) for _ in range(4)]
        game = BridgeGame(players)

        from card_games.common.cards import Card, Suit

        players[0].hand = [
            Card("A", Suit.HEARTS),  # 4 points
            Card("K", Suit.DIAMONDS),  # 3 points
            Card("Q", Suit.CLUBS),  # 2 points
            Card("J", Suit.SPADES),  # 1 point
        ]

        hcp = game.evaluate_hand(players[0])
        assert hcp == 10
