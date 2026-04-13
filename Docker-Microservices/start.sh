#!/usr/bin/env bash
set -euo pipefail

echo "==> Levantando proyecto"
docker compose up --build -d

echo "==> Estado actual"
docker compose ps

echo "==> Aplicación disponible en:"
echo "http://localhost:8000"
