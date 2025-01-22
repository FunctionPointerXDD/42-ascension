#!/bin/bash

apt-get update -y && apt-get install vim -y && \
apt-get install lsof && apt-get install net-tools -y

if [ -d "/rest" ]; then 
    echo "/rest already present, skipping creation"
else
    echo "/rest not found, creating..."
    mkdir -p /rest && chmod -R 755 /rest
fi

pip install -r /home/requirements.txt

cd /rest/tutorial
## [First Try]
# django-admin startproject tutorial
# cd tutorial 
# python manage.py startapp snippets

python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8001