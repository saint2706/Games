# Documentation

This directory contains the Sphinx documentation for the Card & Paper Games project.

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
