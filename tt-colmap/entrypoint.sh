#!/usr/bin/env sh

export FLASK_APP=colmap-server.colmap-server:app
export FLASK_ENV=development
flask run
#while ! echo exit | nc localhost 5432; do sleep 10; done
#flask db upgrade
#gunicorn --worker-class gevent --workers=1 --max-requests 10000 --bind 0.0.0.0:8080 server.server:app
