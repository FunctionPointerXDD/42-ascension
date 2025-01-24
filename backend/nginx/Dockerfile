FROM alpine:3.19

RUN apk update && apk add nginx openssl
RUN adduser -D -g 'www' www
RUN mkdir -p /www && \
    chown -R www:www /var/lib/nginx /www && \
    chmod -R 755 /www
    
#COPY -> release
COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./index.html /www
COPY ./spa.html /www

ADD script.sh /home/script.sh
RUN chmod -R 755 /home/script.sh

EXPOSE 80 
EXPOSE 443 

ENTRYPOINT [ "/home/script.sh" ]