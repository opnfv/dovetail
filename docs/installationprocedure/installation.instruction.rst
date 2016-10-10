.. This work is licensed under a Creative Commons Attribution 4.0 International
.. License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) OPNFV, Huawei Technologies Co.,Ltd and others.

Dovetail Installation
=====================

Abstract
--------

Dovetail currently supports installation on Ubuntu 14.04 or by using a docker image.
Detailed steps about installing Dovetail can be found below.

To use Dovetail you should have access to an OpenStack environment,
with at least Nova, Neutron, Glance, Keystone and Heat installed.


Run dovetail on local machine
-----------------------------

The steps needed to run Dovetail on Ubuntu are:

1. Download source code of Dovetail and prepare the environment it needs.
2. Create the certification configuration .yaml file.
3. Run the certification.


Download Dovetail and prepare the environment
---------------------------------------------

The source code of Dovetail can be got from Git:

::

  git clone http://gerrit.opnfv.org/gerrit/dovetail.git

After that you need to prepare the environment which means install some tools,
modules and anything else Dovetail needs. A file named ``prepare_env.py`` can
do all of these for you.

::

  cd scripts/
  python prepare_env.py

Now the environment should be prepared for running the tests.

Besides, you may want to install it in a python virtualenv, that is beyond the scope
of this installation instruction.

Create the test configuration file
----------------------------------

You can wirte a certification configuration file with the format of yaml,
which can be defined to meet your own requirements. The yaml file should
be located in the folder ``dovetail/scripts/cert``. There provide a sample
file named ``basic.yml``.

::

  certification_basic:
  name: certification_basic
  testcase_list:
    - dovetail.feature.tc001
    - dovetail.vimops.tc001
    - dovetail.vimops.tc002
    - dovetail.vimops.tc003
    - dovetail.vimops.tc004
    - dovetail.vimops.tc005
    - dovetail.vimops.tc006
    - dovetail.vimops.tc007
    - dovetail.vimops.tc009

As you can see, the configuration file combines the test cases you want to run
together, and each of them is defined in ``dovetail/scripts/testcase``. the name
of the configuration file should be certification_**, where ** is the name of
scenario i.e. basic. When running the certification, you can choose which scenario
you want to run.


Run the certification
---------------------

When you get the Dovetail source code, prepare the environment and define the
certification configuration file, you can then run the test case. Take test case
certification_basic as the example. You can run it using the file ``run.py`` with
basic (scenario name) as its argument.

::

  python run.py basic

If you did not give an argument, it will be default set as basic.


Run dovetail on Docker container
--

steps:
1. pull image
2. run container
3. config
4. run testcase

pull image
--

Get the latest docker image from docker hub.

::
 sudo docker pull opnfv/dovetail:latest

run container
--

Start a container from the image that you just pulled.

::
 sudo docker run --privileged=true -v /var/run/docker.sock:/var/run/docker.sock opnfv/dovetail:latest "/bin/bash"

config
--

For now, we need only change value of ``INSTALLER_TYPE`` and ``INSTALLER_IP`` of the variable ``envs`` to your own environment.

::
 sudo docker exec -it $(CONTAINER_ID) "/bin/bash"
 vi /home/opnfv/dovetail/scripts/conf/functest_config.yml
 vi /home/opnfv/dovetail/scripts/conf/yardstick_config.yml

run testcase
--

In docker, you just run following cmds to execute the testcase.

::
 cd /home/opnfv/dovetail/scripts
 python run.py




Output
--

The running log is stored in ``/home/opnfv/dovetail/results/dovetail.log``.
The report of certification is stored in ``/home/opnfv/dovetail/results/dovetail_report.txt``.
