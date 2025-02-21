#!/bin/bash

cd /server

python manage.py makemigrations user
python manage.py migrate user
python manage.py runserver 0.0.0.0:11111
