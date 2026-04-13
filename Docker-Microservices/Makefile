IMAGE_PREFIX ?= docker-microservices
TAG ?= latest

.PHONY: install-dev test test-cov up down logs ps bootstrap start restart clean build-images k8s-apply k8s-delete

install-dev:
	python3 -m pip install -r requirements-dev.txt

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

build-images:
	IMAGE_PREFIX=$(IMAGE_PREFIX) TAG=$(TAG) bash ./scripts/build_images.sh

k8s-apply:
	kubectl apply -k infra/k8s/base

k8s-delete:
	kubectl delete -k infra/k8s/base
