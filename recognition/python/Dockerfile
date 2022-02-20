FROM python:3.9-slim

WORKDIR app

RUN apt update && apt -y install build-essential libpcre3 libpcre3-dev

COPY api .
COPY model/requirments.txt requirments_model.txt
COPY model/src src
RUN pip install -r requirments.txt && pip install -r requirments_model.txt && pip install uwsgi==2.0.20

EXPOSE 5000

CMD uwsgi --ini uwsgi.ini