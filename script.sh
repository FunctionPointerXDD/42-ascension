#!/bin/bash

if [ -d "/app" ]; then 
    echo "/app already present, skipping creation"
else
    echo "/app not found, creating..."
    mkdir -p /app && chmod -R 755 /app
fi

DEV=false

if [ $DEV = true ]; then 
    pip install -r /home/requirements.dev.txt;
fi

if [ -d "/app/mysite" ]; then
    pip install -r /home/requirements.txt
    django-admin startproject /app/mysite
else   
    echo "/app/mysite already present, skipping installation"
fi

python /app/mysite/manage.py runserver 0.0.0.0:8000
