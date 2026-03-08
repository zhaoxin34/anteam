.PHONY: dev lint format type-check test ci install clean

# Install dependencies
install:
	pip install -r requirements.txt
	pip install -e .

# Development server
dev:
	uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Code linting
lint:
	ruff check src/ tests/

# Code formatting
format:
	black src/ tests/
	isort src/ tests/

# Type checking
type-check:
	mypy src/

# Run tests
test:
	pytest tests/ -v --cov=src --cov-report=term-missing

# Run tests without coverage
test-no-cov:
	pytest tests/ -v

# CI - run all checks
ci: lint format type-check test

# Clean up
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	rm -rf .coverage htmlcov/

# Setup pre-commit hooks
pre-commit-install:
	pre-commit install
