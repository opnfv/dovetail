##############################################################################
# Copyright (c) 2019 opnfv.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

FROM ubuntu:18.04
MAINTAINER Stamatis Katsaounis <mokats@intracom-telecom.com>
LABEL version="0.1" description="OPNFV Dovetail Docker Container"

ARG BRANCH=master
ARG SWAGGER_UI_TAG=v3.22.3

RUN \
    apt-get update \
&& \
    apt-get install -y \
        apache2 \
        gcc \
        make \
        git \
        libssl-dev \
        libffi-dev \
        vim \
        python-dev \
        python-pip \
        --no-install-recommends \
&& \
    rm -rf /var/lib/apt/lists/*

RUN pip install -U setuptools wheel

ENV HOME /home/opnfv
ENV REPOS_DIR ${HOME}/dovetail
ENV API_DIR ${REPOS_DIR}/dovetail/api
WORKDIR $HOME

RUN \
    mkdir -p ${REPOS_DIR} \
&& \
    git init /tmp/dovetail \
&& \
    (cd /tmp/dovetail && \
        git fetch --tags https://gerrit.opnfv.org/gerrit/dovetail $BRANCH && \
        git checkout FETCH_HEAD && \
        pip install .) \
&& \
    rm -rf /tmp/dovetail \
&& \
    ln -s /usr/local/lib/python2.7/dist-packages/dovetail ${REPOS_DIR}/dovetail

RUN \
    git clone https://github.com/swagger-api/swagger-ui.git \
&& \
    cd swagger-ui && git checkout $SWAGGER_UI_TAG

WORKDIR ${REPOS_DIR}/dovetail

ENV FLASK_APP ${API_DIR}/app/routes.py
# This port is for flask API in container
EXPOSE 5000
# This port is for Swagger UI in container
EXPOSE 80
CMD bash ${API_DIR}/boot.sh
