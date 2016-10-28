.. This work is licensed under a Creative Commons Attribution 4.0 International
.. License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) OPNFV, Huawei Technologies Co.,Ltd and others.

===========================
Dovetail Tool Installation
===========================

Abstract
########

The Dovetail tool supports installation either directly on the Linux host, or within a Docker container.
The detailed installation procedure on the Linux host or via the Docker container are shown
in the following sections.

There is a need to config the following parameters before Dovetail tool
running on the SUT (System Under Test):

::

  SUT_TYPE, SUT type, e.g., apex, compass, fuel, joid, etc
  SUT_IP, SUT external network IP, e.g., 192.168.200.2
  NODE_NAME, this can be shown in the test result for users to see which pod the dovetail tool runs
  DEPLOY_SCENARIO, deployment scenario, e.g., os-nosdn-nofeature-ha
  BUILD_TAG, this can be shown in the test result for users to identify logs
  CI_DEBUG, true for debug information printed and false for not printed
  DEPLOY_TYPE, baremetal or virtual

Dovetail tool installation on local Linux host environment
##########################################################

In order to install Dovetail into a local Linux host environment, the following steps should
be performed:

Downloading Dovetail tool
--------------------------

Source code downloading:

::

  git clone https://gerrit.opnfv.org/gerrit/dovetail

Environment preparation
-----------------------

Dovetail configuration:

::

  cd {dovetail_path}/dovetail/conf
  vim functest_config.yml
  vim yardstick_config.yml

To modify the ``envs`` parameters, e.g., SUT_TYPE, SUT_IP, NODE_NAME,
DEPLOY_SCENARIO, BUILD_TAG, CI_DEBUG, DEPLOY_TYPE, in the yml files.

System dependencies are installed via the ``prepare_env.py`` file, and you will need ``sudo``
access to complete the installation.

::

  cd {dovetail_path}/dovetail/dovetail
  python prepare_env.py

At this point the environment is now ready for Dovetail execution.

Compliance and certification test cases
----------------------------------------

The compliance and certification test cases can be defined under the ``/dovetail/cert``
directory, which is defined in yaml format.
A sample file named ``basic.yml`` is provided as follows:

::

  certification_basic:
    name: certification_basic
    testcase_list:
      - dovetail.ipv6.tc001

The testcase listed here is dovetail.ipv6.tc001, defined within ``dovetail/testcase``.

Note: if a new test case yaml file is created, its name should start with ``certification_``,
in similiar fashion as the sample file ``certification_basic``.

Running Dovetail tool
---------------------

After environment preparation is complete and test cases added, the Dovetail tool can be run with

::

  python run.py --scenario basic

The value ``basic`` passed to the ``scenario`` flag can be replaced with the test cases yaml file.
If not argument is given, the basic scenario will be run as the default.

Running Dovetail in a Docker container
########################################

The Dovetail tool can be run in a Docker container by utilizing the following steps:

Pull Dovetail Docker image from public Dockerhub
------------------------------------------------

::

  sudo docker pull opnfv/dovetail:<Tag>

<Tag> here is the version, 'latest' is used for the master branch.

Dovetail Docker container creation
----------------------------------

Next, create the ``dovetail-docker-env`` file to define the environment parameters ::

  INSTALLER_TYPE=compass
  INSTALLER_IP=192.168.200.2
  DEPLOY_TYPE=baremetal
  DEPLOY_SCENARIO=ha-nosdn
  CI_DEBUG=true

Then to instantiate the Dovetail Docker container, execute::

    sudo docker run --privileged=true --rm -t \
         --env-file dovetail-docker-env \
         -v /home/opnfv/dovetail/results:/home/opnfv/dovetail/results \
         -v /var/run/docker.sock:/var/run/docker.sock \
         --name <Dovetail_Container_Name> \
         opnfv/dovetail:<Tag> /bin/bash

To attach dovetail container and Running test cases
----------------------------------------------------

Before connecting to the container, you can check the container status by running ::

   docker ps -a

Attach to the container by starting it and obtaining a bash prompt with ::

   docker exec -it <Dovetail_Container_Name> bash

Inside the container the following commands can be executed to trigger the testcases ::

   cd /home/opnfv/dovetail/dovetail
   python run.py --scenario basic

Results Output
###############

The running log is stored in ``/home/opnfv/dovetail/results/dovetail.log``.
The certification report is stored in ``/home/opnfv/dovetail/results/dovetail_report.txt``.
