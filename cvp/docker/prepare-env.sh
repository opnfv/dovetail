#!/bin/bash
FILE=/etc/opnfv_testapi/config.ini


if [ "$mongodb_url" != "" ]; then
    sudo crudini --set --existing $FILE mongo url $mongodb_url
fi

if [ "$base_url" != "" ]; then
    sudo crudini --set --existing $FILE api url $base_url/api/v1
    sudo crudini --set --existing $FILE swagger base_url $base_url
    sudo crudini --set --existing $FILE ui url $base_url
    sudo crudini --set --existing $FILE jira OAUTH_CALLBACK_URL $base_url/api/v1/auth/signin_return_jira
    sudo crudini --set --existing $FILE lfid return_url $base_url/api/v1/auth/signin_return_cas
fi
