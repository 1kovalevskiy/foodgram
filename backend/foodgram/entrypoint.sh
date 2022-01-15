python manage.py collectstatic --noinput &&
python manage.py migrate --noinput &&
python manage.py loaddata dump.json &&
gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000