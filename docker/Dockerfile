FROM ubuntu:14.04
MAINTAINER Leo Wang <grakiss.wanglei@huawei.com>
LABEL version="0.1" description="OPNFV Dovetail Docker Container"

ARG BRANCH=master

RUN \
    apt-get update \
&& \
    apt-get install -y \
        gcc \
        git \
        vim \
        python-dev \
        python-mock \
        python-pip \
        apt-transport-https \
        wget \
        --no-install-recommends \
&& \
    apt-get update

RUN wget -qO- https://get.docker.com/ | sed 's/ docker-engine/ docker-engine=1.12.3-0~trusty/' | sh

ENV HOME /home/opnfv
ENV REPOS_DIR ${HOME}/dovetail
WORKDIR /home/opnfv

RUN \
    mkdir -p ${REPOS_DIR} \
&& \
    git config --global http.sslVerify false \
&& \
    pip install git+https://git.opnfv.org/dovetail@$BRANCH#egg=dovetail \
&& \
    ln -s /usr/local/lib/python2.7/dist-packages/dovetail ${REPOS_DIR}/dovetail

WORKDIR ${REPOS_DIR}/dovetail

# get db schema from opnfv sites
RUN mkdir -p ${REPOS_DIR}/dovetail/utils/local_db
ADD get_db_schema.py ${REPOS_DIR}/dovetail/utils/local_db
RUN cd ${REPOS_DIR}/dovetail/utils/local_db && python get_db_schema.py
