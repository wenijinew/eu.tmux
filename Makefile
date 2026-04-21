.PHONY: install test theme hooks clean

install: ## Install dependencies
	poetry install --no-root

test: ## Run tests
	python3 -m pytest tests/ -v

theme: ## Generate dynamic theme
	./scripts/eutmux.tmux -d

hooks: ## Install tmux hooks
	./scripts/eutmux.tmux -R

lint: ## Check bash and Python syntax
	bash -n scripts/*.sh scripts/*.tmux
	python3 -c "import ast, pathlib; [ast.parse(f.read_text()) for f in pathlib.Path('src').glob('*.py')]"

clean: ## Remove generated files
	rm -f .requirements.installed.txt
	rm -rf __pycache__ src/__pycache__ .pytest_cache

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
