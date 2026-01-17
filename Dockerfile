FROM python:3.12-slim

WORKDIR /app

# Kopiere alle Dateien
COPY . .

# Exponiere den Port (Railway setzt PORT automatisch)
ENV PORT=8080
EXPOSE $PORT

# Starte den HTTP-Server mit PORT aus Umgebungsvariable
CMD python3 -m http.server $PORT
