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
| dovetail run                                                           | Run Dovetail with all test areas within default test suite "compliance_set"                       |
|                                                                        |                                                                                                   |
+------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------+
| dovetail run --testsuite <test_suite_name>                             | Run Dovetail with all test areas within test suite <test_suite_name>                              |
|                                                                        |                                                                                                   |
+------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------+
| dovetail run --testsuite <test_suite_name> --testarea <test_area_name> | Run Dovetail with test area <test_area_name> within test suite <test_suite_name>.                 |
|                                                                        | Test area can be chosen from (mandatory, optional, osinterop, ha, vping, ipv6, tempest, sdnvpn).  |
|                                                                        | Repeat option to set multiple test areas.                                                         |
|                                                                        |                                                                                                   |
+------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------+
| dovetail run --debug | -d                                              | Run Dovetail with a debug mode and show all debug logs                                            |
|                                                                        |                                                                                                   |
+------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------+
| dovetail run --offline                                                 | Run Dovetail offline, use local docker images and will not update them                            |
|                                                                        |                                                                                                   |
+------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------+
| dovetail run --report | -r <db_url>                                    | Push results to local or official DB                                                              |
|                                                                        |                                                                                                   |
+------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------+
| dovetail run --yardstick_tag | -y <yardstick_docker_image_tag>         | Specify yardstick's docker image tag                                                              |
|                                                                        |                                                                                                   |
+------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------+
| dovetail run --functest_tag | -f <functest_docker_image_tag>           | Specify functest's docker image tag                                                               |
|                                                                        |                                                                                                   |
+------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------+
| dovetail run --bottlenecks_tag | -b <bottlenecks_docker_image_tag>     | Specify bottlenecks' docker image tag                                                             |
|                                                                        |                                                                                                   |
+------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------+
| dovetail run --vnf_tag | -v <vnftest_docker_image_tag>                 | Specify vnftest's docker image tag, default is beijing.0                                          |
|                                                                        |                                                                                                   |
+------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------+
| dovetail run --deploy-scenario <deploy_scenario_name>                  | Specify the deploy scenario having as project name 'ovs'                                          |
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
   dovetail, version 0.7.0

Dovetail List Commands
----------------------

.. code-block:: bash

   root@1f230e719e44:~/dovetail/dovetail# dovetail list --help
   Usage: dovetail list [OPTIONS] [TESTSUITE]

     list the testsuite details

   Options:
     -h, --help  Show this message and exit.

.. code-block:: bash

   root@1f230e719e44:~/dovetail/dovetail# dovetail list debug
   - example
       dovetail.example.tc002
   - osinterop
       dovetail.osinterop.tc001
   - vping
       dovetail.vping.tc001
       dovetail.vping.tc002

Dovetail Show Commands
----------------------

.. code-block:: bash

   root@1f230e719e44:~/dovetail/dovetail# dovetail show --help
   Usage: dovetail show [OPTIONS] TESTCASE

     show the testcases details

   Options:
     -h, --help  Show this message and exit.

.. code-block:: bash

   root@1f230e719e44:~/dovetail/dovetail# dovetail show dovetail.vping.tc001
   ---
   dovetail.vping.tc001:
     name: dovetail.vping.tc001
     objective: testing for vping using userdata
     validate:
       type: functest
       testcase: vping_userdata
     report:
       sub_testcase_list:

.. code-block:: bash

   root@1f230e719e44:~/dovetail/dovetail# dovetail show ipv6.tc001
   ---
   dovetail.ipv6.tc001:
     name: dovetail.ipv6.tc001
     objective: Bulk creation and deletion of IPv6 networks, ports and subnets
     validate:
       type: functest
       testcase: tempest_custom
       pre_condition:
         - 'cp /home/opnfv/userconfig/pre_config/tempest_conf.yaml /usr/local/lib/python2.7/dist-packages/functest/opnfv_tests/openstack/tempest/custom_tests/tempest_conf.yaml'
       pre_copy:
         src_file: tempest_custom.txt
         dest_path: /usr/local/lib/python2.7/dist-packages/functest/opnfv_tests/openstack/tempest/custom_tests/test_list.txt
     report:
       sub_testcase_list:
         - tempest.api.network.test_networks.BulkNetworkOpsIpV6Test.test_bulk_create_delete_network[id-d4f9024d-1e28-4fc1-a6b1-25dbc6fa11e2,smoke]
         - tempest.api.network.test_networks.BulkNetworkOpsIpV6Test.test_bulk_create_delete_port[id-48037ff2-e889-4c3b-b86a-8e3f34d2d060,smoke]
         - tempest.api.network.test_networks.BulkNetworkOpsIpV6Test.test_bulk_create_delete_subnet[id-8936533b-c0aa-4f29-8e53-6cc873aec489,smoke]

Dovetail Run Commands
----------------------

.. code-block:: bash

   root@1f230e719e44:~/dovetail/dovetail# dovetail run --help
   Usage: run.py [OPTIONS]

   Dovetail compliance test entry!

   Options:
   -b, --bott_tag TEXT     Overwrite tag for bottlenecks docker container (e.g. cvp.0.4.0)
   -f, --func_tag TEXT     Overwrite tag for functest docker container (e.g. cvp.0.5.0)
   -y, --yard_tag TEXT     Overwrite tag for yardstick docker container (e.g. danube.3.2)
   --deploy-scenario TEXT  Specify the DEPLOY_SCENARIO which will be used as input by each testcase respectively
   --testarea TEXT         compliance testarea within testsuite
   --offline               run in offline method, which means not to update the docker upstream images, functest, yardstick, etc.
   -r, --report TEXT       push results to DB (e.g. --report http://192.168.135.2:8000/api/v1/results)
   --testsuite TEXT        compliance testsuite.
   -d, --debug             Flag for showing debug log on screen.
   -h, --help              Show this message and exit.

.. code-block:: bash

   root@1f230e719e44:~/dovetail/dovetail# dovetail run --testsuite proposed_tests --testarea vping --offline -r http://192.168.135.2:8000/api/v1/results --deploy-scenario os-nosdn-ovs-ha
   2017-10-12 14:57:51,278 - run - INFO - ================================================
   2017-10-12 14:57:51,278 - run - INFO - Dovetail compliance: proposed_tests!
   2017-10-12 14:57:51,278 - run - INFO - ================================================
   2017-10-12 14:57:51,278 - run - INFO - Build tag: daily-master-b80bca76-af5d-11e7-879a-0242ac110002
   2017-10-12 14:57:51,278 - run - INFO - DEPLOY_SCENARIO : os-nosdn-ovs-ha
   2017-10-12 14:57:51,336 - run - WARNING - There is no hosts file /home/jenkins/opnfv/slave_root/workspace/dovetail-compass-huawei-pod7-proposed_tests-danube/cvp/pre_config/hosts.yaml, may be some issues with domain name resolution.
   2017-10-12 14:57:51,517 - run - INFO - >>[testcase]: dovetail.vping.tc001
   2017-10-12 14:58:21,325 - run - INFO - Results have been pushed to database and stored with local file /home/dovetail/results/results.json.
   2017-10-12 14:58:21,337 - run - INFO - >>[testcase]: dovetail.vping.tc002
   2017-10-12 14:58:48,862 - run - INFO - Results have been pushed to database and stored with local file /home/dovetail/results/results.json.
