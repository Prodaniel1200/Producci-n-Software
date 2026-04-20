# Usamos una imagen base de Python 3.11 slim
FROM python:3.11-slim

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos todo el contenido de la aplicación a /app dentro del contenedor
COPY . .

# Instalamos las dependencias del archivo requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Exponemos el puerto 80, ya que es el puerto estándar para aplicaciones web en Azure
EXPOSE 80

# Establecemos el comando para ejecutar la aplicación con Gunicorn (servidor WSGI)
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:app"]