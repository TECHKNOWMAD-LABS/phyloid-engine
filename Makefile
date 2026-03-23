.PHONY: test lint format security clean test-js test-all

test:
	PYTHONPATH=python python3 -m pytest tests/ -v --tb=short

test-cov:
	PYTHONPATH=python python3 -m pytest tests/ --cov=python/phyloid_engine --cov-report=term-missing

test-js:
	node --test test/*.test.js

test-all: test test-js

lint:
	ruff check python/ tests/

format:
	ruff format python/ tests/

security:
	@echo "=== Secret scan ==="
	@grep -rn "password\|secret\|api_key\|token\|API_KEY\|SECRET" python/ src/ || echo "No secrets found"
	@echo "=== Injection scan ==="
	@grep -rn "os\.system\|subprocess\|eval(\|exec(" python/ src/ || echo "No injection vectors found"

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf dist/ build/ .coverage htmlcov/
