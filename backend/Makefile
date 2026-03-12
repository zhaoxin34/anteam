.PHONY: help install install-dev dev lint format type-check test test-no-cov ci clean

# Colors
YELLOW := $(shell tput setaf 3)
BLUE := $(shell tput setaf 4)
GREEN := $(shell tput setaf 2)
NC := $(shell tput sgr0)

help: ## Show this help message
	@echo ""
	@echo "$(BLUE)Backend - Python/FastAPI$(NC)"
	@echo ""
	@echo "$(GREEN)Usage:$(NC)"
	@echo "  make $(YELLOW)<target>$(NC)"
	@echo ""
	@echo "$(GREEN)Installation:$(NC)"
	@echo "  install         Install dependencies"
	@echo "  install-dev    Install with dev dependencies"
	@echo ""
	@echo "$(GREEN)Development:$(NC)"
	@echo "  dev            Start dev server (hot reload)"
	@echo ""
	@echo "$(GREEN)Code Quality:$(NC)"
	@echo "  lint           Run ruff check"
	@echo "  format         Run black + isort"
	@echo "  type-check     Run mypy type check"
	@echo ""
	@echo "$(GREEN)Testing:$(NC)"
	@echo "  test           Run pytest with coverage"
	@echo "  test-no-cov    Run pytest without coverage"
	@echo ""
	@echo "$(GREEN)CI:$(NC)"
	@echo "  ci             Run all CI checks"
	@echo ""
	@echo "$(GREEN)Maintenance:$(NC)"
	@echo "  clean          Clean cache files"
	@echo ""

install: ## Install dependencies
	uv sync

install-dev: ## Install with dev dependencies
	uv sync --all-extras

dev: ## Start dev server (hot reload)
	uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

lint: ## Run ruff check
	uv run ruff check src/ tests/

format: ## Run black + isort
	uv run black src/ tests/
	uv run isort src/ tests/

type-check: ## Run mypy type check
	uv run mypy src/

test: ## Run pytest with coverage
	uv run pytest tests/ -v --cov=src --cov-report=term-missing

test-no-cov: ## Run pytest without coverage
	uv run pytest tests/ -v

ci: ## Run all CI checks
	$(MAKE) lint
	$(MAKE) format
	$(MAKE) type-check
	$(MAKE) test

clean: ## Clean cache files
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .coverage htmlcov/ 2>/dev/null || true
