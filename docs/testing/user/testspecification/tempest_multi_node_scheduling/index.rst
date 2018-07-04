.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Huawei Technologies Co.,Ltd

===========================================================
VM Resource Scheduling on Multiple Nodes test specification
===========================================================

.. toctree::
   :maxdepth: 2

Scope
=====

The VM resource scheduling test area evaluates the ability of the system under
test to support VM resource scheduling on multiple nodes.
The tests in this test area will evaluate capabilities to schedule VM to multiple
compute nodes directly with scheduler hints, and create server groups with policy
affinity and anti-affinity.

References
==========

- Availability zone

  - https://docs.openstack.org/newton/networking-guide/config-az.html

- Scheduling

  - https://docs.openstack.org/kilo/config-reference/content/section_compute-scheduler.html

Definitions and abbreviations
=============================

The following terms and abbreviations are used in conjunction with this test area

- API - Application Programming Interface
- NFVi - Network Functions Virtualization infrastructure
- VIM - Virtual Infrastructure Manager
- VM - Virtual Machine

System Under Test (SUT)
=======================

The system under test is assumed to be the NFVi and VIM in operation on a
Pharos compliant infrastructure.

Test Area Structure
===================

The test area is structured based on server group operations and server operations
on multiple nodes. Each test case is able to run independently, i.e. irrelevant of
the state created by a previous test. Specifically, every test performs clean-up
operations which return the system to the same state as before the test.

All these test cases are included in the test case dovetail.tempest.multi_node_scheduling of
OVP test suite.

Test Descriptions
=================

----------------------
API Used and Reference
----------------------

Security Groups: https://developer.openstack.org/api-ref/network/v2/index.html#security-groups-security-groups

- create security group
- delete security group

Networks: https://developer.openstack.org/api-ref/networking/v2/index.html#networks

- create network
- delete network

Routers and interface: https://developer.openstack.org/api-ref/networking/v2/index.html#routers-routers

- create router
- delete router
- add interface to router

Subnets: https://developer.openstack.org/api-ref/networking/v2/index.html#subnets

- create subnet
- delete subnet

Servers: https://developer.openstack.org/api-ref/compute/

- create keypair
- create server
- show server
- delete server
- add/assign floating IP
- create server group
- delete server group
- list server groups
- show server group details

Ports: https://developer.openstack.org/api-ref/networking/v2/index.html#ports

- create port
- delete port

Floating IPs: https://developer.openstack.org/api-ref/networking/v2/index.html#floating-ips-floatingips

- create floating IP
- delete floating IP

Availability zone: https://developer.openstack.org/api-ref/compute/

- get availability zone

------------------------------------------
Test Case 1 - Schedule VM to compute nodes
------------------------------------------

Test case specification
-----------------------

tempest.scenario.test_server_multinode.TestServerMultinode.test_schedule_to_all_nodes

Test preconditions
------------------

* At least 2 compute nodes
* Openstack nova, neutron services are available
* One public network

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: Get all availability zones AZONES1 in the SUT
* Test action 2: Get all compute nodes in AZONES1
* Test action 3: Get the value of 'min_compute_nodes' which is set by user in tempest
  config file and means the minimum number of compute nodes expected
* **Test assertion 1:** Verify that SUT has at least as many compute nodes as
  specified by the 'min_compute_nodes' threshold
* Test action 4: Create one server for each compute node, up to the 'min_compute_nodes' threshold
* **Test assertion 2:** Verify the number of servers matches the 'min_compute_nodes' threshold
* Test action 5: Get every server's 'hostId' and store them in a set which has no duplicate values
* **Test assertion 3:** Verify the length of the set equals to the number of servers to ensure
  that every server ended up on a different host
* Test action 6: Delete the created servers

Pass / fail criteria
''''''''''''''''''''

This test evaluates the functionality of VM resource scheduling.
Specifically, the test verifies that:

* VMs are scheduled to the requested compute nodes correctly.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A

-------------------------------------------------------------------------------------
Test Case 2 - Test create and delete multiple server groups with same name and policy
-------------------------------------------------------------------------------------

Test case specification
-----------------------

tempest.api.compute.servers.test_server_group.ServerGroupTestJSON.test_create_delete_multiple_server_groups_with_same_name_policy

Test preconditions
------------------

None

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: Generate a random name N1
* Test action 2: Create a server group SERG1 with N1 and policy affinity
* Test action 3: Create another server group SERG2 with N1 and policy affinity
* **Test assertion 1:** The names of SERG1 and SERG2 are the same
* **Test assertion 2:** The 'policies' of SERG1 and SERG2 are the same
* **Test assertion 3:** The ids of SERG1 and SERG2 are different
* Test action 4: Delete SERG1 and SERG2
* Test action 5: List all server groups
* **Test assertion 4:** SERG1 and SERG2 are not in the list

Pass / fail criteria
''''''''''''''''''''

This test evaluates the functionality of creating and deleting server groups with the same name and policy.
Specifically, the test verifies that:

* Server groups can be created with the same name and policy.
* Server groups with the same name and policy can be deleted successfully.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A

----------------------------------------------------------------------
Test Case 3 - Test create and delete server group with affinity policy
----------------------------------------------------------------------

Test case specification
-----------------------

tempest.api.compute.servers.test_server_group.ServerGroupTestJSON.test_create_delete_server_group_with_affinity_policy

Test preconditions
------------------

None

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: Generate a random name N1
* Test action 2: Create a server group SERG1 with N1 and policy affinity
* **Test assertion 1:** The name of SERG1 returned in the response is the same as N1
* **Test assertion 2:** The 'policies' of SERG1 returned in the response is affinity
* Test action 3: Delete SERG1 and list all server groups
* **Test assertion 3:** SERG1 is not in the list

Pass / fail criteria
''''''''''''''''''''

This test evaluates the functionality of creating and deleting server group with affinity policy.
Specifically, the test verifies that:

* Server group can be created with affinity policy and deleted successfully.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A

---------------------------------------------------------------------------
Test Case 4 - Test create and delete server group with anti-affinity policy
---------------------------------------------------------------------------

Test case specification
-----------------------

tempest.api.compute.servers.test_server_group.ServerGroupTestJSON.test_create_delete_server_group_with_anti_affinity_policy

Test preconditions
------------------

None

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: Generate a random name N1
* Test action 2: Create a server group SERG1 with N1 and policy anti-affinity
* **Test assertion 1:** The name of SERG1 returned in the response is the same as N1
* **Test assertion 2:** The 'policies' of SERG1 returned in the response is anti-affinity
* Test action 3: Delete SERG1 and list all server groups
* **Test assertion 3:** SERG1 is not in the list

Pass / fail criteria
''''''''''''''''''''

This test evaluates the functionality of creating and deleting server group with anti-affinity policy.
Specifically, the test verifies that:

* Server group can be created with anti-affinity policy and deleted successfully.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A

-------------------------------------
Test Case 5 - Test list server groups
-------------------------------------

Test case specification
-----------------------

tempest.api.compute.servers.test_server_group.ServerGroupTestJSON.test_list_server_groups

Test preconditions
------------------

None

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: Generate a random name N1
* Test action 2: Create a server group SERG1 with N1 and policy affinity
* Test action 3: List all server groups
* **Test assertion 1:** SERG1 is in the list
* Test action 4: Delete SERG1

Pass / fail criteria
''''''''''''''''''''

This test evaluates the functionality of listing server groups.
Specifically, the test verifies that:

* Server groups can be listed successfully.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A

--------------------------------------------
Test Case 6 - Test show server group details
--------------------------------------------

Test case specification
-----------------------

tempest.api.compute.servers.test_server_group.ServerGroupTestJSON.test_show_server_group

Test preconditions
------------------

None

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: Generate a random name N1
* Test action 2: Create a server group SERG1 with N1 and policy affinity, and stored
  the details (D1) returned in the response
* Test action 3: Show the details (D2) of SERG1
* **Test assertion 1:** All values in D1 are the same as the values in D2
* Test action 4: Delete SERG1

Pass / fail criteria
''''''''''''''''''''

This test evaluates the functionality of showing server group details.
Specifically, the test verifies that:

* Server groups can be shown successfully.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A
