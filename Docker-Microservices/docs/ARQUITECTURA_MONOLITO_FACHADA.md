# Arquitectura monolito fachada + microservicios

## Objetivo
Tener una sola entrada para el servidor web, de modo que la aplicación se vea como un monolito desde fuera, pero que internamente esté compuesta por servicios desacoplados y desplegables de forma independiente.

## Patrón aplicado
Se dejó una **fachada monolítica** compuesta por dos piezas:

1. `gateway`
   - Expone el puerto público.
   - Decide a qué servicio enviar cada petición.
   - Replica la misma estrategia tanto en Docker Compose como en Kubernetes.

2. `web_service`
   - Renderiza HTML con Flask.
   - Mantiene la sesión de usuario.
   - Actúa como BFF para vistas que necesitan lógica web.

Detrás de esa fachada están los microservicios de dominio.

## Flujo de tráfico
### Vistas HTML
Navegador -> `gateway` -> `web_service`

### APIs de dominio
Navegador/cliente -> `gateway` -> microservicio correcto

Ejemplos:
- `/api/auth/*` -> `auth_service`
- `/api/agenda` y `/api/ponentes` -> `agenda_service`
- `/api/contact` -> `contact_service`
- `/api/integrations/*` -> `integrations_service`
- `/api/notifications/*` -> `notifications_service`

### Integración interna
`web_service` -> HTTP interno -> otros servicios

Esto permite que las vistas sigan centralizadas sin volver a caer en un `main.py` que haga todo.

## Ventajas de esta reorganización
- La aplicación conserva una **cara única** para el usuario.
- Cada servicio puede escalar, reiniciarse y desplegarse por separado.
- `gateway` y `Ingress` permiten cambiar la topología sin tocar el frontend.
- El proyecto queda listo para evolucionar desde Docker Compose a Kubernetes sin reescribir la arquitectura.

## Decisiones de infraestructura
- Se cambió el arranque de Flask dev server a **Gunicorn** para un uso más realista en contenedores.
- Se añadieron **healthchecks** en Docker Compose.
- Se añadió **ProxyFix** en `web_service` para respetar `X-Forwarded-*` detrás de Nginx e Ingress.
- Se separó la persistencia en Kubernetes por servicio con PVCs distintos para no compartir volúmenes de forma insegura.

## Qué sigue si quieren endurecer más la arquitectura
- Pasar CSV a PostgreSQL.
- Mover autenticación a JWT o sesión distribuida.
- Añadir observabilidad con Prometheus + Grafana.
- Publicar imágenes en un registry y parametrizar tags por entorno.
