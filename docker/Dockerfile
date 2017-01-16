FROM ubuntu:14.04
MAINTAINER Leo Wang <grakiss.wanglei@huawei.com>
LABEL version="0.1" description="OPNFV Dovetail Docker Container"

ARG BRANCH=master

RUN \
    apt-get update \
&& \
    apt-get install -y \
        python-pip \
        git \
        vim \
        apt-transport-https \
        --no-install-recommends \
&& \
    apt-get update &&  apt-get -y install docker.io

ENV HOME /home/opnfv
ENV REPOS_DIR ${HOME}/dovetail
WORKDIR /home/opnfv

RUN \
    git config --global http.sslVerify false \
&& \
    git clone --depth 1 -b $BRANCH https://gerrit.opnfv.org/gerrit/dovetail.git ${REPOS_DIR} \
&& \
    mkdir -p ${REPOS_DIR}/results \
&& \
    pip install -U pip \
&& \
    pip install -r ${REPOS_DIR}/requirements.txt \
&& \
    cd ${REPOS_DIR} \
&& \
    pip install -e .

WORKDIR ${REPOS_DIR}/dovetail
