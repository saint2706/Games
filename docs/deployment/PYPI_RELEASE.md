# PyPI Release Process

This document describes how to release the games-collection package to PyPI.

## Prerequisites

1. **PyPI Account**: Create an account at https://pypi.org
2. **GitHub Repository Secrets**: Configure trusted publishing in PyPI project settings

## Automated Release Process

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Commit and push changes
4. Create GitHub Release with tag (e.g., `v1.0.1`)
5. GitHub Actions automatically publishes to PyPI

## Manual Testing

Use TestPyPI before releasing to production PyPI.

## Post-Release

- Verify on PyPI
- Test installation
- Update documentation

For complete instructions, see the full documentation in the repository.
