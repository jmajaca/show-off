FROM python:3.10.2-slim

WORKDIR app

RUN apt update && apt -y install build-essential libpcre3 libpcre3-dev

COPY . .
RUN pip install -r requirments.txt && pip install uwsgi

EXPOSE 5000

CMD uwsgi --ini uwsgi.ini