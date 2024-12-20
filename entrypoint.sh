#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Creating Log Files..."
mkdir -p /app/logs
touch /app/logs/django_error.log

echo "Applying database migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "Creating superuser..."
python manage.py make_admin

echo "Seeding preferences..."
python manage.py seed_preferences

echo "Collecting static files..."
python manage.py collectstatic --noinput

# Execute the command passed as arguments
exec "$@"
