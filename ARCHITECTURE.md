# Games Repository Architecture

This document describes the architecture components available in the Games repository for building consistent, extensible game implementations.

## Overview

The `common/architecture` module provides a comprehensive set of architectural patterns and utilities to support game development:

1. **Plugin System** - Add third-party games without modifying core code
2. **Event-Driven Architecture** - Decouple components using events
3. **Save/Load System** - Persist and restore game state
4. **Unified Settings** - Centralized configuration management
5. **Replay/Undo System** - Record and replay game actions
6. **Observer Pattern** - Synchronize GUIs with game state
7. **Game Engine Abstraction** - Common interface for all games

## Components

### 1. Plugin System

Located in `common/architecture/plugin.py`

The plugin system allows third-party developers to add new games without modifying the core codebase.

#### Basic Usage

```python
from common.architecture import GamePlugin, PluginManager, PluginMetadata

class MyGamePlugin(GamePlugin):
    def get_metadata(self):
        return PluginMetadata(
            name="my_game",
            version="1.0.0",
            author="Your Name",
            description="A custom game"
        )
    
    def initialize(self, **kwargs):
        # Plugin initialization code
        pass
    
    def shutdown(self):
        # Cleanup code
        pass
    
    def get_game_class(self):
        return MyGameEngine

# Load plugins
manager = PluginManager(plugin_dirs=[Path("./plugins")])
manager.load_plugin("my_game")
```

#### Creating a Plugin

1. Create a Python file or package in the `plugins` directory
2. Implement the `GamePlugin` interface
3. Define your game engine class
4. Export a `plugin` variable with your plugin instance

### 2. Event-Driven Architecture

Located in `common/architecture/events.py`

The event system enables loose coupling between game components.

#### Basic Usage

```python
from common.architecture import EventBus, EventHandler, Event

class GameEventHandler(EventHandler):
    def handle(self, event: Event):
        print(f"Received: {event.type}")

bus = EventBus()
handler = GameEventHandler()

# Subscribe to specific events
bus.subscribe("PLAYER_MOVE", handler)

# Or subscribe to all events
bus.subscribe_all(handler)

# Emit events
bus.emit("PLAYER_MOVE", data={"player": "Alice", "position": "A1"})

# View event history
history = bus.get_history("PLAYER_MOVE")
```

#### Common Event Types

- `GAME_START` - Game initialization complete
- `GAME_END` - Game finished
- `PLAYER_MOVE` - Player action executed
- `STATE_CHANGE` - Game state updated
- `ERROR` - Error occurred

### 3. Observer Pattern

Located in `common/architecture/observer.py`

The observer pattern allows GUIs to stay synchronized with game state changes.

#### Basic Usage

```python
from common.architecture import Observable, Observer

class GameStateObserver(Observer):
    def update(self, observable, **kwargs):
        print(f"State changed: {kwargs}")

class GameModel(Observable):
    def __init__(self):
        super().__init__()
        self._score = 0
    
    def set_score(self, score):
        old_score = self._score
        self._score = score
        self.notify(property="score", old_value=old_score, new_value=score)

model = GameModel()
observer = GameStateObserver()
model.attach(observer)

model.set_score(100)  # Observer will be notified
```

### 4. Save/Load System

Located in `common/architecture/persistence.py`

Provides consistent save/load functionality across all games.

#### Basic Usage

```python
from common.architecture import SaveLoadManager
from pathlib import Path

manager = SaveLoadManager(save_dir=Path("./saves"))

# Save game state
state = {
    "score": 100,
    "level": 5,
    "players": ["Alice", "Bob"]
}
filepath = manager.save("my_game", state, save_name="quicksave")

# Load game state
loaded = manager.load(filepath)
game_state = loaded["state"]

# List all saves
saves = manager.list_saves("my_game")

# Get save metadata
info = manager.get_save_info(filepath)
```

#### Supported Formats

- **JSON** (default) - Human-readable, good for debugging
- **Pickle** - Binary format, more efficient for complex objects

### 5. Replay/Undo System

Located in `common/architecture/replay.py`

Record game actions for replay functionality and implement undo/redo.

#### Basic Usage

```python
from common.architecture import ReplayManager
import time

manager = ReplayManager(max_history=100)

# Record actions
manager.record_action(
    timestamp=time.time(),
    actor="Player1",
    action_type="MOVE",
    data={"from": "A1", "to": "B2"}
)

# Undo last action
if manager.can_undo():
    action = manager.undo()
    # Revert the action's effects

# Redo undone action
if manager.can_redo():
    action = manager.redo()
    # Reapply the action
```

### 6. Unified Settings System

Located in `common/architecture/settings.py`

Centralized configuration management for all games.

#### Basic Usage

```python
from common.architecture import SettingsManager
from pathlib import Path

manager = SettingsManager(config_dir=Path("./config"))

# Load game settings
settings = manager.load_settings("my_game", defaults={
    "difficulty": "medium",
    "sound": True,
    "theme": "dark"
})

# Access settings
difficulty = settings.get("difficulty")
settings.set("difficulty", "hard")

# Save settings
manager.save_settings("my_game", settings)

# Global settings (shared across all games)
global_settings = manager.get_global_settings()
```

### 7. Game Engine Abstraction

Located in `common/architecture/engine.py`

Provides a common interface for all game engines.

#### Basic Usage

```python
from common.architecture import GameEngine, GameState, GamePhase

class MyGameEngine(GameEngine):
    def initialize(self, **kwargs):
        self._state = GameState(phase=GamePhase.RUNNING)
        self.emit_event("GAME_START")
    
    def reset(self):
        self._state = GameState(phase=GamePhase.SETUP)
        self.emit_event("GAME_RESET")
    
    def is_finished(self):
        return self._state.phase == GamePhase.FINISHED
    
    def get_current_player(self):
        return self.players[self.current_player_index]
    
    def get_valid_actions(self):
        # Return list of valid actions
        return []
    
    def execute_action(self, action):
        # Execute the action
        self.emit_event("PLAYER_MOVE", data={"action": action})
        return True

# Use the engine
engine = MyGameEngine()
engine.initialize()
```

## Integration Example

Here's a complete example integrating multiple architecture components:

```python
from common.architecture import (
    GameEngine, GameState, GamePhase,
    EventBus, SaveLoadManager, ReplayManager,
    Observable, SettingsManager
)
from pathlib import Path
import time

class MyGame(GameEngine):
    def __init__(self):
        super().__init__()
        self.save_manager = SaveLoadManager()
        self.replay_manager = ReplayManager()
        self.settings_manager = SettingsManager()
        
        # Subscribe to own events
        self.event_bus.subscribe("PLAYER_MOVE", self._on_player_move)
    
    def initialize(self, **kwargs):
        self._state = GameState(phase=GamePhase.RUNNING)
        settings = self.settings_manager.load_settings("my_game")
        self.emit_event("GAME_START")
    
    def reset(self):
        self._state = GameState(phase=GamePhase.SETUP)
        self.replay_manager.clear()
        self.emit_event("GAME_RESET")
    
    def is_finished(self):
        return self._state.phase == GamePhase.FINISHED
    
    def get_current_player(self):
        return None
    
    def get_valid_actions(self):
        return []
    
    def execute_action(self, action):
        # Record for replay/undo
        self.replay_manager.record_action(
            timestamp=time.time(),
            actor="player",
            action_type="MOVE",
            data=action,
            state_before=self.save_state()
        )
        
        # Emit event
        self.emit_event("PLAYER_MOVE", data=action)
        
        # Notify observers
        self.notify(action=action)
        
        return True
    
    def _on_player_move(self, event):
        # Handle player move event
        pass
    
    def save_game(self, name="quicksave"):
        """Save the current game state."""
        return self.save_manager.save("my_game", self.save_state(), save_name=name)
    
    def load_game(self, filepath):
        """Load a saved game state."""
        data = self.save_manager.load(filepath)
        self.load_state(data["state"])
```

## Best Practices

1. **Use Events for Decoupling**: Emit events when state changes rather than directly calling methods
2. **Implement Observable**: Make game state observable so GUIs can react to changes
3. **Support Save/Load**: Implement `save_state()` and `load_state()` methods
4. **Record Actions**: Use ReplayManager to enable undo/redo functionality
5. **Centralize Settings**: Use SettingsManager for all configuration
6. **Follow the Interface**: Implement GameEngine interface for consistency

## Testing

The architecture components include comprehensive tests in:
- `tests/test_architecture.py` - Core architecture tests
- `tests/test_plugin_system.py` - Plugin system tests

Run tests with:
```bash
pytest tests/test_architecture.py tests/test_plugin_system.py -v
```

## Future Enhancements

Planned improvements to the architecture:

- [ ] Network multiplayer support in event system
- [ ] Database backend for save/load system
- [ ] Hot-reloading for plugins during development
- [ ] Performance monitoring and profiling
- [ ] State machine framework for game phases
- [ ] Command pattern for action execution
- [ ] Dependency injection container

## Contributing

When adding new games:

1. Extend `GameEngine` for your game logic
2. Use the event system for state changes
3. Implement save/load functionality
4. Add settings support
5. Make state observable for GUI integration
6. Include comprehensive tests

See `CONTRIBUTING.md` for detailed guidelines.
