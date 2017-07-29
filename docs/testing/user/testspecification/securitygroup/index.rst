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
basic security group operations including testing cross/in tenant traffic, testsing
multiple security groups, using port security to disable security groups and
updating security groups.

References
==========

This test area references the following specifications:

- ETSI GS NFV-REL 001

  - http://www.etsi.org/deliver/etsi_gs/NFV-REL/001_099/001/01.01.01_60/gs_nfv-rel001v010101p.pdf

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
the state created by a previous test. Specifially, every test performs clean-up
operations which return the system to the same state as before the test.

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

------------------------------
Port Security and MAC Spoofing
------------------------------

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

* Test action 1: Create an empty security group and store the id returned in the response.
* Test action 2: Generate a random network name that begins with 'network-smoke-'.
* Test action 3: Create a network with the random name by setting 'port_security_enabled'
  True, and store the network's name and id returned in the response.
* **Test assertion 1:** The name used to create the network is equal to the name
  returned in the response.
* Test action 4: Create a tenant router which routes traffic to public network and
  store the router's name and id returned in the response.
* Test action 5: Create a subnet for the network created in test action 3 and store
  the subnet's name and id returned in the response.
* Test action 6: Add a router interface with the stored router id and subnet id.
* Test action 7: List all networks and check whether the network created is in the list.
* **Test assertion 2:** The stored network's name and id are in the network list.
* Test action 8: List all subnets and check whether the subnet created is in the list.
* **Test assertion 3:** The stored subnet id is in the subnet list and the subnet's network
  id is in the network list.
* Test action 9: List all routers and check whether the router created is in the list.
* **Test assertion 4:** The stored router's name and id are in the router list.
* Test action 10: Create a keypair and create a server with this keypair, the network created
  in test action 3 and the security group created in test action 1. Store the server id
  returned in the response.
* Test action 11: Generate a floating ip and assign it to the server.
* Test action 12: Ping the server's floating ip.
* **Test assertion 5:** The ping operation's return codes is zero.
* Test action 13: Use floating ip to ssh to the server.
* **Test assertion 6:** Can ssh to the server without exception.
* Test action 14: Create another network and a subnet with no gateway of this network.
* Test action 15: Connect (hotplug) the server to the new network created in test action 14.
* Test action 16: Get the server's port as the spoof port.
* Test action 17: Get the server's nic as the spoof nic.
* Test action 18: Create a keypair and create another server with this keypair, the network created
  in test action 14 and the security group created in test action 1. Take this server as the peer.
* Test action 19: SSH to the first server to ping the peer server's fixed ip by using the spoof nic.
* **Test assertion 7:** The ping operation's return codes is zero.
* Test action 20: Set the MAC address of the first server's spoof nic to be "00:00:00:00:00:01".
* Test action 21: Get the MAC address of the first server's spoof nic.
* **Test assertion 8:** The MAC address got is equal to "00:00:00:00:00:01".
* Test action 22: SSH to the first server to ping the peer server's fixed ip by using the spoof nic.
* **Test assertion 9:** The ping operation's return codes is non-zero.
* Test action 23: Update the spoof port's security group to be none and set it's
  'port_security_enable' to be False.
* Test action 24: SSH to the first server to ping the peer server's fixed ip by using the spoof nic.
* **Test assertion 10:** The ping operation's return codes is zero.
* Test action 25: Delete all servers, subnets, networks, floating ips, security groups and routers created.
* Test action 26: List all servers, subnets, networks, floating ips, security groups and routers.
* **Test assertion 11:** The "id" parameters are not present in the lists.

Pass / fail criteria
''''''''''''''''''''

This test evaluates the ability to prevent MAC spoofing by using port security.
Specifically, the test verifies that:

* With port security, the ICMP packets from a spoof server can not pass the port.

* Without port security, the ICMP packets from a spoof server can pass the port.

In order to pass this test, all test assertions listed in the test execution
above need to pass.

Post conditions
---------------

N/A

----------------------------------------
Test Security Group Cross Tenant Traffic
----------------------------------------

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

* Test action 1: Choose an alt_tenant which is different from primary tenant.
* Test action 2: Create a keypair of this alt_tenant.
* Test action 3: Generate a random network name that begins with 'network-smoke-'.
* Test action 4: Create an alt_tenant network with the random name by setting
  'port_security_enabled' True, and store the network's name and id returned in the response.
* **Test assertion 1:** The name used to create the network is equal to the name
  returned in the response.
* Test action 5: Create an alt_tenant router which routes traffic to public network and
  store the router's name and id returned in the response.
* Test action 6: Create a subnet for the network created in test action 4 and store
  the subnet's name and id returned in the response.
* Test action 7: Add a router interface with the stored router id and subnet id.
* Test action 8: Create 2 empty securty groups of alt_tenant and stored the names returned
  in the response. One is access security group and the other is default security group.
* Test action 9: Add a tcp rule to the access security group.
* Test action 10: Create a server of alt_tenant with the network created in test action 4,
  the keypair created in test action 2 and the 2 security groups created in test action 8.
* **Test assertion 2:** The names of the 2 security groups in the server's details are
  equal to the names stored in test action 8.
* Test action 11: Generate a floating ip and assign it to the server created in test action 10.
* Test action 12: List all networks and verify the alt_tenant's network is in the list.
* **Test assertion 3:** The name and id of the network created in test action 4 are in the list.
* Test action 13: List all subnets and verify the alt_tenant's subnet is in the list.
* **Test assertion 4:** The id, cidr and network_id of the subnet created in test action 6
  are in the list.
* Test action 14: List all routers and verify the alt_tenant's router is in the list.
* **Test assertion 5:** The name and id of the router created in test action 5 are in the list.
* Test action 15: Get the MAC address of the server created in test action 10.
* Test action 16: Get the server's fixed ip.
* Test action 17: List all ports and check whether the server's MAC address, fixed ip
  and the subnet id are in the ports details.
* **Test assertion 6:** The subnet id is in the set of 'subnet_id' in the ports details.
* **Test assertion 7:** The server ip is in the set of 'ip_address' in the ports details.
* **Test assertion 8:** The MAC address is in the set of 'mac_address' in the ports details.
* Test action 18: Repeat test action 2 to 17 for primary tenant.
* Test action 19: SSH to the server of the primary tenant and ping alt_tenant server's floating ip.
* **Test assertion 9:** The ping operation's return codes is non-zero.
* Test action 20: Add ICMP rule to alt_tenant's default security group.
* Test action 21: SSH to the server of the primary tenant and ping alt_tenant server's floating ip.
* **Test assertion 10:** The ping operation's return codes is zero.
* Test action 22: SSH to the server of the alt_tenant and ping primary tenant server's floating ip.
* **Test assertion 11:** The ping operation's return codes is non-zero.
* Test action 23: Add ICMP rule to primary tenant's default security group.
* Test action 24: SSH to the server of the alt_tenant and ping primary tenant server's floating ip.
* **Test assertion 12:** The ping operation's return codes is zero.
* Test action 25: Delete all servers, subnets, networks, floating ips, security groups and routers created.
* Test action 26: List all servers, subnets, networks, floating ips, security groups and routers.
* **Test assertion 13:** The "id" parameters are not present in the lists.

Pass / fail criteria
''''''''''''''''''''

This test evaluates the ability of the security group to filter packets cross tenant.
Specifically, the test verifies that:

* Without ICMP security group rule, the ICMP packets can not be received by the server
  in another tenant which differs from the source server.

* With ICMP security group rule, the ICMP packets can be received by the server
  in another tenant which differs from the source server.

In order to pass this test, all test assertions listed in the test execution
above need to pass.

Post conditions
---------------

N/A

-------------------------------------
Test Security Group in Tenant Traffic
-------------------------------------

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

* Test action 1: Create a keypair of primary tenant.
* Test action 2: Generate a random network name that begins with 'network-smoke-'.
* Test action 3: Create a primary tenant network with the random name by setting
  'port_security_enabled' True, and store the network's name and id returned in the response.
* **Test assertion 1:** The name used to create the network is equal to the name
  returned in the response.
* Test action 4: Create a primary tenant router which routes traffic to public network and
  store the router's name and id returned in the response.
* Test action 5: Create a subnet for the network created in test action 3 and store
  the subnet's name and id returned in the response.
* Test action 6: Add a router interface with the stored router id and subnet id.
* Test action 7: Create 2 empty securty groups of primary tenant and stored the names returned
  in the response. One is access security group and the other is default security group.
* Test action 8: Add a tcp rule to the access security group.
* Test action 9: Create a server (VM1) of primary tenant with the network created in test action 3,
  the keypair created in test action 1 and the 2 security groups created in test action 7.
* **Test assertion 2:** The names of the 2 security groups in the server's details are
  equal to the names stored in test action 7.
* Test action 10: Generate a floating ip and assign it to the server created in test action 9.
* Test action 11: List all networks and verify the primary tenant's network is in the list.
* **Test assertion 3:** The name and id of the network created in test action 3 are in the list.
* Test action 12: List all subnets and verify the primary tenant's subnet is in the list.
* **Test assertion 4:** The id, cidr and network_id of the subnet created in test action 5
  are in the list.
* Test action 13: List all routers and verify the primary tenant's router is in the list.
* **Test assertion 5:** The name and id of the router created in test action 4 are in the list.
* Test action 14: Get the MAC address of the server created in test action 9.
* Test action 15: Get the server's fixed ip.
* Test action 16: List all ports and check whether the server's MAC address, fixed ip
  and the subnet id are in the ports details.
* **Test assertion 6:** The subnet id is in the set of 'subnet_id' in the ports details.
* **Test assertion 7:** The server ip is in the set of 'ip_address' in the ports details.
* **Test assertion 8:** The MAC address is in the set of 'mac_address' in the ports details.
* Test action 17: Create a server (VM2) of the primary tenant with default security group,
  and get the server id and 'security_groups' returned in the response.
* **Test assertion 9:** The name of the security_groups' returned in the respons
  is equal to 'default'.
* Test action 18: SSH to VM1 and ping VM2's fixed ip.
* **Test assertion 10:** The ping operation's return codes is non-zero.
* Test action 19: Add ICMP security group rule to default security group.
* Test action 20: SSH to VM1 and ping VM2's fixed ip.
* **Test assertion 11:** The ping operation's return codes is zero.
* Test action 21: Delete all servers, subnets, networks, floating ips, security groups and routers created.
* Test action 22: List all servers, subnets, networks, floating ips, security groups and routers.
* **Test assertion 12:** The "id" parameters are not present in the lists.

Pass / fail criteria
''''''''''''''''''''

This test evaluates the ability of the security group to filter packets in one tenant.
Specifically, the test verifies that:

* Without ICMP security group rule, the ICMP packets can not be received by the server
  in the same tenant.

* With ICMP security group rule, the ICMP packets can be received by the server
  in the same tenant.

In order to pass this test, all test assertions listed in the test execution
above need to pass.

Post conditions
---------------

N/A

-----------------------------
Test Multiple Security Groups
-----------------------------

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

* Test action 1: Create a keypair of primary tenant.
* Test action 2: Generate a random network name that begins with 'network-smoke-'.
* Test action 3: Create a primary tenant network with the random name by setting
  'port_security_enabled' True, and store the network's name and id returned in the response.
* **Test assertion 1:** The name used to create the network is equal to the name
  returned in the response.
* Test action 4: Create a primary tenant router which routes traffic to public network and
  store the router's name and id returned in the response.
* Test action 5: Create a subnet for the network created in test action 3 and store
  the subnet's name and id returned in the response.
* Test action 6: Add a router interface with the stored router id and subnet id.
* Test action 7: Create 2 empty securty groups of primary tenant and stored the names returned
  in the response. One is access security group and the other is default security group.
* Test action 8: Add a tcp rule to the access security group.
* Test action 9: Create a server (VM1) of primary tenant with the network created in test action 3,
  the keypair created in test action 1 and the 2 security groups created in test action 7.
* **Test assertion 2:** The names of the 2 security groups in the server's details are
  equal to the names stored in test action 7.
* Test action 10: Generate a floating ip and assign it to the server created in test action 9.
* Test action 11: List all networks and verify the primary tenant's network is in the list.
* **Test assertion 3:** The name and id of the network created in test action 3 are in the list.
* Test action 12: List all subnets and verify the primary tenant's subnet is in the list.
* **Test assertion 4:** The id, cidr and network_id of the subnet created in test action 5
  are in the list.
* Test action 13: List all routers and verify the primary tenant's router is in the list.
* **Test assertion 5:** The name and id of the router created in test action 4 are in the list.
* Test action 14: Get the MAC address of the server created in test action 9.
* Test action 15: Get the server's fixed ip.
* Test action 16: List all ports and check whether the server's MAC address, fixed ip
  and the subnet id are in the ports details.
* **Test assertion 6:** The subnet id is in the set of 'subnet_id' in the ports details.
* **Test assertion 7:** The server ip is in the set of 'ip_address' in the ports details.
* **Test assertion 8:** The MAC address is in the set of 'mac_address' in the ports details.
* Test action 17: Ping the server's floating ip.
* **Test assertion 9:** The ping operation's return codes is non-zero.
* Test action 18: Add ICMP security group rule to default security group.
* Test action 19: Ping the server's floating ip.
* **Test assertion 10:** The ping operation's return codes is zero.
* Test action 20: SSH to the server with it's floating ip, username and keypair.
* **Test assertion 11:** Can SSH to the server successfully.
* Test action 21: Delete all servers, subnets, networks, floating ips, security groups and routers created.
* Test action 22: List all servers, subnets, networks, floating ips, security groups and routers.
* **Test assertion 12:** The "id" parameters are not present in the lists.

Pass / fail criteria
''''''''''''''''''''

This test evaluates the ability of multiple security groups to filter packets.
Specifically, the test verifies that:

* A server with 2 security groups, one with TCP rule and without ICMP rule,
  can not receive the ICMP packets sending from the tempest host machine.

* A server with 2 security groups, one with TCP rule and the other with ICMP rule,
  can receive the ICMP packets sending from the tempest host machine and be connected
  via the SSH client.

In order to pass this test, all test assertions listed in the test execution
above need to pass.

Post conditions
---------------

N/A

-----------------------------------------
Test Port Security Disable Security Group
-----------------------------------------

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

* Test action 1: Create a keypair of primary tenant.
* Test action 2: Generate a random network name that begins with 'network-smoke-'.
* Test action 3: Create a primary tenant network with the random name by setting
  'port_security_enabled' True, and store the network's name and id returned in the response.
* **Test assertion 1:** The name used to create the network is equal to the name
  returned in the response.
* Test action 4: Create a primary tenant router which routes traffic to public network and
  store the router's name and id returned in the response.
* Test action 5: Create a subnet for the network created in test action 3 and store
  the subnet's name and id returned in the response.
* Test action 6: Add a router interface with the stored router id and subnet id.
* Test action 7: Create 2 empty securty groups of primary tenant and stored the names returned
  in the response. One is access security group and the other is default security group.
* Test action 8: Add a tcp rule to the access security group.
* Test action 9: Create a server (VM1) of primary tenant with the network created in test action 3,
  the keypair created in test action 1 and the 2 security groups created in test action 7.
* **Test assertion 2:** The names of the 2 security groups in the server's details are
  equal to the names stored in test action 7.
* Test action 10: Generate a floating ip and assign it to the server created in test action 9.
* Test action 11: List all networks and verify the primary tenant's network is in the list.
* **Test assertion 3:** The name and id of the network created in test action 3 are in the list.
* Test action 12: List all subnets and verify the primary tenant's subnet is in the list.
* **Test assertion 4:** The id, cidr and network_id of the subnet created in test action 5
  are in the list.
* Test action 13: List all routers and verify the primary tenant's router is in the list.
* **Test assertion 5:** The name and id of the router created in test action 4 are in the list.
* Test action 14: Get the MAC address of the server created in test action 9.
* Test action 15: Get the server's fixed ip.
* Test action 16: List all ports and check whether the server's MAC address, fixed ip
  and the subnet id are in the ports details.
* **Test assertion 6:** The subnet id is in the set of 'subnet_id' in the ports details.
* **Test assertion 7:** The server ip is in the set of 'ip_address' in the ports details.
* **Test assertion 8:** The MAC address is in the set of 'mac_address' in the ports details.
* Test action 17: Create a server (VM2) of primary tenant with the network created in test action 3,
  the keypair created in test action 1 and the default security group.
* Test action 18: Find out the VM2's port and stored the port id.
* Test action 19: Update the port by setting 'port_security_enabled' True and 'security_groups'
  to be none with the port id stored in test action 18.
* Test action 20: SSH to VM1 and ping VM2's fixed ip.
* **Test assertion 9:** The ping operation's return codes is non-zero.
* Test action 21: Update the port by setting 'port_security_enabled' False and 'security_groups'
  to be none with the port id stored in test action 18.
* Test action 22: SSH to VM1 and ping VM2's fixed ip.
* **Test assertion 10:** The ping operation's return codes is zero.
* Test action 23: Delete all servers, subnets, networks, floating ips, security groups and routers created.
* Test action 24: List all servers, subnets, networks, floating ips, security groups and routers.
* **Test assertion 11:** The "id" parameters are not present in the lists.

Pass / fail criteria
''''''''''''''''''''

This test evaluates the ability of port security to disable security group.
Specifically, the test verifies that:

* The ICMP packets can not pass the port whose 'port_security_enabled' is True
  and security_groups is none.

* The ICMP packets can pass the port whose 'port_security_enabled' is False
  and security_groups is none.

In order to pass this test, all test assertions listed in the test execution
above need to pass.

Post conditions
---------------

N/A

-------------------------------
Test Update Port Security Group
-------------------------------

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

* Test action 1: Create a keypair of primary tenant.
* Test action 2: Generate a random network name that begins with 'network-smoke-'.
* Test action 3: Create a primary tenant network with the random name by setting
  'port_security_enabled' True, and store the network's name and id returned in the response.
* **Test assertion 1:** The name used to create the network is equal to the name
  returned in the response.
* Test action 4: Create a primary tenant router which routes traffic to public network and
  store the router's name and id returned in the response.
* Test action 5: Create a subnet for the network created in test action 3 and store
  the subnet's name and id returned in the response.
* Test action 6: Add a router interface with the stored router id and subnet id.
* Test action 7: Create 2 empty securty groups of primary tenant and stored the names returned
  in the response. One is access security group and the other is default security group.
* Test action 8: Add a tcp rule to the access security group.
* Test action 9: Create a server (VM1) of primary tenant with the network created in test action 3,
  the keypair created in test action 1 and the 2 security groups created in test action 7.
* **Test assertion 2:** The names of the 2 security groups in the server's details are
  equal to the names stored in test action 7.
* Test action 10: Generate a floating ip and assign it to the server created in test action 9.
* Test action 11: List all networks and verify the primary tenant's network is in the list.
* **Test assertion 3:** The name and id of the network created in test action 3 are in the list.
* Test action 12: List all subnets and verify the primary tenant's subnet is in the list.
* **Test assertion 4:** The id, cidr and network_id of the subnet created in test action 5
  are in the list.
* Test action 13: List all routers and verify the primary tenant's router is in the list.
* **Test assertion 5:** The name and id of the router created in test action 4 are in the list.
* Test action 14: Get the MAC address of the server created in test action 9.
* Test action 15: Get the server's fixed ip.
* Test action 16: List all ports and check whether the server's MAC address, fixed ip
  and the subnet id are in the ports details.
* **Test assertion 6:** The subnet id is in the set of 'subnet_id' in the ports details.
* **Test assertion 7:** The server ip is in the set of 'ip_address' in the ports details.
* **Test assertion 8:** The MAC address is in the set of 'mac_address' in the ports details.
* Test action 17: Create an empty security group whose name starts with "secgroup_new-" and
  store the name of the security group.
* **Test assertion 9:** The name and description of the security group returned in the response
  are equal to the name and description used to created.
* Test action 18: Add a ICMP rule (protocol='icmp',direction='ingress') into the new security group.
* Test action 19: Show the details of the ICMP rule.
* **Test assertion 10:** The rule have the same security group ID with the new security group
  created in test action 17.
* Test action 20: Create a server (VM2) with "default" security group and stored the id and
  the 'security_groups' returned in the response.
* **Test assertion 11:** The name of the security group stored in test action 20 is equal to "default".
* Test action 21: SSH to VM1 and Ping VM2's fixed ip.
* **Test assertion 12:** The ping operation's return codes is non-zero.
* Test action 22: Update port of VM2 with the new security group created in test action 17.
* Test action 23: Show the details of VM2 port and store the name of the security group.
* **Test assertion 13:** The security group name stored in test action 23 is equal to the name
  stored in test action 17.
* Test action 24: SSH to VM1 and Ping VM2's fixed ip.
* **Test assertion 14:** The ping operation's return codes is zero.
* Test action 25: Delete all servers, subnets, networks, floating ips, security groups and routers created.
* Test action 26: List all servers, subnets, networks, floating ips, security groups and routers.
* **Test assertion 15:** The "id" parameters are not present in the lists.

Pass / fail criteria
''''''''''''''''''''

This test evaluates the ability to update port with a new security group.
Specifically, the test verifies that:

* Without ICMP security group rule, the VM can not receive ICMP packets.

* Update the port's security group which has ICMP rule, the VM can receive ICMP packets.

In order to pass this test, all test assertions listed in the test execution
above need to pass.

Post conditions
---------------

N/A
