.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) OPNFV, Huawei Technologies Co.,Ltd and others.

=========================================
Conducting ONAP VNF Testing with Dovetail
=========================================

Overview
--------

As the LFN verification framework, Dovetail covers ONAP VNF tests by integrating
VNF SDK and VVP. This guide introduces only how to use Dovetail to run the tests.
For more details about VNF SDK and VVP, please refer to `ONAP VNF SDK Compliance Verification Program
<https://docs.onap.org/en/latest/submodules/vnfsdk/model.git/docs/files/VNFSDK-LFN-CVC.html>`_
and `ONAP VVP <https://docs.onap.org/en/latest/submodules/vvp/documentation.git/docs/index.html>`_.


Definitions and abbreviations
-----------------------------

- LFN - Linux Foundation Networking
- ONAP - Open Network Automation Platform
- VNF - Virtual Network Function
- SDK - Software Development Kit
- VVP - VNF Validation Program


Environment Preparation
-----------------------

Currently, there are only VNF package validation tests which do not rely on the
ONAP deployment. As a result, the preparation is very simple.


Install Docker
^^^^^^^^^^^^^^

The main prerequisite software for Dovetail is Docker. Please refer to `official
Docker installation guide <https://docs.docker.com/install/>`_ which is relevant
to your Test Host's operating system.


Install VNF SDK Backend (optional)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If it is TOSCA based VNF, then VNF SDK Backend must be installed before the
tests. There is a `docker-compose.yml` in VNFSDK repo which runs 2 docker containers. Use
the following commands to run the containers:

.. code-block:: bash

   $ export NEXUS_DOCKER_REPO=nexus3.onap.org:10001
   $ export REFREPO_TAG=1.2.1-STAGING-20181228T020411Z
   $ export POSTGRES_TAG=latest
   $ export MTU=1450
   $ wget https://raw.githubusercontent.com/onap/vnfsdk-refrepo/master/vnfmarket-be/deployment/install/docker-compose.yml
   $ sudo docker-compose up -d


The command `docker ps` can be used to check if the 2 containers named
'refrepo' and 'postgres' are running.

The VNF package to be tested should be copied to the container 'refrepo'.

.. code-block:: bash

   $ sudo docker cp /path/to/VNF/name.csar refrepo:/opt


Run Tests with Dovetail
^^^^^^^^^^^^^^^^^^^^^^^

For convenience and as a convention, we will create a home directory for storing
all Dovetail related config files and results files:

.. code-block:: bash

   $ mkdir -p ${HOME}/dovetail
   $ export DOVETAIL_HOME=${HOME}/dovetail


For example, here we set Dovetail home directory to be ``${HOME}/dovetail``.
Afterwards, we will create a directory named ``pre_config`` inside this directory
to store all Dovetail config related files:

.. code-block:: bash

   $ mkdir -p ${DOVETAIL_HOME}/pre_config


There should be a file `env_config.sh` inside this directory to provide some info.
For TOSCA based VNFs, it should look like this:

.. code-block:: bash

   $ cat ${DOVETAIL_HOME}/pre_config/env_config.sh
   export HOST_URL="http://<docker host ip>:8702"
   export CSAR_FILE="/path/to/VNF/copied/in/container/name.csar"


For HEAT based VNFs, user should copy an archive of the HEAT template VNF
packages to `pre_config`. The archive must be in gzip tar (tar.gz) format.
In addition, the archive must contain only a directory with the same name
(e.g. vnf_a.tar.gz must only include a directory named vnf_a).

Configuration file `env_config.sh` should look like this for HEAT based VNFs:

.. code-block:: bash

   $ cat ${DOVETAIL_HOME}/pre_config/env_config.sh
   export VNF_ARCHIVE_NAME="vnf_archive_name"


Use the command below to create a Dovetail container and get access to its shell:

.. code-block:: bash

   $ sudo docker run --privileged=true -it \
             -e DOVETAIL_HOME=$DOVETAIL_HOME \
             -v $DOVETAIL_HOME:$DOVETAIL_HOME \
             -v /var/run/docker.sock:/var/run/docker.sock \
             opnfv/dovetail:<tag> /bin/bash


The ``-e`` option sets the DOVETAIL_HOME environment variable in the container
and the ``-v`` options mount files from the Test Host to the destination path
inside the container. The latter option allows the Dovetail container to read
the configuration files and write result files into DOVETAIL_HOME on the Test
Host. The user should be within the Dovetail container shell, once the command
above is executed. In order to run ONAP VNF tests 'latest' <tag> must be used.

Run VNF tests with the following command:

.. code-block:: bash

   $ dovetail run --testsuite <suite name> -d


For TOSCA based VNFs, `<suite name>` is `onap.tosca.2019.04` and for
HEAT based ones, it is `onap.heat.2019.04`.


NOTE: If Dovetail run fails when testing `onap-vtp.validate.csar`, then follow the
below guidelines to run the test again.

.. code-block:: bash

   $ sudo docker exec -it refrepo bash
   $ export OPEN_CLI_HOME=/opt/vtp
   $ cd $OPEN_CLI_HOME/bin
   $ ./oclip-grpc-server.sh
   $ #Exit docker by running CTRL+p+q
