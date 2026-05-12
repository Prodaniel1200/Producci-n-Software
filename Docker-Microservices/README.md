# Producción Software - monolito fachada con microservicios

Este proyecto quedó reorganizado para que tenga una **entrada única tipo monolito** para el servidor web, pero con **microservicios desacoplados** que pueden desplegarse por separado en Docker o Kubernetes.

## Qué cambió
- `gateway/` ahora funciona como **fachada monolítica** y enruta APIs a los microservicios correctos.
- `web_service/` queda como **BFF + SSR**, encargado del HTML, la sesión y la experiencia web.
- Cada microservicio usa **Gunicorn**, healthcheck y configuración separada para despliegues más estables.
- Se agregó `infra/k8s/base/` con manifiestos para desplegar cada servicio de forma independiente.
- Se corrigieron detalles de infraestructura que provocaban fallos de despliegue, como la dependencia faltante de `requests` en `agenda_service`.

## Arquitectura resultante
- Navegador -> `gateway` -> `web_service` para vistas HTML.
- Navegador o cliente API -> `gateway` -> microservicios para rutas como `/api/auth/*`, `/api/agenda`, `/api/contact`, `/api/integrations/*` y `/api/notifications/*`.
- `web_service` también consume internamente a los microservicios por HTTP usando DNS interno de contenedores o servicios de Kubernetes.

Más detalle en `docs/ARQUITECTURA_MONOLITO_FACHADA.md`.

## Estructura principal
- `gateway/`: entrada única del sistema.
- `services/web_service/`: frontend SSR Flask.
- `services/auth_service/`: autenticación.
- `services/agenda_service/`: agenda y ponencias.
- `services/contact_service/`: formulario de contacto.
- `services/integrations_service/`: CONIITI + Outlook.
- `services/notifications_service/`: eventos de notificación.
- `infra/k8s/base/`: despliegue Kubernetes.
- `data/`: persistencia local para Docker Compose.

## Docker Compose
```bash
cp .env.example .env
docker compose up --build
```

Luego abre `http://localhost:8000`.

### Rutas principales detrás de la fachada
- HTML y navegación: `http://localhost:8000/`
- Auth: `http://localhost:8000/api/auth/...`
- Agenda: `http://localhost:8000/api/agenda`
- Ponencias: `http://localhost:8000/api/ponentes`
- Contacto: `http://localhost:8000/api/contact`
- Integraciones: `http://localhost:8000/api/integrations/...`
- Notificaciones: `http://localhost:8000/api/notifications/...`

## Kubernetes
1. Construye y publica tus imágenes con el prefijo que vayas a usar.
2. Ajusta los `image:` de `infra/k8s/base/*.yaml` si vas a usar otro registry.
3. Crea o edita el secreto con tus credenciales y la `SECRET_KEY`.
4. Aplica los manifiestos:

```bash
kubectl apply -k infra/k8s/base
```

El Ingress expone el `gateway`, y desde allí se mantiene la misma fachada monolítica.

## Scripts útiles
- `bash bootstrap.sh`: prepara `.env`, instala dependencias locales y ejecuta pruebas.
- `bash start.sh`: levanta Docker Compose.
- `bash test_all.sh`: corre pruebas y cobertura.
- `bash scripts/build_images.sh`: construye imágenes para despliegue.

## Observaciones
- Conservé `users.csv` para evitar una migración completa inmediata.
- El login soporta usuarios antiguos en texto plano y usuarios nuevos con hash.
- Outlook solo funciona si completas `MS_CLIENT_ID`, `MS_CLIENT_SECRET` y `MS_TENANT_ID`.
