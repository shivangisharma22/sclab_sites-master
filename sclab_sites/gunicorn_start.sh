#!/bin/bash

NAME="sclab_sites"
BASEDIR=$(dirname $( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd ))
FLASKDIR=$BASEDIR"/sclab_sites/"
VENVDIR=$BASEDIR"/venv/"
SOCKFILE=$FLASKDIR"/sock"
NUM_WORKERS=1

echo "Starting $NAME"

# activate the virtualenv
cd $VENVDIR
source bin/activate

export PYTHONPATH=$FLASKDIR:$PYTHONPATH

# Start your unicorn
exec gunicorn run:app -b 127.0.0.1:9000 \
  --name $NAME \
  --workers $NUM_WORKERS \
  --log-level=debug \
  --bind=unix:$SOCKFILE
