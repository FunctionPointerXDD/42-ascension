FROM python:3.11.1

RUN python -m pip install --upgrade pip
RUN python -m pip install django==5.1.5 \
    django-filter \
    djangorestframework \
    requests \
    pillow \
    psycopg2

COPY ./script.sh /home/script.sh
RUN chmod 755 /home/script.sh

WORKDIR /server

CMD [ "bash", "/home/script.sh" ]
