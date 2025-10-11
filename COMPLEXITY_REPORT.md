# Code Complexity Analysis Report

This document provides an analysis of code complexity across the repository and recommendations for future improvements.

Generated: 2025-10-11

## Summary

The codebase has been analyzed using Radon for cyclomatic complexity and maintainability index.

### Complexity Ratings

- **Target:** All functions/methods should have complexity ≤ 10
- **Current State:** Several functions exceed this threshold

### High Complexity Functions (C or higher)

These functions should be considered for refactoring:

#### Critical (D-E-F ratings: 21+)

1. **`paper_games/nim/cli.py:play_classic_nim`** - E (40)
   - Very high complexity, main game loop with many nested conditions
   - Recommendation: Split into separate functions for setup, game loop, and turn handling

2. **`paper_games/tic_tac_toe/cli.py:play`** - D (28)
   - High complexity in main game loop
   - Recommendation: Extract functions for input handling, display updates, and turn logic

3. **`paper_games/battleship/cli.py:_game_loop`** - D (28)
   - Complex game loop with multiple phases
   - Recommendation: Split into phase-specific functions

4. **`paper_games/tic_tac_toe/tic_tac_toe.py:TicTacToeGame.winner`** - D (25)
   - Complex winner detection logic
   - Recommendation: Extract helper functions for checking rows, columns, diagonals

5. **`paper_games/hangman/cli.py:_play_multiplayer`** - D (24)
   - Complex multiplayer logic
   - Recommendation: Split into player setup, turn handling, and scoring

6. **`paper_games/unscramble/cli.py:_play_multiplayer`** - D (23)
   - Complex multiplayer game flow
   - Recommendation: Extract turn logic and scoring to separate functions

7. **`paper_games/tic_tac_toe/ultimate_cli.py:play_ultimate`** - D (21)
   - Complex UI and game loop
   - Recommendation: Separate UI rendering from game logic

#### Moderate-High (C rating: 11-20)

8. **`paper_games/battleship/gui.py:BattleshipGUI._draw_board`** - C (18)
9. **`paper_games/dots_and_boxes/tournament.py:Tournament.play_game`** - C (17)
10. **`paper_games/nim/nim.py:NimGame.computer_move`** - C (17)
11. **`paper_games/unscramble/unscramble.py:load_words_by_difficulty`** - C (16)
12. **`paper_games/battleship/battleship.py:BattleshipGame.ai_shoot`** - C (15)
13. **`paper_games/tic_tac_toe/network_cli.py:play_network_client`** - C (15)
14. **`paper_games/tic_tac_toe/network_cli.py:play_network_server`** - C (14)
15. **`paper_games/battleship/gui.py:BattleshipGUI._on_opponent_canvas_click`** - C (14)
16. **`paper_games/tic_tac_toe/tic_tac_toe.py:TicTacToeGame.minimax`** - C (14)
17. **`paper_games/tic_tac_toe/ultimate.py:UltimateTicTacToeGame.render`** - C (13)
18. **`paper_games/dots_and_boxes/network.py:play_network_game`** - C (13)
19. **`paper_games/nim/nim.py:NimGame.get_strategy_hint`** - C (13)
20. **`paper_games/unscramble/stats.py:GameStats.record_word`** - C (13)
21. **`paper_games/unscramble/stats.py:GameStats.summary`** - C (13)

### Low Maintainability (MI < 20)

These files have low maintainability scores:

1. **`card_games/uno/uno.py`** - MI: 0.00 (very low)
2. **`card_games/poker/poker.py`** - MI: 0.87 (very low)
3. **`card_games/bluff/bluff.py`** - MI: 4.22 (very low)
4. **`card_games/blackjack/game.py`** - MI: 17.97 (low)

**Note:** These are complex game engines with extensive logic. While they have low MI scores, they are well-documented and have comprehensive test coverage.

## Refactoring Priorities

### High Priority (Critical Complexity)

1. **Nim CLI** (`paper_games/nim/cli.py:play_classic_nim`)
   - Complexity: 40 (E rating)
   - Impact: High - main game function
   - Effort: Medium - can be split into logical sections

2. **Tic Tac Toe CLI** (`paper_games/tic_tac_toe/cli.py:play`)
   - Complexity: 28 (D rating)
   - Impact: High - main game function
   - Effort: Medium

3. **Battleship CLI** (`paper_games/battleship/cli.py:_game_loop`)
   - Complexity: 28 (D rating)
   - Impact: High - core game loop
   - Effort: High - complex state management

### Medium Priority (Moderate Complexity)

4. **AI Functions** (various `computer_move` functions)
   - Complexity: 15-17 (C rating)
   - Impact: Medium - affects gameplay
   - Effort: Low-Medium - can extract decision logic

5. **Rendering Functions** (various `render` functions)
   - Complexity: 11-13 (C rating)
   - Impact: Low - display only
   - Effort: Low - can split into helper functions

### Low Priority (Acceptable Complexity)

Functions with complexity 11-13 (C rating) are acceptable but could be improved:
- Network play functions
- Tournament management
- Statistics tracking

## Recommended Refactoring Patterns

### 1. Extract Method

**Before:**
```python
def complex_function():
    # Setup code
    # Validation code
    # Main logic
    # Cleanup code
    pass
```

**After:**
```python
def complex_function():
    _setup()
    _validate()
    _execute_logic()
    _cleanup()

def _setup(): ...
def _validate(): ...
def _execute_logic(): ...
def _cleanup(): ...
```

### 2. State Machine Pattern

For CLI game loops with multiple phases:

```python
class GameState(Enum):
    SETUP = "setup"
    PLAYING = "playing"
    GAME_OVER = "game_over"

def play():
    state = GameState.SETUP
    while state != GameState.GAME_OVER:
        if state == GameState.SETUP:
            state = handle_setup()
        elif state == GameState.PLAYING:
            state = handle_turn()
```

### 3. Strategy Pattern

Already implemented in `common/ai_strategy.py` - use for AI logic:

```python
from common import HeuristicStrategy

def ai_heuristic(move, state):
    return calculate_score(move, state)

ai = HeuristicStrategy(heuristic_fn=ai_heuristic)
move = ai.select_move(valid_moves, game_state)
```

### 4. Command Pattern

For user input handling:

```python
def handle_input(command: str):
    handlers = {
        'move': handle_move,
        'quit': handle_quit,
        'help': handle_help,
    }
    handler = handlers.get(command, handle_invalid)
    return handler()
```

## Monitoring

### Automated Checks

Pre-commit hooks now include complexity checks via Ruff:

```yaml
[tool.ruff.lint.mccabe]
max-complexity = 10
```

### Manual Analysis

Run the complexity check script:

```bash
./scripts/check_complexity.sh
```

### CI Integration (Recommended)

Add to CI pipeline:

```yaml
- name: Check Complexity
  run: |
    pip install radon
    radon cc . -a -n C --exclude="tests/*,colorama/*"
    # Fail if any function has complexity > 20
    radon cc . -n D --exclude="tests/*,colorama/*" && exit 1 || exit 0
```

## Guidelines for New Code

1. **Target complexity ≤ 10** for all new functions
2. **Extract helpers** when approaching the limit
3. **Use base classes** from `common/` module
4. **Run checks** before committing:
   ```bash
   pre-commit run --all-files
   ./scripts/check_complexity.sh
   ```

## Benefits of Refactoring

- **Easier to understand** - Smaller functions are easier to read
- **Easier to test** - Small functions can be tested in isolation
- **Easier to modify** - Changes have limited scope
- **Fewer bugs** - Simpler code has fewer edge cases
- **Better performance** - Easier to optimize small functions

## Next Steps

1. **Address critical complexity** (E-D ratings) in future PRs
2. **Use base classes** for new games
3. **Monitor complexity** in code reviews
4. **Document complex logic** when refactoring isn't feasible
5. **Add tests** before refactoring to ensure behavior preservation

## Conclusion

While some legacy code has high complexity, the project now has:
- ✅ Tools to measure complexity
- ✅ Guidelines for new code
- ✅ Base classes to reduce duplication
- ✅ Automated checks to prevent regression
- ✅ Clear priorities for future refactoring

The focus should be on keeping new code simple while gradually improving existing code as opportunities arise.
