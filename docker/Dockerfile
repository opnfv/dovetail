FROM aarch64/ubuntu:16.04
MAINTAINER Armband team <armband@enea.com>
LABEL version="0.1" description="OPNFV Dovetail AArch64 Docker Container"

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
        --no-install-recommends \
&& \
    apt-get update &&  apt-get -y install docker.io

ENV HOME /home/opnfv
ENV REPOS_DIR ${HOME}/dovetail
WORKDIR /home/opnfv

RUN \
    git config --global http.sslVerify false \
&& \
    git clone https://git.opnfv.org/dovetail ${REPOS_DIR} \
&& \
    mkdir -p ${REPOS_DIR}/results \
&& \
    pip install -U setuptools \
&& \
    pip install -U pip \
&& \
    pip install -r ${REPOS_DIR}/requirements.txt \
&& \
    cd ${REPOS_DIR} \
&& \
    pip install -e .

WORKDIR ${REPOS_DIR}/dovetail
