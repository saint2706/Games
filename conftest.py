"""Pytest configuration and shared fixtures for Games project."""

import pathlib
import random
import sys
from typing import Generator

import pytest

# Ensure project root is in path
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture
def fixed_random() -> Generator[random.Random, None, None]:
    """Provide a seeded random number generator for reproducible tests."""
    yield random.Random(42)


@pytest.fixture
def temp_wordlist(tmp_path: pathlib.Path) -> Generator[pathlib.Path, None, None]:
    """Create a temporary word list file for testing."""
    wordlist_path = tmp_path / "test_words.txt"
    words = ["test", "word", "python", "game", "puzzle", "hangman", "scramble", "solution"]
    wordlist_path.write_text("\n".join(words))
    yield wordlist_path


@pytest.fixture
def mock_stdin(monkeypatch):
    """Mock stdin for CLI testing."""

    class MockStdin:
        def __init__(self, inputs):
            self.inputs = iter(inputs)

        def readline(self):
            return next(self.inputs)

    def _mock_stdin(inputs):
        monkeypatch.setattr("sys.stdin", MockStdin(inputs))

    return _mock_stdin


@pytest.fixture
def capture_output(monkeypatch, capsys):
    """Fixture to capture stdout and stderr."""
    return capsys


# Performance fixtures
@pytest.fixture
def benchmark_iterations() -> int:
    """Default number of iterations for benchmark tests."""
    return 100


@pytest.fixture
def performance_threshold() -> float:
    """Default performance threshold in seconds."""
    return 1.0


# Pytest configuration hooks
def pytest_configure(config):
    """Configure pytest with custom settings."""
    config.addinivalue_line("markers", "unit: Unit tests for individual functions and classes")
    config.addinivalue_line("markers", "integration: Integration tests for CLI and module interactions")
    config.addinivalue_line("markers", "gui: GUI tests requiring display")
    config.addinivalue_line("markers", "performance: Performance benchmarking tests")
    config.addinivalue_line("markers", "slow: Tests that take more than a few seconds")
    config.addinivalue_line("markers", "network: Tests that require network connectivity")


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test location."""
    for item in items:
        # Add integration marker for CLI tests
        if "cli" in item.nodeid.lower():
            item.add_marker(pytest.mark.integration)

        # Add gui marker for GUI tests
        if "gui" in item.nodeid.lower():
            item.add_marker(pytest.mark.gui)

        # Add performance marker for benchmark tests
        if "benchmark" in item.nodeid.lower() or "performance" in item.nodeid.lower():
            item.add_marker(pytest.mark.performance)

        # Add network marker for network tests
        if "network" in item.nodeid.lower():
            item.add_marker(pytest.mark.network)
