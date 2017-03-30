.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Ericsson AB

==============================================
Compliance and Verification program user guide
==============================================

.. toctree::
   :maxdepth: 2

Version history
===============

+------------+----------+------------------+----------------------------------+
| **Date**   | **Ver.** | **Author**       | **Comment**                      |
|            |          |                  |                                  |
+------------+----------+------------------+----------------------------------+
| 2017-03-15 | 0.0.1    | Chris Price      | Draft version                    |
|            |          |                  |                                  |
+------------+----------+------------------+----------------------------------+


Dovetail CVP Testing Overview
=============================

The Dovetail testing framework consists of two major parts: the testing client that executes
all test cases in a vendor lab (self-testing) or a third party lab, and the server system that
is under the OPNFV's administration to store and view test results based on OPNFV Test API. The
following diagram illustrates this overall framework.

/* here is a draft diagram that needs to be revised when exact information is known and fixed */

This section mainly focuses on helping the testers in the vendor's domain attempting to run the
CVP tests.

Dovetail client tool (or just Dovetail tool or Dovetail for short) can be installed in the
jumphost either directly as Python software, or as a Docker(r) container. Comments of pros
and cons of the two options TBD.

The section 'Installing the test tool'_ describes the steps the tester needs to take to install
Dovetail directly from the source. In 2.3, we describe steps needed for installing Dovetail
Docker(r) container. Once installed, and properly configured, the remaining test process is mostly
identical for the two options. In 2.4, we go over the steps of actually running the test suite.
In 2.5, we discuss how to view test results and make sense of them, for example, what the tester
may do in case of unexpected test failures. Section 2.6 describes additional Dovetail features
that are not absolutely necessary in CVP testing but users may find useful for other purposes.
One example is to run Dovetail for in-house testing as preparation before official CVP testing;
another example is to run Dovetail experimental test suites other than the CVP test suite.
Experimental tests may be made available by the community for experimenting less mature test
cases or functionalities for the purpose of getting feedbacks for improvement.

Installing the test tool
========================

Before taking this step, testers should check the hardware and networking requirements of
the POD, and the jumphost in particular, to make sure they are compliant.

In this section, we describe the procedure to install Dovetail client tool that runs the CVP
test suite from the jumphost. The jumphost must have network access to both the public Internet
and to the O&M (Operation and Management) network with access rights to all VIM APIs being tested.

-------------------------------
Checking the Jumphost Readiness
-------------------------------

While Dovetail does not have hard requirement on a specific operating system type or version,
these have been validated by the community through some level of exercise in OPNFV labs or PlugFests.

Ubuntu 16.04.2 LTS (Xenial) for x86_64
Ubuntu 14.04 LTS (Trusty) for x86_64
CentOS-7-1611 for x86_64
Red Hat Enterprise Linux 7.3 for x86_64
Fedora 24 Server for x86_64
Fedora 25 Server for x86_64

------------------------------------
Configuring the Jumphost Environment
------------------------------------

/* First, openstack env variables to be passed to Functest */

The jumphost needs to have the right environmental variable setting to enable access to the
Openstack API. This is usually done through the Openstack credential file.

Sample Openstack credential file environment_config.sh:

/*Project-level authentication scope (name or ID), recommend admin project.*/

export OS_PROJECT_NAME=admin

/* Authentication username, belongs to the project above, recommend admin user.*/

export OS_USERNAME=admin


/* Authentication password.*/

export OS_PASSWORD=secret


/* Authentication URL, one of the endpoints of keystone service. If this is v3 version, there need some extra variables as follows.*/

export OS_AUTH_URL='http://xxx.xxx.xxx.xxx:5000/v3'


/* Default is 2.0. If use keystone v3 API, this should be set as 3.*/

export OS_IDENTITY_API_VERSION=3


/* Domain name or ID containing the user above.  Command to check the domain: openstack
user show <OS_USERNAME>*/

export OS_USER_DOMAIN_NAME=default


/* Domain name or ID containing the project above.  Command to check the domain: openstack
project show <OS_PROJECT_NAME>*/

export OS_PROJECT_DOMAIN_NAME=default


/* home directory for dovetail, if install Dovetail Docker container, DOVETAIL_HOME can
just be /home/opnfv*/

export DOVETAIL_HOME=$HOME/cvp

Export all these variables into environment by,

% source <OpenStack-credential-file-path>


The tester should validate that the Openstack environmental settings are correct by,
% openstack service list

-----------------------------------
Installing Prerequisite on Jumphost
-----------------------------------

1. Dovetail requires Python 2.7 and later

Use the following steps to check if the right version of python is already installed,
and if not, install it.

% python --version

2. Dovetail requires Docker 1.8.0 and later

Use the following steps to check if the right version of Docker is already installed,
and if not, install it.

% docker --version

As the docker installation process is much complex, you can refer to the official
document: https://docs.docker.com/engine/installation/linux/

-------------------------------------
2.2.4 Installing Dovetail on Jumphost
-------------------------------------

A tester can choose one of the following two methods for installing and running Dovetail.
In part1, we explain the steps to install Dovetail from the source. In part2, an alternative
using a Docker image with preinstalled Dovetail is introduced. part1. Installing Dovetail directly

Update and install packages

a) Ubuntu

sudo apt-get update

sudo apt-get -y install gcc  git  vim  python-dev  python-pip  --no-install-recommends

b) centos and redhat

sudo yum -y update

sudo yum -y install epel-release

sudo yum -y install gcc  git  vim-enhanced  python-devel  python-pip

c) fedora

sudo dnf -y update

sudo dnf -y install gcc  git  vim-enhanced  python-devel  python-pip  redhat-rpm-config

p.s  When testing SUT's https service, there need some extra packages, such as
apt-transport-https. This still remains to be verified.


Installing Dovetail

Now we are ready to install Dovetail.

/* Version of dovetail is not specified yet? we are still using the latest in the master
- this needs to be fixed before launch. */

First change directory to $DOVETAIL_HOME,

% cd $DOVETAIL_HOME

% sudo git clone https://git.opnfv.org/dovetail

% cd $DOVETAIL_HOME/dovetail

% sudo pip install -e ./

/* test dovetail install is successful */

% dovetail -h
part2. Installing Dovetail Docker Container

The Dovetail project also maintains a Docker image that has Dovetail test tools preinstalled.

Running CVP Test Suite
======================

------------------
Running Test Suite
------------------

The Dovetail client CLI allows the tester to specify which test suite to run.
By default the results are stored in a local file $DOVETAIL_HOME/dovetail/results.

% dovetail run --testsuite <test suite name> --openrc <path-to-openrc-file> /*?? */

Multiple test suites may be available, testsuites named "debug" and "proposed_tests" are just provided for testing. But for the purpose of running CVP test suite, the test suite name follows the following format,

CVP.<major>.<minor>.<patch>  /* test if this format works */

For example, CVP_1_0_0

% dovetail run --testsuite CVP_1_0_0

When the SUT's VIM (Virtual Infrastructure Manager) is Openstack, its configuration is commonly defined in the openrc file. In that case, you can specify the openrc file in the command line,

% dovetail run --testsuite CVP_1_0_0 --openrc <path-to-openrc-file>

In order to report official results to OPNFV, run the CVP test suite and report to OPNFV official URL,

% dovetail run --testsuite <test suite name> --openrc <path-to-openrc-file> --report https://www.opnfv.org/cvp

The official server https://www.opnfv.org/cvp is still under development, there is a temporal server to use http://205.177.226.237:9997/api/v1/results

--------------------------------
Making Sense of CVP Test Results
--------------------------------

When a tester is performing trial runs, Dovetail stores results in a local file by default.

% cd $DOVETAIL_HOME/dovetail/results



1.  local file

a)  Log file: dovetail.log

/* review the dovetail.log to see if all important information has been captured - in default mode without DEBUG */

/* the end of the log file has a summary of all test case test results */

Additional log files may be of interests: refstack.log, opnfv_yardstick_tcXXX.out ...

b)  Example: Openstack refstack test case example

can see the log details in refstack.log, which has the  passed/skipped/failed test cases result, the failed test cases have rich debug information

for the users to see why this test case fails.

c) Example: OPNFV Yardstick test case example

for yardstick tool, its log is stored in yardstick.log

for each test case result in Yardstick, the logs are stored in opnfv_yardstick_tcXXX.out, respectively.



2. OPNFV web interface

wait for the complement of LF, test community, etc.
2.3.3 Updating Dovetail or Test Suite

% cd $DOVETAIL_HOME/dovetail

% sudo git pull

% sudo pip install -e ./

This step is necessary if dovetail software or the CVP test suite have updates.


Other Dovetail Usage
====================

------------------------
Running Dovetail Locally
------------------------

/*DB*/

---------------------------------------------
Running Dovetail with Experimental Test Cases
---------------------------------------------


--------------------------------------------------
Running Individual Test Cases or for Special Cases
--------------------------------------------------

1. Refstack client to run Defcore testcases

a) By default, for Defcore test cases run by Refstack-client, which are consumed by
DoveTail,  are run followed with automatically generated configuration file, i.e.,
refstack_tempest.conf.

In some circumstances, the automatic configuration file may not quite satisfied with
the SUT, DoveTail provide a way for users to set its configuration file according
to its own SUT manually,

besides, the users should define Defcore testcase file, i.e., defcore.txt, at the
same time. The steps are shown as,

when "Installing Dovetail Docker Container" method is used,


% sudo mkdir /home/opnfv/dovetail/userconfig

% cd /home/opnfv/dovetail/userconfig

% touch refstack_tempest.conf defcore.txt

% vim refstack_tempest.conf

% vim defcore.txt


the recommend way to set refstack_tempest.conf is shown in
https://aptira.com/testing-openstack-tempest-part-1/

the recommended way to edit defcore.txt is to open
https://refstack.openstack.org/api/v1/guidelines/2016.08/tests?target=compute&type=required&alias=true&flag=false
and copy all the test cases into defcore.txt.

Then use “docker run” to create a container,


% sudo docker run --privileged=true -it -v <openrc_path>:<openrc_path> \

-v /home/opnfv/dovetail/results:/home/opnfv/dovetail/results \

-v /home/opnfv/dovetail/userconfig:/home/opnfv/dovetail/userconfig \

-v /var/run/docker.sock:/var/run/docker.sock \

--name <DoveTail_Container_Name> (optional) \

opnfv/dovetail:<Tag> /bin/bash



there is a need to adjust the CVP_1_0_0 testsuite, for dovetail,
defcore.tc001.yml and defcore.tc002.yml are used for automatic and
manual running method, respectively.

Inside the dovetail container,


% cd /home/opnfv/dovetail/compliance

% vim CVP_1_0_0.yml


to add defcore.tc002 and annotate defcore.tc001.


b) when "Installing Dovetail Directly" method is used, before to run
the dovetail commands, there is a need to set configuration file and
defcore test cases file


% cd $DOVETAIL_HOME/dovetail

% mkdir userconfig

% cd userconfig

% touch refstack_tempest.conf defcore.txt

% vim refstack_tempest.conf

% vim defcore.txt

recommended way to set refstack_tempest.conf and defcore.txt is
same as above in  "Installing Dovetail Docker Container" method section.



For Defcore test cases manually running method, there is a need to adjust
the compliance_set test suite,

for dovetail, defcore.tc001.yml and defcore.tc002.yml are used for automatic
and manual running method, respectively.



% cd $DOVETAIL_HOME/dovetail/compliance

% vim CVP_1_0_0.yml


to add defcore.tc002 and annotate defcore.tc001

3 Dovetail Client CLI Manual

This section contains a brief manual for all the features available through the Dovetail client command line interface (CLI).
3.1 Check dovetail commands

% dovetail -h

dovetail.PNG

Dovetail has three commands: list, run and show.
6.2 List
6.2.1 List help

% dovetail list -h

list-help.PNG
6.2.2 List a test suite

List command will list all test cases belong to the given test suite.

% dovetail list compliance_set

list-compliance.PNG

% dovetail list debug

list-debug.PNG

The ipv6, example and nfvi are test areas. If no <TESTSUITE> is given, it will list all testsuites.
6.3 Show

Show command will give the detailed info of one certain test case.
6.3.1 Show help

% dovetail show -h

show-help.PNG
6.3.2 Show test case

show-ipv6.PNG
6.4 Run

Dovetail supports running a named test suite, or one named test area of a test suite.
6.4.1 Run help

% dovetail run -h

run-help.PNGThere are some options:

func_tag: set FuncTest’s Docker tag, for example stable,latest and danube.1.0

openrc: give the path of OpenStack credential file

yard_tag: set Yardstick’s Docker tag

testarea: set a certain testarea within a certain testsuite

offline: run without pull the docker images, and it requires the jumphost to have these images locally. This will ensure DoveTail run in an offline environment.

report: push results to DB or store with files

testsuite: set the testsuite to be tested

debug: flag to show the debug log messages

