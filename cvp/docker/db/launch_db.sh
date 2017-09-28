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
    echo "  host_ip: your localhost ip address "
    echo "  base_url: your public url for website"
    echo ""
    exit 1
fi

export mongodb_port=${mongodb_port:-"27017"}
export testapi_port=${testapi_port:-"8010"}
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
cmd="sudo docker run -itd -p ${mongodb_port}:27017 -v /home/testapi/mongo:/data/db --name ${container_name} ${mongodb_img}"
echo $cmd
${cmd}

echo "Successfully create mongo DB."


echo "=========================="
echo "Create the testapi service."
echo "=========================="

set +e
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
cmd="sudo docker run -itd -p 8010:8010 --name ${container_name} -v /home/testapi/logs:/home/testapi/logs -e mongodb_url=mongodb://${db_host_ip}:${mongodb_port}/ -e base_url=${base_url} ${testapi_img}"
echo $cmd
${cmd}

echo "Wait for testapi to work..."
sleep 10

set +e
web_img="opnfv/dovetail:web.cvp.0.6.0"
echo "Step1: pull the image $web_img."
sudo docker pull $web_img
set -e

container_name='web_cvp'

echo "Step2: remove the exist container with the same name '$container_name' if exists."
sudo docker ps -a -f "name=${container_name}"

if [[ ! -z $(sudo docker ps -aq -f "name=${container_name}") ]]; then
    sudo docker ps -aq -f "name=${container_name}" | xargs sudo docker rm -f
fi

# run web container
echo "Step3: run ${container_name} container."
cmd="sudo docker run -itd -p 8000:8000 -v /home/testapi/logs:/home/testapi/logs --name ${container_name} -e testapi_url=${db_host_ip}:8010 ${web_img}"
echo $cmd
${cmd}

echo "================================="
echo "Upload default project info to DB"
echo "================================="

echo "Init DB info..."
cmd="python ./init_db.py ${db_host_ip} 8010"
echo $cmd
${cmd}

echo "Init dovetail testcase"
cmd="python ./init_dovetail.py ${base_url}/api/v1"
echo $cmd
${cmd}

echo "Successfully load DB info."

