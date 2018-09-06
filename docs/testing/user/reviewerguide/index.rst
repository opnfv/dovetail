.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Ericsson AB

=============================================
OVP Reviewer Guide
=============================================

.. toctree::
   :maxdepth: 2


Introduction
============

This document provides detailed guidance for reviewers on how to handle the result review
process.

The OPNFV Verified program (OVP) provides the ability for users to upload test results in
`OVP portal <https://verified.opnfv.org>`_ and request from OVP community to review them.
After the user submit for review the test results **Status** is changed from 'private' to 'review'
(as shown in figure 2).

OVP administrator will ask for review volunteers using the verified@opnfv.org email alias.
The incoming results for review will be identified by the administrator with particular **Test ID**
and **Owner** values.

Volunteers that will accept the review request can access the test results by login to the
`OVP portal <https://verified.opnfv.org>`_ and the click on the **My Results** tab in top-level
navigation bar.

.. image:: images/ovp_top_nav.png
    :align: center
    :scale: 100%

Figure 1

The corresponding OVP portal result will have a status of 'review'.

.. image:: images/ovp_result_review.png
    :align: center
    :scale: 100%

Figure 2

Reviewers must follow the checklist below to ensure review consistency for the OPNFV
Verified Program (OVP) 2018.09 (Fraser) release at a minimum.

#. **Mandatory Test Area Results** - Validate that results for all mandatory test areas are present.
#. **Test-Case Pass Percentage** - Ensure all tests have passed (100% pass rate).
#. **Log File Verification** - Inspect the log file for each test area.
#. **SUT Info Verification** - Validate the system under test (SUT) hardware and software endpoint info is present.



1. Mandatory Test Area Results
==============================

Test results can be displayed by clicking on the hyperlink under the 'Test ID' column.
User should validate that results for all mandatory test areas are included in the overall test suite. The required
mandatory test cases are:

- functest.vping.userdata
- functest.vping.ssh
- bottlenecks.stress.ping
- functest.tempest.osinterop
- functest.tempest.compute
- functest.tempest.identity_v3
- functest.tempest.image
- functest.tempest.network_api
- functest.tempest.volume
- functest.tempest.neutron_trunk_ports
- functest.tempest.ipv6_api
- functest.security.patrole
- yardstick.ha.nova_api
- yardstick.ha.neutron_server
- yardstick.ha.keystone
- yardstick.ha.glance_api
- yardstick.ha.cinder_api
- yardstick.ha.cpu_load
- yardstick.ha.disk_load
- yardstick.ha.haproxy
- yardstick.ha.rabbitmq
- yardstick.ha.database

*Note, that the 'Test ID' column in this view condenses the UUID used for 'Test ID' to
eight characters even though the 'Test ID' is a longer UUID in the back-end.*

.. image:: images/ovp_result_overview.png
    :align: center
    :scale: 100%

Figure 3

3. Test-Case Pass Percentage
============================

All mandatory test-cases have to run successfully. The below diagram of the 'Test Run Results' is one method and
shows that 94.39% of the mandatory test-cases have passed.
This value must not be lower than 100%.

.. image:: images/ovp_pass_percentage.png
    :align: center
    :width: 350 px

Figure 4

Failed test cases can also be easy identified by the color of pass/total number. :

- Green when all test-cases pass
- Orange when at least one fails
- Red when all test-cases fail

.. image:: images/ovp_pass_fraction.png
    :align: center
    :width: 350 px

Figure 5

4. Log File Verification
========================

Each log file of the mandatory test cases have to be verified for content.

Log files can be displayed by clicking on the setup icon to the right of the results,
as shown in figure below.

.. image:: images/ovp_log_setup.png
    :align: center
    :scale: 100%

Figure 6

*Note, all log files can be found at results/ directory as shown at the following table.*

+------------------------+--------------------------+
| **Mandatory Test Case**| **Location**             |
+------------------------+--------------------------+
| bottlenecks            | results/stress_logs/     |
+------------------------+--------------------------+
| functest.vping         | results/vping_logs/      |
+------------------------+--------------------------+
| functest.tempest       | results/tempest_logs/    |
+------------------------+--------------------------+
| functest.security      | results/security_logs/   |
+------------------------+--------------------------+
| yardstick              | results/ha_logs/         |
+------------------------+--------------------------+


The bottlenecks log must contain the 'SUCCESS' result as shown in following example:

  2018-08-22 14:11:21,815 [INFO] yardstick.benchmark.core.task task.py:127 Testcase: "ping_bottlenecks" **SUCCESS**!!!

Functest logs opens an html page that lists all test cases as shown in figure 7. All test cases must have run
successfuly.

.. image:: images/ovp_log_files_functest_image.png
    :align: center
    :scale: 100%

Figure 7

For the vping test area log file (functest.log). The two entries displayed in the tables below must be present in
this log file.

**functest.vping_userdata**

.. image:: images/ovp_vping_ssh.png
    :align: center
    :scale: 100%

Figure 8

**functest.vping_ssh**

.. image:: images/ovp_vping_user.png
    :align: center
    :scale: 100%

Figure 9

The yardstick log must contain the 'SUCCESS' result for each of the test-cases within this
test area. This can be verified by searching the log for the keyword 'SUCCESS'.

An example of a FAILED and a SUCCESS test case are listed below:

 2018-08-28 10:25:09,946 [ERROR] yardstick.benchmark.scenarios.availability.monitor.monitor_multi monitor_multi.py:78 SLA **failure**: 14.015082 > 5.000000

 2018-08-28 10:23:41,907 [INFO] yardstick.benchmark.core.task task.py:127 Testcase: "opnfv_yardstick_tc052" **SUCCESS**!!!


5. SUT Info Verification
========================

SUT information must be present in the results to validate that all required endpoint services
and at least two controllers were present during test execution. For the results shown below,
click the '**info**' hyperlink in the **SUT** column to navigate to the SUT information page.

.. image:: images/sut_info.png
    :align: center
    :scale: 100%

Figure 10

In the '**Endpoints**' listing shown below for the SUT VIM component, ensure that services are
present for identify, compute, image, volume and network at a minimum by inspecting the
'**Service Type**' column.

.. image:: images/sut_endpoints.png
    :align: center
    :scale: 100%

Figure 11

Inspect the '**Hosts**' listing found below the Endpoints secion of the SUT info page and ensure
at least two hosts are present, as two controllers are required the for the mandatory HA
test-cases.
