FROM python:3.11.1

COPY requirements.txt /home/requirements.txt
COPY ./script.sh /home/script.sh

RUN chmod 755 /home/script.sh

RUN python -m pip install --upgrade pip
RUN python -m pip install django==5.1.5 \
    django-filter \
    djangorestframework \
    requests \
    pillow \
    psycopg2

WORKDIR /server

CMD [ "bash", "/home/script.sh" ]
