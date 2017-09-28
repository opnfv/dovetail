#!/bin/bash
FILE=/etc/nginx/sites-enabled/default

if [ "$testapi_url" != "" ]; then
    sed -i "s/server localhost:8010/server $testapi_url/" $FILE
fi

service supervisor start

tail -f /var/log/supervisor/supervisord.log
