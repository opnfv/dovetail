#!/bin/sh

cd $(dirname $(readlink -f $0))
exec gunicorn -b :5000 --access-logfile - --error-logfile - app.routes:app
