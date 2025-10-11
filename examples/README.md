# Examples

This directory contains example implementations demonstrating how to use the base classes and utilities provided by the
`common` module.

## Available Examples

### simple_game_example.py

A complete implementation of a number guessing game that demonstrates:

- Implementing the `GameEngine` abstract base class
- Using the `RandomStrategy` for easy AI
- Using the `HeuristicStrategy` for intelligent AI
- Proper type hints throughout
- Interactive gameplay

**Run it:**

```bash
python examples/simple_game_example.py
```

**What you'll learn:**

- How to create a game by extending `GameEngine`
- How to implement required methods (`reset`, `make_move`, `is_game_over`, etc.)
- How to use AI strategies for computer opponents
- How to create heuristic functions for intelligent play

## Creating Your Own Game

To create a new game using the base classes:

1. **Define your game class:**

   ```python
   from common import GameEngine, GameState
   from typing import List, Optional

   class MyGame(GameEngine[MoveType, PlayerType]):
       def __init__(self):
           # Initialize game state
           pass

       def reset(self) -> None:
           # Reset to initial state
           pass

       def is_game_over(self) -> bool:
           # Check if game is finished
           pass

       def get_current_player(self) -> PlayerType:
           # Return current player
           pass

       def get_valid_moves(self) -> List[MoveType]:
           # Return list of valid moves
           pass

       def make_move(self, move: MoveType) -> bool:
           # Apply the move
           pass

       def get_winner(self) -> Optional[PlayerType]:
           # Return winner or None
           pass

       def get_game_state(self) -> GameState:
           # Return current state
           pass
   ```

2. **Add AI opponents:**

   ```python
   from common import RandomStrategy, HeuristicStrategy

   # Easy AI
   easy_ai = RandomStrategy()

   # Smart AI with custom heuristic
   def evaluate_move(move, state):
       # Score the move
       return score

   smart_ai = HeuristicStrategy(heuristic_fn=evaluate_move)
   ```

3. **Create a GUI (optional):**

   ```python
   from common import BaseGUI, GUIConfig

   class MyGameGUI(BaseGUI):
       def __init__(self, root, game):
           config = GUIConfig(window_title="My Game")
           super().__init__(root, config)
           self.game = game
           self.build_layout()

       def build_layout(self):
           # Use helper methods
           header = self.create_header(self.root, "My Game")
           log = self.create_log_widget(self.root)
           # ...

       def update_display(self):
           # Update UI based on game state
           pass
   ```

## Tips

- Use type hints for better IDE support
- Keep complexity low (≤10 per method)
- Add tests for your game
- Run `pre-commit` before committing
- Check complexity with `./scripts/check_complexity.sh`

## More Information

See `ARCHITECTURE.md` for detailed documentation on the base classes and patterns.
