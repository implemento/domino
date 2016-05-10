#!/bin/sh

python /usr/src/app/manage.py migrate --database django
python /usr/src/app/manage.py createsuperuser
