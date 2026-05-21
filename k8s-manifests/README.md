# Kubernetes manifests para CONIITI 2026

Este directorio contiene los manifiestos YAML necesarios para desplegar el microservicio `auth-service` en un clúster local de Kubernetes (Minikube o Docker Desktop).

## Qué incluye

- `namespace.yaml`
  - Crea el namespace `coniiti` donde vivirán los recursos.

- `configmap.yaml`
  - Define variables de configuración no sensibles.
  - Ejemplos: `USERS_CSV_PATH`, `FLASK_ENV`, `GUNICORN_WORKERS`, `GUNICORN_THREADS`, `GUNICORN_TIMEOUT`, `REQUEST_TIMEOUT`.

- `secrets.yaml`
  - Define un Secret con datos sensibles codificados en Base64.
  - Ejemplos: `SECRET_KEY`, `MS_CLIENT_ID`, `MS_CLIENT_SECRET`, `MS_TENANT_ID`.

- `auth-service.yaml`
  - Define un `Deployment` para `auth-service`.
  - Define un `Service` de tipo `ClusterIP` para exponer el puerto `5000`.

## Cómo cumple el entregable

### 1. Deployment con límites de recursos
El `Deployment` en `auth-service.yaml` incluye:
- `requests.cpu: "100m"`
- `requests.memory: "128Mi"`
- `limits.cpu: "300m"`
- `limits.memory: "256Mi"`

### 2. Service para exposición
El `Service` en `auth-service.yaml` expone el puerto `5000` y enruta al `Deployment` de `auth-service`.
Esto permite el acceso desde otros pods del clúster.

### 3. Uso de ConfigMap y Secret
- `configmap.yaml` contiene configuración no sensible usada por el servicio.
- `secrets.yaml` contiene datos sensibles usados por el servicio.
- El deployment obtiene variables desde `configMapKeyRef` y `secretKeyRef`.

## Despliegue local

Aplica los recursos en el siguiente orden:

```bash
kubectl apply -f k8s-manifests/namespace.yaml
kubectl apply -f k8s-manifests/configmap.yaml
kubectl apply -f k8s-manifests/secrets.yaml
kubectl apply -f k8s-manifests/auth-service.yaml
```

### Imagen local

Para que el pod arranque correctamente, la imagen debe estar disponible en el clúster local.

Con Minikube:

```bash
minikube image load docker-microservices/auth-service:latest
minikube image load docker-microservices/web-service:latest
```

## Notas importantes

- Este entregable solo modifica `k8s-manifests/`.
- El resto del repositorio no se cambió.
- Si se desea acceder desde `localhost`, se puede usar `minikube service auth-service -n coniiti --url`.
