import pathlib
import sys

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from paper_games.tic_tac_toe.tic_tac_toe import TicTacToeGame


def test_standard_3x3_board():
    """Test that standard 3x3 board still works."""
    game = TicTacToeGame()
    assert len(game.board) == 9
    assert game.board_size == 3
    assert game.win_length == 3


def test_4x4_board():
    """Test 4x4 board creation."""
    game = TicTacToeGame(board_size=4)
    assert len(game.board) == 16
    assert game.board_size == 4
    assert game.win_length == 4


def test_5x5_board():
    """Test 5x5 board creation."""
    game = TicTacToeGame(board_size=5)
    assert len(game.board) == 25
    assert game.board_size == 5
    assert game.win_length == 5


def test_custom_win_length():
    """Test custom win length."""
    game = TicTacToeGame(board_size=4, win_length=3)
    assert game.board_size == 4
    assert game.win_length == 3


def test_winner_horizontal_4x4():
    """Test horizontal winner detection on 4x4 board."""
    game = TicTacToeGame(board_size=4, win_length=3)
    game.make_move(0, 'X')  # A1
    game.make_move(1, 'X')  # A2
    game.make_move(2, 'X')  # A3
    assert game.winner() == 'X'


def test_winner_vertical_4x4():
    """Test vertical winner detection on 4x4 board."""
    game = TicTacToeGame(board_size=4, win_length=3)
    game.make_move(0, 'O')  # A1
    game.make_move(4, 'O')  # B1
    game.make_move(8, 'O')  # C1
    assert game.winner() == 'O'


def test_winner_diagonal_4x4():
    """Test diagonal winner detection on 4x4 board."""
    game = TicTacToeGame(board_size=4, win_length=3)
    game.make_move(0, 'X')  # A1
    game.make_move(5, 'X')  # B2
    game.make_move(10, 'X')  # C3
    assert game.winner() == 'X'


def test_winner_anti_diagonal_5x5():
    """Test anti-diagonal winner detection on 5x5 board."""
    game = TicTacToeGame(board_size=5, win_length=4)
    game.make_move(3, 'O')  # A4
    game.make_move(7, 'O')  # B3
    game.make_move(11, 'O')  # C2
    game.make_move(15, 'O')  # D1
    assert game.winner() == 'O'


def test_no_winner_partial_line():
    """Test that partial lines don't count as wins."""
    game = TicTacToeGame(board_size=4, win_length=3)
    game.make_move(0, 'X')  # A1
    game.make_move(1, 'X')  # A2
    assert game.winner() is None


def test_coordinate_parsing_4x4():
    """Test coordinate parsing for 4x4 board."""
    game = TicTacToeGame(board_size=4)
    assert game.parse_coordinate("A1") == 0
    assert game.parse_coordinate("A4") == 3
    assert game.parse_coordinate("D1") == 12
    assert game.parse_coordinate("D4") == 15


def test_coordinate_parsing_5x5():
    """Test coordinate parsing for 5x5 board."""
    game = TicTacToeGame(board_size=5)
    assert game.parse_coordinate("A1") == 0
    assert game.parse_coordinate("E5") == 24
    assert game.parse_coordinate("C3") == 12


def test_invalid_coordinate():
    """Test that invalid coordinates raise errors."""
    game = TicTacToeGame(board_size=4)
    try:
        game.parse_coordinate("E5")  # Out of bounds for 4x4
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


def test_render_4x4():
    """Test that 4x4 board renders correctly."""
    game = TicTacToeGame(board_size=4)
    rendered = game.render()
    assert "A" in rendered
    assert "D" in rendered
    assert "1" in rendered
    assert "4" in rendered


def test_available_moves_4x4():
    """Test available moves on 4x4 board."""
    game = TicTacToeGame(board_size=4)
    assert len(game.available_moves()) == 16
    game.make_move(0, 'X')
    assert len(game.available_moves()) == 15
    assert 0 not in game.available_moves()


def test_is_draw_4x4():
    """Test draw detection on 4x4 board."""
    game = TicTacToeGame(board_size=4, win_length=4)
    # Fill board in a pattern that prevents any wins
    # Pattern: XOXO / XOXO / OXOX / OXOX
    moves = [
        ('X', 0), ('O', 1), ('X', 2), ('O', 3),
        ('X', 4), ('O', 5), ('X', 6), ('O', 7),
        ('O', 8), ('X', 9), ('O', 10), ('X', 11),
        ('O', 12), ('X', 13), ('O', 14), ('X', 15),
    ]
    for symbol, pos in moves:
        game.make_move(pos, symbol)
    assert game.winner() is None
    assert game.is_draw()


def test_minimax_makes_move():
    """Test that minimax can find a move on larger board."""
    game = TicTacToeGame(board_size=4, win_length=3)
    score, move = game.minimax(True, max_depth=4)
    assert move is not None
    assert move in game.available_moves()


if __name__ == "__main__":
    # Run all tests
    test_functions = [
        test_standard_3x3_board,
        test_4x4_board,
        test_5x5_board,
        test_custom_win_length,
        test_winner_horizontal_4x4,
        test_winner_vertical_4x4,
        test_winner_diagonal_4x4,
        test_winner_anti_diagonal_5x5,
        test_no_winner_partial_line,
        test_coordinate_parsing_4x4,
        test_coordinate_parsing_5x5,
        test_invalid_coordinate,
        test_render_4x4,
        test_available_moves_4x4,
        test_is_draw_4x4,
        test_minimax_makes_move,
    ]
    
    for test_func in test_functions:
        try:
            test_func()
            print(f"✓ {test_func.__name__}")
        except AssertionError as e:
            print(f"✗ {test_func.__name__}: {e}")
        except Exception as e:
            print(f"✗ {test_func.__name__}: {e}")
    
    print("\nAll tests completed!")
