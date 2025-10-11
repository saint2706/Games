# Testing Guide

This document describes the testing infrastructure for the Games project.

## Table of Contents

- [Overview](#overview)
- [Running Tests](#running-tests)
- [Test Coverage](#test-coverage)
- [Test Categories](#test-categories)
- [Performance Testing](#performance-testing)
- [GUI Testing](#gui-testing)
- [Mutation Testing](#mutation-testing)
- [Writing Tests](#writing-tests)
- [Continuous Integration](#continuous-integration)

## Overview

The Games project uses pytest as its testing framework with several plugins for enhanced functionality:

- **pytest**: Core testing framework
- **pytest-cov**: Coverage reporting
- **pytest-qt**: GUI testing support
- **pytest-benchmark**: Performance benchmarking
- **mutmut**: Mutation testing

Current test coverage: **30%+** (goal: **90%+**)

## Running Tests

### Basic Test Execution

Run all tests:

```bash
pytest
```

Run with verbose output:

```bash
pytest -v
```

Run specific test file:

```bash
pytest tests/test_nim.py
```

Run specific test:

```bash
pytest tests/test_nim.py::test_computer_move_leaves_zero_nim_sum_when_possible
```

### Parallel Test Execution

Run tests in parallel (requires pytest-xdist):

```bash
pytest -n auto
```

## Test Coverage

### Generate Coverage Report

Run tests with coverage:

```bash
pytest --cov=paper_games --cov=card_games --cov-report=html --cov-report=term-missing
```

View HTML coverage report:

```bash
open htmlcov/index.html  # macOS/Linux
# or
start htmlcov/index.html  # Windows
```

### Coverage Configuration

Coverage settings are in `pytest.ini`:

- Minimum coverage threshold: 90%
- Excludes: tests, demos, __main__ files
- Reports: HTML, terminal, XML (for CI)

### Current Coverage by Module

Check current coverage:

```bash
pytest --cov=paper_games --cov=card_games --cov-report=term-missing
```

## Test Categories

Tests are organized using pytest markers:

### Unit Tests

```bash
pytest -m unit
```

Test individual functions and classes in isolation.

### Integration Tests

```bash
pytest -m integration
```

Test CLI interfaces and module interactions.

### GUI Tests

```bash
pytest -m gui
```

Test GUI components (requires display).

### Performance Tests

```bash
pytest -m performance
```

Benchmark tests for game algorithms.

### Network Tests

```bash
pytest -m network
```

Tests requiring network connectivity.

### Slow Tests

```bash
pytest -m "not slow"  # Skip slow tests
pytest -m slow        # Run only slow tests
```

## Performance Testing

Performance tests ensure game algorithms run efficiently:

```bash
pytest tests/test_performance.py -v
```

### Benchmarking

Individual benchmarks can be run with:

```bash
pytest tests/test_performance.py::TestNimPerformance::test_nim_computer_move_performance
```

Performance thresholds are defined in each test and will fail if exceeded.

## GUI Testing

GUI tests use pytest-qt and require a display:

```bash
pytest tests/test_gui_framework.py
```

In headless CI environments, GUI tests are automatically skipped.

### Running GUI Tests Locally

Ensure you have a display available:

```bash
# Linux with X11
export DISPLAY=:0
pytest -m gui

# Skip GUI tests
pytest -m "not gui"
```

## Mutation Testing

Mutation testing validates test quality by introducing bugs and checking if tests catch them.

### Run Mutation Tests

```bash
# Run mutation testing
mutmut run

# Show results
mutmut results

# Show specific mutation
mutmut show <id>

# Generate HTML report
mutmut html
```

### Configuration

Mutation testing settings are in `.mutmut.toml`:

- Excludes: GUI files, demos, __main__ files
- Uses coverage data to target tested code
- Parallel execution support

## Writing Tests

### Test Structure

```python
import pytest
from paper_games.nim import NimGame

def test_nim_basic_functionality():
    """Test basic Nim game functionality."""
    game = NimGame([3, 4, 5])
    assert not game.is_over()
    assert game.nim_sum() == 2
```

### Using Fixtures

```python
def test_with_fixture(nim_game_scenarios):
    """Test using a fixture from conftest.py."""
    heaps = nim_game_scenarios["simple_win"]
    game = NimGame(heaps)
    assert not game.is_over()
```

### Markers

Add markers to categorize tests:

```python
@pytest.mark.unit
def test_unit_example():
    """Unit test example."""
    pass

@pytest.mark.integration
def test_integration_example():
    """Integration test example."""
    pass

@pytest.mark.performance
def test_performance_example():
    """Performance test example."""
    pass
```

### Test Fixtures

Common fixtures are available in `conftest.py` and `tests/fixtures/`:

- `fixed_random`: Seeded random generator
- `temp_wordlist`: Temporary word list file
- `nim_game_scenarios`: Common Nim scenarios
- `tic_tac_toe_boards`: Common board states
- `poker_hands`: Poker hand examples
- `seeded_random`: Reproducible randomness

## Continuous Integration

### GitHub Actions Workflows

The project uses GitHub Actions for CI:

#### Test Workflow (`.github/workflows/test.yml`)

- Runs on: Python 3.11, 3.12
- Executes: Full test suite with coverage
- Coverage threshold: 30% (increasing to 90%)

#### CI Workflow (`.github/workflows/ci.yml`)

- Combines: Linting + Testing
- Uploads: Coverage reports to Codecov
- Runs on: All pushes and pull requests

### Running CI Locally

Simulate CI environment:

```bash
# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run linting
black --check .
ruff check .
mdformat --check .

# Run tests with coverage
pytest --cov=paper_games --cov=card_games --cov-report=term-missing
```

## Best Practices

1. **Write tests first**: Use TDD when possible
2. **Test behavior, not implementation**: Focus on what code does, not how
3. **Use descriptive names**: Test names should explain what they test
4. **Keep tests isolated**: Each test should be independent
5. **Use fixtures**: Share common setup code via fixtures
6. **Mock external dependencies**: Don't rely on network, files, etc.
7. **Test edge cases**: Include boundary conditions and error cases
8. **Maintain fast tests**: Keep unit tests under 1 second
9. **Document complex tests**: Add docstrings explaining test purpose
10. **Run tests frequently**: Test early and often during development

## Coverage Goals

### Current Status

- Overall: ~30%
- Paper Games: 40-90% (varies by module)
- Card Games: 20-80% (varies by module)

### Target Coverage by Module

| Module Type | Target | Priority |
| ----------- | ------ | -------- |
| Core game logic | 95%+ | High |
| AI algorithms | 90%+ | High |
| Statistics | 90%+ | Medium |
| CLI interfaces | 80%+ | Medium |
| GUI components | 60%+ | Low |
| Demo scripts | 30%+ | Low |

## Troubleshooting

### Common Issues

#### tkinter not available

```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# macOS
brew install python-tk

# Windows
# Reinstall Python with tkinter support
```

#### Tests timing out

Increase timeout in `pytest.ini` or skip slow tests:

```bash
pytest -m "not slow"
```

#### Coverage not updating

Clear pytest cache:

```bash
pytest --cache-clear
rm -rf .pytest_cache htmlcov .coverage
```

## Additional Resources

- [pytest Documentation](https://docs.pytest.org/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
- [mutmut Documentation](https://mutmut.readthedocs.io/)
- [pytest-qt Documentation](https://pytest-qt.readthedocs.io/)

## Contributing

When contributing tests:

1. Follow existing test patterns
2. Ensure all new code has tests
3. Maintain or increase coverage
4. Add markers appropriately
5. Document complex test scenarios
6. Run full test suite before submitting PR

For more information, see CONTRIBUTING.md (to be created).
