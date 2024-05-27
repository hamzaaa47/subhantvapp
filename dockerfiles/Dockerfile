# Stage 1: Build Stage
# Verwende ein offizielles Python Runtime-Image als Eltern-Image für die Build-Phase
FROM python:3.9-slim as builder

# Install necessary system dependencies for Qt
RUN apt-get update && apt-get install -y \
    libx11-dev \
    libxext-dev \
    libxrender-dev \
    libglib2.0-0 \
    libegl1-mesa \
    libgl1-mesa-glx \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Setze das Arbeitsverzeichnis im Container
WORKDIR /app

# Kopiere nur die benötigten Dateien für die Installation der Abhängigkeiten
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere den Rest des Anwendungs-Codes
COPY . .

# Stage 2: Runtime Stage
# Verwende ein offizielles Python Runtime-Image als Eltern-Image für die Runtime-Phase
FROM python:3.9-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libx11-6 \
    libxext6 \
    libxrender1 \
    libglib2.0-0 \
    libegl1-mesa \
    libgl1-mesa-glx \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Setze das Arbeitsverzeichnis im Container
WORKDIR /app

# Kopiere die installierten Python-Pakete aus dem Build-Image
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

# Kopiere den Rest des Anwendungs-Codes
COPY --from=builder /app /app

ENV DISPLAY=:0

# Definiere den Befehl, der ausgeführt wird, wenn der Container startet
CMD ["python", "src/main.py"]
