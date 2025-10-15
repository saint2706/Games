# Path-Specific Agent Instructions

This file provides specialized instructions for AI coding agents working on specific file types in this repository. These instructions complement the repository-wide AGENTS.md file.

## Purpose

Path-specific instructions are automatically applied when agents work on:
- Test files (`**/test_*.py`)
- GUI files (`**/gui.py`)
- Game implementation files (`**/{card_games,paper_games,dice_games,logic_games,word_games}/**/*.py`)

## How This Works

1. **Agent reads repository-wide instructions** from `.github/AGENTS.md` or `.github/copilot-instructions.md`
2. **Agent identifies file type** based on path and name
3. **Agent loads relevant path-specific instructions** from `.github/instructions/*.instructions.md`
4. **Agent combines all instructions** for comprehensive context

## Available Path-Specific Instructions

### 1. Test Files (`test-files.instructions.md`)

**Applies to**: `**/test_*.py`

**Key Requirements:**
- Use pytest framework exclusively
- Achieve 90%+ code coverage for new code
- Include unit, integration, and edge case tests
- Use descriptive docstrings for all test functions
- Use fixtures from `tests/fixtures/` for reusable data
- Parametrize tests with `@pytest.mark.parametrize`

**Test Organization:**
```python
class TestGameInitialization:
    """Test game initialization scenarios."""
    
    def test_default_initialization(self):
        """Test game initializes with defaults."""
        pass

class TestGameMoves:
    """Test move validation and execution."""
    
    @pytest.fixture
    def game(self):
        """Create game instance for testing."""
        return MyGame()
    
    def test_valid_move(self, game):
        """Test that valid move is accepted."""
        pass
```

### 2. GUI Files (`gui-files.instructions.md`)

**Applies to**: `**/gui.py`

**Key Requirements:**
- Inherit from `BaseGUI` in `common/gui_base.py`
- Use Tkinter as primary framework (PyQt5 for advanced features)
- Keep GUI code separate from game logic
- Use threading for AI moves to keep GUI responsive
- Support keyboard navigation and accessibility
- Implement proper resource cleanup in `quit_game()`

**GUI Structure:**
```python
class MyGameGUI(BaseGUI):
    """GUI for MyGame."""
    
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
    
    def update_display(self) -> None:
        """Update GUI to reflect current game state."""
        pass
```

### 3. Game Implementation Files (`game-implementations.instructions.md`)

**Applies to**: `**/{card_games,paper_games,dice_games,logic_games,word_games}/**/*.py`

**Key Requirements:**
- Inherit from `GameEngine` base class
- Implement required methods: `is_valid_move()`, `make_move()`, `is_game_over()`, `get_winner()`
- Keep function cyclomatic complexity ≤ 10
- Include comprehensive game rules in module docstring
- Use dataclasses for immutable state representation
- Implement AI opponents using `HeuristicStrategy`

**Game Engine Structure:**
```python
"""MyGame implementation.

Game Rules:
1. [Rule 1]
2. [Rule 2]
...

Usage:
    python -m package.my_game
"""
from __future__ import annotations

from typing import Optional
from dataclasses import dataclass
from common import GameEngine

@dataclass
class GameState:
    """Immutable game state."""
    current_player: int
    move_count: int

class MyGame(GameEngine[GameState, str]):
    """Game engine for MyGame."""
    
    def __init__(self, num_players: int = 2) -> None:
        """Initialize game."""
        super().__init__()
        self._initialize_state()
    
    def is_valid_move(self, move: str) -> bool:
        """Validate move."""
        pass
    
    def make_move(self, move: str) -> bool:
        """Execute move."""
        pass
    
    def is_game_over(self) -> bool:
        """Check if game ended."""
        pass
    
    def get_winner(self) -> Optional[int]:
        """Return winner index."""
        pass
```

## Agent Workflow for Different File Types

### Working on Test Files

1. **Understand what's being tested** - Read the implementation file first
2. **Identify test scenarios** - Normal cases, edge cases, error cases
3. **Write test classes** - Group related tests together
4. **Use fixtures** - Create reusable test data
5. **Check coverage** - Ensure 90%+ coverage
6. **Add parametrized tests** - Test multiple scenarios efficiently

### Working on GUI Files

1. **Separate concerns** - GUI code separate from game logic
2. **Use base classes** - Inherit from `BaseGUI`
3. **Handle events** - Mouse, keyboard, window events
4. **Thread AI moves** - Keep GUI responsive
5. **Implement accessibility** - Keyboard navigation, tooltips
6. **Clean up resources** - Proper shutdown in `quit_game()`

### Working on Game Files

1. **Read game rules** - Understand the game thoroughly
2. **Design state** - Create immutable state representation
3. **Plan complexity** - Break complex logic into functions ≤ 10
4. **Implement core** - `is_valid_move`, `make_move`, `is_game_over`
5. **Add AI** - Implement heuristic evaluation
6. **Write tests** - Comprehensive test coverage
7. **Check complexity** - Run `./scripts/check_complexity.sh`

## Validation Checklist by File Type

### Test Files (`test_*.py`)

- [ ] All test functions start with `test_`
- [ ] All tests have descriptive docstrings
- [ ] Coverage reaches 90%+ for new code
- [ ] Fixtures are used for repeated setup
- [ ] Parametrized tests for multiple scenarios
- [ ] Tests are organized in classes by functionality
- [ ] Edge cases are covered

### GUI Files (`gui.py`)

- [ ] Inherits from `BaseGUI`
- [ ] Game logic is separate from GUI
- [ ] AI moves run in separate threads
- [ ] Keyboard shortcuts are implemented
- [ ] Window closes cleanly with resource cleanup
- [ ] Status display shows current game state
- [ ] Controls are user-friendly and accessible

### Game Files (`game_name.py`, `cli.py`, etc.)

- [ ] Inherits from `GameEngine`
- [ ] All required methods implemented
- [ ] Module docstring includes game rules
- [ ] Function complexity ≤ 10 (verified)
- [ ] Complete type hints on all functions
- [ ] Google-style docstrings
- [ ] State is immutable (uses dataclasses)
- [ ] Entry point in `__main__.py`
- [ ] Tests achieve 90%+ coverage

## Common Patterns by File Type

### Test File Pattern

```python
"""Test suite for MyGame."""
from __future__ import annotations

import pytest
from my_game.my_game import MyGame

@pytest.fixture
def game():
    """Create game instance."""
    return MyGame()

class TestMyGame:
    """Test MyGame functionality."""
    
    def test_initialization(self, game):
        """Test game initializes correctly."""
        assert game is not None
    
    @pytest.mark.parametrize("move,expected", [
        ("A1", True),
        ("invalid", False),
    ])
    def test_move_validation(self, game, move, expected):
        """Test move validation."""
        assert game.is_valid_move(move) == expected
```

### GUI File Pattern

```python
"""GUI implementation for MyGame."""
from __future__ import annotations

import tkinter as tk
from typing import Optional
from common import BaseGUI
from .my_game import MyGame

class MyGameGUI(BaseGUI):
    """Graphical interface for MyGame."""
    
    def __init__(self) -> None:
        """Initialize GUI."""
        super().__init__()
        self.game: Optional[MyGame] = None
        self.setup_window("My Game", 800, 600)
        self.create_widgets()
```

### Game File Pattern

```python
"""MyGame implementation."""
from __future__ import annotations

from typing import Optional
from dataclasses import dataclass
from common import GameEngine

@dataclass
class GameState:
    """Game state."""
    current_player: int

class MyGame(GameEngine[GameState, str]):
    """Game engine."""
    
    def __init__(self) -> None:
        """Initialize game."""
        super().__init__()
```

## Quick Reference

### Test File Commands

```bash
# Run specific test file
pytest tests/test_my_game.py -v

# Run with coverage
pytest tests/test_my_game.py --cov=package.my_game

# Run parametrized test
pytest tests/test_my_game.py::TestMyGame::test_move_validation -v
```

### GUI File Commands

```bash
# Run GUI
python -m package.my_game

# Test GUI (if using pytest-qt)
pytest tests/test_my_game_gui.py --qt-api=pyqt5
```

### Game File Commands

```bash
# Check complexity
radon cc package/my_game/my_game.py -s

# Type check
mypy package/my_game/my_game.py

# Run game
python -m package.my_game
```

## Integration with Repository-Wide Instructions

These path-specific instructions **complement** (not replace) the repository-wide instructions in `.github/AGENTS.md`. Both sets of instructions are active simultaneously:

1. **Repository-wide instructions** provide general context (architecture, patterns, workflow)
2. **Path-specific instructions** provide detailed requirements for specific file types
3. **Combined instructions** give agents complete context for any file

## OpenAI Codex Best Practices Applied

Path-specific instructions follow these best practices:

1. **Context-Aware** - Instructions match file type and purpose
2. **Specific Requirements** - Clear expectations for each file type
3. **Actionable Examples** - Copy-paste templates
4. **Validation Checklists** - Measurable success criteria
5. **Quick Reference** - File-type-specific commands
6. **Integration Clarity** - Explains how instructions combine

______________________________________________________________________

**Remember**: Path-specific instructions work **with** repository-wide instructions to provide complete context for AI coding agents.
