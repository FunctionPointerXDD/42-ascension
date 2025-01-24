#!/bin/sh

#create ssl certification
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ${CERTS_KEY_PATH} -out ${CERTS_PATH} -subj "/C=kr/ST=seoul/L=gaepo/O=chansjeo/CN=chans_cert"

chmod 600 ${CERTS_KEY_PATH} ${CERTS_PATH}

sed -i "s|DOMAIN_NAME|${DOMAIN_NAME}|g" /etc/nginx/nginx.conf
sed -i "s|CERTS_PATH|${CERTS_PATH}|g" /etc/nginx/nginx.conf
sed -i "s|CERTS_KEY_PATH|${CERTS_KEY_PATH}|g" /etc/nginx/nginx.conf
 
exec nginx -g "daemon off;"