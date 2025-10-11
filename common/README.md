# Common Module

This module provides reusable components, abstract base classes, and shared functionality across different game
implementations.

## Components

### Game Engine (`game_engine.py`)

Abstract base class for game engines, defining a common interface for:

- Game state management
- Move validation
- Win/loss detection
- Turn management

**Usage Example:**

```python
from common import GameEngine, GameState

class MyGame(GameEngine[int, str]):
    def reset(self) -> None:
        self.board = [" "] * 9
        self.current_player = "X"

    def is_game_over(self) -> bool:
        return self.get_winner() is not None or not self.get_valid_moves()

    def get_current_player(self) -> str:
        return self.current_player

    def get_valid_moves(self) -> List[int]:
        return [i for i, cell in enumerate(self.board) if cell == " "]

    def make_move(self, move: int) -> bool:
        if move not in self.get_valid_moves():
            return False
        self.board[move] = self.current_player
        self.current_player = "O" if self.current_player == "X" else "X"
        return True

    def get_winner(self) -> Optional[str]:
        # Implement win detection logic
        pass

    def get_game_state(self) -> GameState:
        if self.is_game_over():
            return GameState.FINISHED
        return GameState.IN_PROGRESS
```

### GUI Base (`gui_base.py`)

Base class and utilities for creating consistent GUI interfaces:

- Window configuration
- Standard widget creation (headers, labels, logs)
- Common layout patterns
- Log management

**Usage Example:**

```python
from common import BaseGUI, GUIConfig

class MyGameGUI(BaseGUI):
    def __init__(self, root: tk.Tk):
        config = GUIConfig(
            window_title="My Game",
            window_width=800,
            window_height=600,
        )
        super().__init__(root, config)
        self.build_layout()

    def build_layout(self) -> None:
        # Create header
        header = self.create_header(self.root, "Welcome to My Game!")
        header.pack()

        # Create log widget
        self.log = self.create_log_widget(self.root)
        self.log.pack()

        # Log a message
        self.log_message(self.log, "Game started!")

    def update_display(self) -> None:
        # Update GUI based on game state
        pass
```

### AI Strategy (`ai_strategy.py`)

Strategy pattern implementation for AI opponents:

- **RandomStrategy**: Random move selection (easy difficulty)
- **MinimaxStrategy**: Optimal play using minimax algorithm (hard difficulty)
- **HeuristicStrategy**: Heuristic-based move selection (medium difficulty)

**Usage Example:**

```python
from common import RandomStrategy, HeuristicStrategy

# Random AI (easy)
easy_ai = RandomStrategy()
move = easy_ai.select_move(valid_moves, game_state)

# Heuristic AI (medium)
def evaluate_position(move, state):
    # Return score for the move
    return score

medium_ai = HeuristicStrategy(heuristic_fn=evaluate_position)
move = medium_ai.select_move(valid_moves, game_state)
```

## Benefits

1. **Code Reusability**: Common functionality shared across all games
2. **Consistency**: Standardized interfaces and behavior
3. **Maintainability**: Changes to common code benefit all games
4. **Testability**: Abstract interfaces make unit testing easier
5. **Extensibility**: Easy to add new games following established patterns

## Integration

Existing games can gradually adopt these components:

1. Implement `GameEngine` interface for game logic
2. Extend `BaseGUI` for graphical interfaces
3. Use `AIStrategy` implementations for computer opponents
4. Leverage utility methods for common tasks

This approach allows incremental adoption without breaking existing code.
