#!/usr/bin/env bash
set -euo pipefail

echo "==> Ejecutando suite de pruebas"
pytest -v

echo "==> Ejecutando cobertura"
pytest --cov=services --cov-report=term-missing -v