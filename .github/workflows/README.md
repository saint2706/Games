# GitHub Workflows

This directory contains automated workflows for continuous integration, testing, and code quality checks.

## Workflows

### CI Workflows (Run on Push/PR)

#### `ci.yml` - Continuous Integration

Combined workflow that runs all quality checks:

- Linting (Black, Ruff, mdformat)
- Testing on Python 3.11 and 3.12

This is the primary workflow that should pass before merging pull requests.

#### `codeql.yml` - Security Analysis

Analyzes code for security vulnerabilities and coding errors. Runs:

- On push/PR to master/main branches
- Weekly on Mondays (scheduled)

### Manual Workflows

#### `manual-tests.yml` - Run Tests On Demand

Allows maintainers to manually trigger pytest runs with custom Python version matrices, marker expressions, and
additional CLI arguments supplied as a JSON array. Useful for reproducing CI runs or verifying fixes before opening a
pull request.

#### `manual-coverage.yml` - Generate Coverage Reports

Produces HTML and XML coverage reports on demand with optional Codecov uploads and control over whether to include tests
marked as `slow`.

#### `format-and-lint.yml` - Auto-fix Formatting

Manual workflow (workflow_dispatch) that automatically formats code and commits changes. Use this for local development
to fix formatting issues in bulk.

#### `mutation-testing.yml` - Mutation Testing Sweep

Manual or scheduled workflow that runs `mutmut` over a subset of games to evaluate test robustness.

## Dependabot

The `.github/dependabot.yml` configuration enables automated dependency updates:

- Python packages (pip) - weekly
- GitHub Actions - weekly

## Local Development

To run checks locally before pushing:

```bash
# Install tools
pip install black mdformat ruff pytest

# Run linting checks
black --check .
mdformat --check .
ruff check .

# Run tests
pytest tests/ -v
```

## CI Status

All workflows must pass before merging pull requests. The `ci.yml` workflow combines both linting and testing to ensure
code quality.
