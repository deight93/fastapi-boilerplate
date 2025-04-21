ENV ?= dev

service-build:
ifeq ($(ENV), dev)
	docker compose build
else ifeq ($(ENV), prod)
	docker compose -f docker-compose.yml -f docker-compose.prod.yml build
else
	@echo "Error: Unknown ENV value '$(ENV)'"
	@echo "Please set ENV to 'dev' or 'prod'"
	exit 1
endif

service-up:
ifeq ($(ENV), dev)
	docker compose up -d
else ifeq ($(ENV), prod)
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
else
	@echo "Error: Unknown ENV value '$(ENV)'"
	@echo "Please set ENV to 'dev' or 'prod'"
	exit 1
endif

service-down:
ifeq ($(ENV), dev)
	docker compose down
else ifeq ($(ENV), prod)
	docker compose -f docker-compose.yml -f docker-compose.prod.yml down
else
	@echo "Error: Unknown ENV value '$(ENV)'"
	@echo "Please set ENV to 'dev' or 'prod'"
	exit 1
endif

service-clean:
ifeq ($(ENV), dev)
	docker compose down -v
else ifeq ($(ENV), prod)
	docker compose -f docker-compose.yml -f docker-compose.prod.yml down -v
else
	@echo "Error: Unknown ENV value '$(ENV)'"
	@echo "Please set ENV to 'dev' or 'prod'"
	exit 1
endif

api-up:
	docker start app

api-down:
	docker stop app

api-restart:
	docker restart app

code-beauty:
	ruff check --fix . && ruff format

api-log:
	docker compose logs -f app

api-test:
	docker compose exec app pytest --cov-report term-missing --cov --ignore temp

db-migrate:
	docker compose exec app alembic revision --autogenerate -m "${MSG}"

db-upgrade:
	docker compose exec app alembic upgrade head

poetry-show:
	docker compose exec app poetry show

pre-commit:
	pre-commit run --all-files
