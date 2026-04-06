#!/usr/bin/env bash
set -euo pipefail

echo "==> Verificando herramientas necesarias..."

command -v docker >/dev/null 2>&1 || { echo "ERROR: Docker no está instalado"; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "ERROR: Python3 no está instalado"; exit 1; }
command -v pip >/dev/null 2>&1 || { echo "ERROR: pip no está instalado"; exit 1; }

if ! docker compose version >/dev/null 2>&1; then
  echo "ERROR: Docker Compose no está disponible"
  exit 1
fi

echo "==> Herramientas detectadas correctamente"

if [ ! -f ".env" ]; then
  if [ -f ".env.example" ]; then
    echo "==> Creando .env desde .env.example"
    cp .env.example .env
  else
    echo "==> No existe .env.example; creando .env básico"
    cat > .env <<EOF
SECRET_KEY=dev-secret-key
CLIENT_ID=TU_CLIENT_ID
CLIENT_SECRET=TU_CLIENT_SECRET
TENANT_ID=TU_TENANT_ID
DATA_PATH=./data
EOF
  fi
fi

echo "==> Instalando dependencias de desarrollo"
pip install -r requirements-dev.txt

echo "==> Ejecutando pruebas"
pytest -v

echo "==> Construyendo y levantando contenedores"
docker compose up --build -d

echo "==> Estado de contenedores"
docker compose ps

echo "==> Listo. Abre en el navegador:"
echo "http://localhost:8000"