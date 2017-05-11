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

The IPv6 compliance test area will evaluate the ability for a SUT to support IPv6
Tenant Network features and functionality.

References
================

- OPNFV IPv6 project

  - https://wiki.opnfv.org/display/ipv6/IPv6+Home

- upstream openstack api reference

  - http://developer.openstack.org/api-ref

Definitions and abbreviations
=============================

The following terms and abbreviations are used in conjunction with this test area

- CIDR - Classless Inter-Domain Routing
- DHCP - Dynamic Host Configuration Protocol
- DHCPv6 - Dynamic Host Configuration Protocol version 6
- ICMP - Internet Control Message Protocol
- NFVI - Network Functions Virtualization Infrastructure
- NIC - Network Interface Controller
- SDN - Software Defined Network
- SLAAC - Stateless Address Auto Configuration
- TCP - Transmission Control Protocol
- UDP - User Datagram Protocol
- VM - Virtual Machine
- vNIC - virtual Network Interface Card

System Under Test (SUT)
=======================

The system under test is assumed to be the NFVI and VIM deployed with a Pharos compliant infrastructure.

Test Area Structure
====================

The test area is structured based on network, port and subnet operations. Each test case
is able to run independently, i.e. irrelevant of the state created by a previous test.

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

This test case can run in environment deployed on bare metal or virtualized
infrastructure.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
'''''''''''''''

* Test action 1: Create/delete network, create 2 networks in one request,
  asserting that the networks are found in the list after creation
* Test action 2: Create/delete subnet, create 2 subnets in one request,
  asserting that the subnets are found in the list after creation
* Test action 3: Create/delete port, create 2 ports in one request,
  asserting that the ports are found in the list after creation

Pass / fail criteria
'''''''''''''''''''''

The pass criteria for this test case is that all instructions are able to be carried out
according to the described behaviour without deviation.
A negative result will be generated if the above is not met in completion.

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

This test case can run in environment deployed on bare metal or virtualized
infrastructure.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
'''''''''''''''

* Test action 1: Create a network
* Test action 2: Update the name of this network
* Test action 3: Verify network's name has been updated
* Test action 4: Find a CIDR that is not in use yet and create a subnet with it
* Test action 5: Update the name of this subnet
* Test action 6: Verify subnet's name has been update
* Test action 7: Delete the subnet and network

Pass / fail criteria
'''''''''''''''''''''

The pass criteria for this test case is that all instructions are able to be carried out
according to the described behaviour without deviation.
A negative result will be generated if the above is not met in completion.

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

This test case can run in environment deployed on bare metal or virtualized
infrastructure.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
'''''''''''''''

* Test action 1: List all external networks
* Test action 2: Check if external networks found in the listed networks
* Test action 3: Check if no non-external networks found in the listed networks
* Test action 4: Check if the public network found in the listed networks
* Test action 5: List public network's subnets
* Test action 6: Check if the subnet list is empty

Pass / fail criteria
'''''''''''''''''''''

The pass criteria for this test case is that all instructions are able to be carried out
according to the described behaviour without deviation.
A negative result will be generated if the above is not met in completion.

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

This test case can run in environment deployed on bare metal or virtualized
infrastructure.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
'''''''''''''''

* Test action 1: Create a network
* Test action 2: Verify the created network exists in the list of all networks
* Test action 3: Create a subnet of this network with the last subnet block
* Test action 4: Verify the created subnet exists in the list of all subnets
* Test action 5: Delete the network and subnet

Pass / fail criteria
''''''''''''''''''''

The pass criteria for this test case is that all instructions are able to be carried out
according to the described behaviour without deviation.
A negative result will be generated if the above is not met in completion.

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

This test case can run in environment deployed on bare metal or virtualized
infrastructure.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
'''''''''''''''

* Test action 1: Create a network
* Test action 2: List all networks
* Test action 3: Verify the id and name of the created network exist in the list
* Test action 4: Create a subnet of this network
* Test action 5: Show the details of this created subnet
* Test action 6: Verify the id and CIDR shown are equal with the created subnet
* Test action 7: Delete the network and subnet

Pass / fail criteria
'''''''''''''''''''''

The pass criteria for this test case is that all instructions are able to be carried out
according to the described behaviour without deviation.
A negative result will be generated if the above is not met in completion.

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

This test case can run in environment deployed on bare metal or virtualized
infrastructure.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
'''''''''''''''

* Test action 1: Create a network
* Test action 2: Get allocation pools
* Test action 3: Create a subnet of the created network within allocation pools
* Test action 4: Create a port of the created network
* Test action 5: Verify the port's ip is in the range of allocation pools
* Test action 6: Delete the created network, subnet and port

Pass / fail criteria
'''''''''''''''''''''

The pass criteria for this test case is that all instructions are able to be carried out
according to the described behaviour without deviation.
A negative result will be generated if the above is not met in completion.

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

This test case can run in environment deployed on bare metal or virtualized
infrastructure.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
'''''''''''''''

* Test action 1: Create a network
* Test action 2: Create a subnet of this created network
* Test action 3: Create a port of this created network without security group
* Test action 4: Verify the security group of the port is empty
* Test action 5: Delete the created network, subnet and port

Pass / fail criteria
'''''''''''''''''''''

The pass criteria for this test case is that all instructions are able to be carried out
according to the described behaviour without deviation.
A negative result will be generated if the above is not met in completion.

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

This test case can run in environment deployed on bare metal or virtualized
infrastructure.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
'''''''''''''''

* Test action 1: Create a network and a port of it
* Test action 2: Check if the port's admin_state_up is True
* Test action 3: Update the port's name
* Test action 4: Verify the port's name has been updated
* Test action 5: Check if the port's admin_state_up is False
* Test action 6: Delete the network and port

Pass / fail criteria
''''''''''''''''''''

The pass criteria for this test case is that all instructions are able to be carried out
according to the described behaviour without deviation.
A negative result will be generated if the above is not met in completion.

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

This test case can run in environment deployed on bare metal or virtualized
infrastructure.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
'''''''''''''''

* Test action 1: Create a network and a port of it
* Test action 2: List all ports
* Test action 3: Verify the port exists in the list of all ports
* Test action 4: Delete the network and port

Pass / fail criteria
'''''''''''''''''''''

The pass criteria for this test case is that all instructions are able to be carried out
according to the described behaviour without deviation.
A negative result will be generated if the above is not met in completion.

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

This test case can run in environment deployed on bare metal or virtualized
infrastructure.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
'''''''''''''''

* Test action 1: Create a network and a port of it
* Test action 2: Show the details of this created port
* Test action 3: Check if the created port's id exists in the details
* Test action 4: Check if the details shown are the same as the created port except
  the values of the key 'extra_dhcp_opts', 'created_at' and 'updated_at'
* Test action 5: Delete the network and port

Pass / fail criteria
'''''''''''''''''''''

The pass criteria for this test case is that all instructions are able to be carried out
according to the described behaviour without deviation.
A negative result will be generated if the above is not met in completion.

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

This test case can run in environment deployed on bare metal or virtualized
infrastructure.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
'''''''''''''''

* Test action 1: Create networks named network01 and network02
* Test action 2: Create subnet01 in network01, subnet02 in network02 with CIDR
* Test action 3: Create router
* Test action 4: Create interface01 with subnet01 and router
* Test action 5: Verify interface01 exists
* Test action 6: Create interface02 with subnet02 and router
* Test action 7: Verify interface02 exists
* Test action 8: Delete the networks, subnets, router and interfaces

Pass / fail criteria
'''''''''''''''''''''

The pass criteria for this test case is that all instructions are able to be carried out
according to the described behaviour without deviation.
A negative result will be generated if the above is not met in completion.

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

This test case can run in environment deployed on bare metal or virtualized
infrastructure.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
'''''''''''''''

* Test action 1: Create a network, a subnet, a router and a port
* Test action 2: Add router interface to port created
* Test action 3: Verify the interface's keys include 'subnet_id'
* Test action 4: Verify the interface's keys include 'port_id'
* Test action 5: Verify router id is equal to device id in port details
* Test action 6: Delete the network, subnet, router and port

Pass / fail criteria
'''''''''''''''''''''

The pass criteria for this test case is that all instructions are able to be carried out
according to the described behaviour without deviation.
A negative result will be generated if the above is not met in completion.

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

This test case can run in environment deployed on bare metal or virtualized
infrastructure.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
'''''''''''''''

* Test action 1: Create a network, a subnet and a router
* Test action 2: Add a router interface with the router id and subnet id
* Test action 3: Verify the interface's keys are include 'subnet_id'
* Test action 4: Verify the interface's keys are include 'port_id'
* Test action 5: Verify router id is equal to device id in port details
* Test action 6: Delete the network, subnet and router

Pass / fail criteria
''''''''''''''''''''

The pass criteria for this test case is that all instructions are able to be carried out
according to the described behaviour without deviation.
A negative result will be generated if the above is not met in completion.

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

This test case can run in environment deployed on bare metal or virtualized
infrastructure.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
'''''''''''''''

* Test action 1: Create a router, set the admin_state_up to be False,
  and external_network_id to be public network id
* Test action 2: Check if the router's admin_state_up is False
* Test action 3: Check if the router's external network id is the public network id
* Test action 4: Show details of the created router
* Test action 5: Check if the router's name shown is the same as the router created
* Test action 6: List all routers and verify if created router is there in response
* Test action 7: Update the name of router and verify if it is updated
* Test action 8: Delete the router

Pass / fail criteria
'''''''''''''''''''''

The pass criteria for this test case is that all instructions are able to be carried out
according to the described behaviour without deviation.
A negative result will be generated if the above is not met in completion.

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

This test case can run in environment deployed on bare metal or virtualized
infrastructure.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
'''''''''''''''

* Test action 1: Create a security group
* Test action 2: List security groups and verify if created security group is there in response
* Test action 3: Update the name and description of this security group
* Test action 4: Verify if security group is updated
* Test action 5: Show details (the name and description) of the updated security group
* Test action 6: Delete the security group

Pass / fail criteria
''''''''''''''''''''

The pass criteria for this test case is that all instructions are able to be carried out
according to the described behaviour without deviation.
A negative result will be generated if the above is not met in completion.

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

This test case can run in environment deployed on bare metal or virtualized
infrastructure.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
'''''''''''''''

* Test action 1: Create a security group
* Test action 2: Create rules for protocol tcp, udp and icmp
* Test action 3: Show details of the created security rule
* Test action 4: List rules and verify created rule is in response
* Test action 5: Delete the security group and security group rules

Pass / fail criteria
'''''''''''''''''''''

The pass criteria for this test case is that all instructions are able to be carried out
according to the described behaviour without deviation.
A negative result will be generated if the above is not met in completion.

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

This test case can run in environment deployed on bare metal or virtualized
infrastructure.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
'''''''''''''''

* Test action 1: List all security group
* Test action 2: Verify the default security group exists in the list

Pass / fail criteria
'''''''''''''''''''''

The pass criteria for this test case is that all instructions are able to be carried out
according to the described behaviour without deviation.
A negative result will be generated if the above is not met in completion.

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

1. This test case can run in environment deployed on bare metal or virtualized
infrastructure.
2. This test case in test_network_v6 file validates one use-case where they
try to ping6 to the router internal interface. For Opendaylight Boron release,
it supports IPv6 IPAM (IPAddress Assignment), IPv6 Security Groups,
IPv6 east-west routing. However, For Opendaylight Boron
and earlier releases, support for IPv6 north-south communication and ping6 router
support for Openstack Neutron router-interface are not ready, so this case
should run on none SDN controller deployment.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
'''''''''''''''

* Test action 1: Create network with one IPv6 subnet in mode 'dhcpv6_stateless' and create one IPv4 subnet
* Test action 2: Boot two VMs on this network
* Test action 3: Allocate and assign two IPv4 floating IP
* Test action 4: Check that vNICs of all VMs gets all addresses actually assigned
* Test action 5: Check that each VM can ping the other's v4 private address
* Test action 6: Check that each VM can ping all of the other's v6 addresses as well as the router's
* Test action 7: Delete the network and VMs

Pass / fail criteria
'''''''''''''''''''''

The pass criteria for this test case is that all instructions are able to be carried out
according to the described behaviour without deviation.
A negative result will be generated if the above is not met in completion.

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

1. This test case can run in environment deployed on bare metal or virtualized
infrastructure.
2. This test case in test_network_v6 file validates one use-case where they
try to ping6 to the router internal interface. For Opendaylight Boron release,
it supports IPv6 IPAM (IPAddress Assignment), IPv6 Security Groups,
IPv6 east-west routing. However, For Opendaylight Boron
and earlier releases, support for IPv6 north-south communication and ping6 router
support for Openstack Neutron router-interface are not ready, so this case
should run on none SDN controller deployment.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
'''''''''''''''

* Test action 1: Create network with one IPv6 subnet in mode 'dhcpv6_stateless' and create one IPv4 subnet
* Test action 2: Boot two VMs on this network
* Test action 3: Turn on 2nd NIC for Cirros
* Test action 4: Allocate and assign two FIP4
* Test action 5: Check that vNICs of all VMs gets all addresses actually assigned
* Test action 6: Check that each VM can ping the other's v4 private address
* Test action 7: Check that each VM can ping all of the other's v6 addresses as well as the router's
* Test action 8: Delete the network and VMs

Pass / fail criteria
''''''''''''''''''''

The pass criteria for this test case is that all instructions are able to be carried out
according to the described behaviour without deviation.
A negative result will be generated if the above is not met in completion.

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

1. This test case can run in environment deployed on bare metal or virtualized
infrastructure.
2. This test case in test_network_v6 file validates one use-case where they
try to ping6 to the router internal interface. For Opendaylight Boron release,
it supports IPv6 IPAM (IPAddress Assignment), IPv6 Security Groups,
IPv6 east-west routing. However, For Opendaylight Boron
and earlier releases, support for IPv6 north-south communication and ping6 router
support for Openstack Neutron router-interface are not ready, so this case
should run on none SDN controller deployment.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
'''''''''''''''

* Test action 1: Create network with two IPv6 subnets in mode 'dhcpv6_stateless' and create one IPv4 subnet
* Test action 2: Boot two VMs on this network
* Test action 3: Allocate and assign two FIP4
* Test action 4: Check that vNICs of all VMs gets all addresses actually assigned
* Test action 5: Check that each VM can ping the other's v4 private address
* Test action 6: Check that each VM can ping all of the other's v6 addresses as well as the router's
* Test action 7: Delete the network and VMs

Pass / fail criteria
'''''''''''''''''''''

The pass criteria for this test case is that all instructions are able to be carried out
according to the described behaviour without deviation.
A negative result will be generated if the above is not met in completion.

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

1. This test case can run in environment deployed on bare metal or virtualized
infrastructure.
2. This test case in test_network_v6 file validates one use-case where they
try to ping6 to the router internal interface. For Opendaylight Boron release,
it supports IPv6 IPAM (IPAddress Assignment), IPv6 Security Groups,
IPv6 east-west routing. However, For Opendaylight Boron
and earlier releases, support for IPv6 north-south communication and ping6 router
support for Openstack Neutron router-interface are not ready, so this case
should run on none SDN controller deployment.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
'''''''''''''''

* Test action 1: Create network with two IPv6 subnets in mode 'dhcpv6_stateless' and create one IPv4 subnet
* Test action 2: Boot two VMs on this network
* Test action 3: Turn on 2nd NIC for Cirros
* Test action 4: Allocate and assign two FIP4
* Test action 5: Check that vNICs of all VMs gets all addresses actually assigned
* Test action 6: Check that each VM can ping the other's v4 private address
* Test action 7: Check that each VM can ping all of the other's v6 addresses as well as the router's
* Test action 8: Delete the network and VMs

Pass / fail criteria
'''''''''''''''''''''

The pass criteria for this test case is that all instructions are able to be carried out
according to the described behaviour without deviation.
A negative result will be generated if the above is not met in completion.

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

1. This test case can run in environment deployed on bare metal or virtualized
infrastructure.
2. This test case in test_network_v6 file validates one use-case where they
try to ping6 to the router internal interface. For Opendaylight Boron release,
it supports IPv6 IPAM (IPAddress Assignment), IPv6 Security Groups,
IPv6 east-west routing. However, For Opendaylight Boron
and earlier releases, support for IPv6 north-south communication and ping6 router
support for Openstack Neutron router-interface are not ready, so this case
should run on none SDN controller deployment.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
'''''''''''''''

* Test action 1: Create network with one IPv6 subnet in mode 'slaac' and create one IPv4 subnet
* Test action 2: Boot two VMs on this network
* Test action 3: Allocate and assign two FIP4
* Test action 4: Check that vNICs of all VMs gets all addresses actually assigned
* Test action 5: Check that each VM can ping the other's v4 private address
* Test action 6: Check that each VM can ping all of the other's v6 addresses as well as the router's
* Test action 7: Delete the network and VMs

Pass / fail criteria
'''''''''''''''''''''

The pass criteria for this test case is that all instructions are able to be carried out
according to the described behaviour without deviation.
A negative result will be generated if the above is not met in completion.

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

1. This test case can run in environment deployed on bare metal or virtualized
infrastructure.
2. This test case in test_network_v6 file validates one use-case where they
try to ping6 to the router internal interface. For Opendaylight Boron release,
it supports IPv6 IPAM (IPAddress Assignment), IPv6 Security Groups,
IPv6 east-west routing. However, For Opendaylight Boron
and earlier releases, support for IPv6 north-south communication and ping6 router
support for Openstack Neutron router-interface are not ready, so this case
should run on none SDN controller deployment.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
'''''''''''''''

* Test action 1: Create network with one IPv6 subnet in mode 'slaac' and create one IPv4 subnet
* Test action 2: Boot two VMs on this network
* Test action 3: Turn on 2nd NIC for Cirros
* Test action 4: Allocate and assign two FIP4
* Test action 5: Check that vNICs of all VMs gets all addresses actually assigned
* Test action 6: Check that each VM can ping the other's v4 private address
* Test action 7: Check that each VM can ping all of the other's v6 addresses as well as the router's
* Test action 8: Delete the network and VMs

Pass / fail criteria
'''''''''''''''''''''

The pass criteria for this test case is that all instructions are able to be carried out
according to the described behaviour without deviation.
A negative result will be generated if the above is not met in completion.

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

1. This test case can run in environment deployed on bare metal or virtualized
infrastructure.
2. This test case in test_network_v6 file validates one use-case where they
try to ping6 to the router internal interface. For Opendaylight Boron release,
it supports IPv6 IPAM (IPAddress Assignment), IPv6 Security Groups,
IPv6 east-west routing. However, For Opendaylight Boron
and earlier releases, support for IPv6 north-south communication and ping6 router
support for Openstack Neutron router-interface are not ready, so this case
should run on none SDN controller deployment.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
'''''''''''''''

* Test action 1: Create network with two IPv6 subnets in mode 'slaac' and create one IPv4 subnet
* Test action 2: Boot two VMs on this network
* Test action 3: Allocate and assign two FIP4
* Test action 4: Check that vNICs of all VMs gets all addresses actually assigned
* Test action 5: Check that each VM can ping the other's v4 private address
* Test action 6: Check that each VM can ping all of the other's v6 addresses as well as the router's
* Test action 7: Delete the network and VMs

Pass / fail criteria
'''''''''''''''''''''

The pass criteria for this test case is that all instructions are able to be carried out
according to the described behaviour without deviation.
A negative result will be generated if the above is not met in completion.

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

1. This test case can run in environment deployed on bare metal or virtualized
infrastructure.
2. This test case in test_network_v6 file validates one use-case where they
try to ping6 to the router internal interface. For Opendaylight Boron release,
it supports IPv6 IPAM (IPAddress Assignment), IPv6 Security Groups,
IPv6 east-west routing. However, For Opendaylight Boron
and earlier releases, support for IPv6 north-south communication and ping6 router
support for Openstack Neutron router-interface are not ready, so this case
should run on none SDN controller deployment.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
'''''''''''''''

* Test action 1: Create network with two IPv6 subnets in mode 'slaac' and create one IPv4 subnet
* Test action 2: Boot two VMs on this network
* Test action 3: Turn on 2nd NIC for Cirros
* Test action 4: Allocate and assign two FIP4
* Test action 5: Check that vNICs of all VMs gets all addresses actually assigned
* Test action 6: Check that each VM can ping the other's v4 private address
* Test action 7: Check that each VM can ping all of the other's v6 addresses as well as the router's
* Test action 8: Delete the network and VMs

Pass / fail criteria
'''''''''''''''''''''

The pass criteria for this test case is that all instructions are able to be carried out
according to the described behaviour without deviation.
A negative result will be generated if the above is not met in completion.

Post conditions
---------------

NA

