# HELP
.PHONY: help

app_name = data_simulator

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

clean: ## Removes build artifacts and any logs
	rm -rf *.egg-info && rm -rf dist && rm -rf *.log* && rm -rf build
	rm -rf venv && rm -f Pipfile && rm -f Pipfile.lock

env: ## Creates or updates project's virtual enviornment. To activate, run: source venv/bin/activate
	python3 -m venv venv --prompt venv
	venv/bin/pip install -r requirements.txt

update: ## Updates dependencies in virtual environment
	venv/bin/pip install -r requirements.txt

run: venv ## Launches app using virtual environment
	CONFIG_ENV=config.env venv/bin/python -m $(app_name)
