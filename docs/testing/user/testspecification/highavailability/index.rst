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

The HA test area evaluates the ability of the System Under Test to support high
availability of OpenStack controller services.

The tests in this test area will evaluate high availability by killing the
processes of a specific Openstack service, stressing the CPU usage and block
disk I/O on a selected controller node, then check if the related Openstack
service are still accessible through other controller nodes and the killed
processes are recovered on the selected controller node.


References
================

This test area references the following specifications:

- ETSI GS NFV-REL 001

  - http://www.etsi.org/deliver/etsi_gs/NFV-REL/001_099/001/01.01.01_60/gs_nfv-rel001v010101p.pdf


Definitions and abbreviations
=============================

The following terms and abreviations are used in conjunction with this test area

- SUT - System Under Test
- Attackers - tools used to inject fault into the SUT
- Monitors - tools used to evaluate the service outage_time and the process
  outage_time
- Outage_time - the time (seconds) from the specified process being killed to
  recovered
- SLA - Service level agreement
- Max_outage_time - the maximum outage time (seconds) from the specified process
  being killed to recovered to meet SLA


System Under Test (SUT)
=======================

The system under test is assumed to be the NFVi and VIM in operation on a
Pharos compliant infrastructure. The system under test is assumed in High
availability configuration.


Test Area Structure
====================

The HA test area is structured with the following test cases in a sequential
manner.
Preceding test case's failure will not affect the subsequent test cases.
Dependencies of each test case will be introduced in the following test
descriptions.


Test Descriptions
=================

---------------------------------------------------------------
Test Case 1 - Controller node OpenStack service down - nova-api
---------------------------------------------------------------

Short name
----------

opnfv.ha.tc001.nova-api_service_down

Use case specification
----------------------

This test case verifies the high availability of the "nova-api" service provided by
OpenStack controller nodes. It kills the processes of OpenStack "nova-api" service
on a selected controller node, then checks whether the "nova-api" service is still
available by executing command "openstack server list" and the killed processes
are recovered.

Test preconditions
------------------

Three controller nodes are available, denoted as Node1, Node2, Node3 in the
following.
If the high availability of controller nodes is based on active/active, Node1
can be any one of the controller nodes.
If the High availability of controller nodes is based on active/passive, Node1
should be an active controller node.
"nova-api" service is running on Node1.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Methodology for monitoring high availability
''''''''''''''''''''''''''''''''''''''''''''

The high availability of "nova-api" service is evaluated by monitoring service
availability and process outage_time

Service availability is tested by repeatedly executing "openstack server list"
command and checking if the response of the command request is correct. The
command request is executed one by one in loop. When the response fails,
the "nova-api" service is considered in outage.

Process outage_time is tested by checking the status of "nova-api" processes on
the selected controller node. The time of "nova-api" processes being killed to
the time of the "nova-api" processes being recovered is the process outage_time.
Process recovery is verified by checking the existence of "nova-api" processes.

Test execution
''''''''''''''

* Test action 1: Connect to Node1 through SSH, and check that target "nova-api"
  processes are running on Node1
* Test action 2: Start two monitors: one for "nova-api" process and the other
  for "openstack server list" command.
  Each monitor will run as an independent process
* Test action 3: Connect to Node1 through SSH, and then execute the kill_process
  attacker to kill "nova-api" processes
* Test action 4: Calculate the process outage_time of "nova-api" process monitor
* Test action 5: Verify the SLA, process max_recover_time is 20s, test passes if
  the SLA is met
* Test action 6: Check the status of the "nova-api" process on Node1, and restart
  the process if it is not running.

Pass / fail criteria
''''''''''''''''''''

The pass criteria for this test case is that all instructions are able to be
carried out according to the described behavior without deviation, the
killed "nova-api" processes are able to recover within the process
max_outage_time (20s). This max_outage_time (20s) gives the SUT enough time to
recover.

A negative result will be generated if the above is not met in completion.

Post conditions
---------------

No impact on the SUT.


---------------------------------------------------------------------
Test Case 2 - Controller node OpenStack service down - neutron-server
---------------------------------------------------------------------

Short name
----------

opnfv.ha.tc003.neutron-server_service_down

Use case specification
----------------------

This test verifies the high availability of the "neutron-server" service provided
by OpenStack controller nodes. This test case kills the processes of Openstack
"neutron-server" service on a selected controller node, then checks whether
requests of the "openstack router list" command are still processed successfully
and the killed processes are recovered.

Test preconditions
------------------

Three controller nodes are available, denoted as Node1, Node2, Node3 in the
following.
If the high availability is based on active/active, Node1
can be any one of the controller nodes.
If the High availability is based on active/passive, Node1
should be an active controller node.
"neutron-server" service is running on Node1.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Methodology for monitoring high availability
''''''''''''''''''''''''''''''''''''''''''''

The high availability of "neutron-server" service is evaluated by monitoring service
availability and process outage_time

Service availability is tested by repeatedly executing "openstack router list"
command and checking if the response of the command request is correct. The
command request is executed one by one in loop. When the response fails,
the "neutron-server" service is considered in outage.

Process outage_time is tested by checking the status of "neutron-server" processes on
the selected controller node. The time of "neutron-server" processes being killed to
the time of the "neutron-server" processes being recovered is the process outage_time.
Process recovery is verified by checking the existence of "neutron-server" processes.

Test execution
''''''''''''''

* Test action 1: Connect to Node1 through SSH, and check that target "neutron-server"
  processes are running on Node1
* Test action 2: Start two monitors: one for "neutron-server" process and the
  other for "openstack router list" command.
  Each monitor will run as an independent process.
* Test action 3: Connect to Node1 through SSH, and then execute the kill_process
  attacker to kill "neutron-server" processes
* Test action 4: Calculate the process outage_time of "neutron-server" process monitor
* Test action 5: Verify the SLA, process max_recover_time is 20s, test passes
  if the SLA is met
* Test action 6: Check the status of the "neutron-server" process on Node1, and
  restart the process if it is not running

Pass / fail criteria
''''''''''''''''''''

The pass criteria for this test case is that all instructions are able to be
carried out according to the described behavior without deviation, the
killed "neutron-server" processes are able to recover within the process
max_outage_time (20s). This max_outage_time (20s) gives the SUT enough time to
recover.

A negative result will be generated if the above is not met in completion.

Post conditions
---------------

No impact on the SUT.


---------------------------------------------------------------
Test Case 3 - Controller node OpenStack service down - keystone
---------------------------------------------------------------

Short name
----------

opnfv.ha.tc004.keystone_service_down

Use case specification
----------------------

This test verifies the high availability of the "keystone" service provided by
OpenStack controller nodes. This test case kills the processes of Openstack
"keystone" service on a selected controller node, then checks whether the request
of the "openstack user list" command are still processed successfully and the
killed processes are recovered.

Test preconditions
------------------

Three controller nodes are available, denoted as Node1, Node2, Node3 in the
following.
If the high availability is based on active/active, Node1
can be any one of the controller nodes.
If the High availability is based on active/passive, Node1
should be an active controller node.
"keystone" service is running on Node1.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Methodology for monitoring high availability
''''''''''''''''''''''''''''''''''''''''''''

The high availability of "keystone" service is evaluated by monitoring service
availability and process outage_time

Service availability is tested by repeatedly executing "openstack user list"
command and checking if the response of the command request is correct. The
command request is executed one by one in loop. When the response fails,
the "keystone" service is considered in outage.

Process outage_time is tested by checking the status of "keystone" processes on
the selected controller node. The time of "keystone" processes being killed to
the time of the "keystone" processes being recovered is the process outage_time.
Process recovery is verified by checking the existence of "keystone" processes.


Test execution
''''''''''''''

* Test action 1: Connect to Node1 through SSH, and check that target "keystone"
  processes are running on Node1
* Test action 2: Start two monitors: one for "keystone" process and the other
  for "openstack user list" command.
  Each monitor will run as an independent process.
* Test action 3: Connect to Node1 through SSH, and then execute the kill_process
  attacker to kill "keystone" processes
* Test action 4: Calculate the process outage_time of "keystone" process monitor
* Test action 5: Verify the SLA, process max_recover_time is 20s, test passes
  if the SLA is met
* Test action 6: Check the status of the "keystone" process on Node1, and restart
  the process if it is not running for next test cases

Pass / fail criteria
''''''''''''''''''''

The pass criteria for this test case is that all instructions are able to be
carried out according to the described behavior without deviation, the
killed "keystone" processes are able to recover within the process max_outage_time (20s).
This max_outage_time (20s) gives the SUT enough time to
recover.

A negative result will be generated if the above is not met in completion.

Post conditions
---------------

No impact on the SUT.


-----------------------------------------------------------------
Test Case 4 - Controller node OpenStack service down - glance-api
-----------------------------------------------------------------

Short name
----------

opnfv.ha.tc005.glance-api_service_down

Use case specification
----------------------

This test verifies the high availability of the "glance-api" service provided by
OpenStack controller nodes. This test case kills the processes of Openstack
"glance-api" service on a selected controller node, then checks whether the
request of the "openstack image list" command are still processed successfully
and the killed processes are recovered.

Test preconditions
------------------

Three controller nodes are available, denoted as Node1, Node2, Node3 in the
following.
If the high availability is based on active/active, Node1
can be any one of the controller nodes.
If the High availability is based on active/passive, Node1
should be an active controller node.
"glance-api" service is running on Node1.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Methodology for monitoring high availability
''''''''''''''''''''''''''''''''''''''''''''

The high availability of "glance-api" service is evaluated by monitoring service
availability and process outage_time

Service availability is tested by repeatedly executing "openstack image list"
command and checking if the response of the command request is correct. The
command request is executed one by one in loop. When the response fails,
the "glance-api" service is considered in outage.

Process outage_time is tested by checking the status of "glance-api" processes on
the selected controller node. The time of "glance-api" processes being killed to
the time of the "glance-api" processes being recovered is the process outage_time.
Process recovery is verified by checking the existence of "glance-api" processes.

Test execution
''''''''''''''

* Test action 1: Connect to Node1 through SSH, and check that target "glance-api"
  processes are running on Node1
* Test action 2: Start two monitors: one for "glance-api" process and the other
  for "openstack image list" command.
  Each monitor will run as an independent process.
* Test action 3: Connect to Node1 through SSH, and then execute the kill_process
  attacker to kill "glance-api" processes
* Test action 4: Calculate the process outage_time of "glance-api" process monitor
* Test action 5: Verify the SLA, the process max_recover_time is 20s, test passes
  if the SLA is met
* Test action 6: Check the status of the "glance-api" process on Node1, and
  restart the process if it is not running

Pass / fail criteria
''''''''''''''''''''

The pass criteria for this test case is that all instructions are able to be
carried out according to the described behavior without deviation, the
killed "glance-api" processes are able to recover within the process
max_outage_time (20s). This max_outage_time (20s) gives the SUT enough time to
recover.

A negative result will be generated if the above is not met in completion.

Post conditions
---------------

No impact on the SUT.


-----------------------------------------------------------------
Test Case 5 - Controller node Openstack service down - cinder-api
-----------------------------------------------------------------

Short name
----------

opnfv.ha.tc006.cinder-api_service_down

Use case specification
----------------------

This test verifies the high availability of the "cinder-api" service provided by
OpenStack controller nodes. This test case kills the processes of Openstack
"cinder-api" service on a selected controller node, then checks whether the request
of the "openstack volume list" command are still processed successfully and the
killed processes are recovered.

Test preconditions
------------------

Three controller nodes are available, denoted as Node1, Node2, Node3 in the following.
If the high availability is based on active/active, Node1
can be any one of the controller nodes.
If the High availability is based on active/passive, Node1
should be an active controller node.
"cinder-api" service is running on Node1.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Methodology for monitoring high availability
''''''''''''''''''''''''''''''''''''''''''''

The high availability of "cinder-api" service is evaluated by monitoring service
availability and process outage_time

Service availability is tested by repeatedly executing "openstack volume list"
command and checking if the response of the command request is correct. The
command request is executed one by one in loop. When the response fails,
the "cinder-api" service is considered in outage.

Process outage_time is tested by checking the status of "cinder-api" processes on
the selected controller node. The time of "cinder-api" processes being killed to
the time of the "cinder-api" processes being recovered is the process outage_time.
Process recovery is verified by checking the existence of "cinder-api" processes.

Test execution
''''''''''''''

* Test action 1: Connect to Node1 through SSH, and check that target "cinder-api"
  processes are running on Node1
* Test action 2: Start two monitors: one for "cinder-api" process and the other
  for "openstack volume list" command.
  Each monitor will run as an independent process.
* Test action 3: Connect to Node1 through SSH, and then execute the kill_process
  attacker to kill "cinder-api" processes
* Test action 4: Calculate the process outage_time of "cinder-api" process monitor
* Test action 5: Verify the SLA, the process max_outage_time is 20s, test passes
  if the SLA is met
* Test action 6: Check the status of the "cinder-api" process on Node1, and
  restart the process if it is not running for next test cases

Pass / fail criteria
''''''''''''''''''''

The pass criteria for this test case is that all instructions are able to be
carried out according to the described behavior without deviation, the
killed "cinder-api" processes are able to recover within the process max_outage_time (20s).
This max_outage_time is referenced from the ETSI GS NFV-REL 001

A negative result will be generated if the above is not met in completion.

Post conditions
---------------

No impact on the SUT.


------------------------------------------------------------
Test Case 6 - Controller Node CPU Overload High Availability
------------------------------------------------------------

Short name
----------

opnfv.ha.tc009.cpu_overload

Use case specification
----------------------

This test verifies the high availability of control node. When the CPU usage of
a specified controller node is up to 100%, which breaks down the Openstack services
on this node. These Openstack services should able to be accessed by other controller
nodes, and the services on failed controller node should be isolated. This test case
stresses the CPU usage of a specified controller node to 100%, then checks whether
all services provided by the environment are OK with the monitor tools.

Test preconditions
------------------

Three controller nodes are available, denoted as Node1, Node2, Node3 in the following.
If the high availability is based on active/active, Node1
can be any one of the controller nodes.
If the High availability is based on active/passive, Node1
should be an active controller node.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Methodology for monitoring high availability
''''''''''''''''''''''''''''''''''''''''''''

The high availability of related OpenStack service is evaluated by monitoring service
availability

Service availability is tested by repeatedly executing "openstack router list",
"openstack stack list", "openstack volume list", "openstack image list" commands
and checking if the response of the command request is correct. The command
request is executed one by one in loop. When the response fails, the related
service is considered in outage.

Methodology for stressing CPU usage
'''''''''''''''''''''''''''''''''''

To evaluate the high availability of target OpenStack service under heavy CPU
load, the test case will first get the number of logical CPU cores on the target
controller node by shell command, then use the number to execute 'dd' command to
continuously copy from /dev/zero and output to /dev/null in loop. The 'dd' operation
only uses CPU, no I/O operation, which is ideal for stressing the CPU usage.

Since the 'dd' command is continuously executed and the CPU usage rate is stressed
to 100%, the scheduler will schedule each 'dd' command to be processed on a different
logical CPU core. Eventually to achieve all logical CPU cores usage rate to 100%.

Test execution
''''''''''''''

* Test action 1: Start four monitors: one for "openstack image list" command,
  one for "openstack router list" command, one for "openstack stack list"
  command and the last one for "openstack volume list" command. Each monitor
  will run as an independent process.
* Test action 2: Connect to Node1 through SSH, and then execute the stress_cpu
  attacker on Node1
  The stress_cpu attacker will trigger CPU to read from /dev/zero and
  write to /dev/null in loops to achieve all logical CPU cores usage rate to 100%.
* Test action 3: Use monitors to check if the related services are available
* Test action 4: Verify the SLA, test passes if the SLA is met
* Test action 5: Kill the process that stresses the CPU usage

Pass / fail criteria
''''''''''''''''''''

The pass criteria for this test case is that all instructions are able to be
carried out according to the described behavior without deviation, and the
outage_time of the "openstack image list", "openstack router list",
"openstack stack list", "openstack volume list" command request is shorter than
the service max_outage_time (5s).

A negative result will be generated if the above is not met in completion.

Post conditions
---------------

No impact on the SUT.


--------------------------------------------------------------
Test Case 7 - Controller Node Disk I/O Block High Availability
--------------------------------------------------------------

Short name
----------

opnfv.ha.tc010.disk_I/O_block

Use case specification
----------------------

This test verifies the high availability of control node. When the disk I/O of
a specified disk is blocked, which breaks down the Openstack services on this
node, the read and write services should still be accessible through other controller
nodes, and the services on failed controller node should be isolated. This test
case blocks the disk I/O of a specified controller node, then checks whether the
services that need to read or write the disk of the controller node are OK with
some monitor tools.

Test preconditions
------------------

Three controller nodes are available, denoted as Node1, Node2, Node3 in the following.
If the high availability is based on active/active, Node1
can be any one of the controller nodes.
If the High availability is based on active/passive, Node1
should be an active controller node.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Methodology for monitoring high availability
''''''''''''''''''''''''''''''''''''''''''''

The high availability of target OpenStack service is evaluated by monitoring service
availability

Service availability is tested by repeatedly executing "openstack flavor list"
command and checking if the response of the command request is correct. The
command request is executed one by one in loop. When the response fails, the
related service is considered in outage.

Methodology for blocking disk I/O
'''''''''''''''''''''''''''''''''

To evaluate the high availability of target OpenStack service under heavy I/O
load, the test case will execute shell command on the selected controller node
to continuously writting 8kb blocks to /test.dbf

Test execution
''''''''''''''

* Test action 1: Connect to Node1 through SSH, and then execute the block disk
  I/O attacker script on Node1. The block disk I/O attacker script will trigger
  a consistent writting of 8kb blocks to /test.dbf
* Test action 2: Start a monitor: for "openstack flavor list" command
* Test action 3: Create a flavor called "test-001"
* Test action 4: Execute the result checker script to check whether the flavor
  "test-001" is created
* Test action 5: Use monitors to check if the related services are available
* Test action 6: Verify the SLA, the maximum service outage time is set to 5s,
  test passes if the SLA is met
* Test action 7: Excutes the release disk I/O script to release the blocked I/O
  and delete the created "test-001" flavor

Pass / fail criteria
''''''''''''''''''''

The pass criteria for this test case is that all instructions are able to be
carried out according to the described behavior without deviation, and the
flavor "test-001" is created successfully, the outage_time of the
"openstack flaovr list" command request is shorter than the service
max_outage_time (5s).

A negative result will be generated if the above is not met in completion.

Post conditions
---------------

No impact on the SUT.


--------------------------------------------------------------------
Test Case 8 - Controller Load Balance as a Service High Availability
--------------------------------------------------------------------

Short name
----------

opnfv.ha.tc011.load_balance_service_down

Use case specification
----------------------

This test verifies the high availability of the OpenStack Load Balance as a
Service (current is HAProxy) that supports OpenStack on controller node. When
the load balance service of a specified controller node is killed, whether
other load balancers on other controller nodes will work, and whether the
controller node will restart the load balancer are checked. This test case kills
the processes of load balance service on a selected controller node, then checks
whether the request of the related Openstack command is OK and the killed
processes are recovered.

Test preconditions
------------------

Three controller nodes are available, denoted as Node1, Node2, Node3 in the
following.
If the high availability is based on active/active, Node1
can be any one of the controller nodes.
If the High availability is based on active/passive, Node1
should be an active controller node.
"haproxy" service is running on Node1.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Methodology for monitoring high availability
''''''''''''''''''''''''''''''''''''''''''''

The high availability of "haproxy" service is evaluated by monitoring service
availability and process outage_time

Service availability is tested by repeatedly executing "openstack image list"
command and checking if the response of the command request is correct. The
command request is executed one by one in loop. When the response fails,
the "haproxy" service is considered in outage.

Process outage_time is tested by checking the status of "haproxy" processes on
the selected controller node. The time of "haproxy" processes being killed to
the time of the "haproxy" processes being recovered is the process outage_time.
Process recovery is verified by checking the existence of "haproxy" processes.

Test execution
''''''''''''''

* Test action 1: Connect to Node1 through SSH, and check that target "haproxy"
  processes are running on Node1
* Test action 2: Start two monitors: one for "haproxy" process and the other
  for "openstack image list" command. Each monitor will run as an independent
  process.
* Test action 3: Connect to Node1 through SSH, and then execute the kill
  process attacker script with parameter "haproxy"
* Test action 4: Calculate the process outage_time of "haproxy" process monitor
* Test action 5: Verify the SLA, the process max_outage_time is 20s, test passed
  if the SLA is met
* Test action 6: Check the status of the "haproxy" process on Node1, and
  restart the process if it is not running for next test cases.

Pass / fail criteria
''''''''''''''''''''

The pass criteria for this test case is that all instructions are able to be
carried out according to the described behavior without deviation, the killed
"haproxy" processes are able to recover within the process max_outage_time (20s).
This max_outage_time (20s) gives the SUT enough time to
recover.

A negative result will be generated if the above is not met in completion.

Post conditions
---------------

No impact on the SUT.
