import pathlib
import random
import sys

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from paper_games.dots_and_boxes import DotsAndBoxes


def test_computer_takes_bonus_turns_until_no_scoring_moves():
    game = DotsAndBoxes(size=1, rng=random.Random(0))
    # Human draws three sides of the single box.
    assert game.claim_edge("h", 0, 0, game.human_name) == 0
    assert game.claim_edge("v", 0, 0, game.human_name) == 0
    assert game.claim_edge("h", 1, 0, game.human_name) == 0

    moves = game.computer_turn()
    assert moves == [(("v", 0, 1), 1)]

    assert game.scores[game.computer_name] == 1
    assert game.is_finished()


def test_computer_opens_shortest_chain_when_forced():
    game = DotsAndBoxes(size=2, rng=random.Random(0))
    # Replicate the pre-computed state with varying chain penalties.
    preset_edges = [
        ("h", 1, 0),
        ("h", 1, 1),
        ("h", 2, 0),
        ("h", 2, 1),
        ("v", 0, 1),
    ]
    for orient, row, col in preset_edges:
        if orient == "h":
            game.horizontal_edges[(row, col)] = game.human_name
        else:
            game.vertical_edges[(row, col)] = game.human_name

    moves = game.computer_turn()
    assert moves, "Computer should make exactly one move in this forced state."
    first_move, completed = moves[0]
    assert first_move == ("h", 0, 0)
    assert completed == 0
    # Ensure no additional edges were drawn because the computer had to give up the turn.
    assert len(moves) == 1
