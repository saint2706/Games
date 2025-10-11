# Testing Quick Start Guide

This guide helps you get started with testing in the Games project quickly.

## Setup (First Time Only)

```bash
# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Running Tests

### Most Common Commands

```bash
# Run all tests
pytest

# Run all tests with coverage report
./scripts/run_tests.sh coverage

# Run fast tests only (skip slow ones)
./scripts/run_tests.sh fast

# Run specific test category
pytest -m integration  # Integration tests
pytest -m gui          # GUI tests  
pytest -m performance  # Performance tests
```

### Test a Specific File or Test

```bash
# Test a specific file
pytest tests/test_nim.py

# Test a specific function
pytest tests/test_nim.py::test_computer_move_leaves_zero_nim_sum_when_possible

# Test a specific class
pytest tests/test_cli_integration.py::TestNimCLI
```

### View Test Results

```bash
# Verbose output
pytest -v

# Show test names while running
pytest -v --tb=short

# See which tests would run without running them
pytest --collect-only
```

## Coverage

```bash
# Generate coverage report (HTML + terminal)
pytest --cov=paper_games --cov=card_games --cov-report=html --cov-report=term-missing

# Open HTML coverage report (after running above)
# Linux/macOS:
open htmlcov/index.html
# Windows:
start htmlcov/index.html

# Or use the script
./scripts/run_tests.sh coverage
```

## Writing Tests

### Basic Test Structure

```python
# tests/test_myfeature.py
import pytest
from paper_games.mygame import MyGame

def test_basic_functionality():
    """Test basic game functionality."""
    game = MyGame()
    assert game is not None
    assert game.some_method() == expected_value

@pytest.mark.integration
def test_cli_integration():
    """Test CLI integration."""
    # Integration test code here
    pass

@pytest.mark.performance
def test_performance():
    """Test performance."""
    import time
    start = time.time()
    # Run operation
    elapsed = time.time() - start
    assert elapsed < 0.1  # Should be fast
```

### Using Fixtures

```python
def test_with_fixture(nim_game_scenarios):
    """Use a fixture from conftest.py."""
    heaps = nim_game_scenarios["simple_win"]
    game = NimGame(heaps)
    assert not game.is_over()
```

## Test Markers

Mark your tests to categorize them:

```python
@pytest.mark.unit          # Unit test (isolated)
@pytest.mark.integration   # Integration test (CLI, modules)
@pytest.mark.gui           # GUI test (needs display)
@pytest.mark.performance   # Performance benchmark
@pytest.mark.slow          # Takes >10 seconds
@pytest.mark.network       # Needs network
```

Run only specific markers:

```bash
pytest -m integration    # Run only integration tests
pytest -m "not slow"     # Skip slow tests
```

## Debugging Failed Tests

```bash
# Show more context on failure
pytest -v --tb=long

# Stop on first failure
pytest -x

# Drop into debugger on failure
pytest --pdb

# Show print statements
pytest -s
```

## Pre-Commit Checklist

Before committing code:

```bash
# 1. Format code
black .
ruff check . --fix

# 2. Run fast tests
./scripts/run_tests.sh fast

# 3. Check coverage of changed files
pytest --cov=paper_games/your_module --cov-report=term-missing

# 4. Run full test suite (if you have time)
pytest
```

## CI/CD

Tests run automatically on GitHub when you:
- Push to master/main
- Create a pull request

Check the Actions tab on GitHub to see results.

## Getting Help

- **Full Guide**: See [TESTING.md](TESTING.md)
- **Implementation Details**: See [TESTING_SUMMARY.md](TESTING_SUMMARY.md)
- **Script Help**: Run `./scripts/run_tests.sh help`
- **Pytest Help**: Run `pytest --help`

## Common Issues

### tkinter not available

```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# macOS
brew install python-tk
```

### Tests timing out

```bash
# Skip slow tests
pytest -m "not slow"

# Or increase timeout in pytest.ini
```

### Coverage not updating

```bash
# Clear cache
pytest --cache-clear
rm -rf .pytest_cache htmlcov .coverage
```

## Quick Reference

| Command | What It Does |
|---------|--------------|
| `pytest` | Run all tests |
| `pytest -v` | Verbose output |
| `pytest -m integration` | Run integration tests |
| `pytest -k "test_name"` | Run tests matching name |
| `pytest --cov` | Run with coverage |
| `pytest -x` | Stop on first failure |
| `pytest --pdb` | Debug on failure |
| `./scripts/run_tests.sh help` | Show script options |

---

For more details, see [TESTING.md](TESTING.md).
