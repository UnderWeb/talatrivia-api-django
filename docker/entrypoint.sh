#!/bin/bash
# docker/entrypoint.sh - Application container entrypoint
set -e

echo "Waiting for PostgreSQL..."
# Timeout after 30 seconds to prevent infinite loops in CI/CD
timeout=30
while ! nc -z talatrivia-postgres 5432; do
    sleep 0.5
    timeout=$((timeout - 1))
    if [ $timeout -eq 0 ]; then
        echo "Error: PostgreSQL connection timeout"
        exit 1
    fi
done
echo "PostgreSQL started"

# Compile translations for i18n support
echo "Compiling translations..."
python manage.py compilemessages --ignore .venv 2>/dev/null || echo "Warning: No translations to compile or already compiled"

# Collect static files in production environments only
if [ "$DJANGO_SETTINGS_MODULE" = "config.settings.production" ]; then
    echo "Collecting static files..."
    python manage.py collectstatic --noinput --clear
fi

exec "$@"
