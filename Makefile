# Makefile for Games Project
# Provides convenient shortcuts for development tasks

.PHONY: help install test lint format clean workflows

# Default target
help:
	@echo "Games Project - Available Make Targets"
	@echo "======================================"
	@echo ""
	@echo "Setup:"
	@echo "  make install        Install package in editable mode"
	@echo "  make install-dev    Install package with development dependencies"
	@echo "  make setup-act      Install act for local workflow testing"
	@echo ""
	@echo "Development:"
	@echo "  make format         Format code with black and isort"
	@echo "  make lint           Run linters (black, ruff, mdformat)"
	@echo "  make typecheck      Run mypy type checking"
	@echo "  make complexity     Check code complexity"
	@echo ""
	@echo "Testing:"
	@echo "  make test           Run all tests"
	@echo "  make test-fast      Run fast tests (skip slow ones)"
	@echo "  make test-coverage  Run tests with coverage report"
	@echo "  make test-unit      Run only unit tests"
	@echo "  make test-integration Run only integration tests"
	@echo ""
	@echo "Workflows (requires act):"
	@echo "  make workflow-ci       Run CI workflow locally"
	@echo "  make workflow-lint     Run lint workflow locally"
	@echo "  make workflow-test     Run test workflow locally"
	@echo "  make workflow-list     List all available workflows"
	@echo "  make workflow-validate Validate all workflow files"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean          Remove build artifacts and cache files"
	@echo "  make clean-docker   Clean up Docker images used by act"
	@echo ""
	@echo "Documentation:"
	@echo "  make docs           Build Sphinx documentation"
	@echo ""

# Installation targets
install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"
	pre-commit install

setup-act:
	./scripts/setup_act.sh

# Development targets
format:
	black .
	isort .
	mdformat .

lint:
	black --check .
	ruff check .
	mdformat --check .

typecheck:
	mypy .

complexity:
	./scripts/check_complexity.sh

# Testing targets
test:
	pytest

test-fast:
	./scripts/run_tests.sh fast

test-coverage:
	./scripts/run_tests.sh coverage

test-unit:
	pytest -m unit

test-integration:
	pytest -m integration

test-gui:
	pytest -m gui

test-performance:
	pytest -m performance

# Workflow targets
workflow-ci:
	./scripts/run_workflow.sh ci

workflow-lint:
	./scripts/run_workflow.sh lint

workflow-test:
	./scripts/run_workflow.sh test

workflow-coverage:
	./scripts/run_workflow.sh coverage

workflow-build:
	./scripts/run_workflow.sh build

workflow-list:
	./scripts/run_workflow.sh all

workflow-validate:
	python3 scripts/validate_workflows.py

# Cleanup targets
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf .mutmut-cache/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

clean-docker:
	docker system prune -f
	docker volume prune -f

# Documentation targets
docs:
	cd docs && make html
	@echo "Documentation built in docs/build/html/index.html"

# Pre-commit target
pre-commit:
	pre-commit run --all-files

# CI simulation (runs locally what CI would run)
ci-local: lint test-fast
	@echo "✓ Local CI checks passed"
