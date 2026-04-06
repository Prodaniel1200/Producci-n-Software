.PHONY: install-dev test test-unit smoke up down logs

install-dev:
	python -m pip install --upgrade pip
	pip install -r requirements-dev.txt

test:
	pytest

test-unit:
	pytest tests/unit

smoke:
	docker compose up --build -d

down:
	docker compose down

logs:
	docker compose logs -f
