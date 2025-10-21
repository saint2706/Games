Testing Guide
=============

This document describes the testing infrastructure for the Games
project.

Table of Contents
-----------------

-  `Quick Start <#quick-start>`__
-  `Overview <#overview>`__
-  `Running Tests <#running-tests>`__
-  `Test Coverage <#test-coverage>`__
-  `Test Categories <#test-categories>`__
-  `Performance Testing <#performance-testing>`__
-  `GUI Testing <#gui-testing>`__
-  `Mutation Testing <#mutation-testing>`__
-  `Writing Tests <#writing-tests>`__
-  `Continuous Integration <#continuous-integration>`__

Quick Start
-----------

Setup (First Time Only)
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

   # Install package with development dependencies
   pip install -e ".[dev]"

   # Or install from PyPI
   pip install games-collection[dev]

Most Common Commands
~~~~~~~~~~~~~~~~~~~~

.. code:: bash

   # Run all tests
   pytest

   # Run the CI-equivalent suite (skips performance benchmarks)
   pytest -m "not performance"

   # Run all tests with coverage report
   ./scripts/run_tests.sh coverage

   # Run fast tests only (skip slow ones)
   ./scripts/run_tests.sh fast

   # Run specific test category
   pytest -m integration  # Integration tests
   pytest -m gui          # GUI tests
   pytest -m performance  # Performance tests

Test a Specific File or Test
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

   # Test a specific file
   pytest tests/test_nim.py

   # Test a specific function
   pytest tests/test_nim.py::test_computer_move_leaves_zero_nim_sum_when_possible

   # Test a specific class
   pytest tests/test_cli_integration.py::TestNimCLI

Pre-Commit Checklist
~~~~~~~~~~~~~~~~~~~~

Before committing code:

.. code:: bash

   # 1. Format code
   black .
   ruff check . --fix

   # 2. Run fast tests
   ./scripts/run_tests.sh fast

   # 3. Check coverage of changed files
   pytest --cov=paper_games/your_module --cov-report=term-missing

   # 4. Run full test suite (if you have time)
   pytest

Quick Reference
~~~~~~~~~~~~~~~

=============================== =======================
Command                         What It Does
=============================== =======================
``pytest``                      Run all tests
``pytest -v``                   Verbose output
``pytest -m integration``       Run integration tests
``pytest -k "test_name"``       Run tests matching name
``pytest --cov``                Run with coverage
``pytest -x``                   Stop on first failure
``pytest --pdb``                Debug on failure
``./scripts/run_tests.sh help`` Show script options
=============================== =======================

Overview
--------

The Games project uses pytest as its testing framework with several
plugins for enhanced functionality:

-  **pytest**: Core testing framework
-  **pytest-cov**: Coverage reporting
-  **pytest-qt**: GUI testing support
-  **pytest-benchmark**: Performance benchmarking
-  **mutmut**: Mutation testing

Current test coverage: **30%+** (goal: **90%+**)

Running Tests
-------------

Basic Test Execution
~~~~~~~~~~~~~~~~~~~~

Run all tests:

.. code:: bash

   pytest

Run with verbose output:

.. code:: bash

   pytest -v

Run specific test file:

.. code:: bash

   pytest tests/test_nim.py

Run specific test:

.. code:: bash

   pytest tests/test_nim.py::test_computer_move_leaves_zero_nim_sum_when_possible

Parallel Test Execution
~~~~~~~~~~~~~~~~~~~~~~~

Run tests in parallel (requires pytest-xdist):

.. code:: bash

   pytest -n auto

Test Coverage
-------------

Generate Coverage Report
~~~~~~~~~~~~~~~~~~~~~~~~

Run tests with coverage:

.. code:: bash

   pytest --cov=paper_games --cov=card_games --cov-report=html --cov-report=term-missing

View HTML coverage report:

.. code:: bash

   open htmlcov/index.html  # macOS/Linux
   # or
   start htmlcov/index.html  # Windows

Coverage Configuration
~~~~~~~~~~~~~~~~~~~~~~

Coverage settings are in ``pytest.ini``:

-  Minimum coverage threshold: 90%
-  Excludes: tests, demos, **main** files
-  Reports: HTML, terminal, XML (for CI)

Current Coverage by Module
~~~~~~~~~~~~~~~~~~~~~~~~~~

Check current coverage:

.. code:: bash

   pytest --cov=paper_games --cov=card_games --cov-report=term-missing

Test Categories
---------------

Tests are organized using pytest markers:

Unit Tests
~~~~~~~~~~

.. code:: bash

   pytest -m unit

Test individual functions and classes in isolation.

Integration Tests
~~~~~~~~~~~~~~~~~

.. code:: bash

   pytest -m integration

Test CLI interfaces and module interactions.

GUI Tests
~~~~~~~~~

.. code:: bash

   pytest -m gui

Test GUI components (requires display).

Performance Tests
~~~~~~~~~~~~~~~~~

.. code:: bash

   pytest -m performance

Benchmark tests for game algorithms. These are intended for local
validation and are skipped automatically in continuous integration
environments to keep pipeline execution times reasonable.

Network Tests
~~~~~~~~~~~~~

.. code:: bash

   pytest -m network

Tests requiring network connectivity.

Slow Tests
~~~~~~~~~~

.. code:: bash

   pytest -m "not slow"  # Skip slow tests
   pytest -m slow        # Run only slow tests

Performance Testing
-------------------

Performance tests ensure game algorithms run efficiently:

.. code:: bash

   pytest tests/test_performance.py -v

Because performance benchmarks can take significantly longer than
functional tests, the CI configuration skips them by default. Run the
command above (or ``pytest -m performance``) locally to validate
performance before merging.

Benchmarking
~~~~~~~~~~~~

Individual benchmarks can be run with:

.. code:: bash

   pytest tests/test_performance.py::TestNimPerformance::test_nim_computer_move_performance

Performance thresholds are defined in each test and will fail if
exceeded.

GUI Testing
-----------

GUI tests use pytest-qt and require a display:

.. code:: bash

   pytest tests/test_gui_framework.py

In headless CI environments, GUI tests are automatically skipped.

Running GUI Tests Locally
~~~~~~~~~~~~~~~~~~~~~~~~~

Ensure you have a display available:

.. code:: bash

   # Linux with X11
   export DISPLAY=:0
   pytest -m gui

   # Skip GUI tests
   pytest -m "not gui"

Mutation Testing
----------------

Mutation testing validates test quality by introducing bugs and checking
if tests catch them.

Run Mutation Tests
~~~~~~~~~~~~~~~~~~

.. code:: bash

   # Run mutation testing
   mutmut run

   # Show results
   mutmut results

   # Show specific mutation
   mutmut show <id>

   # Generate HTML report
   mutmut html

Configuration
~~~~~~~~~~~~~

Mutation testing settings are in ``pyproject.toml`` under
``[tool.mutmut]``:

-  Paths to mutate: ``paper_games/``, ``card_games/``
-  Excludes: GUI files, demos, ``__main__.py``, ``__init__.py``, tests
-  Uses coverage data to target tested code
-  Test runner: pytest with specific flags

Writing Tests
-------------

Test Structure
~~~~~~~~~~~~~~

.. code:: python

   import pytest
   from paper_games.nim import NimGame

   def test_nim_basic_functionality():
       """Test basic Nim game functionality."""
       game = NimGame([3, 4, 5])
       assert not game.is_over()
       assert game.nim_sum() == 2

Using Fixtures
~~~~~~~~~~~~~~

.. code:: python

   def test_with_fixture(nim_game_scenarios):
       """Test using a fixture from conftest.py."""
       heaps = nim_game_scenarios["simple_win"]
       game = NimGame(heaps)
       assert not game.is_over()

Markers
~~~~~~~

Add markers to categorize tests:

.. code:: python

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

Test Fixtures
~~~~~~~~~~~~~

Common fixtures are available in ``conftest.py`` and
``tests/fixtures/``:

-  ``fixed_random``: Seeded random generator
-  ``temp_wordlist``: Temporary word list file
-  ``nim_game_scenarios``: Common Nim scenarios
-  ``tic_tac_toe_boards``: Common board states
-  ``poker_hands``: Poker hand examples
-  ``seeded_random``: Reproducible randomness

Continuous Integration
----------------------

GitHub Actions Workflows
~~~~~~~~~~~~~~~~~~~~~~~~

The project uses GitHub Actions for CI:

CI Workflow (``.github/workflows/ci.yml``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  Combines: Linting + Testing
-  Uploads: Coverage reports to Codecov
-  Runs on: All pushes and pull requests
-  Test command:
   ``pytest -m "not performance" --cov=paper_games --cov=card_games``

Running CI Locally
~~~~~~~~~~~~~~~~~~

Simulate CI environment:

.. code:: bash

   # Install package with development dependencies
   pip install -e ".[dev]"

   # Run linting
   black --check .
   ruff check .
   mdformat --check .

   # Run tests with coverage (matches CI configuration)
   pytest -m "not performance" --cov=paper_games --cov=card_games --cov-report=term-missing

Best Practices
--------------

1.  **Write tests first**: Use TDD when possible
2.  **Test behavior, not implementation**: Focus on what code does, not
    how
3.  **Use descriptive names**: Test names should explain what they test
4.  **Keep tests isolated**: Each test should be independent
5.  **Use fixtures**: Share common setup code via fixtures
6.  **Mock external dependencies**: Don’t rely on network, files, etc.
7.  **Test edge cases**: Include boundary conditions and error cases
8.  **Maintain fast tests**: Keep unit tests under 1 second
9.  **Document complex tests**: Add docstrings explaining test purpose
10. **Run tests frequently**: Test early and often during development

Coverage Goals
--------------

Current Status
~~~~~~~~~~~~~~

-  Overall: ~30%
-  Paper Games: 40-90% (varies by module)
-  Card Games: 20-80% (varies by module)

Target Coverage by Module
~~~~~~~~~~~~~~~~~~~~~~~~~

=============== ====== ========
Module Type     Target Priority
=============== ====== ========
Core game logic 95%+   High
AI algorithms   90%+   High
Statistics      90%+   Medium
CLI interfaces  80%+   Medium
GUI components  60%+   Low
Demo scripts    30%+   Low
=============== ====== ========

Troubleshooting
---------------

Common Issues
~~~~~~~~~~~~~

tkinter not available
^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

   # Ubuntu/Debian
   sudo apt-get install python3-tk

   # macOS
   brew install python-tk

   # Windows
   # Reinstall Python with tkinter support

Tests timing out
^^^^^^^^^^^^^^^^

Increase timeout in ``pytest.ini`` or skip slow tests:

.. code:: bash

   pytest -m "not slow"

Coverage not updating
^^^^^^^^^^^^^^^^^^^^^

Clear pytest cache:

.. code:: bash

   pytest --cache-clear
   rm -rf .pytest_cache htmlcov .coverage

Additional Resources
--------------------

-  `pytest Documentation <https://docs.pytest.org/>`__
-  `Coverage.py Documentation <https://coverage.readthedocs.io/>`__
-  `mutmut Documentation <https://mutmut.readthedocs.io/>`__
-  `pytest-qt Documentation <https://pytest-qt.readthedocs.io/>`__

Contributing
------------

When contributing tests:

1. Follow existing test patterns
2. Ensure all new code has tests
3. Maintain or increase coverage
4. Add markers appropriately
5. Document complex test scenarios
6. Run full test suite before submitting PR

For more information, see contributors/contributing (to be created).
