# Anteam - Slack-style chat system
# Root Makefile for coordinating frontend and backend

.PHONY: help install install-dev dev-backend dev-frontend test lint format ci clean

help: ## Show this help message
	@echo ""
	@echo "Anteam - Slack-style chat system"
	@echo ""
	@echo "Usage: make <target>"
	@echo ""
	@echo "Installation:"
	@echo "  install        Install all dependencies"
	@echo "  install-dev   Install with dev dependencies"
	@echo ""
	@echo "Development:"
	@echo "  dev-backend   Start backend dev server"
	@echo "  dev-frontend Start frontend dev server"
	@echo ""
	@echo "Code Quality:"
	@echo "  lint          Run linting"
	@echo "  format        Run code formatter"
	@echo "  typecheck     Run type checking"
	@echo ""
	@echo "Testing:"
	@echo "  test          Run all tests"
	@echo ""
	@echo "CI:"
	@echo "  ci            Run all CI checks"
	@echo ""

install: ## Install all dependencies
	@echo "Installing backend dependencies..."
	@$(MAKE) -C backend install
	@echo "Installing frontend dependencies..."
	@$(MAKE) -C frontend install || true

install-dev: ## Install with dev dependencies
	@echo "Installing backend dev dependencies..."
	@$(MAKE) -C backend install-dev
	@echo "Installing frontend dev dependencies..."
	@$(MAKE) -C frontend install || true

dev-backend: ## Start backend dev server
	@$(MAKE) -C backend dev

dev-frontend: ## Start frontend dev server
	@$(MAKE) -C frontend dev

test: ## Run all tests
	@$(MAKE) -C backend test
	@$(MAKE) -C frontend test || true

lint: ## Run linting
	@$(MAKE) -C backend lint
	@$(MAKE) -C frontend lint || true

format: ## Run code formatter
	@$(MAKE) -C backend format
	@$(MAKE) -C frontend format || true

typecheck: ## Run type checking
	@$(MAKE) -C backend type-check
	@$(MAKE) -C frontend type-check || true

ci: ## Run all CI checks
	@$(MAKE) -C backend ci
	@$(MAKE) -C frontend ci || true

clean: ## Clean all cache files
	@$(MAKE) -C backend clean
	@$(MAKE) -C frontend clean || true
