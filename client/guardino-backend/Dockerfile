# ---- Basis-Image ----
FROM python:3.11-slim AS base
# ---- Environment-Variablen ----
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# ---- Arbeitsverzeichnis ----
WORKDIR /app

# ---- System-Dependencies (für psycopg2/asyncpg etc.) ----
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# ---- Python-Dependencies ----
# Erst nur requirements kopieren, damit Docker-Cache besser greift
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# ---- Application Code kopieren ----
COPY . .

# Optional: eigener User, nicht root
RUN useradd -m appuser
USER appuser

# ---- Port & Startkommando ----
EXPOSE 8000

# Falls dein Einstiegspunkt anders ist, hier anpassen
ENTRYPOINT ["/app/entrypoint.sh"]
