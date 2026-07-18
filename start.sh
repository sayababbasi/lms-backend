#!/bin/bash
# start.sh

# Exit on error
set -e

echo "Starting Celery worker in the background..."
celery -A lms_crm worker -l info &

echo "Starting Gunicorn server in the foreground..."
exec gunicorn lms_crm.wsgi:application --bind 0.0.0.0:8000
