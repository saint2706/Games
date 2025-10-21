# Running GitHub Workflows Locally

This guide explains how to execute the repository's GitHub Actions workflows on your development machine. Local workflow runs are invaluable when debugging CI failures or verifying large changes before opening a pull request.

## Prerequisites

* Docker (required by [`act`](https://github.com/nektos/act))
* The [`act` CLI](https://github.com/nektos/act) installed either manually or via the helper script in this repository
* Project dependencies installed with `pip install -e ".[dev]"`

To install `act` using the provided helper:

```bash
./scripts/setup_act.sh
```

## Using `scripts/run_workflow.sh`

The `scripts/run_workflow.sh` helper wraps `act` with sensible defaults and shortcuts for the workflows defined in `.github/workflows/`.

```bash
# Show documentation and available options
./scripts/run_workflow.sh --help

# List all registered workflows
./scripts/run_workflow.sh all

# Run the lint job from the CI workflow
./scripts/run_workflow.sh ci --job lint

# Execute the manual test workflow with verbose logging
./scripts/run_workflow.sh test --verbose
```

The script accepts additional flags to control the Docker platform, pass secret values, and supply alternate event payloads. Refer to the help output for the complete list of options.

## Direct `act` Usage

If you prefer to call `act` directly, the following examples mirror the script behaviour:

```bash
# Run the full CI workflow
act -W .github/workflows/ci.yml

# Execute the documentation build workflow
act -W .github/workflows/docs-build.yml

# Trigger the manual coverage workflow
act workflow_dispatch -W .github/workflows/manual-coverage.yml
```

> **Note:** Some workflows depend on secrets or services that are only available in the hosted GitHub environment. The helper script will highlight these requirements so you can stub or skip them when running locally.

## Troubleshooting

* Ensure Docker is running and has sufficient resources (CPU/RAM) allocated.
* When `act` reports missing images, run `act --list` to see the required container tags and pull them manually.
* Clear the `.act/` directory to reset cached workflow environments if you encounter inconsistent behaviour.

Keeping this guide up to date helps contributors run the same automation locally that CI executes in GitHub Actions.
