#!/bin/ash

python manage.py makemigrations jwtapp
python manage.py migrate jwtapp
python manage.py migrate --fake

gunicorn -w ${WEBSOCKET_WORKER} --threads ${WEBSOCKET_THREAD} -b 0.0.0.0:${JWT_PORT} myjwt.wsgi
