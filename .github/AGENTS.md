# GitHub Copilot Instructions for Games Repository

This file provides context-specific guidance for GitHub Copilot when working in this repository.

## Repository Overview

This is a Python-based games collection featuring card games (Poker, Blackjack, Bluff, Uno, Solitaire, Hearts, Spades,
Gin Rummy, Bridge) and paper games (Tic-Tac-Toe, Battleship, Nim, Hangman, Dots and Boxes, Unscramble, Checkers, Connect
Four, Othello, Sudoku, Mancala). The project emphasizes clean architecture, AI opponents, and both CLI and GUI
interfaces.

## Code Quality Standards

### Formatting and Style

- **Python Version**: 3.9+
- **Line Length**: 160 characters (configured in `pyproject.toml`)
- **Formatter**: Black (enforced via pre-commit hooks)
- **Linter**: Ruff (includes complexity checks)
- **Import Sorting**: isort
- **Type Checking**: mypy (95%+ coverage expected)

### Complexity Management

- **Maximum Cyclomatic Complexity**: 10 per function
- **Target Complexity Rating**: A or B (1-10)
- **Tool**: Radon for complexity analysis
- **Check Script**: `./scripts/check_complexity.sh`

### Type Hints

- All functions MUST include type hints for parameters and return values
- Use `from __future__ import annotations` at the top of every file
- Use typing module for complex types (List, Dict, Optional, etc.)

### Docstrings

- **Format**: Google style
- **Required for**: All public functions, classes, and modules
- **Include**: Args, Returns, Raises sections
- Module-level docstrings should explain game rules and code organization

Example:

```python
from __future__ import annotations

from typing import List, Optional

def calculate_score(items: List[int], multiplier: float = 1.0) -> int:
    """Calculate total score with multiplier.

    Args:
        items: List of item values to sum.
        multiplier: Score multiplier (default: 1.0).

    Returns:
        Total calculated score as integer.

    Raises:
        ValueError: If multiplier is negative.
    """
    if multiplier < 0:
        raise ValueError("Multiplier must be non-negative")
    return int(sum(items) * multiplier)
```

## Architecture Patterns

### Game Structure

Each game follows this structure:

```
game_name/
├── __init__.py          # Package initialization
├── __main__.py          # Entry point (python -m package.game_name)
├── game_name.py         # Core game logic (game engine)
├── cli.py              # Command-line interface (optional)
├── gui.py              # Graphical interface (optional)
├── README.md           # Game-specific documentation
└── tests/              # Tests (or in top-level tests/)
```

### Core Components

1. **GameEngine**: Core logic independent of UI (in `common/game_engine.py`)
1. **BaseGUI**: Common GUI utilities (in `common/gui_base.py`)
1. **AI Strategy**: Strategy pattern for AI opponents (in `common/ai_strategy.py`)

### Available Architectural Patterns

The `common/architecture/` module provides:

- **Plugin System**: Add third-party games (`plugin.py`)
- **Event-Driven Architecture**: Decouple components (`events.py`)
- **Save/Load System**: Persist game state (`persistence.py`)
- **Settings Management**: Centralized configuration (`settings.py`)
- **Replay/Undo System**: Record and replay actions (`replay.py`)
- **Observer Pattern**: Synchronize GUIs with state (`observer.py`)

## Testing Requirements

### Framework and Coverage

- **Framework**: pytest
- **Current Coverage**: 30%+ (goal: 90%+)
- **Required for**: All new game logic
- **Run Tests**: `pytest` or `pytest -v`
- **Coverage**: `pytest --cov=paper_games --cov=card_games --cov-report=html`

### Test Structure

- Tests live in `tests/` directory
- Name pattern: `test_*.py`
- Use fixtures from `tests/fixtures/` for common test data
- Include unit tests, integration tests, and performance benchmarks

### Example Test

```python
import pytest
from game_name.game_name import GameEngine

def test_game_initialization():
    """Test that game initializes with correct state."""
    game = GameEngine(num_players=2)
    assert len(game.players) == 2
    assert game.current_player == 0

def test_valid_move():
    """Test that valid move is accepted."""
    game = GameEngine()
    game.start()
    result = game.make_move("A1")
    assert result is True
```

## Development Workflow

### Before Coding

1. Review existing game implementations for patterns
1. Check `ARCHITECTURE.md` for design guidance
1. Review `CODE_QUALITY.md` for standards
1. Look at `CONTRIBUTING.md` for contribution guidelines

### During Development

1. Write code following PEP 8 (enforced by Black)
1. Add type hints to all functions
1. Keep function complexity ≤ 10
1. Write docstrings for public APIs
1. Add tests for new functionality

### Before Committing

Pre-commit hooks automatically run:

- Black (formatting)
- Ruff (linting + complexity)
- isort (import sorting)
- mypy (type checking)
- YAML/JSON validation
- Trailing whitespace removal

Manual checks:

```bash
# Format code
black .

# Check linting
ruff check --fix .

# Run tests
pytest

# Check complexity
./scripts/check_complexity.sh

# Run pre-commit manually
pre-commit run --all-files
```

## Common Patterns

### Game Engine Pattern

```python
from common import GameEngine
from typing import List

class MyGame(GameEngine[int, str]):  # Generic[StateType, MoveType]
    """Game engine for MyGame."""

    def __init__(self):
        super().__init__()
        # Initialize game state

    def is_valid_move(self, move: str) -> bool:
        """Check if move is valid."""
        # Implement validation logic
        return True

    def make_move(self, move: str) -> bool:
        """Execute a move."""
        if not self.is_valid_move(move):
            return False
        # Apply move and update state
        return True

    def is_game_over(self) -> bool:
        """Check if game has ended."""
        # Implement end condition
        return False
```

### AI Strategy Pattern

```python
from common import HeuristicStrategy

def my_heuristic(state) -> float:
    """Evaluate game state (higher is better for current player)."""
    # Implement heuristic logic
    return score

ai_strategy = HeuristicStrategy(heuristic_fn=my_heuristic)
best_move = ai_strategy.choose_move(game_state, available_moves)
```

### GUI Pattern

```python
from common import BaseGUI
import tkinter as tk

class MyGameGUI(BaseGUI):
    """GUI for MyGame."""

    def __init__(self):
        super().__init__()
        self.setup_window("My Game", 800, 600)
        self.create_widgets()

    def create_widgets(self):
        """Create GUI widgets."""
        # Use helper methods from BaseGUI
        self.create_board()
        self.create_controls()
```

## File Locations

### Documentation

- `README.md` - Main project overview
- `CONTRIBUTING.md` - Contribution guidelines
- `ARCHITECTURE.md` - Architecture patterns
- `CODE_QUALITY.md` - Code quality standards
- `TESTING.md` - Testing guide
- `docs/` - Sphinx documentation

### Code

- `card_games/` - Card game implementations
- `paper_games/` - Paper game implementations
- `common/` - Shared utilities and base classes
- `common/architecture/` - Architectural patterns
- `tests/` - Test suite
- `examples/` - Example implementations

### Configuration

- `pyproject.toml` - Project configuration (Black, Ruff, mypy, pytest)
- `.pre-commit-config.yaml` - Pre-commit hooks
- `pytest.ini` - pytest configuration
- `.mutmut.toml` - Mutation testing configuration

## Dependencies

### Core

- `colorama>=0.4.6` - Terminal colors

### Development

- `pytest>=7.0` - Testing
- `black>=24.0` - Formatting
- `ruff>=0.8` - Linting
- `mypy>=1.0` - Type checking
- `pre-commit>=3.0` - Pre-commit hooks
- `radon>=6.0` - Complexity analysis

### Optional

- `pygame>=2.0` - GUI/sound support (for Uno)
- `tkinter` - GUI support (typically pre-installed)

## Important Guidelines

### DO

- ✅ Use existing base classes (`GameEngine`, `BaseGUI`, `HeuristicStrategy`)
- ✅ Follow the established game structure pattern
- ✅ Add comprehensive docstrings with game rules
- ✅ Include type hints on all functions
- ✅ Keep functions simple (complexity ≤ 10)
- ✅ Write tests for new functionality
- ✅ Use architectural patterns from `common/architecture/`
- ✅ Make games runnable via `python -m package.game_name`

### DON'T

- ❌ Remove or modify existing tests
- ❌ Create functions with complexity > 10
- ❌ Omit type hints or docstrings
- ❌ Break backward compatibility
- ❌ Add dependencies without justification
- ❌ Skip writing tests for new code
- ❌ Commit code that fails pre-commit hooks
- ❌ Exceed 160 character line length

## AI Opponent Implementation

When implementing AI opponents:

1. Use the strategy pattern from `common/ai_strategy.py`
1. Implement heuristic functions that evaluate game state
1. Consider difficulty levels (easy, medium, hard)
1. Document strategy in docstrings
1. Test AI decisions thoroughly

Example:

```python
def evaluate_position(game_state) -> float:
    """Evaluate position (positive favors current player).

    Considers:
    - Material advantage
    - Positional strength
    - Winning probability

    Returns:
        Score in range [-1.0, 1.0]
    """
    # Implementation
```

## GUI Implementation

When adding GUI support:

1. Inherit from `BaseGUI` in `common/gui_base.py`
1. Keep GUI code separate from game logic
1. Use observer pattern for state synchronization
1. Provide both GUI and CLI interfaces
1. Test GUI components with pytest-qt

## Entry Points

All games should be runnable via:

```bash
python -m package.game_name [options]
```

Example `__main__.py`:

```python
"""Entry point for MyGame."""
from .cli import main

if __name__ == "__main__":
    main()
```

## Resources

- **Architecture Guide**: `ARCHITECTURE.md`
- **Code Quality**: `CODE_QUALITY.md`
- **Testing Guide**: `TESTING.md`
- **Contributing**: `CONTRIBUTING.md`
- **Documentation**: `docs/` directory
- **Examples**: `examples/` directory

## Quick Reference Commands

```bash
# Run a game
python -m paper_games.tic_tac_toe
python -m card_games.blackjack

# Development
black .                          # Format code
ruff check --fix .               # Lint and fix
mypy .                          # Type check
pytest                          # Run tests
pytest --cov                    # Test with coverage
./scripts/check_complexity.sh   # Check complexity
pre-commit run --all-files      # Run all hooks

# Install development tools
pip install -r requirements-dev.txt
pre-commit install
```

---

**Remember**: The goal is maintainable, well-documented, tested code that follows consistent patterns across all games.
Prioritize code quality and simplicity over clever solutions.
