# Makefile
.ONESHELL:

.PHONY: test lint format install docker-test docker-up docker-server typecheck add-mod remove-mod list-mods check

# Docker compose command prefix
DOCKER_COMPOSE_RUN := docker-compose run --rm devtools

# Run tests in Docker
test:
	docker-compose up --exit-code-from tests tests

# Build Docker images
build:
	docker-compose build

# Run linter (flake8) in Docker
lint:
	$(DOCKER_COMPOSE_RUN) python -m flake8 .

# Run formatter (black) in Docker
format:
	$(DOCKER_COMPOSE_RUN) python -m black .

# Run static type checker (mypy) in Docker
typecheck:
	$(DOCKER_COMPOSE_RUN) python -m mypy .

# Run tests and start server if tests pass
run:
	docker-compose up --exit-code-from tests dst-server

# Clean up Docker resources
clean:
	docker-compose down --rmi all --volumes --remove-orphans

# Run all checks (linting, type checking, and tests)
check: lint typecheck test

# Add a mod to the dedicated_server_mods_setup.lua file
add-mod:
	@if [ -z "$(filter-out $@,$(MAKECMDGOALS))" ]; then \
		echo "Usage: make add-mod <mod_id>"; \
		exit 1; \
	fi
	@echo "Adding mod(s)..."
	$(DOCKER_COMPOSE_RUN) python common/mod_manager.py add $(filter-out $@,$(MAKECMDGOALS))

# Remove a mod from the dedicated_server_mods_setup.lua file
remove-mod:
	@if [ -z "$(filter-out $@,$(MAKECMDGOALS))" ]; then \
		echo "Usage: make remove-mod <mod_id>"; \
		exit 1; \
	fi
	@echo "Removing mod(s)..."
	$(DOCKER_COMPOSE_RUN) python common/mod_manager.py remove $(filter-out $@,$(MAKECMDGOALS))

# List all mods in the dedicated_server_mods_setup.lua file
list-mods:
	@echo "Listing mods..."
	$(DOCKER_COMPOSE_RUN) python common/mod_manager.py list

# Catch-all target to allow for additional arguments
%:
	@:
