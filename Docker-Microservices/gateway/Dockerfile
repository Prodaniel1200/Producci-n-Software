FROM python:3.11-slim

WORKDIR /app

# Copiar dependencias primero (mejor cache)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto
COPY . .

# Puerto que usa Azure App Service
EXPOSE 80

# IMPORTANTE: asegúrate que tu archivo principal es app.py y tiene "app = Flask(__name__)"
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:app"]