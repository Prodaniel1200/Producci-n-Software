#!/usr/bin/env bash
set -euo pipefail

echo "==> Verificando herramientas necesarias..."

command -v docker >/dev/null 2>&1 || { echo "ERROR: Docker no está instalado"; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "ERROR: Python3 no está instalado"; exit 1; }

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
    echo "==> Creando .env base"
    cat > .env <<EOF
SECRET_KEY=dev-secret-key
AUTH_SERVICE_URL=http://auth-service:5000
AGENDA_SERVICE_URL=http://agenda-service:5000
CONTACT_SERVICE_URL=http://contact-service:5000
INTEGRATIONS_SERVICE_URL=http://integrations-service:5000
NOTIFICATIONS_SERVICE_URL=http://notifications-service:5000
WEB_REQUEST_TIMEOUT=10
AGENDA_REQUEST_TIMEOUT=5
MS_CLIENT_ID=
MS_CLIENT_SECRET=
MS_TENANT_ID=
EOF
  fi
fi

echo "==> Instalando dependencias de desarrollo"
python3 -m pip install -r requirements-dev.txt

echo "==> Ejecutando pruebas"
pytest -v

echo "==> Construyendo y levantando contenedores"
docker compose up --build -d

echo "==> Estado de contenedores"
docker compose ps

echo "==> Listo. Abre en el navegador:"
echo "http://localhost:8000"
