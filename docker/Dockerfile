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
        python-dev \
        python-pip \
        --no-install-recommends \
&& \
    rm -rf /var/lib/apt/lists/*

RUN pip install -U setuptools wheel

ENV HOME /home/opnfv
ENV REPOS_DIR ${HOME}/dovetail
WORKDIR $HOME

RUN \
    git clone https://gerrit.opnfv.org/gerrit/dovetail \
&& \
    cd dovetail \
&& \
    git fetch https://gerrit.opnfv.org/gerrit/dovetail $BRANCH \
&& \
    git checkout FETCH_HEAD \
&& \
    pip install .

WORKDIR ${REPOS_DIR}/dovetail

# get db schema from opnfv sites
# RUN mkdir -p ${REPOS_DIR}/dovetail/utils/local_db
# ADD get_db_schema.py ${REPOS_DIR}/dovetail/utils/local_db
# RUN cd ${REPOS_DIR}/dovetail/utils/local_db && python get_db_schema.py
