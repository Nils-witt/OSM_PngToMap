python manage.py migrate
python manage.py collectstatic --noinput

daphne pngtomap_api.asgi:application -b 0.0.0.0 -p 8000