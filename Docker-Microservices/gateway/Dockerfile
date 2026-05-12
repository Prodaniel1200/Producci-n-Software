FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV PORT=80

EXPOSE 80

CMD ["sh", "-c", "gunicorn -b 0.0.0.0:${PORT} app:app"]