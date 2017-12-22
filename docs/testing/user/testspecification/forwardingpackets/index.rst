.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Huawei Technologies Co.,Ltd

==================================================
Forwarding Packets in Data Path test specification
==================================================

.. toctree::
   :maxdepth: 2

Scope
=====

This test area evaluates the ability of the system under test to support basic packet forwarding.
The test in this test area will evaluate basic packet forwarding through virtual IPv4 networks
in data path, including creating server and verifying network connectivity to the created server
with ping operation using MTU sized packets.

References
==========

N/A

Definitions and abbreviations
=============================

The following terms and abbreviations are used in conjunction with this test
area

- API - Application Programming Interface
- ICMP - Internet Control Message Protocol
- MTU - Maximum Transmission Unit
- NFVi - Network Functions Virtualization infrastructure
- SSH - Secure Shell
- VIM - Virtual Infrastructure Manager
- VM - Virtual Machine

System Under Test (SUT)
=======================

The system under test is assumed to be the NFVi and VIM in operation on a
Pharos compliant infrastructure.

Test Area Structure
===================

The test area is structured based on the basic operations of forwarding packets
in data path through virtual networks. Specifically, the test performs
clean-up operations which return the system to the same state as before the test.

This test case is included in the test case dovetail.tempest.tc001 of OVP test suite.

Test Descriptions
=================

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
- delete server
- add/assign floating ip

Ports: https://developer.openstack.org/api-ref/networking/v2/index.html#ports

- create port
- delete port

Floating IPs: https://developer.openstack.org/api-ref/networking/v2/index.html#floating-ips-floatingips

- create floating ip
- delete floating ip

----------------------------
MTU Sized Frames Fit Through
----------------------------

Test case specification
-----------------------

tempest.scenario.test_network_basic_ops.TestNetworkBasicOps.test_mtu_sized_frames

Test preconditions
------------------

* Nova has been configured to boot VMs with Neutron-managed networking
* Neutron net-mtu extension API
* One public network

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: Create a security group SG1, which has rules for allowing
  incoming and outgoing SSH and ICMP traffic
* Test action 2: Create a neutron network NET1
* Test action 3: Create a tenant router R1 which routes traffic to public network
* Test action 4: Create a subnet SUBNET1 and add it as router interface
* Test action 5: Create a server VM1 with SG1 and NET1, and assign a floating
  ip FIP1 (via R1) to VM1
* Test action 6: Set MTU size to be the default MTU size of the SUT's network
* Test action 7: Host sends MTU sized ICMP packets to VM1 using ``ping``
* **Test assertion 1:** Ping FIP1 using MTU sized packets successfully
* Test action 8: SSH to VM1 with FIP1
* **Test assertion 2:** SSH to VM1 with FIP1 successfully
* Test action 9: Delete SG1, NET1, SUBNET1, R1, VM1 and FIP1

Pass / fail criteria
''''''''''''''''''''

This test evaluates the network connectivity using MTU sized frames.
Specifically, the test verifies that:

* With Neutron net-mtu extension configured, MTU sized packets can fit through network.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A
