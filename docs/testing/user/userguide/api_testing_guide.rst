.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) OPNFV, Huawei Technologies Co.,Ltd and others.

===============================
Running Dovetail by RESTful API
===============================

Overview
--------

Dovetail framework provides RESTful APIs for end users to run all OVP test cases.
Also it provides a Swagger UI for users to find out all APIs and try them out.


Definitions and abbreviations
-----------------------------

- REST - Representational State Transfer
- API - Application Programming Interface
- OVP - OPNFV Verification Program
- UI - User Interface


Environment Preparation
-----------------------


Install Docker
^^^^^^^^^^^^^^

The main prerequisite software for Dovetail is Docker. Please refer to official
Docker installation guide that is relevant to your Test Host's operating system.


Configuring the Test Host Environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For convenience and as a convention, we will create a home directory for storing
all Dovetail related config items and results files:

.. code-block:: bash

   $ mkdir -p ${HOME}/dovetail
   $ export DOVETAIL_HOME=${HOME}/dovetail


Installing Dovetail API
-----------------------

The Dovetail project maintains a Docker image that has both Dovetail API and
Dovetail CLI preinstalled. This Docker image is tagged with versions.
Before pulling the Dovetail image, check the OPNFV's OVP web page first to
determine the right tag for OVP testing.


Downloading Dovetail Docker Image
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The first version of Dovetail API is ovp-3.0.0.

.. code-block:: bash

   $ sudo docker pull opnfv/dovetail:ovp-3.0.0
   ovp-3.0.0: Pulling from opnfv/dovetail
   6abc03819f3e: Pull complete
   05731e63f211: Pull complete
   0bd67c50d6be: Pull complete
   3f737f5d00b2: Pull complete
   c93fd0792ebd: Pull complete
   77d9a9603ec6: Pull complete
   9463cdd9c628: Pull complete
   Digest: sha256:45e2ffdbe217a4e6723536afb5b6a3785d318deff535da275f34cf8393af458d
   Status: Downloaded newer image for opnfv/dovetail:ovp-3.0.0


Deploying Dovetail API
^^^^^^^^^^^^^^^^^^^^^^

The Dovetail API can be deployed by running a Dovetail container with the Docker
image downloaded before.

.. code-block:: bash

   $ docker run -itd -p <swagger_port>:80 -p <api_port>:5000 --privileged=true \
     -e SWAGGER_HOST=<host_ip>:<api_port> -e DOVETAIL_HOME=/home/ovp \
     -v /home/ovp:/home/ovp -v /var/run/docker.sock:/var/run/docker.sock \
     opnfv/dovetail:<version>


In the container, it uses 2 ports for Swagger UI (port 80) and API (port 5000)
respectively. So in order to access to these 2 services outside the container,
it needs to map them to the host ports. It can be any available ports in the host.

The env SWAGGER_HOST is optional. If you will access the Swagger UI webpage with
the same host deploying this container, there is no need to set SWAGGER_HOST.
Otherwise, if you will access the Swagger UI webpage from other machines, then
it needs to set SWAGGER_HOST.


Using Dovetail API
------------------

Here give the guide of where to find out all APIs and how to use them.


Swagger UI Webpage
^^^^^^^^^^^^^^^^^^

After deploying Dovetail container, the Swagger UI webpage can be accessed with
any browser. The url is ``http://localhost:<swagger_port>/dovetail-api/index.html``
if accessing from the same host as deploying this container. Otherwise, the url
is ``http://<host_ip>:<swagger_port>/dovetail-api/index.html``.


Calling APIs
^^^^^^^^^^^^

There are totally 5 APIs provided by Dovetail.

   * Get all test suites

   * Get all test cases

   * Run test cases

   * Run test cases with execution ID

   * Get status of test cases

Here give some easy guide of how to call these APIs. For more detailed infomation,
please refer to the Swagger UI page.


Getting All Test Suites
=======================

   * This is a **GET** function with no parameter to get all test suites defined
     in Dovetail container.

   * The request URL is ``http://<host_ip>:<api_port>/api/v1/scenario/nfvi/testsuites``.

   * The response body is structured as:

     .. code-block:: bash

        {
          "testsuites": {
            "debug": {
              "name": "debug",
              "testcases_list": {
                "optional": [
                  "functest.vping.userdata"
                ]
              }
            },
            "healthcheck": {
              "name": "healthcheck",
              "testcases_list": {
                "optional": [
                  "functest.healthcheck.connection_check"
                ]
              }
            }
          }
        }


Getting All Test Cases
======================

   * This is a **GET** function without no parameter to get all test cases integrated
     in Dovetail container.

   * The request URL is ``http://<host_ip>:<api_port>/api/v1/scenario/nfvi/testcases``.

   * The response body is structured as:

     .. code-block:: bash

        {
          "testcases": [
            {
              "description": "This test case will verify the high availability of the user service provided by OpenStack (keystone) on control node.",
              "scenario": "nfvi",
              "subTestCase": null,
              "testCaseName": "yardstick.ha.keystone"
            },
            {
              "description": "testing for vping using userdata",
              "scenario": "nfvi",
              "subTestCase": null,
              "testCaseName": "functest.vping.userdata"
            },
            {
              "description": "tempest smoke test cases about volume",
              "scenario": "nfvi",
              "subTestCase": [
                "tempest.api.volume.test_volumes_actions.VolumesActionsTest.test_attach_detach_volume_to_instance[compute,id-fff42874-7db5-4487-a8e1-ddda5fb5288d,smoke]",
                "tempest.scenario.test_volume_boot_pattern.TestVolumeBootPattern.test_volume_boot_pattern[compute,id-557cd2c2-4eb8-4dce-98be-f86765ff311b,image,slow,volume]"
              ],
              "testCaseName": "functest.tempest.volume"
            }
          ]
        }


Running Test Cases
==================

   * This is a **POST** function with some parameters to run a subset of the whole test cases.

   * The request URL is ``http://<host_ip>:<api_port>/api/v1/scenario/nfvi/execution``.

   * The request body is structured as following. The ``conf`` section is used to
     give all configuration items those are required to run test cases. They are
     the same as all configuration files provided under ``$DOVETAIL_HOME/pre_config/``.
     If you already have these files under this directory, the whole ``conf`` section
     can be ignored. If you provide these configuration items with the request body,
     then the corresponding files under ``$DOVETAIL_HOME/pre_config/`` will be ignored
     by Dovetail. The ``testcase``, ``testsuite``, ``testarea`` and ``deploy_scenario``
     correspond to ``--testcase``, ``--testsuite``, ``--testarea`` and ``--deploy-scenario``
     defined with Dovetail CLI. The ``options`` section support to set all options
     which have already been implemented by Dovetail CLI including ``--optional``,
     ``--mandatory``, ``--no-clean``, ``--no-api-validation``, ``--offline``,
     ``--report``, ``--stop`` and ``--debug``. For options list in ``options`` section,
     they are set to be ``True``, otherwise, they are set to be ``False``.

     .. code-block:: bash

        {
          "conf": {
            "vm_images": "/home/ovp/images",
            "pods": {
              "nodes": [
                {
                  "name": "node1",
                  "role": "Controller",
                  "ip": "192.168.117.222",
                  "user": "root",
                  "password": "root",
                }
              ],
              "process_info": [
                {
                  "testcase_name": "yardstick.ha.rabbitmq",
                  "attack_host": "node1",
                  "attack_process": "rabbitmq"
                }
              ]
            },
            "tempest_conf": {
              "compute": {
                "min_compute_nodes": "2",
                "volume_device_name": "vdb",
                "max_microversion": "2.65"
              }
            },
            "hosts": {
              "192.168.141.101": [
                "volume.os.com",
                "compute.os.com"
              ]
            },
            "envs": {
              "OS_USERNAME": "admin",
              "OS_PASSWORD": "admin",
              "OS_AUTH_URL": "https://192.168.117.222:5000/v3",
              "EXTERNAL_NETWORK": "ext-net"
            }
          },
          "testcase": [
            "functest.vping.ssh",
            "yardstick.ha.rabbitmq"
          ],
          "testsuite": "ovp.2019.12",
          "testarea": [
            "vping",
            "ha"
          ],
          "deploy_scenario": "os-nosdn-ovs-ha",
          "options": [
            "debug",
            "report"
          ]
        }


   * The response body is structured as:

     .. code-block:: bash

        {
          "result": [
            {
              "endTime": null,
              "executionId": "a65e24c0-1803-11ea-84f4-0242ac110004",
              "results": null,
              "scenario": "nfvi",
              "status": "IN_PROGRESS",
              "testCaseName": "functest.vping.ssh",
              "testSuiteName": "ovp.2019.12",
              "timestart": null
            }
          ]
        }


Running Test Cases with Execution ID
====================================

   * This is a **POST** function with some parameters to run a subset of
     whole test cases and set the execution ID instead of using the random one.

   * The request URL is ``http://<host_ip>:<api_port>/api/v1/scenario/nfvi/execution/{exec_id}``.

   * It's almost the same as the above running test cases API except the execution ID.


Getting Status of Test Cases
============================

   * This is a **POST** function to get the status of some test cases by using
     the execution ID received in the response body of `Running Test Cases`_ or
     `Running Test Cases with Execution ID`_ APIs.

   * The request URL is ``http://<host_ip>:<api_port>/api/v1/scenario/nfvi/execution/status/{exec_id}``.

   * The request body is structured as:

     .. code-block:: bash

        {
          "testcase": [
            "functest.vping.ssh"
          ]
        }

   * The response body is structured as:

     .. code-block:: bash

        {
          "result": [
            {
              "endTime": "2019-12-06 08:39:23",
              "executionId": "a65e24c0-1803-11ea-84f4-0242ac110004",
              "results": {
                "criteria": "PASS",
                "sub_testcase": [],
                "timestart": "2019-12-06 08:38:40",
                "timestop":"2019-12-06 08:39:23"
              },
              "scenario": "nfvi",
              "status": "COMPLETED",
              "testCaseName": "functest.vping.ssh",
              "testSuiteName": "ovp.2019.12",
              "timestart":"2019-12-06 08:38:40"
            }
          ]
        }




Getting Test Results
^^^^^^^^^^^^^^^^^^^^

Each time you call the running test case API, Dovetail creates a directory with the
execution ID as the name under ``$DOVETAIL_HOME`` to store results on the host.
You can find all result files under ``$DOVETAIL_HOME/<executionId>/results``.
If you run test cases with ``report`` option, then there will be a tarball file
under ``$DOVETAIL_HOME/<executionId>`` which can be upload to OVP portal.
