FROM debian:latest

RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y nginx openssh-server tor
    
COPY ./config/nginx.conf /etc/nginx/conf.d/default.conf

COPY ./index.html /var/www/html

COPY ./config/sshd_config /etc/ssh/sshd_config

COPY ./config/torrc /etc/tor/torrc

COPY ./entrypoint.sh .

RUN chmod +x entrypoint.sh

CMD [ "/entrypoint.sh" ]