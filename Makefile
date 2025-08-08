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
	docker start ${CONTAINER_NAME}

api-down:
	docker stop ${CONTAINER_NAME}

api-restart:
	docker restart ${CONTAINER_NAME}

code-beauty:
	uv run ruff check --fix . && uv run ruff format --check .

code-test:
	docker run --rm \
		--env-file .env \
		-v $(PWD)/app:/app/app \
		-v $(PWD)/tests:/app/tests \
		--network fastapi-boilerplate_fastapi-boilerplate-network \
		fastapi-boilerplate-app:latest \
		uv run pytest --durations=0 -vv --cov-report term-missing --cov --ignore temp $(TARGET)

code-test-not-cov:
	docker run --rm \
		--env-file .env \
		-v $(PWD)/app:/app/app \
		-v $(PWD)/tests:/app/tests \
		--network fastapi-boilerplate_fastapi-boilerplate-network \
		fastapi-boilerplate-app:latest \
		uv run pytest --ignore temp $(TARGET)

code-test-report:
	docker run --rm \
		--env-file .env \
		-v $(PWD)/app:/app/app \
		-v $(PWD)/tests:/app/tests \
		-v $(PWD)/htmlcov:/app/htmlcov \
		-v $(PWD)/report:/app/report \
		--network fastapi-boilerplate_fastapi-boilerplate-network \
		fastapi-boilerplate-app:latest \
		uv run pytest --cov=app --cov-report html:/app/htmlcov --ignore temp $(TARGET) --html=/app/report/report.html

api-log:
	docker compose logs -f ${CONTAINER_NAME}

db-migrate:
	docker compose exec app uv run alembic revision --autogenerate -m "${MSG}"

db-upgrade:
	docker compose exec app uv run alembic upgrade head

uv-pip-list:
	uv pip list

pre-commit:
	uv run pre-commit run --all-files
