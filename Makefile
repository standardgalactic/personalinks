.PHONY: help install install-dev test test-cov test-fast lint format type-check clean all experiments experiments-verify lab-export lab-inspect lab-validate lab-replay

help:  ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## Install package in development mode
	python3 -m pip install -e .

install-dev:  ## Install package with development dependencies
	python3 -m pip install -e ".[dev]"

test:  ## Run all tests
	python3 -m pytest

test-cov:  ## Run tests with coverage report
	python3 -m pytest --cov=spherepop --cov-report=html --cov-report=term-missing

test-fast:  ## Run tests excluding slow tests
	python3 -m pytest -m "not slow"

lint:  ## Run linting checks with ruff
	python3 -m ruff check spherepop/ tests/

format:  ## Format code with ruff
	python3 -m ruff format spherepop/ tests/

format-check:  ## Check code formatting without modifying files
	python3 -m ruff format --check spherepop/ tests/

type-check:  ## Run type checking with mypy
	python3 -m mypy \
		spherepop/model.py \
		spherepop/semantics.py \
		spherepop/observers.py \
		spherepop/views.py \
		spherepop/grammar.py \
		spherepop/predicates.py \
		spherepop/path_utils.py \
		spherepop/serialization.py \
		spherepop/lab.py

clean:  ## Remove build artifacts and caches
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.pyo' -delete
	find . -type f -name '*~' -delete

all: lint type-check test  ## Run all checks (lint, type-check, test)

experiments:  ## Run all experiments (01-29)
	python3 -m spherepop.lab run 01..29

experiments-verify: ## Run lab verification against manifest invariants
	python3 -m spherepop.lab verify

LAB_ARTIFACT ?= build/lab-result.json
LAB_EXPERIMENT ?= 07

lab-export: ## Export one experiment run as portable artifact JSON
	python3 -m spherepop.lab export $(LAB_EXPERIMENT) --output $(LAB_ARTIFACT)

lab-inspect: ## Inspect a Config/artifact JSON file
	python3 -m spherepop.lab inspect $(LAB_ARTIFACT)

lab-validate: ## Validate structure + semantics for a Config/artifact JSON file
	python3 -m spherepop.lab validate $(LAB_ARTIFACT)

lab-replay: ## Replay a Config/artifact JSON file
	python3 -m spherepop.lab replay $(LAB_ARTIFACT)

# Quick dev workflow targets
dev-check: format lint type-check test-fast  ## Quick development check (format, lint, type-check, fast tests)

ci: lint type-check test-cov  ## Run CI checks (lint, type-check, coverage)

# Coverage targets
coverage-html:  ## Generate HTML coverage report
	python3 -m pytest --cov=spherepop --cov-report=html
	@echo "\nCoverage report generated in htmlcov/index.html"

coverage-report:  ## Show coverage report in terminal
	python3 -m pytest --cov=spherepop --cov-report=term-missing
