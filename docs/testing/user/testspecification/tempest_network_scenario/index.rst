.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Huawei Technologies Co.,Ltd

===========================================
Tempest Network Scenario test specification
===========================================

.. toctree::
   :maxdepth: 2

Scope
=====

The Tempest Network scenario test area evaluates the ability of the
system under test to support dynamic network runtime operations through the
life of a VNF (e.g. attach/detach, enable/disable, read stats).
The tests in this test area will evaluate IPv4 network runtime operations
functionality. These runtime operations includes hotpluging network interface,
detaching floating-ip from VM, attaching floating-ip to VM, updating subnet's
DNS, updating VM instance port admin state and updating router admin state.

References
==========

- DNS

  - https://docs.openstack.org/newton/networking-guide/config-dns-res.html

Definitions and abbreviations
=============================

The following terms and abbreviations are used in conjunction with this test
area

- API - Application Programming Interface
- DNS - Domain Name System
- ICMP - Internet Control Message Protocol
- MAC - Media Access Control
- NIC - Network Interface Controller
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

The test area is structured based on dynamic network runtime operations. Each
test case is able to run independently, i.e. irrelevant of the state created by
a previous test. Specifically, every test performs clean-up operations which
return the system to the same state as before the test.

All these test cases are included in the test case dovetail.tempest.network_scenario of
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
- update router
- delete router
- add interface to router

Subnets: https://developer.openstack.org/api-ref/networking/v2/index.html#subnets

- create subnet
- update subnet
- delete subnet

Servers: https://developer.openstack.org/api-ref/compute/

- create keypair
- create server
- delete server
- add/assign floating IP
- disassociate floating IP

Ports: https://developer.openstack.org/api-ref/networking/v2/index.html#ports

- create port
- update port
- delete port

Floating IPs: https://developer.openstack.org/api-ref/networking/v2/index.html#floating-ips-floatingips

- create floating IP
- delete floating IP

--------------------------------------
Test Case 1 - Basic network operations
--------------------------------------

Test case specification
-----------------------

tempest.scenario.test_network_basic_ops.TestNetworkBasicOps.test_network_basic_ops

Test preconditions
------------------

* Nova has been configured to boot VMs with Neutron-managed networking
* Openstack nova, neutron services are available
* One public network

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: Create a security group SG1, which has rules for allowing
  incoming SSH and ICMP traffic
* Test action 2: Create a neutron network NET1
* Test action 3: Create a tenant router R1 which routes traffic to public network
* Test action 4: Create a subnet SUBNET1 and add it as router interface
* Test action 5: Create a server VM1 with SG1 and NET1, and assign a floating
  IP FIP1 (via R1) to VM1
* **Test assertion 1:** Ping FIP1 and SSH to VM1 via FIP1 successfully
* **Test assertion 2:** Ping the internal gateway from VM1 successfully
* **Test assertion 3:** Ping the default gateway from VM1 using its floating IP
  FIP1 successfully
* Test action 6: Detach FIP1 from VM1
* **Test assertion 4:** VM1 becomes unreachable after FIP1 disassociated
* Test action 7: Create a new server VM2 with NET1, and associate floating IP FIP1 to VM2
* **Test assertion 5:** Ping FIP1 and SSH to VM2 via FIP1 successfully
* Test action 8: Delete SG1, NET1, SUBNET1, R1, VM1, VM2 and FIP1

Pass / fail criteria
''''''''''''''''''''

This test evaluates the functionality of basic network operations.
Specifically, the test verifies that:

* The Tempest host can ping VM's IP address. This implies, but does not
  guarantee (see the ssh check that follows), that the VM has been assigned the
  correct IP address and has connectivity to the Tempest host.

* The Tempest host can perform key-based authentication to an ssh server hosted
  at VM's IP address. This check guarantees that the IP address is associated
  with the target VM.

* The Tempest host can ssh into the VM via the IP address and successfully ping
  the internal gateway address, implying connectivity to another VM on the same network.

* The Tempest host can ssh into the VM via the IP address and successfully ping
  the default gateway, implying external connectivity.

* Detach the floating-ip from the VM and VM becomes unreachable.

* Associate attached floating ip to a new VM and the new VM is reachable.

* Floating IP status is updated correctly after each change.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A

---------------------------------------
Test Case 2 - Hotplug network interface
---------------------------------------

Test case specification
-----------------------

tempest.scenario.test_network_basic_ops.TestNetworkBasicOps.test_hotplug_nic

Test preconditions
------------------

* Nova has been configured to boot VMs with Neutron-managed networking
* Compute interface_attach feature is enabled
* VM vnic_type is not set to 'direct' or 'macvtap'
* Openstack nova, neutron services are available
* One public network

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: Create a security group SG1, which has rules for allowing
  incoming SSH and ICMP traffic
* Test action 2: Create a neutron network NET1
* Test action 3: Create a tenant router R1 which routes traffic to public network
* Test action 4: Create a subnet SUBNET1 and add it as router interface
* Test action 5: Create a server VM1 with SG1 and NET1, and assign a floating
  IP FIP1 (via R1) to VM1
* **Test assertion 1:** Ping FIP1 and SSH to VM1 with FIP1 successfully
* Test action 6: Create a second neutron network NET2 and subnet SUBNET2, and
  attach VM1 to NET2
* Test action 7: Get VM1's ethernet interface NIC2 for NET2
* **Test assertion 2:** Ping NET2's internal gateway successfully
* Test action 8: Delete SG1, NET1, NET2, SUBNET1, SUBNET2, R1, NIC2, VM1 and FIP1

Pass / fail criteria
''''''''''''''''''''

This test evaluates the functionality of adding network to an active VM.
Specifically, the test verifies that:

* New network interface can be added to an existing VM successfully.

* The Tempest host can ssh into the VM via the IP address and successfully ping
  the new network's internal gateway address, implying connectivity to the new network.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A

-------------------------------------------
Test Case 3 - Update subnet's configuration
-------------------------------------------

Test case specification
-----------------------

tempest.scenario.test_network_basic_ops.TestNetworkBasicOps.test_subnet_details

Test preconditions
------------------

* Nova has been configured to boot VMs with Neutron-managed networking
* DHCP client is available
* Tenant networks should be non-shared and isolated
* Openstack nova, neutron services are available
* One public network

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: Create a security group SG1, which has rules for allowing
  incoming SSH and ICMP traffic
* Test action 2: Create a neutron network NET1
* Test action 3: Create a tenant router R1 which routes traffic to public network
* Test action 4: Create a subnet SUBNET1 and add it as router interface,
  configure SUBNET1 with dns nameserver '1.2.3.4'
* Test action 5: Create a server VM1 with SG1 and NET1, and assign a floating
  IP FIP1 (via R1) to VM1
* **Test assertion 1:** Ping FIP1 and SSH to VM1 with FIP1 successfully
* **Test assertion 2:** Retrieve the VM1's configured dns and verify it matches
  the one configured for SUBNET1
* Test action 6: Update SUBNET1's dns to '9.8.7.6'
* **Test assertion 3:** After triggering the DHCP renew from the VM manually,
  retrieve the VM1's configured dns and verify it has been successfully updated
* Test action 7: Delete SG1, NET1, SUBNET1, R1, VM1 and FIP1

Pass / fail criteria
''''''''''''''''''''

This test evaluates the functionality of updating subnet's configurations.
Specifically, the test verifies that:

* Updating subnet's DNS server configurations are affecting the VMs.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A

----------------------------------------
Test Case 4 - Update VM port admin state
----------------------------------------

Test case specification
-----------------------

tempest.scenario.test_network_basic_ops.TestNetworkBasicOps.test_update_instance_port_admin_state

Test preconditions
------------------

* Nova has been configured to boot VMs with Neutron-managed networking
* Network port_admin_state_change feature is enabled
* Openstack nova, neutron services are available
* One public network

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: Create a security group SG1, which has rules for allowing
  incoming SSH and ICMP traffic
* Test action 2: Create a neutron network NET1
* Test action 3: Create a tenant router R1 which routes traffic to public network
* Test action 4: Create a subnet SUBNET1 and add it as router interface
* Test action 5: Create a server VM1 with SG1 and NET1, and assign a floating
  IP FIP1 (via R1) to VM1
* Test action 6: Create a server VM2 with SG1 and NET1, and assign a floating
  IP FIP2 to VM2
* Test action 7: Get a SSH client SSHCLNT1 to VM2
* **Test assertion 1:** Ping FIP1 and SSH to VM1 with FIP1 successfully
* **Test assertion 2:** Ping FIP1 via SSHCLNT1 successfully
* Test action 8: Update admin_state_up attribute of VM1 port to False
* **Test assertion 3:** Ping FIP1 and SSH to VM1 with FIP1 failed
* **Test assertion 4:** Ping FIP1 via SSHCLNT1 failed
* Test action 9: Update admin_state_up attribute of VM1 port to True
* **Test assertion 5:** Ping FIP1 and SSH to VM1 with FIP1 successfully
* **Test assertion 6:** Ping FIP1 via SSHCLNT1 successfully
* Test action 10: Delete SG1, NET1, SUBNET1, R1, SSHCLNT1, VM1, VM2 and FIP1, FIP2

Pass / fail criteria
''''''''''''''''''''

This test evaluates the VM public and project connectivity status by changing VM port
admin_state_up to True & False. Specifically, the test verifies that:

* Public and project connectivity is reachable before updating admin_state_up
  attribute of VM port to False.

* Public and project connectivity is unreachable after updating admin_state_up
  attribute of VM port to False.

* Public and project connectivity is reachable after updating admin_state_up
  attribute of VM port from False to True.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A

---------------------------------------
Test Case 5 - Update router admin state
---------------------------------------

Test case specification
-----------------------

tempest.scenario.test_network_basic_ops.TestNetworkBasicOps.test_update_router_admin_state

Test preconditions
------------------

* Nova has been configured to boot VMs with Neutron-managed networking
* Multi-tenant networks capabilities
* Openstack nova, neutron services are available
* One public network

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: Create a security group SG1, which has rules for allowing
  incoming SSH and ICMP traffic
* Test action 2: Create a neutron network NET1
* Test action 3: Create a tenant router R1 which routes traffic to public network
* Test action 4: Create a subnet SUBNET1 and add it as router interface
* Test action 5: Create a server VM1 with SG1 and NET1, and assign a floating
  IP FIP1 (via R1) to VM1
* **Test assertion 1:** Ping FIP1 and SSH to VM1 with FIP1 successfully
* Test action 6: Update admin_state_up attribute of R1 to False
* **Test assertion 2:** Ping FIP1 and SSH to VM1 with FIP1 failed
* Test action 7: Update admin_state_up attribute of R1 to True
* **Test assertion 3:** Ping FIP1 and SSH to VM1 with FIP1 successfully
* Test action 8: Delete SG1, NET1, SUBNET1, R1, VM1 and FIP1

Pass / fail criteria
''''''''''''''''''''

This test evaluates the router public connectivity status by changing
router admin_state_up to True & False.
Specifically, the test verifies that:

* Public connectivity is reachable before updating admin_state_up attribute of router to False.

* Public connectivity is unreachable after updating admin_state_up attribute of router to False.

* Public connectivity is reachable after updating admin_state_up attribute of router.
  from False to True

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A
