#!/bin/bash
##############################################################################
# Copyright (c) 2016 HUAWEI TECHNOLOGIES CO.,LTD and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

if [ "$#" -ne 2 ]; then
    echo "Error: missing parameter! try again like this:"
    echo ""
    echo "./launch_db.sh 192.168.115.2 http://116.66.187.136:9999"
    echo ""
    echo "parameters:"
    echo "  db_host_ip: your localhost ip address "
    echo "  base_url: your public url for website"
    echo ""
    exit 1
fi

export mongodb_port=${mongodb_port:-"27017"}
export testapi_port=${testapi_port:-"8000"}
export db_host_ip=${db_host_ip:-"$1"}
export base_url=${base_url:-"$2"}


set -e

echo "==================="
echo "Create the mongodb."
echo "==================="

set +e
# pull image mongo:3.2.1
mongodb_img="mongo:3.2.1"
echo "Step1: pull the image $mongodb_img."
sudo docker pull $mongodb_img
set -e

container_name='mongodb'

echo "Step2: remove the exist container with the same name '$container_name' if exists."
sudo docker ps -a -f "name=${container_name}"

if [[ ! -z $(sudo docker ps -aq -f "name=${container_name}") ]]; then
    sudo docker ps -aq -f "name=${container_name}" | xargs sudo docker rm -f
fi

# run mongodb container
echo "Step3: run ${container_name} container."
cmd="sudo docker run -itd -p ${mongodb_port}:27017 --name ${container_name} ${mongodb_img}"
echo $cmd
${cmd}

echo "Successfully create mongo DB."


echo "=========================="
echo "Create the testapi service."
echo "=========================="

set +e
# pull image opnfv/testapi:cvp.0.5.0
testapi_img="opnfv/testapi:cvp.0.5.0"
echo "Step1: pull the image $testapi_img."
sudo docker pull $testapi_img
set -e

container_name='testapi'

echo "Step2: remove the exist container with the same name '$container_name' if exists."
sudo docker ps -a -f "name=${container_name}"

if [[ ! -z $(sudo docker ps -aq -f "name=${container_name}") ]]; then
    sudo docker ps -aq -f "name=${container_name}" | xargs sudo docker rm -f
fi

# run testapi container
echo "Step3: run ${container_name} container."
cmd="sudo docker run -itd -p ${testapi_port}:8000 --name ${container_name} -e mongodb_url=mongodb://${db_host_ip}:${mongodb_port}/ -e base_url=${base_url} ${testapi_img}"
echo $cmd
${cmd}

echo "Wait for testapi to work..."
sleep 10

echo "================================="
echo "Upload default project info to DB"
echo "================================="

echo "Init DB info..."
cmd="python ./init_db.py ${db_host_ip} ${testapi_port}"
echo ${cmd}
${cmd}

echo "Successfully load DB info."

