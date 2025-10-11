# Code Quality Standards and Guidelines

This document outlines the code quality standards, tools, and best practices for the Games repository.

## Overview

The codebase follows consistent standards for formatting, linting, testing, and complexity management. These standards are enforced through automated tools and pre-commit hooks.

## Code Quality Tools

### 1. Pre-commit Hooks

Pre-commit hooks automatically check and fix code quality issues before commits.

**Installation:**

```bash
pip install pre-commit
pre-commit install
```

**What gets checked:**

- **Black** - Code formatting
- **Ruff** - Linting and import sorting
- **isort** - Import organization
- **mypy** - Static type checking
- **Trailing whitespace** - Removes trailing spaces
- **YAML/JSON validation** - Checks configuration files
- **Large files** - Prevents commits of files >1MB

**Usage:**

```bash
# Run on staged files (automatic on commit)
git commit -m "Your message"

# Run on all files manually
pre-commit run --all-files

# Run specific hook
pre-commit run black --all-files
```

### 2. Code Formatting (Black)

Black is the code formatter with line length set to 160.

**Run manually:**

```bash
black .
```

**Configuration:** `pyproject.toml`

```toml
[tool.black]
line-length = 160
```

### 3. Linting (Ruff)

Ruff is a fast Python linter that checks for errors, style issues, and complexity.

**Run manually:**

```bash
ruff check .
ruff check --fix .  # Auto-fix issues
```

**Configuration:** `pyproject.toml`

```toml
[tool.ruff]
line-length = 160

[tool.ruff.lint]
select = ["E", "F", "I", "C90"]  # Errors, Pyflakes, isort, McCabe complexity
ignore = ["E402"]  # Allow imports not at top

[tool.ruff.lint.mccabe]
max-complexity = 10  # Maximum cyclomatic complexity
```

**Key checks:**

- E: PEP 8 errors
- F: Pyflakes (undefined names, unused imports)
- I: Import sorting
- C90: Cyclomatic complexity (max 10)

### 4. Type Checking (mypy)

Mypy performs static type analysis.

**Run manually:**

```bash
mypy .
```

**Configuration:** `pyproject.toml`

```toml
[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
ignore_missing_imports = true
no_strict_optional = true
```

### 5. Complexity Analysis (Radon)

Radon analyzes code complexity and maintainability.

**Run the analysis script:**

```bash
./scripts/check_complexity.sh
```

**Manual usage:**

```bash
# Cyclomatic complexity
radon cc . -a -s

# Maintainability index
radon mi . -s

# Show only problematic files
radon cc . -n B  # Show complexity B and above
```

**Complexity ratings:**

- **A (1-5)**: Simple, low risk ✅
- **B (6-10)**: Moderate complexity ⚠️
- **C (11-20)**: Moderate to high complexity ⚠️
- **D (21-30)**: High complexity 🔴
- **E (31-40)**: Very high complexity 🔴
- **F (41+)**: Extremely high complexity 🔴

**Target:** Keep all methods at complexity ≤10 (A or B rating)

## Code Standards

### Type Hints

All code should include type hints for better IDE support and type safety.

**Required:**

```python
from __future__ import annotations  # At the top of every file

from typing import List, Optional, Dict

def calculate_score(items: List[int], multiplier: float = 1.0) -> int:
    """Calculate total score.

    Args:
        items: List of item values.
        multiplier: Score multiplier.

    Returns:
        Total calculated score.
    """
    return int(sum(items) * multiplier)
```

**Type hint coverage:** 95%+ of functions should have type hints

### Docstrings

All public functions, classes, and modules should have docstrings.

**Format:** Google style

```python
def my_function(param1: str, param2: int) -> bool:
    """Brief description of what the function does.

    More detailed explanation if needed.

    Args:
        param1: Description of first parameter.
        param2: Description of second parameter.

    Returns:
        Description of return value.

    Raises:
        ValueError: Description of when this is raised.
    """
    pass
```

### Complexity Guidelines

**Keep functions simple:**

- Maximum complexity: 10
- Maximum lines per function: 50 (guideline)
- Maximum parameters: 5 (guideline)

**Refactoring triggers:**

- Complexity > 10: Split into smaller functions
- Function > 50 lines: Consider breaking up
- Nested loops > 2 levels: Extract to separate functions
- Too many parameters: Use dataclasses or config objects

**Example refactoring:**

```python
# Before (complexity: 12)
def complex_function(a, b, c, d, e):
    result = 0
    if a > 0:
        for i in range(a):
            if b > 0:
                for j in range(b):
                    if c > 0:
                        result += c * d * e
    return result

# After (complexity: 6 + 4 = 10 total, but split across functions)
def calculate_multiplier(c: int, d: int, e: int) -> int:
    """Calculate the multiplier value."""
    return c * d * e if c > 0 else 0

def complex_function(a: int, b: int, c: int, d: int, e: int) -> int:
    """Calculate result based on parameters."""
    result = 0
    if a > 0:
        multiplier = calculate_multiplier(c, d, e)
        result = sum(multiplier for _ in range(a) for _ in range(b) if b > 0)
    return result
```

### Import Organization

Imports should be organized in the following order:

1. Standard library imports
1. Third-party imports
1. Local imports

**Example:**

```python
from __future__ import annotations

import random
import sys
from typing import List, Optional

import colorama

from .game_engine import GameEngine
from .utils import helper_function
```

This is automatically enforced by isort and Ruff.

## Testing Standards

### Test Coverage

**Target:** 90%+ test coverage for all modules

**Run tests:**

```bash
# All tests
pytest

# With coverage
pytest --cov=. --cov-report=html
pytest --cov=. --cov-report=term-missing

# Specific test file
pytest tests/test_common_base_classes.py -v
```

### Test Structure

```python
"""Test module for feature X.

This module tests the functionality of feature X including
edge cases and error handling.
"""

import unittest
from typing import List

from module import FeatureX


class TestFeatureX(unittest.TestCase):
    """Tests for FeatureX class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.feature = FeatureX()

    def test_basic_functionality(self) -> None:
        """Test basic functionality."""
        result = self.feature.do_something()
        self.assertEqual(result, expected_value)

    def test_edge_case(self) -> None:
        """Test edge case handling."""
        with self.assertRaises(ValueError):
            self.feature.do_something_invalid()
```

## Workflow

### Development Workflow

1. **Create a feature branch**

   ```bash
   git checkout -b feature/my-feature
   ```

1. **Make changes**

   - Write code following standards
   - Add type hints
   - Keep complexity low
   - Add tests

1. **Check quality locally**

   ```bash
   # Format code
   black .

   # Check linting
   ruff check --fix .

   # Run tests
   pytest

   # Check complexity
   ./scripts/check_complexity.sh
   ```

1. **Commit changes**

   ```bash
   git add .
   git commit -m "Add feature X"
   # Pre-commit hooks run automatically
   ```

1. **Push and create PR**

   ```bash
   git push origin feature/my-feature
   ```

### Pre-commit Hook Failures

If pre-commit hooks fail:

1. **Review the error messages**
1. **Fix the issues** (or let the tool auto-fix)
1. **Stage the changes** (`git add .`)
1. **Commit again**

**Common fixes:**

```bash
# Black formatting issues
black .
git add .
git commit -m "Your message"

# Import sorting
isort .
git add .
git commit -m "Your message"

# Linting issues
ruff check --fix .
git add .
git commit -m "Your message"
```

## Continuous Improvement

### Code Review Checklist

When reviewing code, check for:

- ✅ Type hints on all functions
- ✅ Docstrings on public APIs
- ✅ Complexity ≤10 per function
- ✅ Tests for new functionality
- ✅ No obvious bugs or edge cases
- ✅ Clear variable names
- ✅ Follows existing patterns
- ✅ Pre-commit hooks pass

### Refactoring Guidelines

When refactoring:

1. **Start with tests** - Ensure existing tests pass
1. **Make small changes** - One improvement at a time
1. **Run tests frequently** - After each change
1. **Check complexity** - Ensure it improves
1. **Update documentation** - Keep it in sync

### Performance Considerations

- Profile before optimizing
- Optimize hot paths first
- Don't sacrifice readability for minor gains
- Document performance-critical sections

## Resources

- **Black documentation:** https://black.readthedocs.io/
- **Ruff documentation:** https://docs.astral.sh/ruff/
- **mypy documentation:** https://mypy.readthedocs.io/
- **Radon documentation:** https://radon.readthedocs.io/
- **pre-commit documentation:** https://pre-commit.com/

## Questions?

If you have questions about code quality standards, please:

1. Check this document
1. Review `ARCHITECTURE.md` for patterns
1. Look at existing code examples
1. Open an issue for discussion
