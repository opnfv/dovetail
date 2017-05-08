.. This work is licensed under a Creative Commons Attribution 4.0 International
.. License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) OPNFV, China Mobile and others.

=====================
HA test specification
=====================

.. toctree::
   :maxdepth: 2

Scope
=====

The HA test area evaluates the ability of the system under test to support high
availability.

The tests in this suite will evaluate killing the processes of a specific
Openstack service on a selected control node, then checks whether the request
of the related Openstack command is OK and the killed processes are recovered.

References
================

This test suite assumes support for the following specifications:

- ETSI GS NFV-REL 001

  - http://www.etsi.org/deliver/etsi_gs/NFV-REL/001_099/001/01.01.01_60/gs_nfv-rel001v010101p.pdf

Definitions and abbreviations
=============================

The following terms and abreviations are used in conjunction with this test
suite

- attackers - tools used to inject fault into the SUT
- monitors - tools used to evaluate the SUT performance
- service_outage_time - the outage time (seconds) of the specified Openstack
  command request
- process_recover_time - the time (seconds) from the specified process being
  killed to recovered
- SLA - Service level agreement

System Under Test (SUT)
=======================

The system under test is assumed to be the NFVi in operation on an Pharos
compliant infrastructure.

Test Suite Structure
====================

The HA test suite is structured with the following test cases in a sequence manner.

Test Descriptions
=================

------------------------------------------------------------
Test Case 1 - Control node Openstack service down - nova-api
------------------------------------------------------------

Use case specification
----------------------

This test verifies the high availability of the nova-api service provided by
OpenStack on control node. This test case kills the processes of Openstack
nova-api service on a selected control node, then checks whether the request of
the related Openstack command is OK and the killed processes are recovered.

Test preconditions
------------------

One controller node is available, denoted as Node1 in the following.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

* Test action 1: Connect the Node1 through SSH, and checked the target "nova-api" processes are running on Node1
* Test action 2: Start two monitors: one for "nova-api" process and one for "openstack image list" command.
  Each monitor will run with independently process
* Test action 3: Connect the Node1 through SSH, and then execute the kill process script with param value "nova-api"
* Test action 4: Stop monitors after a period of time specified by "monitor_time"
* Test action 5: Verify the SLA, test passes if the SLA passes
* Test action 6: Check the status of the "nova-api" process on Node1, and restart the process if it is not running for next test cases

The pass criteria for this test case is that all instructions are able to be
carried out according to the described behaviour without deviation, the
killed "nova-api" processes are able to recover within the max_recover_time,
and the outage time of the "openstack image list" command request is shorter
than the max_outage_time.

A negative result will be generated if the above is not met in completion.

Post conditions
---------------

No impact on the SUT.


------------------------------------------------------------------
Test Case 2 - Control node Openstack service down - neutron-server
------------------------------------------------------------------

Use case specification
----------------------

This test verifies the high availability of the neutron-server service provided
by OpenStack on control node. This test case kills the processes of Openstack
neutron-server service on a selected control node, then checks whether the
request of the related Openstack command is OK and the killed processes are
recovered.

Test preconditions
------------------

One controller node is available, denoted as Node1 in the following.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

* Test action 1: Connect the Node1 through SSH, and checked the target "neutron-server" processes are running on Node1
* Test action 2: Start two monitors: one for "neutron-server" process and one for "openstack router list" command.
  Each monitor will run with independently process.
* Test action 3: Connect the Node1 through SSH, and then execute the kill process script with param value "neutron-server"
* Test action 4: Stop monitors after a period of time specified by "monitor_time"
* Test action 5: Verify the SLA, test passes if the SLA passes
* Test action 6: Check the status of the "neutron-server" process on Node1, and restart the process if it is not running for next test cases

The pass criteria for this test case is that all instructions are able to be
carried out according to the described behaviour without deviation, the
killed "neutron-server" processes are able to recover within the
max_recover_time, and the outage time of the "openstack router list" command
request is shorter than the max_outage_time.

A negative result will be generated if the above is not met in completion.

Post conditions
---------------

No impact on the SUT.


------------------------------------------------------------
Test Case 3 - Control node Openstack service down - keystone
------------------------------------------------------------

Use case specification
----------------------

This test verifies the high availability of the keystone service provided by
OpenStack on control node. This test case kills the processes of Openstack
keystone service on a selected control node, then checks whether the request of
the related Openstack command is OK and the killed processes are recovered.

Test preconditions
------------------

One controller node is available, denoted as Node1 in the following.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

* Test action 1: Connect the Node1 through SSH, and checked the target "keystone" processes are running on Node1
* Test action 2: Start two monitors: one for "keystone" process and one for "openstack user list" command.
  Each monitor will run with independently process.
* Test action 3: Connect the Node1 through SSH, and then execute the kill process script with param value "keystone"
* Test action 4: Stop monitors after a period of time specified by "monitor_time"
* Test action 5: Verify the SLA, test passes if the SLA passes
* Test action 6: Check the status of the "keystone" process on Node1, and restart the process if it is not running for next test cases

The pass criteria for this test case is that all instructions are able to be
carried out according to the described behaviour without deviation, the
killed "keystone" processes are able to recover within the max_recover_time,
and the outage time of the "openstack user list" command request is shorter
than the max_outage_time.

A negative result will be generated if the above is not met in completion.

Post conditions
---------------

No impact on the SUT.


--------------------------------------------------------------
Test Case 4 - Control node Openstack service down - glance-api
--------------------------------------------------------------

Use case specification
----------------------

This test verifies the high availability of the glance-api service provided by
OpenStack on control node. This test case kills the processes of Openstack
glance-api service on a selected control node, then checks whether the request
of the related Openstack command is OK and the killed processes are recovered.

Test preconditions
------------------

One controller node is available, denoted as Node1 in the following.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

* Test action 1: Connect the Node1 through SSH, and checked the target "glance-api" processes are running on Node1
* Test action 2: Start two monitors: one for "glance-api" process and one for "openstack image list" command.
  Each monitor will run with independently process.
* Test action 3: Connect the Node1 through SSH, and then execute the kill process script with param value "glance-api"
* Test action 4: Stop monitors after a period of time specified by "monitor_time"
* Test action 5: Verify the SLA, test passes if the SLA passes
* Test action 6: Check the status of the "glance-api" process on Node1, and restart the process if it is not running for next test cases

The pass criteria for this test case is that all instructions are able to be
carried out according to the described behaviour without deviation, the
killed "glance-api" processes are able to recover within the max_recover_time,
and the outage time of the "openstack image list" command request is shorter
than the max_outage_time.

A negative result will be generated if the above is not met in completion.

Post conditions
---------------

No impact on the SUT.


--------------------------------------------------------------
Test Case 5 - Control node Openstack service down - cinder-api
--------------------------------------------------------------

Use case specification
----------------------

This test verifies the high availability of the cinder-api service provided by
OpenStack on control node. This test case kills the processes of Openstack
cinder-api service on a selected control node, then checks whether the request
of the related Openstack command is OK and the killed processes are recovered.

Test preconditions
------------------

One controller node is available, denoted as Node1 in the following.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------


* Test action 1: Connect the Node1 through SSH, and checked the target "cinder-api" processes are running on Node1
* Test action 2: Start two monitors: one for "cinder-api" process and one for "openstack volume list" command.
  Each monitor will run with independently process.
* Test action 3: Connect the Node1 through SSH, and then execute the kill process script with param value "cinder-api"
* Test action 4: Stop monitors after a period of time specified by "monitor_time"
* Test action 5: Verify the SLA, test passes if the SLA passes
* Test action 6: Check the status of the "cinder-api" process on Node1, and restart the process if it is not running for next test cases

The pass criteria for this test case is that all instructions are able to be
carried out according to the described behaviour without deviation, the
killed "cinder-api" processes are able to recover within the max_recover_time,
and the outage time of the "openstack volume list" command request is shorter
than the max_outage_time.

A negative result will be generated if the above is not met in completion.

Post conditions
---------------

No impact on the SUT.


----------------------------------------------------------------------
Test Case 6 - OpenStack Controller Node CPU Overload High Availability
----------------------------------------------------------------------

Use case specification
----------------------

This test verifies the high availability of control node. When the CPU usage of
a specified controller node is stressed to 100%, which breaks down the
Openstack services on this node. These Openstack service should able to be
accessed by other controller nodes, and the services on failed controller node
should be isolated.This test case stresses the CPU uasge of a specified control
node to 100%, then checks whether all services provided by the environment are
OK with some monitor tools.

Test preconditions
------------------

One controller node is available, denoted as Node1 in the following.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

* Test action 1: Start four monitors: one for "openstack image list" command,
  one for "openstack router list" command, one for "openstack stack list" command
  and one for "openstack volume list" command. Each monitor will run with independently process.
* Test action 2: Connect the Node1 through SSH, and then execute the stress cpu script on Node1
* Test action 3: Stop monitors after a period of time specified by "monitor_time"
* Test action 4: Verify the SLA, test passes if the SLA passes
* Test action 5: Kill the process that stresses the CPU usage

The pass criteria for this test case is that all instructions are able to be
carried out according to the described behaviour without deviation, and the
outage time of the "openstack image list", "openstack router list",
"openstack stack list", "openstack volume list" command request is shorter than
the max_outage_time.

A negative result will be generated if the above is not met in completion.

Post conditions
---------------

No impact on the SUT.


------------------------------------------------------------------------
Test Case 7 - OpenStack Controller Node Disk I/O Block High Availability
------------------------------------------------------------------------

Use case specification
----------------------

This test verifies the high availability of control node. When the disk I/O of
a specified disk is blocked, which breaks down the Openstack services on this
node. Read and write services should still be accessed by other controller
nodes, and the services on failed controller node should be isolated. This test
case blocks the disk I/O of a specified control node, then checks whether the
services that need to read or wirte the disk of the control node are OK with
some monitor tools.

Test preconditions
------------------

One controller node is available, denoted as Node1 in the following.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

* Test action 1: Connect the Node1 through SSH, and then execute the block disk I/O script on Node1.
* Test action 2: Start a monitor: for "openstack flavor list" command
* Test action 3: Create a flavor called "test-001"
* Test action 4: Execute the result checker script to check whether the flavor "test-001" is created
* Test action 5: Stop monitors after a period of time specified by "monitor_time"
* Test action 6: Verify the SLA, test passes if the SLA passes
* Test action 7: Excutes the release disk I/O script to release the blocked I/O and delete the created "test-001" flavor

The pass criteria for this test case is that all instructions are able to be
carried out according to the described behaviour without deviation, and the
flavor "test-001" is created successfully, outage time of the "openstack flaovr
list" command request is shorter than the max_outage_time.

A negative result will be generated if the above is not met in completion.

Post conditions
---------------

No impact on the SUT.


-------------------------------------------------------------------------
Test Case 8 - OpenStack Controller Load Balance Service High Availability
-------------------------------------------------------------------------

Use case specification
----------------------

This test verifies the high availability of the load balance service(current is
HAProxy) that supports OpenStack on controller node. When the load balance
service of a specified controller node is killed, whether other load balancers
on other controller nodes will work, and whether the controller node will
restart the load balancer are checked. This test case kills the processes of
load balance service on a selected control node, then checks whether the
request of the related Openstack command is OK and the killed processes are
recovered.

Test preconditions
------------------

One controller node is available, denoted as Node1 in the following.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

* Test action 1: Connect the Node1 through SSH, and checked the target "haproxy" processes are running on Node1
* Test action 2: Start two monitors: one for "haproxy" process and one for "openstack image list" command.
  Each monitor will run with independently process.
* Test action 3: Connect the Node1 through SSH, and then execute the kill process script with param value "haproxy"
* Test action 4: Stop monitors after a period of time specified by "monitor_time"
* Test action 5: Verify the SLA, test passes if the SLA passes
* Test action 6: Check the status of the "haproxy" process on Node1, and restart the process if it is not running for next test cases.

The pass criteria for this test case is that all instructions are able to be
carried out according to the described behaviour without deviation, the
killed "haproxy" processes are able to recover within the max_recover_time,
and the outage time of the "openstack image list" command request is shorter
than the max_outage_time.

A negative result will be generated if the above is not met in completion.

Post conditions
---------------

No impact on the SUT.