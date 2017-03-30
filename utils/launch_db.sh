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
    echo "./launch_db.sh 192.168.115.2"
    echo ""
    echo "parameters:"
    echo "  db_host_ip: your localhost ip address "
    echo ""
    exit 1
fi

export mongodb_port=${mongodb_port:-"27017"}
export testapi_port=${testapi_port:-"8000"}
export db_host_ip=${db_host_ip:-"$1"}

set -e

echo "==================="
echo "Create the mongodb."
echo "==================="

# pull image kkltcjk/mongodb:reporting
mongodb_img="kkltcjk/mongodb:reporting"
echo "Step1: pull the image $mongodb_img."
sudo docker pull $mongodb_img > /dev/null

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

# pull image kkltcjk/testapi:reporting
testapi_img="kkltcjk/testapi:reporting"
echo "Step1: pull the image $testapi_img."
sudo docker pull $testapi_img > /dev/null

container_name='testapi'

echo "Step2: remove the exist container with the same name '$container_name' if exists."
sudo docker ps -a -f "name=${container_name}"

if [[ ! -z $(sudo docker ps -aq -f "name=${container_name}") ]]; then
    sudo docker ps -aq -f "name=${container_name}" | xargs sudo docker rm -f
fi

# run testapi container
echo "Step3: run ${container_name} container."
cmd="sudo docker run -itd -p ${testapi_port}:8000 --name ${container_name} -e mongodb_url=mongodb://${db_host_ip}:${mongodb_port}/ ${testapi_img}"
echo $cmd
${cmd}

echo "Successfully create the testapi service."

echo "================================="
echo "Upload default project info to DB"
echo "================================="

# For Ubuntu, there is file /etc/lsb-release
# For Centos and redhat, there is file /etc/redhat-release
if [ -f /etc/lsb-release ]; then
    sudo apt-get update > /dev/null
    sudo apt-get install -y python-pip > /dev/null
elif [ -f /etc/redhat-release ]; then
    sudo yum -y update > /dev/null
    sudo yum -y install epel-release > /dev/null
    sudo yum -y install python-pip > /dev/null
else
    echo "This operating system is not currently supported."
    exit 1
fi

pip install requests > /dev/null

echo "Init DB info..."
cmd="python ./init_db.py ${db_host_ip} ${testapi_port}"
echo ${cmd}
${cmd} > /dev/null

echo "Successfully load DB info."

