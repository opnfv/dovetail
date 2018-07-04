.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Huawei Technologies Co.,Ltd

===================================================
Security Group and Port Security test specification
===================================================

.. toctree::
   :maxdepth: 2

Scope
=====

The security group and port security test area evaluates the ability of the
system under test to support packet filtering by security group and port security.
The tests in this test area will evaluate preventing MAC spoofing by port security,
basic security group operations including testing cross/in tenant traffic, testing
multiple security groups, using port security to disable security groups and
updating security groups.

References
==========

N/A

Definitions and abbreviations
=============================

The following terms and abbreviations are used in conjunction with this test
area

- API - Application Programming Interface
- ICMP - Internet Control Message Protocol
- MAC - Media Access Control
- NFVi - Network Functions Virtualization infrastructure
- SSH - Secure Shell
- TCP - Transmission Control Protocol
- VIM - Virtual Infrastructure Manager
- VM - Virtual Machine

System Under Test (SUT)
=======================

The system under test is assumed to be the NFVi and VIM in operation on a
Pharos compliant infrastructure.

Test Area Structure
===================

The test area is structured based on the basic operations of security group and
port security. Each test case is able to run independently, i.e. irrelevant of
the state created by a previous test. Specifically, every test performs clean-up
operations which return the system to the same state as before the test.

All these test cases are included in the test case dovetail.tempest.network_security of
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
- list networks
- create floating ip
- delete floating ip

Routers and interface: https://developer.openstack.org/api-ref/networking/v2/index.html#routers-routers

- create router
- delete router
- list routers
- add interface to router

Subnets: https://developer.openstack.org/api-ref/networking/v2/index.html#subnets

- create subnet
- list subnets
- delete subnet

Servers: https://developer.openstack.org/api-ref/compute/

- create keypair
- create server
- delete server
- add/assign floating ip

Ports: https://developer.openstack.org/api-ref/networking/v2/index.html#ports

- update port
- list ports
- show port details

--------------------------------------------
Test Case 1 - Port Security and MAC Spoofing
--------------------------------------------

Test case specification
-----------------------

tempest.scenario.test_network_basic_ops.TestNetworkBasicOps.test_port_security_macspoofing_port

Test preconditions
------------------

* Neutron port-security extension API
* Neutron security-group extension API
* One public network

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: Create a security group SG1, which has rules for allowing incoming
  SSH and ICMP traffic
* Test action 2: Create a neutron network NET1
* Test action 3: Create a tenant router R1 which routes traffic to public network
* Test action 4: Create a subnet SUBNET1 and add it as router interface
* Test action 5: Create a server VM1 with SG1 and NET1, and assign a floating ip
  FIP1 (via R1) to VM1
* Test action 6: Verify can ping FIP1 successfully and can SSH to VM1 with FIP1
* Test action 7: Create a second neutron network NET2 and subnet SUBNET2, and attach VM1 to NET2
* Test action 8: Get VM1's ethernet interface NIC2 for NET2
* Test action 9: Create second server VM2 on NET2
* Test action 10: Verify VM1 is able to communicate with VM2 via NIC2
* Test action 11: Login to VM1 and spoof the MAC address of NIC2 to "00:00:00:00:00:01"
* Test action 12: Verify VM1 fails to communicate with VM2 via NIC2
* **Test assertion 1:** The ping operation is failed
* Test action 13: Update 'security_groups' to be none for VM1's NIC2 port
* Test action 14: Update 'port_security_enable' to be False for VM1's NIC2 port
* Test action 15: Verify now VM1 is able to communicate with VM2 via NIC2
* **Test assertion 2:** The ping operation is successful
* Test action 16: Delete SG1, NET1, NET2, SUBNET1, SUBNET2, R1, VM1, VM2 and FIP1

Pass / fail criteria
''''''''''''''''''''

This test evaluates the ability to prevent MAC spoofing by using port security.
Specifically, the test verifies that:

* With port security, the ICMP packets from a spoof server cannot pass the port.

* Without port security, the ICMP packets from a spoof server can pass the port.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A

------------------------------------------------------
Test Case 2 - Test Security Group Cross Tenant Traffic
------------------------------------------------------

Test case specification
-----------------------

tempest.scenario.test_security_groups_basic_ops.TestSecurityGroupsBasicOps.test_cross_tenant_traffic

Test preconditions
------------------

* Neutron security-group extension API
* Two tenants
* One public network

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: Create a neutron network NET1 for primary tenant
* Test action 2: Create a primary tenant router R1 which routes traffic to public network
* Test action 3: Create a subnet SUBNET1 and add it as router interface
* Test action 4: Create 2 empty security groups SG1 and SG2 for primary tenant
* Test action 5: Add a tcp rule to SG1
* Test action 6: Create a server VM1 with SG1, SG2 and NET1, and assign a floating ip
  FIP1 (via R1) to VM1
* Test action 7: Repeat test action 1 to 6 and create NET2, R2, SUBNET2, SG3, SG4,
  FIP2 and VM2 for an alt_tenant
* Test action 8: Verify VM1 fails to communicate with VM2 through FIP2
* **Test assertion 1:** The ping operation is failed
* Test action 9: Add ICMP rule to SG4
* Test action 10: Verify VM1 is able to communicate with VM2 through FIP2
* **Test assertion 2:** The ping operation is successful
* Test action 11: Verify VM2 fails to communicate with VM1 through FIP1
* **Test assertion 3:** The ping operation is failed
* Test action 12: Add ICMP rule to SG2
* Test action 13: Verify VM2 is able to communicate with VM1 through FIP1
* **Test assertion 4:** The ping operation is successful
* Test action 14: Delete SG1, SG2, SG3, SG4, NET1, NET2, SUBNET1, SUBNET2, R1, R2,
  VM1, VM2, FIP1 and FIP2

Pass / fail criteria
''''''''''''''''''''

This test evaluates the ability of the security group to filter packets cross tenant.
Specifically, the test verifies that:

* Without ICMP security group rule, the ICMP packets cannot be received by the server
  in another tenant which differs from the source server.

* With ingress ICMP security group rule enabled only at tenant1, the server in tenant2
  can ping server in tenant1 but not the reverse direction.

* With ingress ICMP security group rule enabled at tenant2 also, the ping works from both directions.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A

---------------------------------------------------
Test Case 3 - Test Security Group in Tenant Traffic
---------------------------------------------------

Test case specification
-----------------------

tempest.scenario.test_security_groups_basic_ops.TestSecurityGroupsBasicOps.test_in_tenant_traffic

Test preconditions
------------------

* Neutron security-group extension API
* One public network

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: Create a neutron network NET1
* Test action 2: Create a tenant router R1 which routes traffic to public network
* Test action 3: Create a subnet SUBNET1 and add it as router interface
* Test action 4: Create 2 empty security groups SG1 and SG2
* Test action 5: Add a tcp rule to SG1
* Test action 6: Create a server VM1 with SG1, SG2 and NET1, and assign a floating ip
  FIP1 (via R1) to VM1
* Test action 7: Create second server VM2 with default security group and NET1
* Test action 8: Verify VM1 fails to communicate with VM2 through VM2's fixed ip
* **Test assertion 1:** The ping operation is failed
* Test action 9: Add ICMP security group rule to default security group
* Test action 10: Verify VM1 is able to communicate with VM2 through VM2's fixed ip
* **Test assertion 2:** The ping operation is successful
* Test action 11: Delete SG1, SG2, NET1, SUBNET1, R1, VM1, VM2 and FIP1

Pass / fail criteria
''''''''''''''''''''

This test evaluates the ability of the security group to filter packets in one tenant.
Specifically, the test verifies that:

* Without ICMP security group rule, the ICMP packets cannot be received by the server
  in the same tenant.

* With ICMP security group rule, the ICMP packets can be received by the server
  in the same tenant.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A

-------------------------------------------
Test Case 4 - Test Multiple Security Groups
-------------------------------------------

Test case specification
-----------------------

tempest.scenario.test_security_groups_basic_ops.TestSecurityGroupsBasicOps.test_multiple_security_groups

Test preconditions
------------------

* Neutron security-group extension API
* One public network

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: Create a neutron network NET1
* Test action 2: Create a tenant router R1 which routes traffic to public network
* Test action 3: Create a subnet SUBNET1 and add it as router interface
* Test action 4: Create 2 empty security groups SG1 and SG2
* Test action 5: Add a tcp rule to SG1
* Test action 6: Create a server VM1 with SG1, SG2 and NET1, and assign a floating ip
  FIP1 (via R1) to VM1
* Test action 7: Verify failed to ping FIP1
* **Test assertion 1:** The ping operation is failed
* Test action 8: Add ICMP security group rule to SG2
* Test action 9: Verify can ping FIP1 successfully
* **Test assertion 2:** The ping operation is successful
* Test action 10: Verify can SSH to VM1 with FIP1
* **Test assertion 3:** Can SSH to VM1 successfully
* Test action 11: Delete SG1, SG2, NET1, SUBNET1, R1, VM1 and FIP1

Pass / fail criteria
''''''''''''''''''''

This test evaluates the ability of multiple security groups to filter packets.
Specifically, the test verifies that:

* A server with 2 security groups, one with TCP rule and without ICMP rule,
  cannot receive the ICMP packets sending from the tempest host machine.

* A server with 2 security groups, one with TCP rule and the other with ICMP rule,
  can receive the ICMP packets sending from the tempest host machine and be connected
  via the SSH client.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A

-------------------------------------------------------
Test Case 5 - Test Port Security Disable Security Group
-------------------------------------------------------

Test case specification
-----------------------

tempest.scenario.test_security_groups_basic_ops.TestSecurityGroupsBasicOps.test_port_security_disable_security_group

Test preconditions
------------------

* Neutron security-group extension API
* Neutron port-security extension API
* One public network

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: Create a neutron network NET1
* Test action 2: Create a tenant router R1 which routes traffic to public network
* Test action 3: Create a subnet SUBNET1 and add it as router interface
* Test action 4: Create 2 empty security groups SG1 and SG2
* Test action 5: Add a tcp rule to SG1
* Test action 6: Create a server VM1 with SG1, SG2 and NET1, and assign a floating ip
  FIP1 (via R1) to VM1
* Test action 7: Create second server VM2 with default security group and NET1
* Test action 8: Update 'security_groups' to be none and 'port_security_enabled' to be
  True for VM2's port
* Test action 9: Verify VM1 fails to communicate with VM2 through VM2's fixed ip
* **Test assertion 1:** The ping operation is failed
* Test action 10: Update 'security_groups' to be none and 'port_security_enabled' to be
  False for VM2's port
* Test action 11: Verify VM1 is able to communicate with VM2 through VM2's fixed ip
* **Test assertion 2:** The ping operation is successful
* Test action 12: Delete SG1, SG2, NET1, SUBNET1, R1, VM1, VM2 and FIP1

Pass / fail criteria
''''''''''''''''''''

This test evaluates the ability of port security to disable security group.
Specifically, the test verifies that:

* The ICMP packets cannot pass the port whose 'port_security_enabled' is True
  and security_groups is none.

* The ICMP packets can pass the port whose 'port_security_enabled' is False
  and security_groups is none.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A

---------------------------------------------
Test Case 6 - Test Update Port Security Group
---------------------------------------------

Test case specification
-----------------------

tempest.scenario.test_security_groups_basic_ops.TestSecurityGroupsBasicOps.test_port_update_new_security_group

Test preconditions
------------------

* Neutron security-group extension API
* One public network

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: Create a neutron network NET1
* Test action 2: Create a tenant router R1 which routes traffic to public network
* Test action 3: Create a subnet SUBNET1 and add it as router interface
* Test action 4: Create 2 empty security groups SG1 and SG2
* Test action 5: Add a tcp rule to SG1
* Test action 6: Create a server VM1 with SG1, SG2 and NET1, and assign a floating ip
  FIP1 (via R1) to VM1
* Test action 7: Create third empty security group SG3
* Test action 8: Add ICMP rule to SG3
* Test action 9: Create second server VM2 with default security group and NET1
* Test action 10: Verify VM1 fails to communicate with VM2 through VM2's fixed ip
* **Test assertion 1:** The ping operation is failed
* Test action 11: Update 'security_groups' to be SG3 for VM2's port
* Test action 12: Verify VM1 is able to communicate with VM2 through VM2's fixed ip
* **Test assertion 2:** The ping operation is successful
* Test action 13: Delete SG1, SG2, SG3, NET1, SUBNET1, R1, VM1, VM2 and FIP1

Pass / fail criteria
''''''''''''''''''''

This test evaluates the ability to update port with a new security group.
Specifically, the test verifies that:

* Without ICMP security group rule, the VM cannot receive ICMP packets.

* Update the port's security group which has ICMP rule, the VM can receive ICMP packets.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A
