---------------------------------------------------------------------------
Test Case 10 - Controller node OpenStack service down - Controller Restart
---------------------------------------------------------------------------

Short name
----------

dovetail.ha.controller_restart

Use case specification
----------------------

This test case verifies that the high availability of controller node is working
properly.
Specifically, this test case shutdowns a specified controller node with some
fault injection tools, then checks whether all services provided by the
controller node are OK with some monitor tools.

Test preconditions
------------------

In this test case, an attacker called "host-shutdown" is needed.
This attacker includes two parameters: fault_type and host.

The purpose of this attacker is to shutdown a controller and check whether the
services are handled by this controller are still working normally.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Methodology for verifying service continuity and recovery
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''

In order to verify this service one monitor is going to be used.

This monitor is using an OpenStack command and the respective command name of
the OpenStack component that we want to verify that the respective service is
still running normally.

In this test case, there is one metric: 1)service_outage_time: which indicates
the maximum outage time (seconds) of the specified OpenStack command request.

Test execution
''''''''''''''
* Test action 1: Connect to Node1 through SSH, and check that controller services
  are running on normally
* Test action 2: Create a image with "openstack image create test-cirros
  --file cirros-0.3.5-x86_64-disk.img --disk-format qcow2 --container-format bare"
* Test action 3: Execute"openstack flavor create m1.test --id auto --ram 512
  --disk 1 --vcpus 1" to create flavor "m1.test".
* Test action 4: This test case needs two configuration files:
  1) test case file: opnfv_yardstick_tc019.yaml
  2) POD file: pod.yaml
* Test action 5: Start monitors: each monitor will run with independently
  process and for different OpenStack components. The monitor info will be collected.
* Test action 6: Connect to Node1 through SSH, and then execute the shutdown script
  on the host. The host will be shutdown.
* Test action 7: Stop monitors after a period of time specified by "waiting_time".
  The monitor info will be aggregated.
* Test action 8: Verify the SLA and set the verdict of the test case to pass or fail.


Pass / fail criteria
''''''''''''''''''''

Check whether the SLA is passed.

The controller operations are carried out in above order and no errors occur.

A negative result will be generated if the above is not met in completion.

Post conditions
---------------

It is the action when the test cases exist.
It will check the status of the specified process on the host, and restart
the process if it is not running for next test cases
