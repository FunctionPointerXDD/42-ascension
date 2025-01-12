#!/bin/bash

if [ -d "/app/mysite" ]; then 
    echo "/app already present, skipping creation"
else
    echo "/app/mysite not found, creating..."
    mkdir -p /app/mysite && chmod -R 755 /app/mysite
fi

pip install -r /home/requirements.txt

cd /app/mysite

django-admin startproject config .
python manage.py runserver 0.0.0.0:8000

if [ -d /app/mysite/pybo ]; then
    echo "/app/mysite/pybo already present , skipping.."
else
    django-admin startapp pybo
