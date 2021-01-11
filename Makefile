#
## EPITECH PROJECT, 2020
## Astropi
## File description:
## Makefile
##

NAME	=	astropi

all: ## Build
	cp src/astropi.py $(NAME)
	chmod +x $(NAME)

install: ## Install dependencies
	pip3 install -r requirements.txt

clean: ## Clean the workspace
	rm -rf $(NAME)
	find . -type f -name '*.pyc' -delete

help: ## Display help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: all clean
