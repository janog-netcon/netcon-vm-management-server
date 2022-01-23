#!/bin/bash

export GOOGLE_APPLICATION_CREDENTIALS=/var/app/creds.json
cd /var/app

# The port will be used for uwsgi, default.conf needs to be changed as well if the value changes
uwsgi --ini uwsgi.ini &

nginx -g "daemon off;"
