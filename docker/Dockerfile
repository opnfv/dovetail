FROM ubuntu:14.04
MAINTAINER Leo Wang <grakiss.wanglei@huawei.com>
LABEL version="0.1" description="OPNFV Dovetail Docker Container"

RUN apt-get update && apt-get install -y \
docker.io \
python-pip \
git \
--no-install-recommends

RUN pip install pyyaml
RUN pip install click

ENV HOME /home/opnfv
WORKDIR /home/opnfv
ENV REPOS_DIR /home/opnfv/dovetail

RUN git config --global http.sslVerify false
RUN git clone https://gerrit.opnfv.org/gerrit/dovetail.git ${REPOS_DIR}

RUN mkdir -p ${REPOS_DIR}/results

