#!/usr/bin/env bash
set -euo pipefail

# Ensure runtime dirs
mkdir -p /data /app/staticfiles ${MEDIA_ROOT:-/data/media}

# Default envs if not provided
export PORT=${PORT:-8080}
export DB_PATH=${DB_PATH:-/data/db.sqlite3}
export MEDIA_ROOT=${MEDIA_ROOT:-/data/media}
export DEBUG=${DEBUG:-False}

python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Start ASGI server (Channels via Daphne)
exec daphne -b 0.0.0.0 -p "$PORT" ecommerce.asgi:application
