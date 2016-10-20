.. This work is licensed under a Creative Commons Attribution 4.0 International
.. License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) OPNFV, Huawei Technologies Co.,Ltd and others.

===========================
Dovetail Tool Installation
===========================

Abstract
########

Dovetail tool supports installation both on Linux OS and by using a docker image.
The detailed installation procedure on Linux OS or via docker image are shown in next sections.

The SUT(System Under Test) should expose interface with parameters

::

  SUT_TYPE, SUT type, e.g., apex, compass, fuel, joid, etc
  SUT_IP, SUT external network IP, e.g., 192.168.200.2
  NODE_NAME, this can be shown in the test result for users to see which pod the dovetail tool runs
  DEPLOY_SCENARIO, deployment scenario, e.g., os-nosdn-nofeature-ha
  BUILD_TAG, this can be shown in the test result for users to identify logs
  CI_DEBUG, true for debug information printed and false for not printed
  DEPLOY_TYPE, baremetal or virtual

these parameters should be correctly configed before dovetail tool running.

Dovetail tool installation on local Linux OS environment
########################################################

Dovetail tool supports installation on local Linux OS environment.
The steps needed to run dovetail tool on are:

Dovetail tool downloading
--------------------------

Source code downloading:

::

  git clone https://gerrit.opnfv.org/gerrit/dovetail

Environment preparation
-----------------------

Configuration file adaptation:

::

  cd {dovetail_path}/dovetail/conf
  vim functest_config.yml
  vim yardstick_config.yml

to modify the ``envs`` parameters, i.e., SUT_TYPE, SUT_IP, NODE_NAME,
DEPLOY_SCENARIO, BUILD_TAG, CI_DEBUG, DEPLOY_TYPE, in the yml files.

Dependent packages are stored in ``prepare_env.py``, dependencies installation can be
completed by:

::

  cd {dovetail_path}/dovetail/dovetail
  python prepare_env.py

Now the environment should be ready for dovetail tool running.

Compliance & Certification test cases
-----------------------------------

the compliance&certification test cases can be defined under ``/dovetail/cert``
directory, which is shown in the format of yaml. A sample is provided named as ``basic.yml``,
it is shown as

::

  certification_basic:
    name: certification_basic
    testcase_list:
      - dovetail.ipv6.tc001

the testcase listed, here is dovetail.ipv6.tc001, should already been defined under ``dovetail/testcase``.

Note: if a new test cases yaml file is created, its name should be started with ``certification_``,
such as the sample is ``certification_basic``.

Dovetail tool running
---------------------

After environment preparation done and C&C test cases added, the dovetail tool can be run with

::

  python run.py --scenario basic


the basic here can be replaced with the test cases yaml file name. If not an argument given,
basic will be run as the default.

Dovetail tool run by using Docker container
###########################################

The dovetail tool can be run by using docker container, the detailed steps are shown below

Pull dovetail docker image from public dockerhub
------------------------------------------------

::

  sudo docker pull opnfv/dovetail:<Tag>

<Tag> here is the version sign, 'latest' is used for the master branch.

Dovetail docker container creation
----------------------------------

To make a file used for the environment, such as 'dovetail-docker-env',

::

  INSTALLER_TYPE=compass
  INSTALLER_IP=192.168.200.2
  DEPLOY_TYPE=baremetal
  DEPLOY_SCENARIO=ha-nosdn
  CI_DEBUG=true

Note: please adjust the content according to the environment.

Then to create the dovetail docker::

    sudo docker run --privileged=true --rm -t \
         --env-file dovetail-docker-env \
         -v /home/opnfv/dovetail/results:/home/opnfv/dovetail/results \
         -v /var/run/docker.sock:/var/run/docker.sock \
         --name <Dovetail_Container_Name> \
         opnfv/dovetail:<Tag> /bin/bash

To attach dovetail container and run test cases
-----------------------------------------------

Before trying to attach the dovetail container, the status can be checked by ::

   docker ps -a

to attach the dovetail container with status 'Up' and start bash mode::

   docker exec -it <Dovetail_Container_Name> bash

Inside the dovetail docker, following cmds can be executed to run the testcases::

   cd /home/opnfv/dovetail/dovetail
   python run.py --scenario basic

Results Output
###############

The running log is stored in ``/home/opnfv/dovetail/results/dovetail.log``.
The report of certification is stored in ``/home/opnfv/dovetail/results/dovetail_report.txt``.
