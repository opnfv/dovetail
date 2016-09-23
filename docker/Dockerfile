FROM ubuntu:14.04
MAINTAINER Leo Wang <grakiss.wanglei@huawei.com>
LABEL version="0.1" description="OPNFV Dovetail Docker Container"

RUN apt-get update && apt-get install -y \
python-pip \
git \
apt-transport-https \
--no-install-recommends

RUN apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D

RUN mkdir -p /etc/apt/sources.list.d

RUN echo deb https://apt.dockerproject.org/repo ubuntu-trusty main > /etc/apt/sources.list.d/docker.list

RUN apt-get update &&  apt-get install -y docker-engine=1.9.1-0~trusty

RUN pip install pyyaml \
click \
jinja2

ENV HOME /home/opnfv
ENV REPOS_DIR /home/opnfv/dovetail
WORKDIR /home/opnfv

RUN git config --global http.sslVerify false
RUN git clone https://gerrit.opnfv.org/gerrit/dovetail.git ${REPOS_DIR}

RUN mkdir -p ${REPOS_DIR}/results

WORKDIR /home/opnfv/dovetail/scripts
