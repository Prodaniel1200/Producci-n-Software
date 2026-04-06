.PHONY: install-dev test test-cov up down logs ps bootstrap start restart clean

install-dev:
	pip install -r requirements-dev.txt

test:
	pytest -v

test-cov:
	pytest --cov=services --cov-report=term-missing -v

up:
	docker compose up --build -d

down:
	docker compose down

logs:
	docker compose logs -f

ps:
	docker compose ps

bootstrap:
	bash ./bootstrap.sh

start:
	bash ./start.sh

restart:
	docker compose down
	docker compose up --build -d

clean:
	docker compose down -v