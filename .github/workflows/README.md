# GitHub Workflows

This directory contains automated workflows for continuous integration, testing, and code quality checks.

## Workflows

### CI Workflows (Run on Push/PR)

#### `ci.yml` - Continuous Integration

Combined workflow that runs all quality checks:

- Linting (Black, Ruff, mdformat)
- Testing on Python 3.11 and 3.12

This is the primary workflow that should pass before merging pull requests.

#### `test.yml` - Testing

Runs the pytest test suite on multiple Python versions (3.11, 3.12) to ensure compatibility.

#### `lint.yml` - Code Quality

Checks code formatting and style compliance without making changes:

- Black for Python formatting
- mdformat for Markdown formatting
- Ruff for linting

#### `codeql.yml` - Security Analysis

Analyzes code for security vulnerabilities and coding errors. Runs:

- On push/PR to master/main branches
- Weekly on Mondays (scheduled)

### Manual Workflows

#### `format-and-lint.yml` - Auto-fix Formatting

Manual workflow (workflow_dispatch) that automatically formats code and commits changes.
Use this for local development to fix formatting issues in bulk.

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

All workflows must pass before merging pull requests. The `ci.yml` workflow combines both linting and testing to ensure code quality.
