FROM ubuntu:18.04
RUN apt-get update && apt install python3 -y && apt install python3-pip -y && pip3 install Flask && pip3 install redis && pip3 install pymongo
COPY *.py /file-server/
COPY logging.conf /file-server/
ENTRYPOINT python3 /file-server/app.py
VOLUME /var/log
