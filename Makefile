.PHONY: install test lint format clean docs

install:
	pip install -e ".[dev]"

test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=hybrid_agents --cov-report=html --cov-report=term

lint:
	ruff check hybrid_agents/ examples/ tests/
	mypy hybrid_agents/

format:
	black hybrid_agents/ examples/ tests/
	ruff check --fix hybrid_agents/ examples/ tests/

clean:
	rm -rf build/ dist/ *.egg-info
	rm -rf .pytest_cache/ .mypy_cache/ .ruff_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

docs:
	@echo "Documentation at docs/"

help:
	@echo "Available commands:"
	@echo "  make install    - Install package and dependencies"
	@echo "  make test       - Run tests"
	@echo "  make test-cov   - Run tests with coverage"
	@echo "  make lint       - Run linters"
	@echo "  make format     - Format code"
	@echo "  make clean      - Clean build artifacts"
	@echo "  make docs       - Open documentation"
