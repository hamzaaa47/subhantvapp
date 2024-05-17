# Stage 1: Build Stage
# Verwende ein offizielles Python Runtime-Image als Eltern-Image für die Build-Phase
FROM python:3.9-slim as builder

# Setze das Arbeitsverzeichnis im Container
WORKDIR /app

# Kopiere nur die benötigten Dateien für die Installation der Abhängigkeiten
COPY requirements.txt .

# Installiere benötigte Pakete
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere den restlichen Quellcode in das Arbeitsverzeichnis
COPY . .

# Stage 2: Runtime Stage
# Verwende wieder ein offizielles Python Runtime-Image als Basis
FROM python:3.9-slim

# Setze das Arbeitsverzeichnis im Container
WORKDIR /app

# Kopiere nur die nötigen Artefakte aus dem Builder
COPY --from=builder /app /app

# Lege fest, welcher Befehl beim Start des Containers ausgeführt werden soll
CMD ["python", "./main.py"]
