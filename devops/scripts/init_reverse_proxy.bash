#!/bin/bash

echo 'Creating reverse proxies'

echo 'Creating configuration'
SHOW_OFF_UI_URL="$(minikube service show-off-ui -n show-off --url)"
SHOW_OFF_API_URL="$(minikube service show-off-api -n show-off --url)"
DETECTION_API_URL="$(minikube service detection-api -n show-off --url)"
mkdir /etc/nginx/sites-available/
touch /etc/nginx/sites-available/reverse-proxy.conf
cp ../configs/reverse_proxy.conf /etc/nginx/sites-available/reverse-proxy.conf

sed -i "s;SHOW_OFF_UI_URL;$SHOW_OFF_UI_URL;g" /etc/nginx/sites-available/reverse-proxy.conf
sed -i "s;SHOW_OFF_API_URL;$SHOW_OFF_API_URL;g" /etc/nginx/sites-available/reverse-proxy.conf
sed -i "s;DETECTION_API_URL;$DETECTION_API_URL;g" /etc/nginx/sites-available/reverse-proxy.conf

echo 'Applying configuration'
service nginx reload

echo 'All done'