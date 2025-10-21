# Documentation

The `docs/` directory contains the Sphinx project for the Games Collection. All audience-specific guides now live inside Sphinx so that players, developers, operators, and contributors read from a single, versioned source of truth.

## Structure

- `source/` – reStructuredText files that power the site.
  - `overview.rst` – project goals and audience.
  - `players/` – player-facing guides such as `index.rst`, `user_guide.rst`, and the expanded `games_catalog.rst`.
  - `developers/` – engineering references including `developer_guide.rst`, `architecture.rst`, and the converted guides from `docs/development/` and `docs/gui/`.
  - `operations/` – workflow validation reports, status dashboards, and archived investigations.
  - `contributors/` – contribution policies migrated from `CONTRIBUTING.md`.
  - `conf.py` – Sphinx configuration.
- `build/` – Generated output (ignored by Git).
- `images/` – Shared assets used by the docs.
- `requirements.txt` – Dependencies needed to build the documentation.

Historic Markdown guides in `docs/development/`, `docs/gui/`, `docs/status/`, and `docs/workflows/` have been converted into the sections above. Any remaining Markdown files in those folders exist only as repository history and should not be edited going forward.

## Building the site

1. Install the documentation dependencies:

   ```bash
   pip install -r docs/requirements.txt
   ```

2. Build the HTML output:

   ```bash
   cd docs
   make html
   ```

3. Open the generated pages at `docs/build/html/index.html`.

For other formats, run `make latexpdf`, `make epub`, or `make text` from the same directory.

## Writing new content

- Add new pages inside `docs/source/` and reference them from `docs/source/index.rst` (or another toctree) so they appear in navigation.
- Use reStructuredText and follow Sphinx best practices (headings, code blocks, cross references).
- Keep examples in sync with the current command-line interfaces and module names.
- When describing new games or systems, update the Sphinx docs rather than creating new Markdown files.
