---
applyTo: "**/{card_games,paper_games,dice_games,logic_games,word_games}/**/*.py"
---

# Game Implementation Requirements

When implementing or modifying game files, follow these specific guidelines:

## File Structure

Each game package should follow this structure:

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

## Core Game Engine Requirements

1. **Inherit from GameEngine**: Use the base class from `common/game_engine.py`
1. **Type Hints**: All functions must have complete type hints
1. **Docstrings**: Include game rules in module-level docstring
1. **Complexity**: Keep function complexity ≤ 10 (verify with `./scripts/check_complexity.sh`)

## Required Methods

Every game engine must implement:

```python
from __future__ import annotations

from common import GameEngine
from typing import List, Optional

class MyGame(GameEngine[StateType, MoveType]):
    """Game engine for MyGame.
    
    Rules:
    1. [Explain game rules here]
    2. [...]
    
    Attributes:
        [Document key attributes]
    """
    
    def __init__(self, num_players: int = 2):
        """Initialize game with specified number of players."""
        super().__init__()
        # Initialize game state
    
    def is_valid_move(self, move: MoveType) -> bool:
        """Check if a move is valid in current state."""
        # Implementation
        pass
    
    def make_move(self, move: MoveType) -> bool:
        """Execute a move if valid."""
        if not self.is_valid_move(move):
            return False
        # Apply move and update state
        return True
    
    def is_game_over(self) -> bool:
        """Check if game has ended."""
        # Implementation
        pass
    
    def get_winner(self) -> Optional[int]:
        """Return winner index or None if game not over."""
        # Implementation
        pass
```

## AI Opponent Implementation

1. **Use Strategy Pattern**: Import from `common/ai_strategy.py`
1. **Implement Heuristic**: Create evaluation function for game state
1. **Difficulty Levels**: Support easy, medium, hard if applicable
1. **Document Strategy**: Explain AI approach in docstrings

Example:

```python
from common import HeuristicStrategy

def evaluate_position(game_state) -> float:
    """Evaluate game position for current player.
    
    Considers:
    - Material advantage
    - Positional strength
    - Winning probability
    
    Returns:
        Score in range [-1.0, 1.0] where positive favors current player.
    """
    # Implementation
    pass

ai_strategy = HeuristicStrategy(heuristic_fn=evaluate_position)
```

## CLI Implementation

1. **Simple and Clear**: Use straightforward text-based interface
1. **Input Validation**: Always validate user input
1. **Error Messages**: Provide helpful error messages
1. **Game Loop**: Implement clean game loop with proper exit conditions

## Module-Level Documentation

Every game module should start with a comprehensive docstring:

```python
"""Poker game implementation.

This module implements Texas Hold'em poker with support for:
- 2-10 players
- Standard poker hands (high card through royal flush)
- Betting rounds (pre-flop, flop, turn, river)
- AI opponents with difficulty levels

Game Rules:
1. Each player receives 2 hole cards
2. 5 community cards are dealt in stages
3. Players make best 5-card hand from 7 available cards
4. Betting occurs in rounds with standard actions (check, bet, fold, raise)

Usage:
    python -m card_games.poker
    
    from card_games.poker import Poker
    game = Poker(num_players=4)
    game.start()
"""
```

## Code Quality

- **Complexity**: Functions must have cyclomatic complexity ≤ 10
- **Line Length**: Maximum 160 characters
- **Type Hints**: Required on all functions
- **Docstrings**: Google style, required for all public APIs

## Common Patterns

### State Management

```python
@dataclass
class GameState:
    """Immutable game state representation."""
    players: List[Player]
    current_player: int
    board: Board
    # ... other state
```

### Move Validation

```python
def is_valid_move(self, move: Move) -> bool:
    """Validate move without modifying state."""
    if not self._is_players_turn(move.player):
        return False
    if not self._is_legal_position(move.position):
        return False
    # ... other checks
    return True
```

## Testing Requirements

- Write comprehensive tests for new game logic
- Test all edge cases (invalid moves, game over conditions, etc.)
- Include integration tests for full game flow
- Aim for 90%+ code coverage
