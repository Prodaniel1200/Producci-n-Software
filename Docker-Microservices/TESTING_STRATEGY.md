# Estrategia de pruebas - Producci-n-Software

## Objetivo
Este documento prepara el proyecto para ejecutar pruebas unitarias, pruebas de resiliencia y la demostracion del requisito funcional: apagar el microservicio de notificaciones, crear una ponencia desde el Front y comprobar que la aplicacion no se rompe.

## Cobertura incorporada
La suite creada valida:
- auth_service: registro, duplicados, login legacy y login con hash.
- contact_service: validacion y persistencia.
- integrations_service: scraping CONIITI y validaciones Outlook.
- agenda_service: paginacion, creacion de ponencias, degradacion controlada ante falla de notificaciones.
- notifications_service: endpoint y validaciones.
- web_service: rutas publicas, login, registro, agenda, contacto, integraciones y creacion de ponencia desde el front.

## Comandos base
```bash
make install-dev
make test
```

## Estructura de pruebas
- `tests/unit/`: pruebas unitarias y de componentes Flask.
- `tests/integration/`: espacio reservado para pruebas entre servicios reales por docker compose.
- `tests/conftest.py`: fixtures y cargadores de servicios.

## Criterio de aprobacion para el video
La creacion de la ponencia debe seguir funcionando aunque `notifications_service` este apagado. El sistema no debe devolver error 500 ni romper la navegacion. El comportamiento esperado es:
- la ponencia se crea
- se redirige al usuario a agenda
- el sistema muestra un aviso de degradacion controlada

## Proximo paso recomendado
Agregar pruebas de integracion reales con `docker compose up -d` y un runner que ejercite el flujo completo contra `gateway`.
