.. This work is licensed under a Creative Commons Attribution 4.0 International
.. License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) OPNFV, Huawei Technologies Co.,Ltd and others.

================================
Dovetail Command-line Interface
================================


Command Line Introduction
==========================

Dovetail command-line interface is supported, for help on the **dovetail** command, enter:

::

  dovetail --help

**dovetail** optional arguments:

::

  --version
      show program's version number and exit
  list <testsuite_name>
      list the testsuite details
  show <testcase_name>
      show the testsuite details
  run <arguments>
      run the testcases

- for **dovetail list**, if the <testsuite_name> ommitted,
all the testsuites defined under /dovetail/compliance directory
and related testcases will be listed, otherwise,
the testsuite's testarea and testcases are listed.
- for **dovetail show**, the <testcase_name> is required, the contents defined
in <testcase_name>.yml is shown.
- for **dovetail run**, by running ``dovetail run --help``, the ``dovetail run``
usage is shown as

+------------------------+-----------------------------------------------------+
|Options                 |                                                     |
+========================+=====================================================+
| -t, --SUT_TYPE         |Installer type of the system under test (SUT).       |
+------------------------+-----------------------------------------------------+
| --creds                |Openstack Credential file location                   |
+------------------------+-----------------------------------------------------+
| -i, --SUT_IP           |IP of the system under test (SUT).                   |
+------------------------+-----------------------------------------------------+
| -d, --debug            |True for showing debug log on screen.                |
+------------------------+-----------------------------------------------------+
| -f, --func_tag         |Overwrite tag for functest docker container (e.g.    |
|                        |stable or latest)                                    |
+------------------------+-----------------------------------------------------+
| -y, --yard_tag         |Overwrite tag for yardstick docker container (e.g.   |
|                        |stable or latest)                                    |
+------------------------+-----------------------------------------------------+
| --testarea             |compliance testarea within testsuite                 |
+------------------------+-----------------------------------------------------+
| --testsuite            |compliance testsuite.                                |
+------------------------+-----------------------------------------------------+
|  -h, --help            |Show this message and exit.                          |
+------------------------+-----------------------------------------------------+

if no arguments is given, the default testsuite will be performed, i.e., the ``compliance_set``
testsuite with default configurations.

For more information about **dovetail** command line, please refer to the wiki page [3]_

Parameters defination with config file
======================================

The default **dovetail run** parameters can be modified in
``dovetail/dovetail/conf/cmd_config.yml``, which is shown as:

::

  cli:
    arguments:
      config:
        # This is a simple example of arguments.
        # Dovetail has no need of this kind of parameters currently.
        # The arguments must be given orderly at the run-time.
        #
        # docker_tag:
        #   flags: 'docker_tag'
        #   path:
        #     - 'functest/docker_tag'
        #     - 'yardstick/docker_tag'
      control:

    options:
      config:
        SUT_TYPE:
          flags:
            - '--SUT_TYPE'
            - '-t'
          path:
            - 'functest/envs'
            - 'yardstick/envs'
          help: 'Installer type of the system under test (SUT).'
        yard_tag:
          flags:
            - '--yard_tag'
            - '-y'
          path:
            - 'yardstick/docker_tag'
          help: 'Overwrite tag for yardstick docker container (e.g. stable or latest)'
        func_tag:
          flags:
            - '--func_tag'
            - '-f'
          path:
            - 'functest/docker_tag'
          help: 'Overwrite tag for functest docker container (e.g. stable or latest)'
      control:
        testsuite:
          flags:
            - '--testsuite'
          default: 'compliance_set'
          help: 'compliance testsuite.'
        testarea:
          flags:
            - '--testarea'
          default: 'full'
          help: 'compliance testarea within testsuite'

Click module is used to parse parameters defined in the above
config file, two subsections are included in this file,
**arguments** and **options**, which corresponds to two types of parameters in click.

Arguments and Options
+++++++++++++++++++++
Only **options** is used now, which means parameters can be given or not without
sequence restriction.

Config and control
++++++++++++++++++

All options/arguments are divided into two parts: **config** and **control**.
The config ones are used for updating functest or yardstick config files according
to the **path** given.  For example, functest's config file is
``dovetail/dovetail/conf/functest_config.yml``, following is a simple example:

::

  docker_tag: latest
  envs: '-e INSTALLER_TYPE=compass -e INSTALLER_IP=192.168.200.2
         -e NODE_NAME=dovetail-pod -e DEPLOY_SCENARIO=ha_nosdn
         -e BUILD_TAG=dovetail -e CI_DEBUG=true -e DEPLOY_TYPE=baremetal'

If running with the command ``python run.py --SUT_TYPE fuel -f stable``, then
the configs will be changed into

::

  docker_tag: stable
  envs: '-e INSTALLER_TYPE=fuel -e INSTALLER_IP=192.168.200.2
         -e NODE_NAME=dovetail-pod -e DEPLOY_SCENARIO=ha_nosdn
         -e BUILD_TAG=dovetail -e CI_DEBUG=true -e DEPLOY_TYPE=baremetal'

The config options/arguments can be added or deleted by modifying
``cmd_config.yml`` rather than changing the source code. However, for control
command, besides adding it into ``cmd_config.yml``, some other operations about
the source code are also needed.


. [3] https://wiki.opnfv.org/display/dovetail/Dovetail+Command+Line
