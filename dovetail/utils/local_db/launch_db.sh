#!/bin/bash
##############################################################################
# Copyright (c) 2016 HUAWEI TECHNOLOGIES CO.,LTD and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

export mongodb_port=${mongodb_port:-"27017"}
export testapi_port=${testapi_port:-"8000"}

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

container_name='mongodb_offline_dovetail'

echo "Step2: remove the exist container with the same name '$container_name' if exists."
sudo docker ps -a -f "name=${container_name}"

if [[ ! -z $(sudo docker ps -aq -f "name=${container_name}" -f "ancestor=${mongodb_img}") ]]; then
    sudo docker ps -aq -f "name=${container_name}" -f "ancestor=${mongodb_img}" | xargs sudo docker rm -f
fi

# run mongodb container
echo "Step3: run ${container_name} container."
cmd="sudo docker run -itd -p ${mongodb_port}:27017 -v ${DOVETAIL_HOME}/testapi/mongo:/data/db --name ${container_name} ${mongodb_img}"
echo $cmd
${cmd}

echo "Successfully create mongo DB."

echo "Step4: get the internal IP of ${container_name} container..."
get_ip_cmd="ip a | grep eth0 | grep inet | awk '{print \$2}' | cut -d'/' -f 1"
mongo_ip=$(sudo docker exec ${container_name} /bin/bash -c "${get_ip_cmd}")
echo "The internal IP of container ${container_name} is ${mongo_ip}"


echo "=========================="
echo "Create the testapi service."
echo "=========================="

set +e
testapi_img="opnfv/testapi:cvp.0.3.0"
echo "Step1: pull the image $testapi_img."
sudo docker pull $testapi_img
set -e

container_name='testapi_offline_dovetail'

echo "Step2: remove the exist container with the same name '$container_name' if exists."
sudo docker ps -a -f "name=${container_name}"

if [[ ! -z $(sudo docker ps -aq -f "name=${container_name}" -f "ancestor=${testapi_img}") ]]; then
    sudo docker ps -aq -f "name=${container_name}" -f "ancestor=${testapi_img}" | xargs sudo docker rm -f
fi

# run testapi container
echo "Step3: run ${container_name} container."
cmd="sudo docker run -itd -p ${testapi_port}:8000 --name ${container_name} -v ${DOVETAIL_HOME}/testapi/logs:/home/testapi/logs -e mongodb_url=mongodb://${mongo_ip}:${mongodb_port}/ ${testapi_img}"
echo $cmd
${cmd}

echo "Step4: get the internal IP of ${container_name} container..."
get_ip_cmd="ip a | grep eth0 | grep inet | awk '{print \$2}' | cut -d'/' -f 1"
testapi_ip=$(sudo docker exec ${container_name} /bin/bash -c "${get_ip_cmd}")
echo "The internal IP of container ${container_name} is ${testapi_ip}"

echo "Wait for testapi to work..."
sleep 10

echo "================================="
echo "Upload default project info to DB"
echo "================================="

echo "Init DB info..."
cmd="python /home/opnfv/dovetail/dovetail/utils/local_db/init_db.py ${testapi_ip} ${testapi_port}"
echo $cmd
${cmd}

echo "Successfully load DB info."
