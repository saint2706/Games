# Agent Instructions for Games Repository

This file provides specialized instructions for AI coding agents (GitHub Copilot, OpenAI Codex) working in this repository. These instructions follow OpenAI Codex best practices for clear, actionable guidance.

## Agent Role and Context

**You are a Python game development specialist** working on a comprehensive games collection. Your primary responsibilities:

1. **Implement game logic** following established patterns
1. **Maintain code quality** with strict standards (complexity ≤ 10, type hints, docstrings)
1. **Write comprehensive tests** achieving 90%+ coverage
1. **Follow architectural patterns** from the `common/` module
1. **Preserve existing functionality** while making targeted improvements

## Repository Structure

```
card_games/      # Card game implementations (Poker, Blackjack, Uno, etc.)
paper_games/     # Board/pencil games (Chess, Tic-Tac-Toe, Sudoku, etc.)
dice_games/      # Dice-based games (Craps, Yahtzee, Farkle)
logic_games/     # Puzzle games (Sokoban, Minesweeper)
word_games/      # Word/trivia games (Crossword, Hangman)
common/          # Shared utilities, base classes, architectural patterns
tests/           # Comprehensive test suite
docs/            # Sphinx documentation
```

## Critical Code Quality Standards

### Python Requirements

- **Version**: 3.9+ with `from __future__ import annotations`
- **Line Length**: 160 characters maximum
- **Formatter**: Black (run `black .` before committing)
- **Linter**: Ruff with complexity checks (run `ruff check --fix .`)
- **Type Checker**: mypy with 95%+ coverage (run `mypy .`)

### Complexity Rules (CRITICAL)

- **Maximum Cyclomatic Complexity**: 10 per function (enforced)
- **Verification**: Run `./scripts/check_complexity.sh` before committing
- **Target**: A or B complexity rating (1-10 range)
- **Refactor immediately** if complexity exceeds 10

### Type Hints (REQUIRED)

Every function MUST have complete type hints:

```python
from __future__ import annotations

from typing import List, Optional, Dict, Tuple

def process_game_state(
    players: List[str],
    scores: Dict[str, int],
    round_num: int = 1
) -> Tuple[str, int]:
    """Process game state and return winner."""
    # Implementation
    pass
```

**Common types to use:**

- `List[T]`, `Dict[K, V]`, `Set[T]`, `Tuple[T, ...]`
- `Optional[T]` for nullable values
- `Union[A, B]` for multiple types
- Custom types from `typing` module

### Docstrings (REQUIRED - Google Style)

**All public functions, classes, and modules** must have docstrings:

```python
def calculate_score(items: List[int], multiplier: float = 1.0) -> int:
    """Calculate total score with multiplier.

    This function sums all item values and applies a multiplier.
    Used for final score calculation in multi-round games.

    Args:
        items: List of item values to sum. Each value must be non-negative.
        multiplier: Score multiplier applied to sum (default: 1.0).

    Returns:
        Total calculated score as integer, rounded down.

    Raises:
        ValueError: If multiplier is negative.
        TypeError: If items contains non-numeric values.

    Example:
        >>> calculate_score([10, 20, 30], 1.5)
        90
    """
    if multiplier < 0:
        raise ValueError("Multiplier must be non-negative")
    return int(sum(items) * multiplier)
```

## Architecture Patterns (FOLLOW STRICTLY)

### Standard Game Structure

**Every game MUST follow this exact structure:**

```
game_name/
├── __init__.py          # Package initialization, exports main classes
├── __main__.py          # Entry point: python -m package.game_name
├── game_name.py         # Core game logic (GameEngine subclass)
├── cli.py              # Command-line interface (optional)
├── gui.py              # Graphical interface (optional)
├── README.md           # Game-specific documentation with rules
└── tests/              # Or in top-level tests/game_name/
```

### Required Base Classes

**ALWAYS inherit from these base classes:**

1. **GameEngine** (`common/game_engine.py`)

   - Core game logic
   - State management
   - Move validation
   - Win/loss conditions

1. **BaseGUI** (`common/gui_base.py`)

   - GUI framework
   - Window management
   - Event handling
   - Common UI components

1. **HeuristicStrategy** (`common/ai_strategy.py`)

   - AI opponent logic
   - Position evaluation
   - Move selection
   - Difficulty levels

### Architectural Patterns Available

**USE these from `common/architecture/` when appropriate:**

| Pattern | File | Use When |
|---------|------|----------|
| Plugin System | `plugin.py` | Adding third-party games |
| Event-Driven | `events.py` | Decoupling components |
| Persistence | `persistence.py` | Save/load game state |
| Settings | `settings.py` | Managing configuration |
| Replay/Undo | `replay.py` | Recording game actions |
| Observer | `observer.py` | Syncing multiple views |

## Testing Requirements (MANDATORY)

### Coverage Goals

- **Framework**: pytest (exclusively)
- **Current Coverage**: 30%+ (increasing to 90%+)
- **NEW CODE REQUIREMENT**: 90%+ coverage for all new code
- **Run Tests**: `pytest -v` (verbose) or `pytest --cov` (with coverage)
- **Coverage Report**: `pytest --cov=card_games --cov=paper_games --cov-report=html`

### Test Organization

```
tests/
├── fixtures/              # Reusable test data
├── test_card_games/       # Card game tests
├── test_paper_games/      # Paper game tests
├── test_common/           # Common module tests
└── conftest.py           # Shared pytest configuration
```

### Required Test Types

**For every game, write:**

1. **Initialization Tests** - Verify correct setup
1. **Valid Move Tests** - Test accepted moves
1. **Invalid Move Tests** - Test rejected moves
1. **Win Condition Tests** - Test game-over scenarios
1. **Edge Case Tests** - Test boundary conditions
1. **Integration Tests** - Test full game flow

### Test Template

```python
"""Test suite for MyGame.

Tests cover initialization, move validation, game logic,
win conditions, and edge cases.
"""
from __future__ import annotations

import pytest
from my_game.my_game import MyGame

class TestMyGameInitialization:
    """Test game initialization."""

    def test_default_initialization(self):
        """Test game initializes with default settings."""
        game = MyGame()
        assert game is not None
        assert game.current_player == 0

    def test_custom_players(self):
        """Test initialization with custom player count."""
        game = MyGame(num_players=4)
        assert len(game.players) == 4

class TestMyGameMoves:
    """Test move validation and execution."""

    @pytest.fixture
    def game(self):
        """Create game instance for testing."""
        game = MyGame()
        game.start()
        return game

    def test_valid_move_accepted(self, game):
        """Test that valid move is accepted and applied."""
        result = game.make_move("A1")
        assert result is True
        assert game.move_count == 1

    def test_invalid_move_rejected(self, game):
        """Test that invalid move is rejected."""
        result = game.make_move("invalid")
        assert result is False
        assert game.move_count == 0

    @pytest.mark.parametrize("move,expected", [
        ("A1", True),
        ("B2", True),
        ("Z9", False),
    ])
    def test_move_validation(self, game, move, expected):
        """Test multiple move scenarios."""
        assert game.is_valid_move(move) == expected

class TestMyGameWinConditions:
    """Test game-over scenarios."""

    def test_player_wins(self):
        """Test win condition detection."""
        game = MyGame()
        game.start()
        # Set up winning state
        assert game.is_game_over() is True
        assert game.get_winner() == 0
```

## Development Workflow (STEP-BY-STEP)

### Phase 1: Planning (Before Writing Code)

1. **Research existing implementations**

   ```bash
   # Find similar games
   ls card_games/ paper_games/ dice_games/
   # Review their structure
   ```

1. **Review documentation**

   - `docs/architecture/ARCHITECTURE.md` - Design patterns
   - `docs/development/CODE_QUALITY.md` - Quality standards
   - `CONTRIBUTING.md` - Contribution guidelines
   - Game-specific READMEs in each package

1. **Plan complexity strategy**

   - Break complex logic into functions ≤10 complexity
   - Identify reusable patterns from `common/`
   - Plan test scenarios

### Phase 2: Implementation (During Coding)

**REQUIRED ACTIONS for every code change:**

1. **Add type hints** to all functions (no exceptions)
1. **Write docstrings** (Google style) for public APIs
1. **Check complexity** after each function:
   ```bash
   radon cc path/to/file.py -s
   ```
1. **Keep functions simple** - refactor if complexity > 10
1. **Write tests** alongside code (TDD preferred)

### Phase 3: Validation (Before Committing)

**Run these checks in order:**

```bash
# 1. Format code (auto-fixes)
black .

# 2. Sort imports (auto-fixes)
isort .

# 3. Lint and fix issues (auto-fixes when possible)
ruff check --fix .

# 4. Check complexity (manual check)
./scripts/check_complexity.sh

# 5. Type check (no auto-fix)
mypy .

# 6. Run tests (with coverage)
pytest --cov

# 7. Run all pre-commit hooks
pre-commit run --all-files
```

### Pre-commit Hooks (Automatic)

These run automatically on `git commit`:

- ✅ Black formatting
- ✅ Ruff linting
- ✅ isort import sorting
- ✅ mypy type checking
- ✅ YAML/JSON validation
- ✅ Trailing whitespace removal
- ✅ End-of-file fixer
- ✅ Large file detection
- ✅ Merge conflict detection

**If hooks fail:** Fix issues and commit again

## Implementation Patterns (COPY THESE)

### Pattern 1: Game Engine (REQUIRED)

**Every game MUST implement this pattern:**

```python
"""MyGame implementation.

This module implements MyGame with support for:
- 2-4 players
- Standard rules with variations
- AI opponents with difficulty levels
- CLI and GUI interfaces

Game Rules:
1. [Describe rule 1]
2. [Describe rule 2]
...

Usage:
    python -m package_name.my_game
    
    from package_name.my_game import MyGame
    game = MyGame(num_players=2)
    game.start()
"""
from __future__ import annotations

from typing import List, Optional
from dataclasses import dataclass

from common import GameEngine

@dataclass
class GameState:
    """Immutable game state representation."""
    players: List[str]
    current_player: int
    board: List[List[str]]
    move_count: int

class MyGame(GameEngine[GameState, str]):
    """Game engine for MyGame.
    
    Manages game state, validates moves, and determines winners.
    """

    def __init__(self, num_players: int = 2) -> None:
        """Initialize game with specified number of players.
        
        Args:
            num_players: Number of players (2-4).
            
        Raises:
            ValueError: If num_players not in valid range.
        """
        super().__init__()
        if not 2 <= num_players <= 4:
            raise ValueError("num_players must be 2-4")
        self.num_players = num_players
        self._initialize_state()

    def _initialize_state(self) -> None:
        """Initialize game state. Complexity: 3"""
        self.state = GameState(
            players=[f"Player {i+1}" for i in range(self.num_players)],
            current_player=0,
            board=[["" for _ in range(3)] for _ in range(3)],
            move_count=0
        )

    def is_valid_move(self, move: str) -> bool:
        """Check if move is valid in current state.
        
        Args:
            move: Move to validate (e.g., "A1", "B2").
            
        Returns:
            True if move is valid, False otherwise.
        """
        # Validation logic (keep complexity ≤ 10)
        return True

    def make_move(self, move: str) -> bool:
        """Execute a move if valid.
        
        Args:
            move: Move to execute.
            
        Returns:
            True if move executed successfully, False otherwise.
        """
        if not self.is_valid_move(move):
            return False
        # Apply move and update state
        self.state.move_count += 1
        return True

    def is_game_over(self) -> bool:
        """Check if game has ended.
        
        Returns:
            True if game is over, False otherwise.
        """
        # Check win/draw conditions
        return False

    def get_winner(self) -> Optional[int]:
        """Return winner index or None.
        
        Returns:
            Winner player index (0-based), or None if no winner yet.
        """
        if not self.is_game_over():
            return None
        # Determine winner
        return None
```

### Pattern 2: AI Strategy (RECOMMENDED)

```python
from __future__ import annotations

from typing import List
from common import HeuristicStrategy

def evaluate_position(state: GameState) -> float:
    """Evaluate game position for current player.
    
    Heuristic considers:
    - Material advantage (pieces, cards, etc.)
    - Positional strength
    - Winning probability
    
    Args:
        state: Current game state.
        
    Returns:
        Score in range [-1.0, 1.0] where positive favors current player.
    """
    score = 0.0
    
    # Evaluate material advantage
    material = _evaluate_material(state)
    score += material * 0.5
    
    # Evaluate position
    position = _evaluate_position(state)
    score += position * 0.3
    
    # Evaluate winning probability
    win_prob = _evaluate_win_probability(state)
    score += win_prob * 0.2
    
    return max(-1.0, min(1.0, score))

def _evaluate_material(state: GameState) -> float:
    """Evaluate material advantage. Complexity: 4"""
    # Implementation
    pass

def _evaluate_position(state: GameState) -> float:
    """Evaluate positional strength. Complexity: 5"""
    # Implementation
    pass

def _evaluate_win_probability(state: GameState) -> float:
    """Evaluate winning probability. Complexity: 6"""
    # Implementation
    pass

# Create AI strategy with heuristic
ai_strategy = HeuristicStrategy(heuristic_fn=evaluate_position)

# Use in game
best_move = ai_strategy.choose_move(game.state, game.get_valid_moves())
```

### Pattern 3: GUI Implementation (OPTIONAL)

```python
from __future__ import annotations

import tkinter as tk
from typing import Optional

from common import BaseGUI
from .my_game import MyGame

class MyGameGUI(BaseGUI):
    """GUI for MyGame using Tkinter.
    
    Provides interactive graphical interface with:
    - Visual game board
    - Control buttons
    - Score display
    - AI opponent support
    """

    def __init__(self) -> None:
        """Initialize GUI components."""
        super().__init__()
        self.game: Optional[MyGame] = None
        self.setup_window("My Game", 800, 600)
        self.create_widgets()

    def create_widgets(self) -> None:
        """Create and layout GUI widgets."""
        self.create_board()
        self.create_controls()
        self.create_status_display()

    def create_board(self) -> None:
        """Create visual game board."""
        self.board_frame = tk.Frame(self.window)
        self.board_frame.pack(side=tk.LEFT, padx=10, pady=10)
        # Create board elements

    def create_controls(self) -> None:
        """Create game control buttons."""
        self.control_frame = tk.Frame(self.window)
        self.control_frame.pack(side=tk.RIGHT, padx=10, pady=10)
        
        tk.Button(
            self.control_frame,
            text="New Game",
            command=self.new_game
        ).pack(pady=5)

    def new_game(self) -> None:
        """Start a new game."""
        self.game = MyGame()
        self.game.start()
        self.update_display()
```

## Error Handling and Edge Cases

### Common Error Scenarios

**ALWAYS handle these:**

1. **Invalid Input**

   ```python
   def process_move(self, move: str) -> bool:
       """Process move with validation."""
       if not isinstance(move, str):
           raise TypeError(f"move must be str, got {type(move)}")
       if not move.strip():
           raise ValueError("move cannot be empty")
       # Continue processing
   ```

1. **Boundary Conditions**

   ```python
   def get_cell(self, row: int, col: int) -> str:
       """Get board cell with bounds checking."""
       if not (0 <= row < self.board_size):
           raise IndexError(f"row {row} out of range [0, {self.board_size})")
       if not (0 <= col < self.board_size):
           raise IndexError(f"col {col} out of range [0, {self.board_size})")
       return self.board[row][col]
   ```

1. **State Validation**

   ```python
   def make_move(self, move: str) -> bool:
       """Execute move with state validation."""
       if self.is_game_over():
           raise RuntimeError("Cannot make move: game is over")
       if not self.is_valid_move(move):
           return False
       # Execute move
   ```

### Edge Cases Checklist

For every game, test:

- [ ] Empty input
- [ ] Null/None values
- [ ] Boundary values (0, max, -1, max+1)
- [ ] Game start state
- [ ] Game end state
- [ ] Single player scenario
- [ ] Maximum players scenario
- [ ] Concurrent move attempts
- [ ] Invalid state transitions

## Repository Navigation

### Documentation Structure

```
docs/
├── architecture/
│   └── ARCHITECTURE.md          # Design patterns
├── development/
│   ├── CODE_QUALITY.md         # Quality standards
│   ├── TESTING.md              # Testing guide
│   └── IMPLEMENTATION_NOTES.md # Implementation details
├── planning/
│   └── TODO.md                 # Future plans
└── README.md                   # Documentation index
```

### Key Files to Review

**Before implementing any game:**

1. `docs/architecture/ARCHITECTURE.md` - Understand patterns
1. `docs/development/CODE_QUALITY.md` - Quality standards
1. `CONTRIBUTING.md` - Contribution process
1. Similar game implementation in same category

### Configuration Files

| File | Purpose |
|------|---------|
| `pyproject.toml` | Black, Ruff, mypy, pytest config |
| `.pre-commit-config.yaml` | Pre-commit hooks |
| `pytest.ini` | pytest settings |
| `requirements.txt` | Core dependencies |
| `requirements-dev.txt` | Development dependencies |

## Critical Do's and Don'ts

### ✅ MUST DO (Non-negotiable)

1. **Inherit from base classes**

   - `GameEngine` for game logic
   - `BaseGUI` for GUI implementations
   - `HeuristicStrategy` for AI opponents

1. **Maintain complexity ≤ 10**

   - Run `./scripts/check_complexity.sh` after changes
   - Refactor immediately if exceeded

1. **Add complete type hints**

   - All function parameters
   - All return types
   - Use `from __future__ import annotations`

1. **Write comprehensive docstrings**

   - Google style format
   - Include Args, Returns, Raises, Example

1. **Write tests with 90%+ coverage**

   - Unit tests for all functions
   - Integration tests for game flow
   - Edge case tests

1. **Follow structure pattern**

   - Use standard game directory structure
   - Create `__main__.py` for CLI entry point

1. **Run validation before committing**

   ```bash
   black . && ruff check --fix . && mypy . && pytest --cov
   ```

### ❌ MUST NOT DO (Will cause rejection)

1. **Remove or modify existing tests** (unless fixing bugs)
1. **Create functions with complexity > 10** (will fail validation)
1. **Omit type hints or docstrings** (required for all public APIs)
1. **Break backward compatibility** (existing code must still work)
1. **Add dependencies without justification** (discuss first)
1. **Skip writing tests** (no untested code allowed)
1. **Commit failing pre-commit hooks** (must pass all checks)
1. **Exceed 160 character line length** (Black enforces this)
1. **Use global variables** (use class attributes or parameters)
1. **Hard-code magic numbers** (use named constants)

### ⚠️ SHOULD AVOID (Best practices)

- Don't duplicate code - extract to common utilities
- Don't ignore edge cases - handle all scenarios
- Don't use bare `except:` - catch specific exceptions
- Don't mutate function parameters - return new values
- Don't use mutable default arguments - use `None` pattern

## Quick Reference

### Essential Commands

```bash
# Running games
python -m paper_games.tic_tac_toe    # CLI game
python -m card_games.blackjack       # Another example

# Code quality (run in order)
black .                              # 1. Format code
isort .                              # 2. Sort imports
ruff check --fix .                   # 3. Lint and fix
./scripts/check_complexity.sh        # 4. Check complexity
mypy .                               # 5. Type check
pytest --cov                         # 6. Test with coverage

# Pre-commit (runs all checks)
pre-commit run --all-files           # Manual run
pre-commit install                   # Enable automatic runs

# Development setup
pip install -e ".[dev]"              # Install in dev mode
```

### Complexity Check Examples

```bash
# Check single file
radon cc path/to/file.py -s

# Check entire directory
radon cc card_games/ -s -a

# Check specific function
radon cc path/to/file.py -s | grep function_name
```

### Coverage Commands

```bash
# Run tests with coverage
pytest --cov=card_games --cov=paper_games

# Generate HTML report
pytest --cov=card_games --cov=paper_games --cov-report=html

# View report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

## Resources and Documentation

| Resource | Location | Purpose |
|----------|----------|---------|
| Architecture Guide | `docs/architecture/ARCHITECTURE.md` | Design patterns |
| Code Quality | `docs/development/CODE_QUALITY.md` | Standards |
| Testing Guide | `docs/development/TESTING.md` | Test requirements |
| Contributing | `CONTRIBUTING.md` | Contribution process |
| Examples | `examples/` | Sample implementations |
| API Docs | `docs/build/html/` | Generated docs |

## Agent Success Criteria

**Your code change is successful when:**

1. ✅ All pre-commit hooks pass
1. ✅ `pytest --cov` shows 90%+ coverage for new code
1. ✅ `./scripts/check_complexity.sh` reports no functions > 10
1. ✅ `mypy .` reports no type errors
1. ✅ Game runs without errors: `python -m package.game_name`
1. ✅ Documentation is updated (if applicable)
1. ✅ Code follows existing patterns in the codebase

## Common Mistakes to Avoid

1. **Forgetting `from __future__ import annotations`**

   - Add at top of every Python file

1. **Not checking complexity**

   - Run `./scripts/check_complexity.sh` regularly

1. **Missing test coverage**

   - Write tests before/during implementation (TDD)

1. **Ignoring type hints**

   - Add to all functions, no exceptions

1. **Skipping docstrings**

   - Required for all public functions and classes

1. **Not using base classes**

   - Always inherit from `GameEngine`, `BaseGUI`, etc.

1. **Committing without validation**

   - Run full validation suite before pushing

## OpenAI Codex Best Practices Applied

This AGENTS.md follows OpenAI Codex best practices:

1. **Clear Role Definition** - Specifies agent's role as Python game specialist
1. **Specific Requirements** - Explicit complexity, type hint, and testing requirements
1. **Actionable Examples** - Copy-paste code templates for common patterns
1. **Step-by-Step Workflow** - Detailed development phases with commands
1. **Error Prevention** - Do's/Don'ts with clear consequences
1. **Success Criteria** - Measurable outcomes for code changes
1. **Quick Reference** - Commands and resources for easy access

______________________________________________________________________

**Remember**: Quality over speed. Maintainable, well-documented, tested code that follows patterns is always preferred over quick hacks.
