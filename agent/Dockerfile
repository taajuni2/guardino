# --- Stage 1: Base image ---
FROM python:3.11-slim

# Arbeitsverzeichnis
WORKDIR /agent

# Systemabhängigkeiten (optional für z. B. watchdog, pyyaml)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libmagic1 \
 && rm -rf /var/lib/apt/lists/*

# Requirements zuerst kopieren für Caching
COPY requirements.txt .

# Dependencies installieren
RUN pip install --no-cache-dir -r requirements.txt

# Quellcode & Config kopieren
COPY . .

# Standard-Umgebungsvariablen (optional)
ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/agent

# --- Startkommando ---
# Falls dein Agent ein async main() hat:
CMD ["python", "main.py"]
