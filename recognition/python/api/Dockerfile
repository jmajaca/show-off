FROM python:3.9-slim

WORKDIR app

RUN apt update && apt -y install build-essential libpcre3 libpcre3-dev

COPY . ./api
RUN pip install -r api/requirments.txt && pip install uwsgi==2.0.20

COPY ../model ./model
RUN pip install -r model/requirments.txt

EXPOSE 5000

CMD uwsgi --ini api/uwsgi.ini