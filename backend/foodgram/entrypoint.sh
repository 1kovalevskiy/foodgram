python manage.py collectstatic --noinput &&
sleep 10 &&
python manage.py migrate --noinput &&
sleep 10 &&
python manage.py loaddata dump.json &&
gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000