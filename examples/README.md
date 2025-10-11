# Architecture Examples

This directory contains example scripts demonstrating the architecture components.

## Running Examples

All examples should be run from the repository root with the correct PYTHONPATH:

```bash
cd /home/runner/work/Games/Games
PYTHONPATH=/home/runner/work/Games/Games python examples/architecture_demo.py
```

Or use the Python module approach:

```bash
cd /home/runner/work/Games/Games
python -m examples.architecture_demo
```

## Available Examples

### architecture_demo.py

A comprehensive demonstration of all architecture components:

1. **Plugin System** - Loading and managing plugins
2. **Game Engine** - Creating game instances
3. **Event System** - Event-driven architecture
4. **Observer Pattern** - State change notifications
5. **Settings System** - Configuration management
6. **Replay System** - Action recording
7. **Save/Load System** - Game state persistence
8. **Replay Analysis** - Reviewing recorded actions
9. **Undo System** - Undoing/redoing actions
10. **Event History** - Analyzing event patterns

The demo uses the example number guessing game plugin to demonstrate all features in action.

### Expected Output

When you run the demo, you'll see:
- Plugin discovery and loading
- Event notifications as game progresses
- State change observations
- Settings loading and usage
- Game being played with 4 guesses
- Save/load operations
- Replay analysis showing all actions
- Undo/redo functionality
- Event statistics

## Creating Your Own Examples

To create a new example:

1. Create a Python file in this directory
2. Import the architecture components you need
3. Use the example_plugin or create your own test plugin
4. Make the file executable: `chmod +x your_example.py`
5. Add documentation to this README

Example template:

```python
#!/usr/bin/env python
"""Your example description."""

from pathlib import Path
from common.architecture import PluginManager

def main():
    # Your example code here
    pass

if __name__ == "__main__":
    main()
```

## Tips

- Always run examples from the repository root
- Use `PYTHONPATH` to ensure imports work correctly
- Check the plugin system is working with `discover_plugins()`
- Use temporary directories for save/settings to avoid cluttering the repo
- Add descriptive output so others can follow what's happening

## Further Reading

- See `ARCHITECTURE.md` for detailed component documentation
- Check `plugins/README.md` for plugin development guide
- Review `tests/test_architecture.py` for usage patterns
