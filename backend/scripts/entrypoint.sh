#!/usr/bin/env sh
set -e

echo "Waiting for database..."

until nc -z db 5432; do
  echo "Waiting for Postgres..."
  sleep 1
done

echo "Database is up."

echo "Running migrations..."
alembic upgrade head

echo "Starting server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
