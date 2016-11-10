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

The compliance and certification test cases can be defined under the ``/dovetail/compliance``
directory, which is defined in yaml format.
A sample file named ``compliance_set.yml`` is provided as follows:

::

  compliance_set:
    name: compliance_set
    testcases_list:
      - dovetail.ipv6.tc001

The testcase listed here is dovetail.ipv6.tc001, defined within ``dovetail/testcase``.

Running Dovetail tool
---------------------

After environment preparation is complete and test cases added, the Dovetail tool can be run with

::

  python run.py --testsuite compliance_set

The value ``compliance_set`` passed to the ``testsuite`` flag can be replaced with the test cases yaml file.
If not argument is given, the compliance_set testsuite will be run as the default.

Moreover, the testcases in given testarea can be run with ``testarea`` command line argument, such as
testarea ``ipv6`` in ``compliance_set``

::

  python run.py --testsuite compliance_set --testarea ipv6

Dovetail provides some sets, ``debug``, ``proposed_tests`` and ``compliance_set``,
``debug`` is used for locally and Continuous Integration(CI) developing purpose,
which provides typical testcase examples, feel free to edit it when develops locally, such as
only to run a testcase which only takes minutes. ``proposed_tests`` is the testcase
candidate which mainly comes from the wiki link
https://wiki.opnfv.org/display/dovetail/Dovetail+Test+Areas+and+Test+Cases.
``compliance_set`` is used for compliance. Moreover, dovetail tool can be easily
extended to support more complicated compliance requirements,
such as feature set based or scenario based compliance.

If you want to run ``debug``, just run with

::

  python run.py --testsuite debug

Running Dovetail in a Docker container
########################################

The Dovetail tool can be run in a Docker container by utilizing the following steps:

Pull Dovetail Docker image from public Dockerhub
------------------------------------------------

::

  sudo docker pull opnfv/dovetail:<Tag>

<Tag> here is the version, 'latest' is used for the master branch.

As an alternative way, you can build own docker image from Dockfile(s) under ``docker/`` directory,
``Dockerfile`` is based on ubuntu system and ``Dockerfile.centos7`` is for centos7.

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
   python run.py --testsuite compliance_set

Results Output
###############

The running log is stored in ``/home/opnfv/dovetail/results/dovetail.log``.
The compliance report is stored in ``/home/opnfv/dovetail/results/dovetail_report.txt``.
