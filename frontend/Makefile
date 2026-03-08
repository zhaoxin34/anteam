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

# Run tests
test:
	npm run test

# CI - run all checks
ci: lint format type-check test

# Clean up
clean:
	rm -rf dist/
	rm -rf node_modules/
