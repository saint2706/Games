# Documentation

This directory contains the Sphinx documentation for the Card & Paper Games project.

## Quick Start

Welcome to the Games documentation! This guide will help you navigate the comprehensive documentation.

### 📚 What's Available

#### For Players and Users

1. **[Tutorial Series](source/tutorials/index.rst)** - Learn how to play each game
   - 🎮 [Poker Tutorial](source/tutorials/poker_tutorial.rst) - Texas Hold'em and Omaha
   - 🃏 [Bluff Tutorial](source/tutorials/bluff_tutorial.rst) - Master the art of deception
   - 🎰 [Blackjack Tutorial](source/tutorials/blackjack_tutorial.rst) - Beat the dealer
   - 🎴 [Uno Tutorial](source/tutorials/uno_tutorial.rst) - Classic card game
   - ✏️ [Paper Games Tutorial](source/tutorials/paper_games_tutorial.rst) - Tic-Tac-Toe, Battleship, and more

#### For Developers

2. **[Architecture Documentation](source/architecture/index.rst)** - Understand how games are built
   - 🏗️ [Architecture Overview](source/architecture/index.rst) - Design patterns and principles
   - ♠️ [Poker Architecture](source/architecture/poker_architecture.rst) - Deep dive with diagrams
   - 🎭 [Bluff Architecture](source/architecture/bluff_architecture.rst) - Game mechanics and AI
   - 🤖 [AI Strategies](source/architecture/ai_strategies.rst) - Algorithms explained (Minimax, Monte Carlo, etc.)

3. **[Code Examples](source/examples/index.rst)** - Learn by doing
   - 30+ practical code examples
   - Common patterns and best practices
   - Custom game creation
   - AI integration

4. **[API Reference](source/api/)** - Complete module documentation
   - [Card Games API](source/api/card_games.rst)
   - [Paper Games API](source/api/paper_games.rst)

#### For Contributors

5. **[Contributing Guidelines](../CONTRIBUTING.md)** - Join the project
   - Code style guide
   - How to add new games
   - Testing requirements
   - Pull request process

## Building the Documentation

### Prerequisites

Install Sphinx and the required theme:

```bash
pip install sphinx sphinx_rtd_theme
```

### Building HTML Documentation

```bash
cd docs
make html
```

The generated HTML documentation will be in `build/html/`. Open `build/html/index.html` in a web browser.

### Building Other Formats

```bash
# PDF (requires LaTeX)
make latexpdf

# ePub
make epub

# Plain text
make text
```

### Cleaning Build Files

```bash
make clean
```

## Documentation Structure

```
docs/
├── source/
│   ├── index.rst              # Main documentation index
│   ├── conf.py                # Sphinx configuration
│   ├── tutorials/             # Getting started guides
│   │   ├── poker_tutorial.rst
│   │   ├── bluff_tutorial.rst
│   │   ├── blackjack_tutorial.rst
│   │   ├── uno_tutorial.rst
│   │   └── paper_games_tutorial.rst
│   ├── architecture/          # Design and architecture docs
│   │   ├── index.rst
│   │   ├── poker_architecture.rst
│   │   ├── bluff_architecture.rst
│   │   └── ai_strategies.rst
│   ├── examples/              # Code examples
│   │   └── index.rst
│   ├── api/                   # API reference (auto-generated)
│   │   ├── card_games.rst
│   │   └── paper_games.rst
│   └── contributing.rst       # Contribution guidelines
├── Makefile                   # Build automation (Unix)
├── make.bat                   # Build automation (Windows)
└── README.md                  # This file
```

## Writing Documentation

### reStructuredText (RST) Basics

Documentation uses reStructuredText format:

```rst
Section Title
=============

Subsection
----------

**Bold text** and *italic text*

Code blocks:

.. code-block:: python

   def example():
       return "Hello"

Links:

`Link text <https://example.com>`_

Lists:

* Item 1
* Item 2
* Item 3
```

### Adding New Pages

1. Create a new `.rst` file in the appropriate directory
2. Add it to the `toctree` in the parent `index.rst`
3. Rebuild the documentation

### API Documentation

API documentation is automatically generated from docstrings using Sphinx autodoc.

To document a new module:

```rst
Module Name
===========

.. automodule:: package.module
   :members:
   :undoc-members:
   :show-inheritance:
```

## Contributing to Documentation

When contributing documentation:

1. Follow the existing style and structure
2. Use clear, concise language
3. Include code examples where appropriate
4. Test that the documentation builds without errors
5. Check for broken links and formatting issues

## Viewing Documentation Online

Once published, documentation will be available at:

* GitHub Pages: (to be configured)
* Read the Docs: (to be configured)

## Getting Help

For questions about documentation:

* Open an issue on GitHub
* Check Sphinx documentation: https://www.sphinx-doc.org/
* Review existing documentation files for examples
