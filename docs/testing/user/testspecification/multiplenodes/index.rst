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
test to support virtual machine resource scheduling on multiple nodes.
The tests in this test area will evaluate schedule virtual machines to multiple
compute nodes directly with scheduler hints.

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

The test area is structured based on server Operations. Each
test case is able to run independently, i.e. irrelevant of the state created by
a previous test. Specifically, every test performs clean-up operations which
return the system to the same state as before the test.

Test Descriptions
=================

API Used and Reference
----------------------

Security Groups: https://developer.openstack.org/api-ref/network/v2/index.html#security-groups-security-groups

- create security group
- delete security group

Networks: https://developer.openstack.org/api-ref/networking/v2/index.html#networks

- create netowrk
- delete netowrk

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
* **Test assertion 1:** Verify that SUT has at least as many compute nodes as
  specified by the 'min_compute_nodes' threshold
* Test action 3: Create one server for each compute node, up to the 'min_compute_nodes' threshold
* **Test assertion 2:** Verify each server is located on the requested compute node
* **Test assertion 3:** Verify the number of servers matches the 'min_compute_nodes' threshold
* **Test assertion 4:** Verify every server ended up on a different compute node
* Test action 4: Delete the created servers

Pass / fail criteria
''''''''''''''''''''

This test evaluates the functionality of VM resource scheduling.
Specifically, the test verifies that:

* Virtual machines are scheduled to the requested compute nodes correctly.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A
