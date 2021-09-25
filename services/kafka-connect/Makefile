# HELP
.PHONY: help

image_name = kafka-connect

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## Builds a docker image
	docker build -t $(image_name) .

shell:
	docker run -it --rm --entrypoint bash $(image_name)

run:
	docker run -it $(image_name)