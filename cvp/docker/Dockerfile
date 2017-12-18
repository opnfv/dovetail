#######################################################
#   Docker container for OPNFV-TESTAPI
#######################################################
# Purpose: run opnfv-testapi for gathering test results
#
# Maintained by SerenaFeng
# Build:
#    $ docker build -t opnfv/testapi:tag .
#
# Execution:
#    $ docker run -dti -p 8001:8000 \
#      -e "base_url=http://10.63.243.17:8001" \
#      -e "mongodb_url=mongodb://10.63.243.17:27017/" \
#      opnfv/testapi:tag
#
# NOTE: providing swagger_url, mongodb_url is optional.
#       If not provided, it will use the default one
#       configured in config.ini
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

FROM ubuntu:14.04
MAINTAINER SerenaFeng <feng.xiaowei@zte.com.cn>
LABEL version="v1" description="OPNFV TestAPI Docker container"

ARG BRANCH=master

ENV HOME /home

# Packaged dependencies
RUN apt-get update && apt-get install -y \
curl \
git \
gcc \
wget \
python-dev \
python-pip \
crudini \
libffi-dev \
libssl-dev \
libxml2-dev \
libxslt1-dev \
--no-install-recommends

RUN pip install -U setuptools

WORKDIR /home

#RUN pip install --upgrade pip

RUN git config --global http.sslVerify false

RUN git clone https://gerrit.opnfv.org/gerrit/dovetail.git

WORKDIR /home/dovetail
RUN git checkout -f $BRANCH

RUN mkdir -p /home/testapi
RUN mkdir -p /home/testapi/logs/api
RUN cp -rf /home/dovetail/cvp/* /home/testapi

WORKDIR /home/dovetail/cvp
RUN pip install -r requirements.txt
RUN bash install.sh

RUN sed -i '152,152s/)/,\ verify=False)/g' /usr/local/lib/python2.7/dist-packages/cas.py

CMD ["bash", "docker/start-server.sh"]
