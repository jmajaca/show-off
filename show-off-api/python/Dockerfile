FROM python:3.9.12-slim

WORKDIR app

RUN apt update && apt -y install build-essential libpcre3 libpcre3-dev ffmpeg libsm6 libxext6

COPY . .
RUN pip install -r requirments.txt && pip install uwsgi

EXPOSE 5000

CMD uwsgi --ini uwsgi.ini