#!/bin/bash

echo 'Creating reverse proxy for show-ui via http port 80'

echo 'Creating configuration'
SHOW_OFF_UI_URL="$(minikube service show-off-ui -n show-off --url)"
mkdir /etc/nginx/sites-available/
touch /etc/nginx/sites-available/reverse-proxy.conf
cp ../configs/reverse_proxy.conf /etc/nginx/sites-available/reverse-proxy.conf

sed -i "s;SHOW_OFF_UI_URL;$SHOW_OFF_UI_URL;g" /etc/nginx/sites-available/reverse-proxy.conf

echo 'Applying configuration'
service nginx reload

echo 'All done'