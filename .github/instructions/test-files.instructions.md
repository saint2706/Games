---
applyTo: "**/test_*.py"
---

# Test File Requirements

When writing or modifying test files in this repository, follow these guidelines:

## Testing Framework

- **Framework**: pytest
- **Current Coverage**: 30%+ (goal: 90%+)
- **Location**: All tests in `tests/` directory

## Test Structure Requirements

1. **File Naming**: All test files must start with `test_` prefix (e.g., `test_poker.py`)
1. **Function Naming**: Test functions must start with `test_` prefix
1. **Fixtures**: Use fixtures from `tests/fixtures/` for common test data
1. **Imports**: Always include `from __future__ import annotations` at the top

## Test Types

Include these types of tests as appropriate:

- **Unit Tests**: Test individual functions and methods in isolation
- **Integration Tests**: Test how components work together
- **Performance Benchmarks**: Use `pytest-benchmark` for performance-critical code

## Required Test Patterns

### Game Initialization Tests

```python
def test_game_initialization():
    """Test that game initializes with correct state."""
    game = GameEngine(num_players=2)
    assert len(game.players) == 2
    assert game.current_player == 0
```

### Valid/Invalid Move Tests

```python
def test_valid_move():
    """Test that valid move is accepted."""
    game = GameEngine()
    game.start()
    result = game.make_move("A1")
    assert result is True

def test_invalid_move():
    """Test that invalid move is rejected."""
    game = GameEngine()
    game.start()
    result = game.make_move("invalid")
    assert result is False
```

### Game Over Tests

```python
def test_game_over_condition():
    """Test that game ends when win condition is met."""
    game = GameEngine()
    # Set up winning condition
    assert game.is_game_over() is True
```

## Assertions

- Use descriptive assertion messages when needed
- Prefer specific assertions (e.g., `assert x == 5` over `assert x`)
- Use `pytest.raises()` for exception testing

## Fixtures and Parametrization

- Use `@pytest.fixture` for reusable test setup
- Use `@pytest.mark.parametrize` for testing multiple scenarios
- Keep fixtures simple and focused

## Documentation

- Every test function needs a docstring explaining what it tests
- Document complex test setup in comments
- Explain why specific values are used in tests

## Coverage

- Aim for 90%+ coverage for new code
- Test edge cases and error conditions
- Test both success and failure paths

## Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_poker.py

# Run with coverage
pytest --cov=card_games --cov=paper_games

# Run with verbose output
pytest -v
```
