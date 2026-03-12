.PHONY: dev build lint format type-check test ci install clean

# Install dependencies
install:
	npm install

# Development server
dev:
	npm run dev

# Build for production
build:
	npm run build

# Code linting
lint:
	npm run lint

# Code formatting
format:
	npm run format

# Type checking
type-check:
	npm run type-check

# Run tests (skip if no test files exist)
test:
	@if ls src/**/*.test.{ts,tsx} 1> /dev/null 2>&1; then \
		npm run test -- --run; \
	else \
		echo "No test files found, skipping tests"; \
	fi

# CI - run all checks
ci: lint format type-check test

# Clean up
clean:
	rm -rf dist/
	rm -rf node_modules/
