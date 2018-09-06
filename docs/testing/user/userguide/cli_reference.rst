.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) OPNFV

.. _cli-reference:

=========================================
Dovetail Command Line Interface Reference
=========================================

Dovetail command line is to have a simple command line interface in Dovetail to
make easier for users to handle the functions that dovetail framework provides.

Commands List
=============

+------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------+
| Commands                                                               | Action                                                                                            |
|                                                                        |                                                                                                   |
+========================================================================+===================================================================================================+
| dovetail --help | -h                                                   | Show usage of command "dovetail"                                                                  |
|                                                                        |                                                                                                   |
+------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------+
| dovetail --version                                                     | Show version number                                                                               |
|                                                                        |                                                                                                   |
+------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------+
| **Dovetail List Commands**                                                                                                                                                 |
|                                                                                                                                                                            |
+------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------+
| dovetail list --help | -h                                              | Show usage of command "dovetail list"                                                             |
|                                                                        |                                                                                                   |
+------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------+
| dovetail list                                                          | List all available test suites and all test cases within each test suite                          |
|                                                                        |                                                                                                   |
+------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------+
| dovetail list <test_suite_name>                                        | List all available test areas within test suite <test_suite_name>                                 |
|                                                                        |                                                                                                   |
+------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------+
| **Dovetail Show Commands**                                                                                                                                                 |
|                                                                                                                                                                            |
+------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------+
| dovetail show --help | -h                                              | Show usage of command "dovetail show"                                                             |
|                                                                        |                                                                                                   |
+------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------+
| dovetail show <test_case_name>                                         | Show the details of one test case                                                                 |
|                                                                        |                                                                                                   |
+------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------+
| **Dovetail Run Commands**                                                                                                                                                  |
|                                                                                                                                                                            |
+------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------+
| dovetail run --help | -h                                               | Show usage of command "dovetail run"                                                              |
|                                                                        |                                                                                                   |
+------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------+
| dovetail run                                                           | Run Dovetail with all test cases within default test suite                                        |
|                                                                        |                                                                                                   |
+------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------+
| dovetail run --testsuite <test_suite_name>                             | Run Dovetail with all test cases within test suite <test_suite_name>                              |
|                                                                        |                                                                                                   |
+------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------+
| dovetail run --testsuite <test_suite_name> --testarea <test_area_name> | Run Dovetail with test area <test_area_name> within test suite <test_suite_name>.                 |
|                                                                        | Test area can be chosen from (vping, tempest, security, ha, stress, bgpvpn, vnf, snaps).          |
|                                                                        | Repeat option to set multiple test areas.                                                         |
|                                                                        |                                                                                                   |
+------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------+
| dovetail run --testcase <test_case_name>                               | Run Dovetail with one or more specified test cases.                                               |
|                                                                        | Repeat option to set multiple test cases.                                                         |
|                                                                        |                                                                                                   |
+------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------+
| dovetail run --mandatory --testsuite <test_suite_name>                 | Run Dovetail with all mandatory test cases within test suite <test_suite_name>                    |
|                                                                        |                                                                                                   |
+------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------+
| dovetail run --optional --testsuite <test_suite_name>                  | Run Dovetail with all optional test cases within test suite <test_suite_name>                     |
|                                                                        |                                                                                                   |
+------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------+
| dovetail run --debug | -d                                              | Run Dovetail with debug mode and show all debug logs                                              |
|                                                                        |                                                                                                   |
+------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------+
| dovetail run --offline                                                 | Run Dovetail offline, use local docker images instead of download online                          |
|                                                                        |                                                                                                   |
+------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------+
| dovetail run --report | -r <db_url>                                    | Package the results directory which can be used to upload to OVP web portal                       |
|                                                                        |                                                                                                   |
+------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------+
| dovetail run --deploy-scenario <deploy_scenario_name>                  | Specify the deploy scenario having as project name 'ovs'                                          |
|                                                                        |                                                                                                   |
+------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------+
| dovetail run --no-api-validation                                       | Disable strict API response validation                                                            |
|                                                                        |                                                                                                   |
+------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------+
| dovetail run --no-clean | -n                                           | Keep all Containers created for debuging                                                          |
|                                                                        |                                                                                                   |
+------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------+
| dovetail run --stop | -s                                               | Stop immediately when one test case failed                                                        |
|                                                                        |                                                                                                   |
+------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------+


Commands Examples
=================

Dovetail Commands
-----------------

.. code-block:: bash

   root@1f230e719e44:~/dovetail/dovetail# dovetail --help
   Usage: dovetail [OPTIONS] COMMAND [ARGS]...

   Options:
     --version   Show the version and exit.
     -h, --help  Show this message and exit.

   Commands:
     list  list the testsuite details
     run   run the testcases
     show  show the testcases details

.. code-block:: bash

   root@1f230e719e44:~/dovetail/dovetail# dovetail --version
   dovetail, version 2018.9.0

Dovetail List Commands
----------------------

.. code-block:: bash

   root@1f230e719e44:~/dovetail/dovetail# dovetail list --help
   Usage: dovetail list [OPTIONS] [TESTSUITE]

     list the testsuite details

   Options:
     -h, --help  Show this message and exit.

.. code-block:: bash

   root@1f230e719e44:~/dovetail/dovetail# dovetail list ovp.2018.09
   - mandatory
       functest.vping.userdata
       functest.vping.ssh
       functest.tempest.osinterop
       functest.tempest.compute
       functest.tempest.identity_v3
       functest.tempest.image
       functest.tempest.network_api
       functest.tempest.volume
       functest.tempest.neutron_trunk_ports
       functest.tempest.ipv6_api
       functest.security.patrole
       yardstick.ha.nova_api
       yardstick.ha.neutron_server
       yardstick.ha.keystone
       yardstick.ha.glance_api
       yardstick.ha.cinder_api
       yardstick.ha.cpu_load
       yardstick.ha.disk_load
       yardstick.ha.haproxy
       yardstick.ha.rabbitmq
       yardstick.ha.database
       bottlenecks.stress.ping
   - optional
       functest.tempest.ipv6_scenario
       functest.tempest.multi_node_scheduling
       functest.tempest.network_security
       functest.tempest.vm_lifecycle
       functest.tempest.network_scenario
       functest.tempest.bgpvpn
       functest.bgpvpn.subnet_connectivity
       functest.bgpvpn.tenant_separation
       functest.bgpvpn.router_association
       functest.bgpvpn.router_association_floating_ip
       yardstick.ha.neutron_l3_agent
       yardstick.ha.controller_restart
       functest.vnf.vims
       functest.vnf.vepc
       functest.snaps.smoke

Dovetail Show Commands
----------------------

.. code-block:: bash

   root@1f230e719e44:~/dovetail/dovetail# dovetail show --help
   Usage: dovetail show [OPTIONS] TESTCASE

     show the testcases details

   Options:
     -h, --help  Show this message and exit.

.. code-block:: bash

   root@1f230e719e44:~/dovetail/dovetail# dovetail show functest.vping.ssh
   ---
   functest.vping.ssh:
     name: functest.vping.ssh
     objective: testing for vping using ssh
     validate:
       type: functest
       testcase: vping_ssh
     report:
       source_archive_files:
         - functest.log
       dest_archive_files:
         - vping_logs/functest.vping.ssh.log
       check_results_file: 'functest_results.txt'
       sub_testcase_list:

.. code-block:: bash

   root@1f230e719e44:~/dovetail/dovetail# dovetail show functest.tempest.image
   ---
   functest.tempest.image:
     name: functest.tempest.image
     objective: tempest smoke test cases about image
     validate:
       type: functest
       testcase: tempest_custom
       pre_condition:
         - 'cp /home/opnfv/userconfig/pre_config/tempest_conf.yaml /usr/lib/python2.7/site-packages/functest/opnfv_tests/openstack/tempest/custom_tests/tempest_conf.yaml'
         - 'cp /home/opnfv/userconfig/pre_config/testcases.yaml /usr/lib/python2.7/site-packages/xtesting/ci/testcases.yaml'
       pre_copy:
         src_file: tempest_custom.txt
         dest_path: /usr/lib/python2.7/site-packages/functest/opnfv_tests/openstack/tempest/custom_tests/test_list.txt
     report:
       source_archive_files:
         - functest.log
         - tempest_custom/tempest.log
         - tempest_custom/tempest-report.html
       dest_archive_files:
         - tempest_logs/functest.tempest.image.functest.log
         - tempest_logs/functest.tempest.image.log
         - tempest_logs/functest.tempest.image.html
       check_results_file: 'functest_results.txt'
       sub_testcase_list:
         - tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_register_upload_get_image_file[id-139b765e-7f3d-4b3d-8b37-3ca3876ee318,smoke]
         - tempest.api.image.v2.test_versions.VersionsTest.test_list_versions[id-659ea30a-a17c-4317-832c-0f68ed23c31d,smoke]

Dovetail Run Commands
----------------------

.. code-block:: bash

   root@1f230e719e44:~/dovetail/dovetail# dovetail run --help
   Usage: run.py [OPTIONS]

   Dovetail compliance test entry!

   Options:
   --deploy-scenario TEXT  Specify the DEPLOY_SCENARIO which will be used as input by each testcase respectively
   --optional              Run all optional test cases.
   --offline               run in offline method, which means not to update the docker upstream images, functest, yardstick, etc.
   -r, --report            Create a tarball file to upload to OVP web portal
   -d, --debug             Flag for showing debug log on screen.
   --testcase TEXT         Compliance testcase. Specify option multiple times to include multiple test cases.
   --testarea TEXT         Compliance testarea within testsuite. Specify option multiple times to include multiple test areas.
   -s, --stop              Flag for stopping on test case failure.
   -n, --no-clean          Keep all Containers created for debuging.
   --no-api-validation     disable strict API response validation
   --mandatory             Run all mandatory test cases.
   --testsuite TEXT        compliance testsuite.
   -h, --help              Show this message and exit.

.. code-block:: bash

   root@1f230e719e44:~/dovetail/dovetail# dovetail run --testcase functest.vping.ssh --offline -r --deploy-scenario os-nosdn-ovs-ha
   2017-10-12 14:57:51,278 - run - INFO - ================================================
   2017-10-12 14:57:51,278 - run - INFO - Dovetail compliance: ovp.2018.09!
   2017-10-12 14:57:51,278 - run - INFO - ================================================
   2017-10-12 14:57:51,278 - run - INFO - Build tag: daily-master-b80bca76-af5d-11e7-879a-0242ac110002
   2017-10-12 14:57:51,278 - run - INFO - DEPLOY_SCENARIO : os-nosdn-ovs-ha
   2017-10-12 14:57:51,336 - run - WARNING - There is no hosts file /home/dovetail/pre_config/hosts.yaml, may be some issues with domain name resolution.
   2017-10-12 14:57:51,336 - run - INFO - Get hardware info of all nodes list in file /home/cvp/pre_config/pod.yaml ...
   2017-10-12 14:57:51,336 - run - INFO - Hardware info of all nodes are stored in file /home/cvp/results/all_hosts_info.json.
   2017-10-12 14:57:51,517 - run - INFO - >>[testcase]: functest.vping.ssh
   2017-10-12 14:58:21,325 - report.Report - INFO - Results have been stored with file /home/cvp/results/functest_results.txt.
   2017-10-12 14:58:21,325 - report.Report - INFO -

   Dovetail Report
   Version: 2018.09
   Build Tag: daily-master-b80bca76-af5d-11e7-879a-0242ac110002
   Test Date: 2018-08-13 03:23:56 UTC
   Duration: 291.92 s

   Pass Rate: 0.00% (1/1)
   vping:                     pass rate 100%
   -functest.vping.ssh        PASS
