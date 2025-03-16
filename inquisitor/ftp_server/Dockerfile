FROM debian:latest

RUN apt-get update && apt-get install -y vsftpd net-tools

RUN mkdir -p /vsftpd/empty /anon_ftp

RUN chmod -R 755 /vsftpd/empty

RUN chown -R ftp:ftp /anon_ftp
RUN chmod -R 555 /anon_ftp
# RUN chmod -R 755 /anon_ftp/upload

COPY ./vsftpd.conf /etc/vsftpd.conf

CMD ["vsftpd"]
