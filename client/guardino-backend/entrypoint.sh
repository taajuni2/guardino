#!/bin/sh
set -e

sleep 5s
echo "DB ist erreichbar, führe Alembic-Migrationen aus..."
alembic upgrade head

echo "Starte Uvicorn..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000