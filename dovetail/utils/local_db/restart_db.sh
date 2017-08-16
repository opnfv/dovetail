#!/bin/bash
##############################################################################
# Copyright (c) 2016 HUAWEI TECHNOLOGIES CO.,LTD and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


if [ "$#" -ne 1 ]; then
    echo "Error: missing parameter! try again like this:"
    echo ""
    echo "./restart_db.sh 192.168.115.2"
    echo ""
    echo "parameters:"
    echo "  db_host_ip: your localhost ip address"
    echo ""
    exit 1
fi

export mongodb_port=${mongodb_port:-"27017"}
export testapi_port=${testapi_port:-"8000"}
export db_host_ip=${db_host_ip:-"$1"}

sudo docker rm -f testapi
sudo docker run -itd -p $testapi_port:8000 --name testapi \
    -e mongodb_url=mongodb://$db_host_ip:$mongodb_port/ opnfv/testapi:cvp.0.5.0
