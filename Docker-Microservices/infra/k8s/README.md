# Kubernetes

Los manifiestos en `base/` despliegan cada microservicio por separado y dejan a `gateway` como entrada única del sistema.

## Aplicar
```bash
kubectl apply -k infra/k8s/base
```

## Antes de aplicar
- Reemplaza las imágenes `docker-microservices/...` por las de tu registry si hace falta.
- Completa `infra/k8s/base/secrets.template.yaml` con `SECRET_KEY` y credenciales de Outlook.
- Verifica que tu cluster tenga un Ingress Controller llamado `nginx`.

## Persistencia
- `users-data-pvc`: autenticación.
- `contact-data-pvc`: mensajes de contacto.

## Punto de entrada
El Ingress publica únicamente al servicio `gateway` y el enrutamiento interno queda centralizado allí, para mantener la fachada monolítica.
