#!/usr/bin/env bash
set -euo pipefail

IMAGE_PREFIX=${IMAGE_PREFIX:-docker-microservices}
TAG=${TAG:-latest}

docker build -t "${IMAGE_PREFIX}/gateway:${TAG}" ./gateway
docker build -t "${IMAGE_PREFIX}/web-service:${TAG}" ./services/web_service
docker build -t "${IMAGE_PREFIX}/auth-service:${TAG}" ./services/auth_service
docker build -t "${IMAGE_PREFIX}/agenda-service:${TAG}" ./services/agenda_service
docker build -t "${IMAGE_PREFIX}/contact-service:${TAG}" ./services/contact_service
docker build -t "${IMAGE_PREFIX}/integrations-service:${TAG}" ./services/integrations_service
docker build -t "${IMAGE_PREFIX}/notifications-service:${TAG}" ./services/notifications_service

echo "==> Imágenes construidas con prefijo ${IMAGE_PREFIX} y tag ${TAG}"
