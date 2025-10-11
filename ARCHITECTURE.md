# Architecture and Code Quality Improvements

This document describes the architectural patterns and code quality improvements implemented in this project.

## Overview

The Games repository has been enhanced with reusable components, standardized patterns, and code quality tools to
improve maintainability, consistency, and testability.

## Base Classes and Abstract Interfaces

### GameEngine Base Class

All game engines can implement the `GameEngine` abstract base class, which provides a consistent interface for:

- Game state management
- Move validation
- Turn management
- Win/loss detection

**Location:** `common/game_engine.py`

**Benefits:**

- Consistent API across all games
- Easier to understand and maintain
- Better testability through standard interfaces
- Simplified integration with GUIs and other components

**Example:**

```python
from common import GameEngine, GameState
from typing import List, Optional

class MyCustomGame(GameEngine[int, str]):
    """A custom game implementation."""

    def __init__(self):
        self.board = [" "] * 9
        self.current = "X"

    def reset(self) -> None:
        self.board = [" "] * 9
        self.current = "X"

    def is_game_over(self) -> bool:
        return self.get_winner() is not None or not self.get_valid_moves()

    def get_current_player(self) -> str:
        return self.current

    def get_valid_moves(self) -> List[int]:
        return [i for i, cell in enumerate(self.board) if cell == " "]

    def make_move(self, move: int) -> bool:
        if move not in self.get_valid_moves():
            return False
        self.board[move] = self.current
        self.current = "O" if self.current == "X" else "X"
        return True

    def get_winner(self) -> Optional[str]:
        # Implement win detection
        return None

    def get_game_state(self) -> GameState:
        return GameState.FINISHED if self.is_game_over() else GameState.IN_PROGRESS
```

### BaseGUI Class

GUI implementations can extend `BaseGUI` to use standardized widget creation and layout patterns.

**Location:** `common/gui_base.py`

**Benefits:**

- Consistent look and feel across games
- Reusable widget creation methods
- Simplified logging and status updates
- Standard configuration options

**Example:**

```python
import tkinter as tk
from common import BaseGUI, GUIConfig

class MyGameGUI(BaseGUI):
    def __init__(self, root: tk.Tk, game):
        config = GUIConfig(
            window_title="My Game",
            window_width=800,
            window_height=600,
        )
        super().__init__(root, config)
        self.game = game
        self.build_layout()

    def build_layout(self) -> None:
        # Use helper methods from BaseGUI
        header = self.create_header(self.root, "Welcome!")
        header.pack()

        # Create a log widget
        self.log = self.create_log_widget(self.root)
        self.log.pack()

        # Create a status label
        self.status = self.create_status_label(self.root, "Ready to play")
        self.status.pack()

    def update_display(self) -> None:
        # Update based on game state
        self.log_message(self.log, "Turn completed")
```

### AI Strategy Pattern

AI opponents are implemented using the Strategy pattern, allowing different algorithms to be plugged in.

**Location:** `common/ai_strategy.py`

**Available Strategies:**

1. **RandomStrategy**: Random move selection (easy difficulty)
2. **HeuristicStrategy**: Move selection based on a heuristic function (medium difficulty)
3. **MinimaxStrategy**: Optimal play using minimax (hard difficulty - requires game-specific implementation)

**Example:**

```python
from common import RandomStrategy, HeuristicStrategy

# Easy AI - random moves
easy_ai = RandomStrategy()
move = easy_ai.select_move(game.get_valid_moves(), game)

# Medium AI - heuristic-based
def my_heuristic(move, state):
    # Evaluate move quality
    return score

medium_ai = HeuristicStrategy(heuristic_fn=my_heuristic)
move = medium_ai.select_move(game.get_valid_moves(), game)
```

## Code Quality Tools

### Pre-commit Hooks

Pre-commit hooks automatically enforce code quality standards before commits.

**Setup:**

```bash
pip install pre-commit
pre-commit install
```

**What's checked:**

- **Black**: Code formatting (line length: 160)
- **Ruff**: Linting and import sorting
- **isort**: Import organization
- **mypy**: Static type checking
- **Standard hooks**: Trailing whitespace, YAML validation, etc.

**Configuration:** `.pre-commit-config.yaml`

**Usage:**

```bash
# Run on all files
pre-commit run --all-files

# Automatic on commit
git commit -m "message"
```

### Code Complexity Analysis

Radon is configured to analyze code complexity and maintainability.

**Script:** `scripts/check_complexity.sh`

**Usage:**

```bash
./scripts/check_complexity.sh
```

**What's analyzed:**

- **Cyclomatic Complexity**: Measures code complexity (target: ≤10)
- **Maintainability Index**: Measures code maintainability (target: ≥20)

**Ruff configuration** also includes McCabe complexity checks (max: 10).

### Type Hints

The codebase uses type hints throughout for better IDE support and type safety.

**Standard:**

- All functions have return type annotations
- All function parameters have type annotations
- `from __future__ import annotations` is used for forward references

**Example:**

```python
from __future__ import annotations
from typing import List, Optional

def get_valid_moves(board: List[str]) -> List[int]:
    """Get valid moves from the board."""
    return [i for i, cell in enumerate(board) if cell == " "]
```

## Project Configuration

### pyproject.toml

Enhanced configuration includes:

- **Build system** configuration
- **Project metadata** and dependencies
- **Tool configurations** for Black, Ruff, mypy, pytest
- **Complexity limits** (max complexity: 10)

### Requirements

**Core:**

- `colorama>=0.4.6` - Terminal colors

**Development:**

- `pytest>=7.0` - Testing
- `black>=24.0` - Code formatting
- `ruff>=0.8` - Linting
- `mypy>=1.0` - Type checking
- `pre-commit>=3.0` - Git hooks
- `radon>=6.0` - Complexity analysis

**Optional (GUI):**

- `pygame>=2.0` - Sound effects

## Testing

### Test Structure

Tests are organized by module in the `tests/` directory.

**Running tests:**

```bash
# All tests
pytest

# Specific module
pytest tests/test_common_base_classes.py

# With coverage
pytest --cov=. --cov-report=html
```

### Test Coverage

The new `common` module has 100% test coverage with 12 tests covering:

- GameEngine interface implementation
- AI strategy selection algorithms
- Move validation logic

## Migration Guide

Existing games can gradually adopt these patterns:

### Step 1: Implement GameEngine (Optional)

```python
class ExistingGame(GameEngine[MoveType, PlayerType]):
    # Implement required methods
    pass
```

### Step 2: Use BaseGUI for new GUIs

```python
class ExistingGameGUI(BaseGUI):
    # Use helper methods
    pass
```

### Step 3: Replace AI logic with strategies

```python
# Old: Custom AI logic
def computer_move():
    # Complex logic here
    pass

# New: Strategy pattern
ai = HeuristicStrategy(heuristic_fn=my_heuristic)
move = ai.select_move(valid_moves, game_state)
```

### Step 4: Add type hints (if missing)

```python
# Add to top of file
from __future__ import annotations

# Add to functions
def my_function(param: str) -> int:
    return len(param)
```

## Benefits Summary

1. **Code Reusability**: Shared components reduce duplication
2. **Consistency**: Standardized patterns across all games
3. **Maintainability**: Easier to understand and modify
4. **Quality**: Automated checks ensure standards
5. **Testability**: Abstract interfaces simplify testing
6. **Extensibility**: New features easier to add
7. **Developer Experience**: Better IDE support with type hints

## Future Enhancements

Potential improvements building on this foundation:

- Dependency injection container
- Event-driven architecture
- Save/load game state system
- Plugin system for third-party games
- Unified settings/preferences system
- Observer pattern for GUI synchronization

## Contributing

When adding new games or features:

1. Consider extending `GameEngine` for game logic
2. Extend `BaseGUI` for graphical interfaces
3. Use AI strategies for computer opponents
4. Run pre-commit hooks before committing
5. Add tests for new functionality
6. Keep complexity under 10 (use `scripts/check_complexity.sh`)
7. Add type hints to all new code

For questions or suggestions, please open an issue.
