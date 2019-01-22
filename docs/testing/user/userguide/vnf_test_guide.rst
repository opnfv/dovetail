.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) OPNFV, Huawei Technologies Co.,Ltd and others.

=========================================
Conducting ONAP VNF Testing with Dovetail
=========================================

Overview
--------

As the LFN verification framework, Dovetail covers ONAP VNF tests by integrating
VTP. This guide only introduces how to use Dovetail to do the tests. For more
details about VTP, please refer to `ONAP VNF SDK Compliance Verification Program
<https://docs.onap.org/en/latest/submodules/vnfsdk/model.git/docs/files/VNFSDK-LFN-CVC.html>`_.


Definitions and abbreviations
-----------------------------

- LFN - Linux Foundation Networking
- ONAP - Open Network Automation Platform
- VNF - Virtual Network Function
- VTP - VNF Test Platform


Prepring Environment
--------------------

Currently, there are only VNF package validation tests which don't rely on the
ONAP deployment. So the preparation is very simple.


Install Docker
^^^^^^^^^^^^^^

The main prerequisite software for Dovetail is Docker. Please refer to official
Docker installation guide that is relevant to your Test Host's operating system.


Install VTP Backend
^^^^^^^^^^^^^^^^^^^

There is a `docker-compose.yml` in VNFSDK repo to run 2 docker containers. Use
the following commands to run the containers.

.. code-block:: bash

   $ export NEXUS_DOCKER_REPO=nexus3.onap.org:10001
   $ export REFREPO_TAG=1.2.1-STAGING-20181228T020411Z
   $ export POSTGRES_TAG=latest
   $ export MTU=1450
   $ wget https://raw.githubusercontent.com/onap/vnfsdk-refrepo/master/vnfmarket-be/deployment/install/docker-compose.yml
   $ docker-compose up -d


Then you can use command `docker ps` to check if there are 2 containers named
'refrepo' and 'postgres' running.

The VNF package to be tested should be copied to container 'refrepo'.

.. code-block:: bash

   $ docker cp /path/to/VNF/name.csar refrepo:/opt


Run Tests with Dovetail
^^^^^^^^^^^^^^^^^^^^^^^

For convenience and as a convention, we will create a home directory for storing
all Dovetail related config files and results files:

.. code-block:: bash

   $ mkdir -p ${HOME}/dovetail
   $ export DOVETAIL_HOME=${HOME}/dovetail


For example, here we set dovetail home directory to be ``${HOME}/dovetail``.
Then create a directory named ``pre_config`` inside this directory to store all
Dovetail related config files:

.. code-block:: bash

   $ mkdir -p ${DOVETAIL_HOME}/pre_config


There should be a file `env_config.sh` inside this directory and provides some info.

.. code-block:: bash

   $ cat ${DOVETAIL_HOME}/pre_config/env_config.sh
   export HOST_URL="http://<docker host ip>:8702"
   export CSAR_FILE="/path/to/VNF/copied/in/container/name.csar"


Use the command below to create a Dovetail container and get access to its shell.

.. code-block:: bash

   $ sudo docker run --privileged=true -it \
             -e DOVETAIL_HOME=$DOVETAIL_HOME \
             -v $DOVETAIL_HOME:$DOVETAIL_HOME \
             -v /var/run/docker.sock:/var/run/docker.sock \
             opnfv/dovetail:<tag> /bin/bash


The ``-e`` option sets the DOVETAIL_HOME environment variable in the container
and the ``-v`` options mounts files from the test host to the destination path
inside the container. The latter option allows the Dovetail container to read
the configuration files and write result files into DOVETAIL_HOME on the Test
Host. The user should be within the Dovetail container shell, once the command
above is executed. The <tag> can be used for ONAP VNF tests is 'latest'.

Run VNF tests with command:

.. code-block:: bash

   $ dovetail run --testcase onap-vtp.validate.csar -d


NOTE: if failed to run, then follow below guidelines and then try to run the test again.

.. code-block:: bash

   $ docker exec -it refrepo bash
   $ export OPEN_CLI_HOME=/opt/vtp
   $ cd $OPEN_CLI_HOME/bin
   $ ./oclip-grpc-server.sh
   $ Exit docker by running CTRL+p+q
