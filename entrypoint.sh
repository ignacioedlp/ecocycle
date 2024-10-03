#!/bin/sh

echo "Running collectstatic..."
python manage.py collectstatic --no-input --settings=ecocycle.settings.production

echo "Running migrations..."
python manage.py wait_for_db --settings=ecocycle.settings.production
python manage.py migrate --settings=ecocycle.settings.production

echo "Running seeds..."
python manage.py create_materials_and_depositos --settings=ecocycle.settings.production

# si no tengo PORT en mi entorno, asigno 8000
if [ -z "$PORT" ]; then
  export PORT=8000
fi

echo "Starting server..."
gunicorn --env DJANGO_SETTINGS_MODULE=ecocycle.settings.production ecocycle.wsgi:application --bind 0.0.0.0:$PORT