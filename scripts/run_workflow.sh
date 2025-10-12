#!/bin/bash
# Script to run GitHub Actions workflows locally using act
# Provides an easy interface to test and debug workflows

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo -e "${BLUE}GitHub Actions Local Workflow Runner${NC}"
echo "======================================"
echo ""

# Check if act is installed
if ! command -v act &> /dev/null; then
    echo -e "${RED}Error: act is not installed${NC}"
    echo ""
    echo "Install act using:"
    echo "  ./scripts/setup_act.sh"
    echo ""
    echo "Or manually:"
    echo "  macOS: brew install act"
    echo "  Linux: See https://github.com/nektos/act"
    echo "  Windows: choco install act-cli"
    exit 1
fi

# Show help
show_help() {
    cat << EOF
Usage: $0 [workflow] [options]

Run GitHub Actions workflows locally for testing and debugging.

Workflows:
  ci                Run the main CI workflow (lint + test)
  lint              Run format-and-lint workflow
  test              Run manual-tests workflow
  coverage          Run manual-coverage workflow
  mutation          Run mutation-testing workflow
  build             Run build-executables workflow
  codeql            Run CodeQL security analysis
  publish           Run publish-pypi workflow (release event)
  all               List all available workflows

Options:
  -j, --job JOB     Run only specified job (default: all jobs)
  -e, --event FILE  Use custom event payload file
  -s, --secret KEY=VALUE
                    Pass a secret (can be used multiple times)
  -v, --verbose     Verbose output
  -n, --dry-run     Show what would be run without executing
  --list-jobs       List all jobs in the workflow
  -h, --help        Show this help message

Docker Options:
  -P PLATFORM       Run on specific platform (ubuntu-latest, etc.)
  --container-architecture ARCH
                    Container architecture (linux/amd64, linux/arm64)

Examples:
  # Run the CI workflow
  $0 ci

  # Run only the lint job from CI workflow
  $0 ci --job lint

  # Run tests with verbose output
  $0 test --verbose

  # List all workflows
  $0 all

  # Dry run to see what would execute
  $0 ci --dry-run

  # Run with custom event payload
  $0 ci --event .github/workflows/events/push.json

Environment Variables:
  ACT_PLATFORM      Default platform (e.g., ubuntu-latest=node:16-buster)
  DOCKER_HOST       Docker host to use

For more information, see: docs/development/LOCAL_WORKFLOWS.md
EOF
}

# List all workflows
list_workflows() {
    echo -e "${BLUE}Available workflows:${NC}"
    echo ""
    
    for workflow in "$PROJECT_ROOT/.github/workflows"/*.yml; do
        if [ -f "$workflow" ]; then
            filename=$(basename "$workflow")
            name=$(grep -m1 "^name:" "$workflow" | sed 's/name: *//;s/"//g' || echo "Unnamed")
            echo "  ${filename%.yml}"
            echo "    Name: $name"
            echo "    Path: .github/workflows/$filename"
            echo ""
        fi
    done
    
    echo "Run a workflow with: $0 <workflow-name>"
}

# Parse command line arguments
WORKFLOW=""
JOB=""
EVENT_FILE=""
SECRETS=()
VERBOSE=""
DRY_RUN=""
LIST_JOBS=""
PLATFORM=""
ARCH=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -j|--job)
            JOB="$2"
            shift 2
            ;;
        -e|--event)
            EVENT_FILE="$2"
            shift 2
            ;;
        -s|--secret)
            SECRETS+=("$2")
            shift 2
            ;;
        -v|--verbose)
            VERBOSE="--verbose"
            shift
            ;;
        -n|--dry-run)
            DRY_RUN="--dryrun"
            shift
            ;;
        --list-jobs)
            LIST_JOBS="--list"
            shift
            ;;
        -P)
            PLATFORM="$2"
            shift 2
            ;;
        --container-architecture)
            ARCH="$2"
            shift 2
            ;;
        all)
            list_workflows
            exit 0
            ;;
        *)
            if [ -z "$WORKFLOW" ]; then
                WORKFLOW="$1"
            else
                echo -e "${RED}Error: Unknown argument: $1${NC}"
                echo ""
                show_help
                exit 1
            fi
            shift
            ;;
    esac
done

# Check if workflow is specified
if [ -z "$WORKFLOW" ]; then
    echo -e "${YELLOW}No workflow specified${NC}"
    echo ""
    show_help
    exit 1
fi

# Map workflow names to files
case "$WORKFLOW" in
    ci)
        WORKFLOW_FILE="ci.yml"
        ;;
    lint)
        WORKFLOW_FILE="format-and-lint.yml"
        ;;
    test|tests)
        WORKFLOW_FILE="manual-tests.yml"
        ;;
    coverage)
        WORKFLOW_FILE="manual-coverage.yml"
        ;;
    mutation)
        WORKFLOW_FILE="mutation-testing.yml"
        ;;
    build|build-executables)
        WORKFLOW_FILE="build-executables.yml"
        ;;
    codeql)
        WORKFLOW_FILE="codeql.yml"
        ;;
    publish|pypi)
        WORKFLOW_FILE="publish-pypi.yml"
        ;;
    *)
        # Check if it's a direct filename
        if [ -f "$PROJECT_ROOT/.github/workflows/$WORKFLOW" ]; then
            WORKFLOW_FILE="$WORKFLOW"
        elif [ -f "$PROJECT_ROOT/.github/workflows/${WORKFLOW}.yml" ]; then
            WORKFLOW_FILE="${WORKFLOW}.yml"
        else
            echo -e "${RED}Error: Unknown workflow: $WORKFLOW${NC}"
            echo ""
            echo "Available workflows:"
            list_workflows
            exit 1
        fi
        ;;
esac

WORKFLOW_PATH="$PROJECT_ROOT/.github/workflows/$WORKFLOW_FILE"

if [ ! -f "$WORKFLOW_PATH" ]; then
    echo -e "${RED}Error: Workflow file not found: $WORKFLOW_PATH${NC}"
    exit 1
fi

# Change to project root
cd "$PROJECT_ROOT"

# Build act command
ACT_CMD="act"

# Add event type (default to push for most workflows)
if [ -z "$EVENT_FILE" ]; then
    # Determine event type from workflow
    # Check release first as it's typically the primary production trigger
    # Use more specific pattern to match event triggers in the 'on:' section
    if grep -E "^  release:" "$WORKFLOW_PATH" > /dev/null 2>&1; then
        ACT_CMD="$ACT_CMD release"
    elif grep -E "^  schedule:" "$WORKFLOW_PATH" > /dev/null 2>&1; then
        ACT_CMD="$ACT_CMD schedule"
    elif grep -E "^  pull_request:" "$WORKFLOW_PATH" > /dev/null 2>&1; then
        ACT_CMD="$ACT_CMD pull_request"
    elif grep -E "^  workflow_dispatch:" "$WORKFLOW_PATH" > /dev/null 2>&1; then
        ACT_CMD="$ACT_CMD workflow_dispatch"
    else
        ACT_CMD="$ACT_CMD push"
    fi
else
    ACT_CMD="$ACT_CMD --eventpath $EVENT_FILE"
fi

# Add workflow file
ACT_CMD="$ACT_CMD --workflows $WORKFLOW_PATH"

# Add job if specified
if [ -n "$JOB" ]; then
    ACT_CMD="$ACT_CMD --job $JOB"
fi

# Add secrets
for secret in "${SECRETS[@]}"; do
    ACT_CMD="$ACT_CMD --secret $secret"
done

# Add verbose flag
if [ -n "$VERBOSE" ]; then
    ACT_CMD="$ACT_CMD $VERBOSE"
fi

# Add dry-run flag
if [ -n "$DRY_RUN" ]; then
    ACT_CMD="$ACT_CMD $DRY_RUN"
fi

# Add list flag
if [ -n "$LIST_JOBS" ]; then
    ACT_CMD="$ACT_CMD $LIST_JOBS"
fi

# Add platform
if [ -n "$PLATFORM" ]; then
    ACT_CMD="$ACT_CMD -P $PLATFORM"
fi

# Add architecture
if [ -n "$ARCH" ]; then
    ACT_CMD="$ACT_CMD --container-architecture $ARCH"
fi

# Show what we're running
echo -e "${BLUE}Running workflow:${NC} $WORKFLOW_FILE"
if [ -n "$JOB" ]; then
    echo -e "${BLUE}Job:${NC} $JOB"
fi
echo ""

# Run act
echo -e "${GREEN}Executing:${NC} $ACT_CMD"
echo ""

eval "$ACT_CMD"

echo ""
echo -e "${GREEN}✓ Workflow execution complete${NC}"
