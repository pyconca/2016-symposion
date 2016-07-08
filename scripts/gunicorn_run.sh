#!/bin/bash

NAME="symposion2016"
DJANGODIR=/srv/www/pycon.ca/staging.2016/django/symposion2016
SOCKFILE=/srv/www/pycon.ca/staging.2016/django/run/gunicorn.sock
USER=deploy
GROUP=deploy
NUM_WORKERS=3
DJANGO_SETTINGS_MODULE=symposion2016.settings.prod
DJANGO_WSGI_MODULE=symposion2016.wsgi
DATABASE_URL=postgres://{{ db_user }}:{{ db_pass }}@localhost:5432/{{ db_name }}

# Activate the virtual environment
cd $DJANGODIR
source ../env/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export DATABASE_URL=$DATABASE_URL
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --log-level=debug \
  --log-file=-