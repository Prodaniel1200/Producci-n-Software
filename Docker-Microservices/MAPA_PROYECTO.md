# Mapa del proyecto integrado

## Fachada monolítica
- `gateway/`: punto de entrada único del sistema.
- `services/web_service/`: BFF y servidor SSR Flask. Renderiza HTML y protege las rutas que dependen de sesión.

## Microservicios desplegables de forma independiente
- `services/auth_service/`: login y registro.
- `services/agenda_service/`: agenda paginada, ponentes y notificación de nuevas ponencias.
- `services/contact_service/`: persistencia del formulario de contacto.
- `services/integrations_service/`: CONIITI + flujo base de Outlook.
- `services/notifications_service/`: procesamiento de eventos de notificación.

## Infraestructura
- `docker-compose.yml`: entorno local con healthchecks y arranque ordenado.
- `infra/k8s/base/`: despliegue por servicio para Kubernetes.
- `docs/ARQUITECTURA_MONOLITO_FACHADA.md`: explicación del patrón de despliegue.

## Persistencia
- `data/users.csv`: usuarios heredados y nuevos registros locales para Docker Compose.
- `data/contact_messages.csv`: mensajes del formulario para Docker Compose.
- En Kubernetes la persistencia se separa en PVCs por servicio.

## Equivalencia con tu proyecto anterior
- `main/app.py` se reparte entre `gateway`, `web_service` y los microservicios.
- `main/scraper.py` vive en `services/integrations_service/app/providers/coniiti_provider.py`.
- `templates/` y `static/` viven en `services/web_service/app/`.
