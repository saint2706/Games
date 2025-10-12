# Scripts Directory

This directory contains utility scripts for development, testing, building, and workflow management.

## Overview

| Script | Purpose | Usage |
| ----------------------- | -------------------------------------------- | -------------------------- |
| `setup_act.sh` | Install act for local workflow testing | `./setup_act.sh` |
| `run_workflow.sh` | Run GitHub Actions workflows locally | `./run_workflow.sh ci` |
| `run_tests.sh` | Run test suite with various options | `./run_tests.sh all` |
| `check_complexity.sh` | Check code complexity with Radon | `./check_complexity.sh` |
| `build_executable.sh` | Build standalone executables | `./build_executable.sh` |
| `launcher.py` | Launch games from command line | `python launcher.py` |
| `test_mcp_servers.py` | Test MCP server configurations | `python test_mcp_servers.py` |
| `validate_mcp_config.py` | Validate MCP configuration files | `python validate_mcp_config.py` |

## Workflow Testing Scripts

### setup_act.sh

Installs `act`, a tool for running GitHub Actions workflows locally.

**Usage:**

```bash
./scripts/setup_act.sh
```

**Features:**

- Auto-detects OS (Linux/macOS/Windows)
- Downloads latest version from GitHub
- Installs to user directory (no sudo needed on Linux)
- Provides installation instructions for Windows

**Supported Platforms:**

- Linux (x86_64, arm64)
- macOS (via Homebrew)
- Windows (instructions for Chocolatey/Scoop/winget)

### run_workflow.sh

Run GitHub Actions workflows locally with act for testing and debugging.

**Basic Usage:**

```bash
# Run a workflow
./scripts/run_workflow.sh ci

# List all workflows
./scripts/run_workflow.sh all

# Show help
./scripts/run_workflow.sh --help
```

**Common Workflows:**

```bash
./scripts/run_workflow.sh ci          # CI workflow (lint + test)
./scripts/run_workflow.sh lint        # Linting and formatting
./scripts/run_workflow.sh test        # Test suite
./scripts/run_workflow.sh coverage    # Coverage report
./scripts/run_workflow.sh build       # Build executables
./scripts/run_workflow.sh mutation    # Mutation testing
```

**Advanced Options:**

```bash
# Run specific job
./scripts/run_workflow.sh ci --job lint

# Dry run (see what would execute)
./scripts/run_workflow.sh ci --dry-run

# List jobs in workflow
./scripts/run_workflow.sh ci --list-jobs

# Verbose output
./scripts/run_workflow.sh ci --verbose

# Custom event payload
./scripts/run_workflow.sh ci --event .github/workflows/events/push.json
```

**Documentation:**

- Full guide: [docs/development/LOCAL_WORKFLOWS.md](../docs/development/LOCAL_WORKFLOWS.md)
- Quick start: [docs/development/WORKFLOW_TESTING_QUICKSTART.md](../docs/development/WORKFLOW_TESTING_QUICKSTART.md)

## Testing Scripts

### run_tests.sh

Run the test suite with various configurations.

**Usage:**

```bash
./scripts/run_tests.sh [test_type] [coverage]
```

**Test Types:**

```bash
./scripts/run_tests.sh all          # Run all tests (default)
./scripts/run_tests.sh unit         # Unit tests only
./scripts/run_tests.sh integration  # Integration tests only
./scripts/run_tests.sh gui          # GUI tests only
./scripts/run_tests.sh performance  # Performance tests only
./scripts/run_tests.sh fast         # Fast tests (skip slow ones)
./scripts/run_tests.sh coverage     # Generate coverage report
./scripts/run_tests.sh mutation     # Mutation testing
./scripts/run_tests.sh help         # Show help
```

**Examples:**

```bash
# Run all tests with coverage
./scripts/run_tests.sh all coverage

# Run fast tests only
./scripts/run_tests.sh fast

# Run unit tests
./scripts/run_tests.sh unit
```

**Coverage Report:**

When running with coverage, an HTML report is generated in `htmlcov/index.html`.

### check_complexity.sh

Check code complexity using Radon to ensure functions stay below complexity threshold.

**Usage:**

```bash
./scripts/check_complexity.sh
```

**What It Checks:**

- Cyclomatic complexity (target: ≤10 per function)
- Complexity grades (target: A or B)
- Flags functions that exceed thresholds

**Output:**

```
Checking complexity for: card_games/
✓ All functions have complexity ≤10
✓ All files have grade A or B
```

**Note:** C90 complexity checking in Ruff is temporarily disabled. Use this script to verify complexity manually.

## Build Scripts

### build_executable.sh

Build standalone executables using PyInstaller or Nuitka.

**Usage:**

```bash
./scripts/build_executable.sh [tool]
```

**Tools:**

- `pyinstaller` - Fast, widely compatible (default)
- `nuitka` - Smaller, faster executables

**Examples:**

```bash
# Build with PyInstaller (default)
./scripts/build_executable.sh

# Build with Nuitka
./scripts/build_executable.sh nuitka
```

**Output:**

Executables are created in the `dist/` directory.

**Documentation:**

- [build_configs/README.md](../build_configs/README.md)
- [docs/deployment/DEPLOYMENT.md](../docs/deployment/DEPLOYMENT.md)

## Launcher Script

### launcher.py

Interactive launcher for all games in the collection.

**Usage:**

```bash
python scripts/launcher.py

# Or as a module
python -m scripts.launcher
```

**Features:**

- Lists all available games
- Launches games by number or name
- Shows game descriptions
- Interactive menu

**Example:**

```
Games Collection Launcher
=========================

Available Games:

Card Games:
  1. Poker (Texas Hold'em)
  2. Blackjack
  3. Uno
  ...

Paper Games:
  15. Tic-Tac-Toe
  16. Battleship
  ...

Enter game number or name (q to quit):
```

## MCP Testing Scripts

### test_mcp_servers.py

Test MCP (Model Context Protocol) server configurations.

**Usage:**

```bash
python scripts/test_mcp_servers.py
```

### validate_mcp_config.py

Validate MCP configuration files for correctness.

**Usage:**

```bash
python scripts/validate_mcp_config.py
```

## Using Scripts with Make

Most scripts can also be run via Makefile targets:

```bash
# Workflow testing
make setup-act          # Install act
make workflow-ci        # Run CI workflow
make workflow-list      # List all workflows

# Testing
make test               # Run all tests
make test-fast          # Fast tests only
make test-coverage      # Tests with coverage
make complexity         # Check complexity

# Development
make lint               # Run linters
make format             # Format code
```

See `make help` for all available targets.

## Script Dependencies

### Python Scripts

Require Python 3.9+ and dependencies from `requirements.txt` and `requirements-dev.txt`:

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Bash Scripts

Require:

- Bash 4.0+
- Common Unix utilities (grep, sed, awk, etc.)
- Docker (for workflow testing scripts)

### Workflow Scripts

Additional requirements:

- **act**: Install with `./scripts/setup_act.sh`
- **Docker**: Required for running workflows locally

## Contributing

When adding new scripts:

1. Make scripts executable: `chmod +x script.sh`
1. Add a help message (`--help` flag)
1. Include error handling and validation
1. Document in this README
1. Add corresponding Makefile targets if appropriate

## Troubleshooting

### Permission Denied

Make scripts executable:

```bash
chmod +x scripts/*.sh
```

### Script Not Found

Ensure you're in the project root:

```bash
cd /path/to/Games
./scripts/script.sh
```

### Docker Issues (Workflow Scripts)

Ensure Docker is running:

```bash
docker ps
```

If not running:

```bash
# Linux
sudo systemctl start docker

# macOS/Windows
# Open Docker Desktop
```

## Related Documentation

- [Development Guide](../docs/development/)
- [Testing Guide](../docs/development/TESTING.md)
- [Workflow Testing Guide](../docs/development/LOCAL_WORKFLOWS.md)
- [Deployment Guide](../docs/deployment/DEPLOYMENT.md)
- [Contributing Guide](../CONTRIBUTING.md)

## Getting Help

- Check the help message: `./scripts/script.sh --help`
- Read the relevant documentation (links above)
- Check the project README: [../README.md](../README.md)
- Open an issue: https://github.com/saint2706/Games/issues
