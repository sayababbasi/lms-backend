#!/bin/bash
# start.sh

# Exit on error
set -e

echo "Starting Celery worker in the background..."
celery -A lms_crm worker --concurrency=1 -l info &

echo "Starting Gunicorn server in the foreground..."
exec gunicorn lms_crm.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2 --threads 4 --timeout 300
