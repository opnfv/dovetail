FROM ubuntu:18.04
MAINTAINER Stamatis Katsaounis <mokats@intracom-telecom.com>
LABEL version="0.1" description="OPNFV Dovetail Docker Container"

ARG BRANCH=master

RUN \
    apt-get update \
&& \
    apt-get install -y \
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

WORKDIR ${REPOS_DIR}/dovetail

ENV FLASK_APP ${API_DIR}/app/routes.py
EXPOSE 5000
CMD ${API_DIR}/boot.sh
