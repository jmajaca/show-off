FROM python:3.6-slim

WORKDIR app

RUN apt update && apt -y install build-essential libpcre3 libpcre3-dev

COPY . .
RUN pip install -r requirments.txt && pip install -r requirments_api.txt && pip install uwsgi==2.0.20

EXPOSE 5000

CMD uwsgi --ini uwsgi.ini
