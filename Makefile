# ======================================================
# Talatrivia API - Development Commands
# ======================================================

PROJECT_NAME ?= talatrivia
MAIN_SERVICE ?= talatrivia-api-django
COMPOSE := docker compose -p $(PROJECT_NAME)

# ======================================================
# Project Setup
# ======================================================
help: ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*?##' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "} {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

bootstrap: ## Initialize development environment
	$(COMPOSE) build --no-cache
	@command -v pre-commit >/dev/null 2>&1 || pip install pre-commit
	@pre-commit install

# ======================================================
# Docker Operations
# ======================================================
build: ## Build Docker images
	$(COMPOSE) build

build-no-cache: ## Build images without cache
	$(COMPOSE) build --no-cache

up: ## Start all services
	$(COMPOSE) up -d

up-logs: ## Start services with logs
	$(COMPOSE) up

down: ## Stop and remove containers
	$(COMPOSE) down

logs: ## Tail all logs
	$(COMPOSE) logs -f

logs-app: ## Tail application logs
	$(COMPOSE) logs -f $(MAIN_SERVICE)

clean: ## Remove containers, volumes and orphans
	$(COMPOSE) down -v --remove-orphans

# ======================================================
# Development Workflow
# ======================================================
dev-core: ## Start core infrastructure (DB, Redis)
	$(COMPOSE) up -d talatrivia-postgres talatrivia-redis

dev-full: up logs-app ## Start all services and tail logs

shell: ## Open bash in application container
	$(COMPOSE) exec $(MAIN_SERVICE) bash

# ======================================================
# Django Commands
# ======================================================
migrate: ## Apply database migrations
	$(COMPOSE) run --rm $(MAIN_SERVICE) python manage.py migrate

migrations: ## Create new migrations
	$(COMPOSE) run --rm $(MAIN_SERVICE) python manage.py makemigrations

createsuperuser: ## Create admin user
	$(COMPOSE) run --rm $(MAIN_SERVICE) python manage.py createsuperuser

shell-plus: ## Django shell plus (if django-extensions available)
	$(COMPOSE) run --rm $(MAIN_SERVICE) python manage.py shell_plus || \
		$(COMPOSE) run --rm $(MAIN_SERVICE) python manage.py shell

# ======================================================
# Quality Assurance
# ======================================================
test: ## Run test suite
	$(COMPOSE) run --rm $(MAIN_SERVICE) pytest

test-coverage: ## Run tests with coverage report
	$(COMPOSE) run --rm $(MAIN_SERVICE) pytest --cov=apps --cov-report=term --cov-report=html

lint: ## Run code quality checks
	$(COMPOSE) run --rm $(MAIN_SERVICE) sh -c "flake8 . && black --check . && isort --check-only ."

format: ## Auto-format code
	$(COMPOSE) run --rm $(MAIN_SERVICE) sh -c "black . && isort ."

# ======================================================
# Utilities
# ======================================================
py-clean: ## Remove Python cache files
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
