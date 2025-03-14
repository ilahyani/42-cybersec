FROM debian

RUN apt-get update && apt-get upgrade -y \
    && apt-get install gdb libc6-i386 -y

CMD ["tail", "-f", "/dev/null"]