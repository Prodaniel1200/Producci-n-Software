# Producción Software - integrado con microservicios

Esta versión toma tu estructura original (`main/app.py`, `main/scraper.py`, `templates/`, `static/`, `data/users.csv`) y la reorganiza en una arquitectura híbrida que sí puedes arrancar desde cero.

## Qué quedó separado
- `gateway/`: entrada con Nginx
- `services/web_service/`: frontend SSR Flask
- `services/auth_service/`: login y registro
- `services/agenda_service/`: agenda y ponentes
- `services/contact_service/`: contacto
- `services/integrations_service/`: CONIITI + Outlook
- `data/`: persistencia simple para desarrollo

## Arranque
```bash
cp .env.example .env
docker compose up --build
```

Luego abre `http://localhost:8000`.

## Dónde va cada cosa
- Todo lo que renderiza HTML va en `services/web_service/app/templates/`.
- Todo lo estático va en `services/web_service/app/static/`.
- La lógica externa de CONIITI quedó en `services/integrations_service/app/providers/coniiti_provider.py`.
- La autenticación quedó en `services/auth_service/`.
- Los datos heredados quedaron en `data/users.csv`.

## Observaciones
- Conservé `users.csv` para que no tengas que migrar todo de golpe.
- Los usuarios nuevos se guardan con hash.
- El login soporta usuarios viejos en texto plano y nuevos con hash.
- Outlook solo funciona si completas las variables MSAL.
