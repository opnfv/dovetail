#!/bin/sh

mkdir -p /var/www/html/dovetail-api
cp -r /home/opnfv/swagger-ui/dist/* /var/www/html/dovetail-api
cp /home/opnfv/dovetail/dovetail/api/swagger.yaml /var/www/html/dovetail-api
sed -i 's#url: "https://petstore.swagger.io/v2/swagger.json"#url: "swagger.yaml"#g' /var/www/html/dovetail-api/index.html
sed -i '/deepLinking: true,/a\        validatorUrl: null,' /var/www/html/dovetail-api/index.html

if [[ -n ${SWAGGER_HOST} ]]; then
    sed -i "s/host: localhost:8888/host: ${SWAGGER_HOST}/g" /var/www/html/dovetail-api/swagger.yaml
fi

/etc/init.d/apache2 start

cd $(dirname $(readlink -f $0))
exec gunicorn -b :5000 --access-logfile - --error-logfile - app.routes:app
