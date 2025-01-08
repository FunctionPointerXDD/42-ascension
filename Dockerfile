FROM python:3.11.1

# ensure that the python output
#i.e the stdout and stderr streams are sent straight to terminal
ENV PYTHONUNBUFFERED 1

ARG DEV=false

COPY requirements.txt /home/
COPY requirements.dev.txt /home/
COPY ./script.sh /home/script.sh

RUN chmod 755 /home/script.sh

#install this only if it is dev mode

EXPOSE 8000

WORKDIR /app

CMD [ "bash", "/home/script.sh" ]
