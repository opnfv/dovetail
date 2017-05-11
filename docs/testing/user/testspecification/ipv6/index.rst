.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) OPNFV

========================
IPv6 test specification
========================

.. toctree::
   :maxdepth: 2

Scope
=====

The IPv6 compliance test suite will evaluate the ability for a SUT to support IPv6
Tenant Network features and functionality provided by OPNFV platform.

References
================

- OPNFV ivp6 project

  - https://wiki.opnfv.org/display/ipv6/IPv6+Home

- upstream openstack api reference

  - http://developer.openstack.org/api-ref

Definitions and abbreviations
=============================

The following terms and abbreviations are used in conjunction with this test area

- CIDR - Classless Inter-Domain Routing
- DHCP - Dynamic Host Configuration Protocol
- DHCPv6 - Dynamic Host Configuration Protocol version 6
- ICMP - internet control message protocol
- NFVi - Network functions virtualization infrastructure
- NIC - Network Interface Controller
- SDN - Software Defined Network
- SLAAC - Stateless Address Auto Configuration
- TCP - transmission control protocol
- UDP - user datagram protocol
- VM - Virtual Machine
- vNIC - virtual Network Interface Controller

System Under Test (SUT)
=======================

The system under test is assumed to be the NFVi in operation on an Pharos compliant infrastructure.

Test Suite Structure
====================

The test suite is structured in some way that I am unable to articulate at this time.

Test Descriptions
=================

-----------------------------------------------------------------
Test Case 1 - Create and Delete an IPv6 Network, Port and Subnet
-----------------------------------------------------------------

Use case specification
----------------------

tempest.api.network.test_networks.BulkNetworkOpsIpV6Test.test_bulk_create_delete_network
tempest.api.network.test_networks.BulkNetworkOpsIpV6Test.test_bulk_create_delete_port
tempest.api.network.test_networks.BulkNetworkOpsIpV6Test.test_bulk_create_delete_subnet

Test preconditions
------------------

environment can be deployed on bare metal of virtualized infrastructure,
deployment can be HA or non-HA.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

* Test action 1: create/delete network, create 2 networks in one request,
  asserting that the networks are found in the list after creation
* Test action 2: create/delete subnet, create 2 subnets in one request,
  asserting that the subnets are found in the list after creation
* Test action 3: create/delete port, create 2 ports in one request,
  asserting that the ports are found in the list after creation

If normal response code 200 is returned, the test passes. Otherwise,
the test fails with various error codes.

Post conditions
---------------

NA

-------------------------------------------------------------------
Test Case 2 - Create, Update and Delete an IPv6 Network and Subnet
-------------------------------------------------------------------

Use case specification
----------------------

tempest.api.network.test_networks.NetworksIpV6Test.test_create_update_delete_network_subnet

Test preconditions
------------------

environment can be deployed on bare metal of virtualized infrastructure,
deployment can be HA or non-HA.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

* Test action 1: Create a network
* Test action 2: Verify network update
* Test action 3: Find a CIDR that is not in use yet and create a subnet with it
* Test action 4: Verify subnet update
* Test action 5: Delete subnet and network

If normal response code 200 is returned, the test passes. Otherwise,
the test fails with various error codes.

Post conditions
---------------

NA

-------------------------------------------------
Test Case 3 - Check External Network Visibility
-------------------------------------------------

Use case specification
----------------------

tempest.api.network.test_networks.NetworksIpV6Test.test_external_network_visibility

Test preconditions
------------------

environment can be deployed on bare metal of virtualized infrastructure,
deployment can be HA or non-HA.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

* Test action 1: List all networks
* Test action 2: Check if external networks found in the listed networks
* Test action 3: Check if subnet exists in the external network

If normal response code 200 is returned, the test passes. Otherwise,
the test fails with various error codes.

Post conditions
---------------

NA

---------------------------------------------------------
Test Case 4 - List IPv6 Networks and Subnets of a Tenant
---------------------------------------------------------

Use case specification
----------------------

tempest.api.network.test_networks.NetworksIpV6Test.test_list_networks
tempest.api.network.test_networks.NetworksIpV6Test.test_list_subnets

Test preconditions
------------------

environment can be deployed on bare metal of virtualized infrastructure,
deployment can be HA or non-HA.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

* Test action 1: Verify the networks exists in the list of all networks
* Test action 2: Verify the subnet exists in the list of all subnets

If normal response code 200 is returned, the test passes. Otherwise,
the test fails with various error codes.

Post conditions
---------------

NA

------------------------------------------------------------
Test Case 5 - Show Information of an IPv6 Network and Subnet
------------------------------------------------------------

Use case specification
----------------------

tempest.api.network.test_networks.NetworksIpV6Test.test_show_network
tempest.api.network.test_networks.NetworksIpV6Test.test_show_subnet

Test preconditions
------------------

environment can be deployed on bare metal of virtualized infrastructure,
deployment can be HA or non-HA.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

* Test action 1: Verify the details of a network
* Test action 2: Verify the details of a subnet

If normal response code 200 is returned, the test passes. Otherwise,
the test fails with various error codes.

Post conditions
---------------

NA

-------------------------------------------------------------
Test Case 6 - Create an IPv6 Port in Allowed Allocation Pools
-------------------------------------------------------------

Use case specification
----------------------

tempest.api.network.test_ports.PortsIpV6TestJSON.test_create_port_in_allowed_allocation_pools

Test preconditions
------------------

environment can be deployed on bare metal of virtualized infrastructure,
deployment can be HA or non-HA.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

* Test action 1: Create network
* Test action 2: Get allocation pools
* Test action 3: Create subnet of the created network within allocation pools
* Test action 4: Create port of the created network
* Test action 5: Verify the port ip is in the range of allocation pools

If normal response code 200 is returned, the test passes. Otherwise,
the test fails with various error codes.

Post conditions
---------------

NA

-----------------------------------------------------------
Test Case 7 - Create an IPv6 Port without Security Groups
-----------------------------------------------------------

Use case specification
----------------------

tempest.api.network.test_ports.PortsIpV6TestJSON.test_create_port_with_no_securitygroups

Test preconditions
------------------

environment can be deployed on bare metal of virtualized infrastructure,
deployment can be HA or non-HA.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

* Test action 1: Create network
* Test action 2: Create subnet of the network
* Test action 3: Create port of the network without security group
* Test action 4: Verify the security group of the network is empty

If normal response code 200 is returned, the test passes. Otherwise,
the test fails with various error codes.

Post conditions
---------------

NA

-----------------------------------------------------
Test Case 8 - Create, Update and Delete an IPv6 Port
-----------------------------------------------------

Use case specification
----------------------

tempest.api.network.test_ports.PortsIpV6TestJSON.test_create_update_delete_port

Test preconditions
------------------

environment can be deployed on bare metal of virtualized infrastructure,
deployment can be HA or non-HA.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

* Test action 1: Verify port creation
* Test action 2: Schedule port deletion with verification upon test completion
* Test action 3: Verify port update
* Test action 4: Delete port

If normal response code 200 is returned, the test passes. Otherwise,
the test fails with various error codes.

Post conditions
---------------

NA

-----------------------------------------
Test Case 9 - List IPv6 Ports of a Tenant
-----------------------------------------

Use case specification
----------------------

tempest.api.network.test_ports.PortsIpV6TestJSON.test_list_ports

Test preconditions
------------------

environment can be deployed on bare metal of virtualized infrastructure,
deployment can be HA or non-HA.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

* Test action 1: List all ports
* Test action 2: Verify the port exists in the list of all ports

If normal response code 200 is returned, the test passes. Otherwise,
the test fails with various error codes.

Post conditions
---------------

NA

-----------------------------------------------
Test Case 10 - Show Information of an IPv6 Port
-----------------------------------------------

Use case specification
----------------------

tempest.api.network.test_ports.PortsIpV6TestJSON.test_show_port

Test preconditions
------------------

environment can be deployed on bare metal of virtualized infrastructure,
deployment can be HA or non-HA.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

* Test action 1: Verify the details of port

If normal response code 200 is returned, the test passes. Otherwise,
the test fails with various error codes.

Post conditions
---------------

NA

---------------------------------------------------------
Test Case 11 - Add Multiple Interfaces for an IPv6 Router
---------------------------------------------------------

Use case specification
----------------------

tempest.api.network.test_routers.RoutersIpV6Test.test_add_multiple_router_interfaces

Test preconditions
------------------

environment can be deployed on bare metal of virtualized infrastructure,
deployment can be HA or non-HA.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

* Test action 1: Create networks named network01 and network02
* Test action 2: Create subnet01 in network01, subnet02 in network02 with CIDR
* Test action 3: Create router
* Test action 4: Create interface01 with subnet01 and router
* Test action 5: Verify interface
* Test action 6: Create interface02 with subnet02 and router
* Test action 7: Verify interface

If normal response code 200 is returned, the test passes. Otherwise,
the test fails with various error codes.

Post conditions
---------------

NA

-------------------------------------------------------------------
Test Case 12 - Add and Remove an IPv6 Router Interface with port_id
-------------------------------------------------------------------

Use case specification
----------------------

tempest.api.network.test_routers.RoutersIpV6Test.test_add_remove_router_interface_with_port_id

Test preconditions
------------------

environment can be deployed on bare metal of virtualized infrastructure,
deployment can be HA or non-HA.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

* Test action 1: Create network, subnet, router and port
* Test action 2: Add router interface to port created
* Test action 3: Verify router id is equal to device id in port details

If normal response code 200 is returned, the test passes. Otherwise,
the test fails with various error codes.

Post conditions
---------------

NA

---------------------------------------------------------------------
Test Case 13 - Add and Remove an IPv6 Router Interface with subnet_id
---------------------------------------------------------------------

Use case specification
----------------------

tempest.api.network.test_routers.RoutersIpV6Test.test_add_remove_router_interface_with_subnet_id

Test preconditions
------------------

environment can be deployed on bare metal of virtualized infrastructure,
deployment can be HA or non-HA.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

* Test action 1: Create network, subnet and router
* Test action 2: Add router interface with subnet id
* Test action 3: Verify router id is equal to device id in port details

If normal response code 200 is returned, the test passes. Otherwise,
the test fails with various error codes.

Post conditions
---------------

NA

-------------------------------------------------------------------
Test Case 14 - Create, Show, List, Update and Delete an IPv6 router
-------------------------------------------------------------------

Use case specification
----------------------

tempest.api.network.test_routers.RoutersIpV6Test.test_create_show_list_update_delete_router

Test preconditions
------------------

Environment can be deployed on bare metal of virtualized infrastructure,
deployment can be HA or non-HA.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

* Test action 1: Create a router
* Test action 2: Show details of the created router
* Test action 3: List routers and verify if created router is there in response
* Test action 4: Update the name of router and verify if it is updated
* Test action 5: Delete the router

If normal response code 200 is returned, the test passes. Otherwise,
the test fails with various error codes.

Post conditions
---------------

NA

---------------------------------------------------------------------------
Test Case 15 - Create, List, Update, Show and Delete an IPv6 security group
---------------------------------------------------------------------------

Use case specification
----------------------

tempest.api.network.test_security_groups.SecGroupIPv6Test.test_create_list_update_show_delete_security_group

Test preconditions
------------------

Environment can be deployed on bare metal of virtualized infrastructure,
deployment can be HA or non-HA.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

* Test action 1: Create a security group
* Test action 2: List security groups and verify if created security group is there in response
* Test action 3: Update the name and description of this security group
* Test action 4: Verify if security group is updated
* Test action 5: Show details of the updated security group
* Test action 6: Delete the security group

If normal response code 200 is returned, the test passes. Otherwise,
the test fails with various error codes.

Post conditions
---------------

NA

---------------------------------------------------------------
Test Case 16 - Create, Show and Delete IPv6 security group rule
---------------------------------------------------------------

Use case specification
----------------------

tempest.api.network.test_security_groups.SecGroupIPv6Test.test_create_show_delete_security_group_rule

Test preconditions
------------------

Environment can be deployed on bare metal of virtualized infrastructure,
deployment can be HA or non-HA.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

* Test action 1: Create a security group
* Test action 2: Create rules for protocol tcp, udp and icmp
* Test action 3: Show details of the created security rule
* Test action 4: List rules and verify created rule is in response
* Test action 5: Delete the security group and security group rules

If normal response code 200 is returned, the test passes. Otherwise,
the test fails with various error codes.

Post conditions
---------------

NA

----------------------------------------
Test Case 17 - List IPv6 Security Groups
----------------------------------------

Use case specification
----------------------

tempest.api.network.test_security_groups.SecGroupIPv6Test.test_list_security_groups

Test preconditions
------------------

Environment can be deployed on bare metal of virtualized infrastructure,
deployment can be HA or non-HA.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

* Test action 1: List all security group
* Test action 2: Verify the default security group exist in list

If normal response code 200 is returned, the test passes. Otherwise,
the test fails with various error codes.

Post conditions
---------------

NA


---------------------------------------------------------
Test Case 18 - IPv6 Address Assignment - DHCPv6 Stateless
---------------------------------------------------------

Use case specification
----------------------

tempest.scenario.test_network_v6.TestGettingAddress.test_dhcp6_stateless_from_os

Test preconditions
------------------

1. Environment can be deployed on bare metal of virtualized infrastructure,
deployment can be HA or non-HA.
2. This test case is a scenario tests, it needs to boot virtual machines and ping6
in addition to test APIs, ping6 to vRouter is not supported by SDN controller yet,
such as Opendaylight (Boron and previous releases), so it is scenario dependent.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

* Test action 1: Create network with one IPv6 subnet in mode 'dhcpv6_stateless' and create one IPv4 subnet
* Test action 2: Boot two VMs on this network
* Test action 3: Allocate and assign two IPv4 floating IP
* Test action 4: Check that vNICs of all VMs gets all addresses actually assigned
* Test action 5: Check that each VM can ping the other's v4 private address
* Test action 6: Check that each VM can ping all of the other's v6 addresses as well as the router's

If normal response code 200 is returned, the test passes. Otherwise,
the test fails with various error codes.

Post conditions
---------------

NA

---------------------------------------------------------------------
Test Case 19 - IPv6 Address Assignment - Dual Stack, DHCPv6 Stateless
---------------------------------------------------------------------

Use case specification
----------------------

tempest.scenario.test_network_v6.TestGettingAddress.test_dualnet_dhcp6_stateless_from_os

Test preconditions
------------------

1. Environment can be deployed on bare metal of virtualized infrastructure,
deployment can be HA or non-HA.
2. This test case is a scenario tests, it needs to boot virtual machines and ping6
in addition to test APIs, ping6 to vRouter is not supported by SDN controller yet,
such as Opendaylight (Boron and previous releases), so it is scenario dependent.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

* Test action 1: Create network with one IPv6 subnet in mode 'dhcpv6_stateless' and create one IPv4 subnet
* Test action 2: Boot two VMs on this network
* Test action 3: Turn on 2nd NIC for Cirros
* Test action 4: Allocate and assign two FIP4
* Test action 5: Check that vNICs of all VMs gets all addresses actually assigned
* Test action 6: Check that each VM can ping the other's v4 private address
* Test action 7: Check that each VM can ping all of the other's v6 addresses as well as the router's

If normal response code 200 is returned, the test passes. Otherwise,
the test fails with various error codes.

Post conditions
---------------

NA

----------------------------------------------------------------------------
Test Case 20 - IPv6 Address Assignment - Multiple Prefixes, DHCPv6 Stateless
----------------------------------------------------------------------------

Use case specification
----------------------

tempest.scenario.test_network_v6.TestGettingAddress.test_multi_prefix_dhcpv6_stateless

Test preconditions
------------------

1. Environment can be deployed on bare metal of virtualized infrastructure,
deployment can be HA or non-HA.
2. This test case is a scenario tests, it needs to boot virtual machines and ping6
in addition to test APIs, ping6 to vRouter is not supported by SDN controller yet,
such as Opendaylight (Boron and previous releases), so it is scenario dependent.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

* Test action 1: Create network with two IPv6 subnets in mode 'dhcpv6_stateless' and create one IPv4 subnet
* Test action 2: Boot two VMs on this network
* Test action 3: Allocate and assign two FIP4
* Test action 4: Check that vNICs of all VMs gets all addresses actually assigned
* Test action 5: Check that each VM can ping the other's v4 private address
* Test action 6: Check that each VM can ping all of the other's v6 addresses as well as the router's

If normal response code 200 is returned, the test passes. Otherwise,
the test fails with various error codes.

Post conditions
---------------

NA

----------------------------------------------------------------------------------------
Test Case 21 - IPv6 Address Assignment - Dual Stack, Multiple Prefixes, DHCPv6 Stateless
----------------------------------------------------------------------------------------

Use case specification
----------------------

tempest.scenario.test_network_v6.TestGettingAddress.test_dualnet_multi_prefix_dhcpv6_stateless

Test preconditions
------------------

1. Environment can be deployed on bare metal of virtualized infrastructure,
deployment can be HA or non-HA.
2. This test case is a scenario tests, it needs to boot virtual machines and ping6
in addition to test APIs, ping6 to vRouter is not supported by SDN controller yet,
such as Opendaylight (Boron and previous releases), so it is scenario dependent.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

* Test action 1: Create network with two IPv6 subnets in mode 'dhcpv6_stateless' and create one IPv4 subnet
* Test action 2: Boot two VMs on this network
* Test action 3: Turn on 2nd NIC for Cirros
* Test action 4: Allocate and assign two FIP4
* Test action 5: Check that vNICs of all VMs gets all addresses actually assigned
* Test action 6: Check that each VM can ping the other's v4 private address
* Test action 7: Check that each VM can ping all of the other's v6 addresses as well as the router's

If normal response code 200 is returned, the test passes. Otherwise,
the test fails with various error codes.

Post conditions
---------------

NA

----------------------------------------------
Test Case 22 - IPv6 Address Assignment - SLAAC
----------------------------------------------

Use case specification
----------------------

tempest.scenario.test_network_v6.TestGettingAddress.test_slaac_from_os

Test preconditions
------------------

1. Environment can be deployed on bare metal of virtualized infrastructure,
deployment can be HA or non-HA.
2. This test case is a scenario tests, it needs to boot virtual machines and ping6
in addition to test APIs, ping6 to vRouter is not supported by SDN controller yet,
such as Opendaylight (Boron and previous releases), so it is scenario dependent.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

* Test action 1: Create network with one IPv6 subnet in mode 'slaac' and create one IPv4 subnet
* Test action 2: Boot two VMs on this network
* Test action 3: Allocate and assign two FIP4
* Test action 4: Check that vNICs of all VMs gets all addresses actually assigned
* Test action 5: Check that each VM can ping the other's v4 private address
* Test action 6: Check that each VM can ping all of the other's v6 addresses as well as the router's

If normal response code 200 is returned, the test passes. Otherwise,
the test fails with various error codes.

Post conditions
---------------

NA

----------------------------------------------------------
Test Case 23 - IPv6 Address Assignment - Dual Stack, SLAAC
----------------------------------------------------------

Use case specification
----------------------

tempest.scenario.test_network_v6.TestGettingAddress.test_dualnet_slaac_from_os

Test preconditions
------------------

1. Environment can be deployed on bare metal of virtualized infrastructure,
deployment can be HA or non-HA.
2. This test case is a scenario tests, it needs to boot virtual machines and ping6
in addition to test APIs, ping6 to vRouter is not supported by SDN controller yet,
such as Opendaylight (Boron and previous releases), so it is scenario dependent.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

* Test action 1: Create network with one IPv6 subnet in mode 'slaac' and create one IPv4 subnet
* Test action 2: Boot two VMs on this network
* Test action 3: Turn on 2nd NIC for Cirros
* Test action 4: Allocate and assign two FIP4
* Test action 5: Check that vNICs of all VMs gets all addresses actually assigned
* Test action 6: Check that each VM can ping the other's v4 private address
* Test action 7: Check that each VM can ping all of the other's v6 addresses as well as the router's

If normal response code 200 is returned, the test passes. Otherwise,
the test fails with various error codes.

Post conditions
---------------

NA

-----------------------------------------------------------------
Test Case 24 - IPv6 Address Assignment - Multiple Prefixes, SLAAC
-----------------------------------------------------------------

Use case specification
----------------------

tempest.scenario.test_network_v6.TestGettingAddress.test_multi_prefix_slaac

Test preconditions
------------------

1. Environment can be deployed on bare metal of virtualized infrastructure,
deployment can be HA or non-HA.
2. This test case is a scenario tests, it needs to boot virtual machines and ping6
in addition to test APIs, ping6 to vRouter is not supported by SDN controller yet,
such as Opendaylight (Boron and previous releases), so it is scenario dependent.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

* Test action 1: Create network with two IPv6 subnets in mode 'slaac' and create one IPv4 subnet
* Test action 2: Boot two VMs on this network
* Test action 3: Allocate and assign two FIP4
* Test action 4: Check that vNICs of all VMs gets all addresses actually assigned
* Test action 5: Check that each VM can ping the other's v4 private address
* Test action 6: Check that each VM can ping all of the other's v6 addresses as well as the router's

If normal response code 200 is returned, the test passes. Otherwise,
the test fails with various error codes.

Post conditions
---------------

NA

-----------------------------------------------------------------------------
Test Case 25 - IPv6 Address Assignment - Dual Stack, Multiple Prefixes, SLAAC
-----------------------------------------------------------------------------

Use case specification
----------------------

tempest.scenario.test_network_v6.TestGettingAddress.test_dualnet_multi_prefix_slaac

Test preconditions
------------------

1. Environment can be deployed on bare metal of virtualized infrastructure,
deployment can be HA or non-HA.
2. This test case is a scenario tests, it needs to boot virtual machines and ping6
in addition to test APIs, ping6 to vRouter is not supported by SDN controller yet,
such as Opendaylight (Boron and previous releases), so it is scenario dependent.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

* Test action 1: Create network with two IPv6 subnets in mode 'slaac' and create one IPv4 subnet
* Test action 2: Boot two VMs on this network
* Test action 3: Turn on 2nd NIC for Cirros
* Test action 4: Allocate and assign two FIP4
* Test action 5: Check that vNICs of all VMs gets all addresses actually assigned
* Test action 6: Check that each VM can ping the other's v4 private address
* Test action 7: Check that each VM can ping all of the other's v6 addresses as well as the router's

If normal response code 200 is returned, the test passes. Otherwise,
the test fails with various error codes.

Post conditions
---------------

NA
