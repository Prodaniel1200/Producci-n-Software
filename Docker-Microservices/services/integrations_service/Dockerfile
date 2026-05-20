# Usamos una imagen base de Python 3.11 slim
FROM python:3.11-slim

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos todo el contenido de la aplicación a /app dentro del contenedor
COPY . .

# Instalamos las dependencias del archivo requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Puerto que usa el stack interno de Docker Compose
EXPOSE 5000

# Ejecutamos la aplicación con el objeto app exportado desde run.py
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]