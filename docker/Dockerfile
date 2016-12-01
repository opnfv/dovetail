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
        apt-transport-https \
        --no-install-recommends \
&& \
    apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D \
&& \
    mkdir -p /etc/apt/sources.list.d \
&& \
    echo deb https://apt.dockerproject.org/repo ubuntu-trusty main > /etc/apt/sources.list.d/docker.list \
&& \
    apt-get update &&  apt-get install -y docker-engine=1.12.3-0~trusty \
&& \
    pip install pyyaml \
        click \
        jinja2

ENV HOME /home/opnfv
ENV REPOS_DIR ${HOME}/dovetail
WORKDIR /home/opnfv

RUN \
    git config --global http.sslVerify false \
&& \
    git clone --depth 1 -b $BRANCH https://gerrit.opnfv.org/gerrit/dovetail.git ${REPOS_DIR} \
&& \
    mkdir -p ${REPOS_DIR}/results

WORKDIR ${REPOS_DIR}/dovetail
