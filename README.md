# Games Collection

The Games Collection brings together more than forty classic games implemented
in Python. Card tables, pen-and-paper puzzles, dice showdowns, word challenges,
and logic brainteasers all live in a single repository with shared engines,
artificial intelligence opponents, and optional graphical interfaces.

The project targets players who want quick access to familiar favourites and
contributors who enjoy extending game mechanics or experimenting with strategy
algorithms.

## Highlights

- **Broad catalogue** – 49 playable games spanning card, paper, dice, logic, and
  word genres. See the [Games Catalogue](docs/source/players/games_catalog.rst) for the
  full list.
- **Multiple interfaces** – Launch titles from the command line, via the
  `games-collection` menu, or with Tkinter/PyQt graphical front ends where
  available.
- **Reusable infrastructure** – Shared modules under ``games_collection.core``
  provide AI strategies, save/load support, event dispatch, replay recording,
  accessibility helpers, and more.
- **Educational tooling** – Several games ship with hint systems, tutorials, and
  probability calculators that make the collection a useful teaching aid.

## Installation

### From PyPI

Install the published package to get the latest stable release:

```bash
pip install games-collection
```

Optional extras install the GUI stack and developer tooling:

```bash
pip install games-collection[gui]
pip install games-collection[dev]
```

### From Source

Working on the codebase or trying unreleased features? Clone the repository and
perform an editable install:

```bash
git clone https://github.com/saint2706/Games.git
cd Games
pip install -e .[dev]
```

## Running games

After installation you have several options:

- **Interactive menu** – Run `games-collection` to browse all installed titles.

- **Console scripts** – Call commands such as `games-blackjack`,
  `games-tic-tac-toe`, or `games-farkle` directly.

- **Module execution** – Use Python’s module runner when you want additional
  flags or to inspect help text:

  ```bash
  python -m games_collection.games.card.blackjack --help
  python -m games_collection.games.paper.connect_four --gui
  python -m games_collection.games.dice.craps
  ```

  Legacy import paths such as ``card_games.blackjack`` remain available through
  compatibility shims to ease migration for external integrations.

Many games accept a `--gui` flag to launch graphical interfaces. PyQt5 is the primary GUI framework, with Tkinter available as a fallback. You can select a specific framework with `--gui-framework pyqt5` or `--gui-framework tkinter`.

## Repository layout

```text
src/
├── games_collection/
│   ├── catalog/             Metadata registry powering docs and launchers
│   ├── core/                Shared engines, AI strategies, GUIs, persistence
│   └── games/
│       ├── card/            Card-based titles (Blackjack, Poker, Uno, Hearts)
│       ├── paper/           Board and pencil games (Chess, Sudoku, Yahtzee)
│       ├── dice/            Dice-driven experiences (Craps, Farkle)
│       ├── logic/           Puzzle boxes (Sokoban, Minesweeper)
│       └── word/            Vocabulary challenges (Crossword, Trivia)
card_games/                  Compatibility shim for legacy imports
paper_games/                 Compatibility shim for legacy imports
dice_games/                  Compatibility shim for legacy imports
logic_games/                 Compatibility shim for legacy imports
word_games/                  Compatibility shim for legacy imports
common/                      Compatibility shim for legacy imports
plugins/                     Playable game plugins
scripts/                     Launchers registered as console entry points
docs/                        Sphinx documentation
examples/                    Sample integrations and automation snippets
tests/                       Automated test suite mirroring the package structure
```

## Development workflow

1. Install dependencies with `pip install -e .[dev]`.
2. Set up pre-commit hooks with `pre-commit install`.
3. Format code with `black .` and `ruff check --fix .` (line length 160).
4. Run static analysis using `mypy .` and, optionally, `radon cc ...`.
5. Execute the full test suite: `pytest` or `pytest --cov`.
6. Update documentation in `docs/` and add entries to `CHANGELOG.md` for notable changes.

## Documentation

This README provides a high-level summary. The canonical guides now live in the Sphinx project, grouped by audience so everybody reads from the same source of truth:

- [Player resources](docs/source/players/index.rst) cover installation, launch options, and the [games catalog](docs/source/players/games_catalog.rst) detail pages.
- [Developer documentation](docs/source/developers/index.rst) contains coding standards, implementation guides, and GUI references.
- [Operations playbooks](docs/source/operations/index.rst) track workflow validation, release status, and archival reports.
- [Contributor policies](docs/source/contributors/index.rst) replace the standalone CONTRIBUTING.md file.

Build the HTML site with:

```bash
cd docs
pip install -r requirements.txt
make html
```

Generated pages will be available in `docs/build/html/index.html`.

## Contributing

Contributions are welcome! Please open an issue or discussion to propose new
ideas, then follow the steps in [Contributor Guide](docs/source/contributors/contributing.rst). Remember to
include tests and documentation updates alongside code changes.

## License

This project is released under the MIT License. See [LICENSE](LICENSE) for full
terms.
