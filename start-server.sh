#!/usr/bin/env bash
# start-server.sh
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
    (cd RobinHoodAdmin; python manage.py createsuperuser --no-input; python manage.py collectstatic --noinput;)
fi
(cd RobinHoodAdmin; gunicorn RobinHoodAdmin.wsgi --user www-data --bind 0.0.0.0:8010 --workers 3) &
nginx -g "daemon off;"