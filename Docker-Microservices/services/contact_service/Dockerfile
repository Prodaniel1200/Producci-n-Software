FROM python:3.11-slim

WORKDIR /app

# Copiar dependencias primero (mejor cache)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto
COPY . .

# Puerto que usa el stack interno de Docker Compose
EXPOSE 5000

# Ejecutamos la aplicación con el objeto app exportado desde run.py
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]