Code Quality Standards and Guidelines
=====================================

This document outlines the code quality standards, tools, and best
practices for the Games repository.

Overview
--------

The codebase follows consistent standards for formatting, linting,
testing, and complexity management. These standards are enforced through
automated tools and pre-commit hooks.

Code Quality Tools
------------------

1. Pre-commit Hooks
~~~~~~~~~~~~~~~~~~~

Pre-commit hooks automatically check and fix code quality issues before
commits.

**Installation:**

.. code:: bash

   pip install pre-commit
   pre-commit install

**What gets checked:**

-  **Black** - Code formatting
-  **Ruff** - Linting and import sorting
-  **isort** - Import organization
-  **mypy** - Static type checking
-  **Trailing whitespace** - Removes trailing spaces
-  **YAML/JSON validation** - Checks configuration files
-  **Large files** - Prevents commits of files >1MB

**Usage:**

.. code:: bash

   # Run on staged files (automatic on commit)
   git commit -m "Your message"

   # Run on all files manually
   pre-commit run --all-files

   # Run specific hook
   pre-commit run black --all-files

2. Code Formatting (Black)
~~~~~~~~~~~~~~~~~~~~~~~~~~

Black is the code formatter with line length set to 160.

**Run manually:**

.. code:: bash

   black .

**Configuration:** ``pyproject.toml``

.. code:: toml

   [tool.black]
   line-length = 160

3. Linting (Ruff)
~~~~~~~~~~~~~~~~~

Ruff is a fast Python linter that checks for errors, style issues, and
complexity.

**Run manually:**

.. code:: bash

   ruff check .
   ruff check --fix .  # Auto-fix issues

**Configuration:** ``pyproject.toml``

.. code:: toml

   [tool.ruff]
   line-length = 160

   [tool.ruff.lint]
   select = ["E", "F", "I", "C90"]  # Errors, Pyflakes, isort, McCabe complexity
   ignore = ["E402"]  # Allow imports not at top

   [tool.ruff.lint.mccabe]
   max-complexity = 10  # Maximum cyclomatic complexity

**Key checks:**

-  E: PEP 8 errors
-  F: Pyflakes (undefined names, unused imports)
-  I: Import sorting
-  C90: Cyclomatic complexity (max 10)

4. Type Checking (mypy)
~~~~~~~~~~~~~~~~~~~~~~~

Mypy performs static type analysis.

**Run manually:**

.. code:: bash

   mypy .

**Configuration:** ``pyproject.toml``

.. code:: toml

   [tool.mypy]
   python_version = "3.9"
   warn_return_any = true
   warn_unused_configs = true
   ignore_missing_imports = true
   no_strict_optional = true

5. Complexity Analysis (Radon)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Radon analyzes code complexity and maintainability.

**Run the analysis script:**

.. code:: bash

   ./scripts/check_complexity.sh

**Manual usage:**

.. code:: bash

   # Cyclomatic complexity
   radon cc . -a -s

   # Maintainability index
   radon mi . -s

   # Show only problematic files
   radon cc . -n B  # Show complexity B and above

**Complexity ratings:**

-  **A (1-5)**: Simple, low risk ✅
-  **B (6-10)**: Moderate complexity ⚠️
-  **C (11-20)**: Moderate to high complexity ⚠️
-  **D (21-30)**: High complexity 🔴
-  **E (31-40)**: Very high complexity 🔴
-  **F (41+)**: Extremely high complexity 🔴

**Target:** Keep all methods at complexity ≤10 (A or B rating)

Code Standards
--------------

Type Hints
~~~~~~~~~~

All code should include type hints for better IDE support and type
safety.

**Required:**

.. code:: python

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

**Type hint coverage:** 95%+ of functions should have type hints

Docstrings
~~~~~~~~~~

All public functions, classes, and modules should have docstrings.

**Format:** Google style

.. code:: python

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

Complexity Guidelines
~~~~~~~~~~~~~~~~~~~~~

**Keep functions simple:**

-  Maximum complexity: 10
-  Maximum lines per function: 50 (guideline)
-  Maximum parameters: 5 (guideline)

**Refactoring triggers:**

-  Complexity > 10: Split into smaller functions
-  Function > 50 lines: Consider breaking up
-  Nested loops > 2 levels: Extract to separate functions
-  Too many parameters: Use dataclasses or config objects

**Example refactoring:**

.. code:: python

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

Import Organization
~~~~~~~~~~~~~~~~~~~

Imports should be organized in the following order:

1. Standard library imports
2. Third-party imports
3. Local imports

**Example:**

.. code:: python

   from __future__ import annotations

   import random
   import sys
   from typing import List, Optional

   import colorama

   from .game_engine import GameEngine
   from .utils import helper_function

This is automatically enforced by isort and Ruff.

Testing Standards
-----------------

Test Coverage
~~~~~~~~~~~~~

**Target:** 90%+ test coverage for all modules

**Run tests:**

.. code:: bash

   # All tests
   pytest

   # With coverage
   pytest --cov=. --cov-report=html
   pytest --cov=. --cov-report=term-missing

   # Specific test file
   pytest tests/test_common_base_classes.py -v

Test Structure
~~~~~~~~~~~~~~

.. code:: python

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

Workflow
--------

Development Workflow
~~~~~~~~~~~~~~~~~~~~

1. **Create a feature branch**

   .. code:: bash

      git checkout -b feature/my-feature

2. **Make changes**

   -  Write code following standards
   -  Add type hints
   -  Keep complexity low
   -  Add tests

3. **Check quality locally**

   .. code:: bash

      # Format code
      black .

      # Check linting
      ruff check --fix .

      # Run tests
      pytest

      # Check complexity
      ./scripts/check_complexity.sh

4. **Commit changes**

   .. code:: bash

      git add .
      git commit -m "Add feature X"
      # Pre-commit hooks run automatically

5. **Push and create PR**

   .. code:: bash

      git push origin feature/my-feature

Pre-commit Hook Failures
~~~~~~~~~~~~~~~~~~~~~~~~

If pre-commit hooks fail:

1. **Review the error messages**
2. **Fix the issues** (or let the tool auto-fix)
3. **Stage the changes** (``git add .``)
4. **Commit again**

**Common fixes:**

.. code:: bash

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

Continuous Improvement
----------------------

Code Review Checklist
~~~~~~~~~~~~~~~~~~~~~

When reviewing code, check for:

-  ✅ Type hints on all functions
-  ✅ Docstrings on public APIs
-  ✅ Complexity ≤10 per function
-  ✅ Tests for new functionality
-  ✅ No obvious bugs or edge cases
-  ✅ Clear variable names
-  ✅ Follows existing patterns
-  ✅ Pre-commit hooks pass

Refactoring Guidelines
~~~~~~~~~~~~~~~~~~~~~~

When refactoring:

1. **Start with tests** - Ensure existing tests pass
2. **Make small changes** - One improvement at a time
3. **Run tests frequently** - After each change
4. **Check complexity** - Ensure it improves
5. **Update documentation** - Keep it in sync

Performance Considerations
~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Profile before optimizing
-  Optimize hot paths first
-  Don’t sacrifice readability for minor gains
-  Document performance-critical sections

Resources
---------

-  **Black documentation:** https://black.readthedocs.io/
-  **Ruff documentation:** https://docs.astral.sh/ruff/
-  **mypy documentation:** https://mypy.readthedocs.io/
-  **Radon documentation:** https://radon.readthedocs.io/
-  **pre-commit documentation:** https://pre-commit.com/

Questions?
----------

If you have questions about code quality standards, please:

1. Check this document
2. Review ``developers/architecture`` for patterns
3. Look at existing code examples
4. Open an issue for discussion

--------------

Code Complexity Analysis
------------------------

This section provides an analysis of code complexity across the
repository and recommendations for future improvements.

**Last Updated:** 2025-10-11

Current State Summary
~~~~~~~~~~~~~~~~~~~~~

The codebase has been analyzed using Radon for cyclomatic complexity and
maintainability index.

**Complexity Ratings:**

-  **Target:** All functions/methods should have complexity ≤ 10
-  **Current State:** Several functions exceed this threshold

High Complexity Functions (C or higher)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These functions should be considered for refactoring:

Critical (D-E-F ratings: 21+)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. **``src/games_collection/games/paper/nim/cli.py:play_classic_nim``** - E (40)

   -  Very high complexity, main game loop with many nested conditions
   -  Recommendation: Split into separate functions for setup, game
      loop, and turn handling

2. **``src/games_collection/games/paper/tic_tac_toe/cli.py:play``** - D (28)

   -  High complexity in main game loop
   -  Recommendation: Extract functions for input handling, display
      updates, and turn logic

3. **``src/games_collection/games/paper/battleship/cli.py:_game_loop``** - D (28)

   -  Complex game loop with multiple phases
   -  Recommendation: Split into phase-specific functions

4. **``src/games_collection/games/paper/tic_tac_toe/tic_tac_toe.py:TicTacToeGame.winner``** -
   D (25)

   -  Complex winner detection logic
   -  Recommendation: Extract helper functions for checking rows,
      columns, diagonals

5. **``src/games_collection/games/paper/hangman/cli.py:_play_multiplayer``** - D (24)

   -  Complex multiplayer logic
   -  Recommendation: Split into player setup, turn handling, and
      scoring

6. **``src/games_collection/games/paper/unscramble/cli.py:_play_multiplayer``** - D (23)

   -  Complex multiplayer game flow
   -  Recommendation: Extract turn logic and scoring to separate
      functions

7. **``src/games_collection/games/paper/tic_tac_toe/ultimate_cli.py:play_ultimate``** - D
   (21)

   -  Complex UI and game loop
   -  Recommendation: Separate UI rendering from game logic

Moderate-High (C rating: 11-20)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  **``src/games_collection/games/paper/battleship/gui.py:BattleshipGUI._draw_board``** - C
   (18)
-  **``src/games_collection/games/paper/dots_and_boxes/tournament.py:Tournament.play_game``**
   - C (17)
-  **``src/games_collection/games/paper/nim/nim.py:NimGame.computer_move``** - C (17)
-  **``src/games_collection/games/paper/unscramble/unscramble.py:load_words_by_difficulty``**
   - C (16)
-  **``src/games_collection/games/paper/battleship/battleship.py:BattleshipGame.ai_shoot``**
   - C (15)
-  **``src/games_collection/games/paper/tic_tac_toe/network_cli.py:play_network_client``** -
   C (15)
-  **``src/games_collection/games/paper/tic_tac_toe/network_cli.py:play_network_server``** -
   C (14)
-  **``src/games_collection/games/paper/battleship/gui.py:BattleshipGUI._on_opponent_canvas_click``**
   - C (14)
-  **``src/games_collection/games/paper/tic_tac_toe/tic_tac_toe.py:TicTacToeGame.minimax``**
   - C (14)
-  **``src/games_collection/games/paper/tic_tac_toe/ultimate.py:UltimateTicTacToeGame.render``**
   - C (13)
-  **``src/games_collection/games/paper/dots_and_boxes/network.py:play_network_game``** - C
   (13)
-  **``src/games_collection/games/paper/nim/nim.py:NimGame.get_strategy_hint``** - C (13)
-  **``src/games_collection/games/paper/unscramble/stats.py:GameStats.record_word``** - C
   (13)
-  **``src/games_collection/games/paper/unscramble/stats.py:GameStats.summary``** - C (13)

Low Maintainability (MI < 20)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These files have low maintainability scores:

1. **``src/games_collection/games/card/uno/uno.py``** - MI: 0.00 (very low)
2. **``src/games_collection/games/card/poker/poker.py``** - MI: 0.87 (very low)
3. **``src/games_collection/games/card/bluff/bluff.py``** - MI: 4.22 (very low)
4. **``src/games_collection/games/card/blackjack/game.py``** - MI: 17.97 (low)

**Note:** These are complex game engines with extensive logic. While
they have low MI scores, they are well-documented and have comprehensive
test coverage.

Refactoring Priorities
~~~~~~~~~~~~~~~~~~~~~~

High Priority (Critical Complexity)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. **Nim CLI** (``src/games_collection/games/paper/nim/cli.py:play_classic_nim``)

   -  Complexity: 40 (E rating)
   -  Impact: High - main game function
   -  Effort: Medium - can be split into logical sections

2. **Tic Tac Toe CLI** (``src/games_collection/games/paper/tic_tac_toe/cli.py:play``)

   -  Complexity: 28 (D rating)
   -  Impact: High - main game function
   -  Effort: Medium

3. **Battleship CLI** (``src/games_collection/games/paper/battleship/cli.py:_game_loop``)

   -  Complexity: 28 (D rating)
   -  Impact: High - core game loop
   -  Effort: High - complex state management

Medium Priority (Moderate Complexity)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

4. **AI Functions** (various ``computer_move`` functions)

   -  Complexity: 15-17 (C rating)
   -  Impact: Medium - affects gameplay
   -  Effort: Low-Medium - can extract decision logic

5. **Rendering Functions** (various ``render`` functions)

   -  Complexity: 11-13 (C rating)
   -  Impact: Low - display only
   -  Effort: Low - can split into helper functions

Low Priority (Acceptable Complexity)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Functions with complexity 11-13 (C rating) are acceptable but could be
improved:

-  Network play functions
-  Tournament management
-  Statistics tracking

Recommended Refactoring Patterns
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Extract Method
^^^^^^^^^^^^^^^^^

**Before:**

.. code:: python

   def complex_function():
       # Setup code
       # Validation code
       # Main logic
       # Cleanup code
       pass

**After:**

.. code:: python

   def complex_function():
       _setup()
       _validate()
       _execute_logic()
       _cleanup()

   def _setup(): ...
   def _validate(): ...
   def _execute_logic(): ...
   def _cleanup(): ...

2. State Machine Pattern
^^^^^^^^^^^^^^^^^^^^^^^^

For CLI game loops with multiple phases:

.. code:: python

   class GameState(Enum):
       SETUP = "setup"
       PLAYING = "playing"
       GAME_OVER = "game_over"

   def play():
       state = GameState.SETUP
       while state != GameState.GAME_OVER:
           if state == GameState.SETUP:
               state = handle_setup()
           elif state == GameState.PLAYING:
               state = handle_turn()

3. Strategy Pattern
^^^^^^^^^^^^^^^^^^^

Already implemented in ``src/games_collection/core/ai_strategy.py`` - use for AI logic:

.. code:: python

   from games_collection.core import HeuristicStrategy

   def ai_heuristic(move, state):
       return calculate_score(move, state)

   ai = HeuristicStrategy(heuristic_fn=ai_heuristic)
   move = ai.select_move(valid_moves, game_state)

4. Command Pattern
^^^^^^^^^^^^^^^^^^

For user input handling:

.. code:: python

   def handle_input(command: str):
       handlers = {
           'move': handle_move,
           'quit': handle_quit,
           'help': handle_help,
       }
       handler = handlers.get(command, handle_invalid)
       return handler()

Complexity Monitoring
~~~~~~~~~~~~~~~~~~~~~

Automated Checks
^^^^^^^^^^^^^^^^

Pre-commit hooks now include complexity checks via Ruff:

.. code:: yaml

   [tool.ruff.lint.mccabe]
   max-complexity = 10

Manual Analysis
^^^^^^^^^^^^^^^

Run the complexity check script:

.. code:: bash

   ./scripts/check_complexity.sh

CI Integration (Recommended)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Add to CI pipeline:

.. code:: yaml

   - name: Check Complexity
     run: |
       pip install radon
       radon cc . -a -n C --exclude="tests/*,colorama/*"
       # Fail if any function has complexity > 20
       radon cc . -n D --exclude="tests/*,colorama/*" && exit 1 || exit 0

Guidelines for New Code
~~~~~~~~~~~~~~~~~~~~~~~

1. **Target complexity ≤ 10** for all new functions

2. **Extract helpers** when approaching the limit

3. **Use base classes** from ``src/games_collection/core/`` module

4. **Run checks** before committing:

   .. code:: bash

      pre-commit run --all-files
      ./scripts/check_complexity.sh

Benefits of Refactoring
~~~~~~~~~~~~~~~~~~~~~~~

-  **Easier to understand** - Smaller functions are easier to read
-  **Easier to test** - Small functions can be tested in isolation
-  **Easier to modify** - Changes have limited scope
-  **Fewer bugs** - Simpler code has fewer edge cases
-  **Better performance** - Easier to optimize small functions

Next Steps
~~~~~~~~~~

1. **Address critical complexity** (E-D ratings) in future PRs
2. **Use base classes** for new games
3. **Monitor complexity** in code reviews
4. **Document complex logic** when refactoring isn’t feasible
5. **Add tests** before refactoring to ensure behavior preservation

Conclusion
~~~~~~~~~~

While some legacy code has high complexity, the project now has:

-  ✅ Tools to measure complexity
-  ✅ Guidelines for new code
-  ✅ Base classes to reduce duplication
-  ✅ Automated checks to prevent regression
-  ✅ Clear priorities for future refactoring

The focus should be on keeping new code simple while gradually improving
existing code as opportunities arise.
