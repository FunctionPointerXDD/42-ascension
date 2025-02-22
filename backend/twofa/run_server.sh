#!/bin/ash

python manage.py makemigrations twofaapp
python manage.py migrate twofaapp
python manage.py migrate --fake

gunicorn -w ${WEBSOCKET_WORKER} --threads ${WEBSOCKET_THREAD} -b 0.0.0.0:${TWOFA_PORT} twofa.wsgi