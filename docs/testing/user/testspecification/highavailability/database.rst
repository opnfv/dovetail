----------------------------------------------------------------
Test Case 9 - Controller node OpenStack service down - Database
----------------------------------------------------------------

Short name
----------

dovetail.ha.database

Use case specification
----------------------

This test case verifies that the high availability of the data base instances
used by OpenStack (mysql) on control node is working properly.
Specifically, this test case kills the processes of database service on a
selected control node, then checks whether the request of the related
OpenStack command is OK and the killed processes are recovered.

Test preconditions
------------------

In this test case, an attacker called "kill-process" is needed.
This attacker includes three parameters: fault_type, process_name and host.

The purpose of this attacker is to kill any purpose with a specific process
name which is run on the host node. In case that multiple processes use the
same name on the host node, all of them are going to be killed by this attacker.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Methodology for verifying service continuity and recovery
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''

In order to verify this service two different monitors are going to be used.

As first monitor is used a OpenStack command and acts as watcher for
database connection of different OpenStack components.

For second monitor is used a process monitor and the main purpose is to watch
whether the database processes on the host node are killed properly.

Therefore, in this test case, there are two metrics:
- service_outage_time, which indicates the maximum outage time (seconds)
  of the specified OpenStack command request
- process_recover_time, which indicates the maximum time (seconds) from the
  process being killed to recovered

Test execution
''''''''''''''
* Test action 1: Connect to Node1 through SSH, and check that "database"
  processes are running on Node1
* Test action 2: Create a image with "openstack image create test-cirros
  --file cirros-0.3.5-x86_64-disk.img --disk-format qcow2 --container-format bare"
* Test action 3: Execute"openstack flavor create m1.test --id auto --ram 512
  --disk 1 --vcpus 1" to create flavor "m1.test".
* Test action 4: This test case needs two configuration files:
  1) test case file: opnfv_yardstick_tc090.yaml
  2) POD file: pod.yaml
* Test action 5: Start two monitors: one for "database" processes on the host
  node and the other for connection toward database from different OpenStack
  components.
  Each monitor will run as an independent process
* Test action 6: Connect to Node1 through SSH, and then kill the "mysql"
  process(es)
* Test action 7: Stop monitors after a period of time specified by "waiting_time".
  The monitor info will be aggregated.
* Test action 8: Verify the SLA and set the verdict of the test case to pass or fail.


Pass / fail criteria
''''''''''''''''''''

Check whether the SLA is passed.

The database operations are carried out in above order and no errors occur.

A negative result will be generated if the above is not met in completion.

Post conditions
---------------

It is the action when the test cases exist.
It will check the status of the specified process on the host, and restart
the process if it is not running for next test cases
