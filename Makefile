service-build:
	docker-compose build

service-up:
	docker-compose up -d

service-down:
	docker-compose down

service-clean:
	docker-compose down -v

api-up:
	docker start app

api-down:
	docker stop app

api-restart:
	docker restart app

code-beauty:
	ruff check --fix .

api-log:
	docker-compose logs -f app

api-test:
	docker-compose exec app pytest --cov-report term-missing --cov --ignore temp

db-migrate:
	docker-compose exec app alembic revision --autogenerate -m "${MSG}"

db-upgrade:
	docker-compose exec app alembic upgrade head

poetry-show:
	docker-compose exec app poetry show