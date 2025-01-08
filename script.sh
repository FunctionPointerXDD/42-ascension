#!/bin/bash

apt update -y  && apt install -y vim && apt install lsof && apt install net-tools -y

if [ -d "/app" ]; then 
    echo "/app already present, skipping creation"
else
    echo "/app not found, creating..."
    mkdir -p /app && chmod -R 755 /app
fi

cd app

pip install -r /home/requirements.txt

if [ $DEV = true ]; then 
    pip install -r /home/requirements.dev.txt;
fi

django-admin startproject mysite
 
python mysite/manage.py runserver 0.0.0.0:8000