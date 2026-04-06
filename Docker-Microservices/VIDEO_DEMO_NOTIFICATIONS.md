# Guion de video - resiliencia cuando falla notifications_service

## Objetivo del video
Demostrar en aproximadamente 1 minuto que la aplicacion tolera la caida del microservicio de notificaciones y sigue permitiendo crear una ponencia desde el Front.

## Preparacion
```bash
cp .env.example .env
make smoke
```

Abrir en navegador:
- `http://localhost:8000/login`
- `http://localhost:8000/agenda`
- `http://localhost:8000/ponentes/nueva`

## Guion sugerido
1. Mostrar brevemente que todos los contenedores estan arriba:
   ```bash
   docker compose ps
   ```
2. Apagar el microservicio de notificaciones:
   ```bash
   docker compose stop notifications_service
   ```
3. Volver a mostrar estado:
   ```bash
   docker compose ps
   ```
4. En el navegador, iniciar sesion.
5. Entrar a `Nueva ponencia`.
6. Crear una ponencia con datos reales de prueba.
7. Guardar.
8. Mostrar que:
   - la pagina responde
   - la app no cae
   - aparece mensaje de degradacion controlada
   - la agenda sigue cargando
9. Cerrar con la idea: la creacion del dato es critica; la notificacion es secundaria y su falla no rompe el sistema.

## Frase tecnica recomendada para explicar el comportamiento
"La aplicacion implementa degradacion controlada. Si el servicio de notificaciones no responde, agenda_service no revierte la operacion principal; registra la advertencia y permite que la ponencia sea creada exitosamente."
