# Mapa del proyecto integrado

## Entrada
- `gateway/`: recibe las peticiones del navegador y las manda a `web_service`.
- `services/web_service/`: servidor Flask principal que renderiza HTML y consume otros servicios por HTTP.

## Microservicios
- `services/auth_service/`: login y registro.
- `services/agenda_service/`: agenda paginada y ponentes.
- `services/contact_service/`: persistencia del formulario de contacto.
- `services/integrations_service/`: scraping de CONIITI y flujo base de Outlook.

## Persistencia
- `data/users.csv`: usuarios heredados.
- `data/contact_messages.csv`: mensajes del formulario.

## Equivalencia con tu proyecto anterior
- `main/app.py` se repartió entre `web_service` y los microservicios.
- `main/scraper.py` pasó a `integrations_service/app/providers/coniiti_provider.py`.
- `templates/` pasó a `services/web_service/app/templates/`.
- `static/` pasó a `services/web_service/app/static/`.
