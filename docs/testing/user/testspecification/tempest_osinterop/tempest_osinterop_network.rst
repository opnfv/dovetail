.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Ericsson AB, Huawei Technologies Co.,Ltd

=========================================
VIM network operations test specification
=========================================

Scope
=====

The VIM network test area evaluates the ability of the system under test to support
VIM network operations. The test cases documented here are the network API test cases
in the Openstack Interop guideline 2018.11 as implemented by the Refstack client.
These test cases will evaluate basic Openstack (as a VIM) network operations including
basic CRUD operations on L2 networks, L2 network ports and security groups.

Definitions and Abbreviations
=============================

The following terms and abbreviations are used in conjunction with this test area

- API - Application Programming Interface
- CRUD - Create, Read, Update and Delete
- NFVi - Network Functions Virtualization infrastructure
- VIM - Virtual Infrastructure Manager

System Under Test (SUT)
=======================

The system under test is assumed to be the NFVi and VIM in operation on a
Pharos compliant infrastructure.

Test Area Structure
====================

The test area is structured based on VIM network operations. Each test case is able
to run independently, i.e. irrelevant of the state created by a previous test.
Specifically, every test performs clean-up operations which return the system to
the same state as before the test.

For brevity, the test cases in this test area are summarized together based on
the operations they are testing.

All these test cases are included in the test case functest.tempest.osinterop of
OVP test suite.

Test Descriptions
=================

----------------------
API Used and Reference
----------------------

Network: https://docs.openstack.org/api-ref/network/v2/index.html

- create network
- update network
- list networks
- show network details
- delete network

- create subnet
- update subnet
- list subnets
- show subnet details
- delete subnet

- create port
- bulk create ports
- update port
- list ports
- show port details
- delete port

- create security group
- update security group
- list security groups
- show security group
- delete security group

- create security group rule
- list security group rules
- show security group rule
- delete security group rule

-----------------------------------------------------------------------
Test Case 1 - Basic CRUD operations on L2 networks and L2 network ports
-----------------------------------------------------------------------

Test case specification
-----------------------

tempest.api.network.test_networks.NetworksTest.test_create_delete_subnet_with_allocation_pools
tempest.api.network.test_networks.NetworksTest.test_create_delete_subnet_with_dhcp_enabled
tempest.api.network.test_networks.NetworksTest.test_create_delete_subnet_with_gw
tempest.api.network.test_networks.NetworksTest.test_create_delete_subnet_with_gw_and_allocation_pools
tempest.api.network.test_networks.NetworksTest.test_create_delete_subnet_with_host_routes_and_dns_nameservers
tempest.api.network.test_networks.NetworksTest.test_create_delete_subnet_without_gateway
tempest.api.network.test_networks.NetworksTest.test_create_delete_subnet_all_attributes
tempest.api.network.test_networks.NetworksTest.test_create_update_delete_network_subnet
tempest.api.network.test_networks.NetworksTest.test_delete_network_with_subnet
tempest.api.network.test_networks.NetworksTest.test_external_network_visibility
tempest.api.network.test_networks.NetworksTest.test_list_networks
tempest.api.network.test_networks.NetworksTest.test_list_networks_fields
tempest.api.network.test_networks.NetworksTest.test_list_subnets
tempest.api.network.test_networks.NetworksTest.test_list_subnets_fields
tempest.api.network.test_networks.NetworksTest.test_show_network
tempest.api.network.test_networks.NetworksTest.test_show_network_fields
tempest.api.network.test_networks.NetworksTest.test_show_subnet
tempest.api.network.test_networks.NetworksTest.test_show_subnet_fields
tempest.api.network.test_networks.NetworksTest.test_update_subnet_gw_dns_host_routes_dhcp
tempest.api.network.test_ports.PortsTestJSON.test_create_bulk_port
tempest.api.network.test_ports.PortsTestJSON.test_create_port_in_allowed_allocation_pools
tempest.api.network.test_ports.PortsTestJSON.test_create_update_delete_port
tempest.api.network.test_ports.PortsTestJSON.test_list_ports
tempest.api.network.test_ports.PortsTestJSON.test_list_ports_fields
tempest.api.network.test_ports.PortsTestJSON.test_port_list_filter_by_router_id
tempest.api.network.test_ports.PortsTestJSON.test_show_port
tempest.api.network.test_ports.PortsTestJSON.test_show_port_fields

Test preconditions
------------------

Neutron is available.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: Create a network and create a subnet of this network by setting
  allocation_pools, then check the details of the subnet and delete the subnet and network
* **Test assertion 1:** The allocation_pools returned in the response equals to the one used
  to create the subnet, and the network and subnet ids are not found after deletion
* Test action 2: Create a network and create a subnet of this network by setting
  enable_dhcp "True", then check the details of the subnet and delete the subnet and network
* **Test assertion 2:** The enable_dhcp returned in the response is "True" and the network
  and subnet ids are not found after deletion
* Test action 3: Create a network and create a subnet of this network by setting
  gateway_ip, then check the details of the subnet and delete the subnet and network
* **Test assertion 3:** The gateway_ip returned in the response equals to the one used to
  create the subnet, and the network and subnet ids are not found after deletion
* Test action 4: Create a network and create a subnet of this network by setting allocation_pools
  and gateway_ip, then check the details of the subnet and delete the subnet and network
* **Test assertion 4:** The allocation_pools and gateway_ip returned in the response equal to
  the ones used to create the subnet, and the network and subnet ids are not found after deletion
* Test action 5: Create a network and create a subnet of this network by setting host_routes and
  dns_nameservers, then check the details of the subnet and delete the subnet and network
* **Test assertion 5:** The host_routes and dns_nameservers returned in the response equal to
  the ones used to create the subnet, and the network and subnet ids are not found after deletion
* Test action 6: Create a network and create a subnet of this network without setting
  gateway_ip, then delete the subnet and network
* **Test assertion 6:** The network and subnet ids are not found after deletion
* Test action 7: Create a network and create a subnet of this network by setting enable_dhcp "true",
  gateway_ip, ip_version, cidr, host_routes, allocation_pools and dns_nameservers,
  then check the details of the subnet and delete the subnet and network
* **Test assertion 7:** The values returned in the response equal to the ones used to
  create the subnet, and the network and subnet ids are not found after deletion
* Test action 8: Create a network and update this network's name, then create a subnet and update
  this subnet's name, delete the subnet and network
* **Test assertion 8:** The network's status and subnet's status are both 'ACTIVE' after creation,
  their names equal to the new names used to update, and the network and subnet ids are not
  found after deletion
* Test action 9: Create a network and create a subnet of this network, then delete this network
* **Test assertion 9:** The subnet has also been deleted after deleting the network
* Test action 10: List all external networks, find the one with the same public_network_id
  as defined in tempest.conf and list its subnets
* **Test assertion 10:** The external network can be found, no internal network got by the
  list operation, if this external network is shared, the subnets list is not empty,
  otherwise, it should be empty
* Test action 11: Create a network and list all networks
* **Test assertion 11:** The network created is found in the list
* Test action 12: Create a network and list networks with the id and name of the created network
* **Test assertion 12:** The id and name of the list network equal to the created network's id and name
* Test action 13: Create a network and create a subnet of this network, then list all subnets
* **Test assertion 13:** The subnet created is found in the list
* Test action 14: Create a network and create a subnet of this network, then list subnets with
  the id and network_id of the created subnet
* **Test assertion 14:** The id and network_id of the list subnet equal to the created subnet
* Test action 15: Create a network and show network's details with the id of the created network
* **Test assertion 15:** The id and name returned in the response equal to the created network's id and name
* Test action 16: Create a network and just show network's id and name info with the id of the created network
* **Test assertion 16:** The keys returned in the response are only id and name, and the values
  of all the keys equal to network's id and name
* Test action 17: Create a network and create a subnet of this network, then show subnet's details
  with the id of the created subnet
* **Test assertion 17:** The id and cidr info returned in the response equal to the created
  subnet's id and cidr
* Test action 18: Create a network and create a subnet of this network, then show subnet's id and
  network_id info with the id of the created subnet
* **Test assertion 18:** The keys returned in the response are just id and network_id, and the values
  of all the keys equal to subnet's id and network_id
* Test action 19: Create a network and create a subnet of this network, then update subnet's
  name, host_routes, dns_nameservers and gateway_ip
* **Test assertion 19:** The name, host_routes, dns_nameservers and gateway_ip returned in the
  response equal to the values used to update the subnet
* Test action 20: Create 2 networks and bulk create 2 ports with the ids of the created networks
* **Test assertion 20:** The network_id of each port equals to the one used to create the port and
  the admin_state_up of each port is True
* Test action 21: Create a network and create a subnet of this network by setting allocation_pools,
  then create a port with the created network's id
* **Test assertion 21:** The ip_address of the created port is in the range of the allocation_pools
* Test action 22: Create a network and create a port with its id, then update the port's name and
  set its admin_state_up to be False
* **Test assertion 22:** The name returned in the response equals to the name used to update
  the port and the port's admin_state_up is False
* Test action 23: Create a network and create a port with its id, then list all ports
* **Test assertion 23:** The created port is found in the list
* Test action 24: Create a network and create a port with its id, then list ports with the id
  and mac_address of the created port
* **Test assertion 24:** The created port is found in the list
* Test action 25: Create a network and create a subnet, port with its id, create a router
  and add this port as this router's interface, then list ports with this router id
* **Test assertion 25:** The number of the ports list is 1, the port id and device_id
  getting with the list operation are the same as the ones got when creating them
* Test action 26: Create a network and create a port with its id, then show the port's details
* **Test assertion 26:** The key 'id' is in the details
* Test action 27: Create a network and create a port with its id, then show the port's id
  and mac_address info with the port's id
* **Test assertion 27:** The keys returned in the response are just id and mac_address,
  and the values of all the keys equal to port's id and mac_address

Pass / Fail criteria
''''''''''''''''''''

These test cases evaluate the ability of basic CRUD operations on L2 networks and L2 network ports.
Specifically it verifies that:

* Subnets can be created successfully by setting different parameters.
* Subnets can be updated after being created.
* Ports can be bulk created with network ids.
* Port's security group(s) can be updated after being created.
* Networks/subnets/ports can be listed with their ids and other parameters.
* All details or special fields' info of networks/subnets/ports can be shown with their ids.
* Networks/subnets/ports can be successfully deleted.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A

------------------------------------------------------
Test Case 2 - Basic CRUD operations on security groups
------------------------------------------------------

Test case specification
-----------------------

tempest.api.network.test_security_groups.SecGroupTest.test_create_list_update_show_delete_security_group
tempest.api.network.test_security_groups.SecGroupTest.test_create_security_group_rule_with_additional_args
tempest.api.network.test_security_groups.SecGroupTest.test_create_security_group_rule_with_icmp_type_code
tempest.api.network.test_security_groups.SecGroupTest.test_create_security_group_rule_with_protocol_integer_value
tempest.api.network.test_security_groups.SecGroupTest.test_create_security_group_rule_with_remote_group_id
tempest.api.network.test_security_groups.SecGroupTest.test_create_security_group_rule_with_remote_ip_prefix
tempest.api.network.test_security_groups.SecGroupTest.test_create_show_delete_security_group_rule
tempest.api.network.test_security_groups.SecGroupTest.test_list_security_groups
tempest.api.network.test_security_groups_negative.NegativeSecGroupTest.test_create_additional_default_security_group_fails
tempest.api.network.test_security_groups_negative.NegativeSecGroupTest.test_create_duplicate_security_group_rule_fails
tempest.api.network.test_security_groups_negative.NegativeSecGroupTest.test_create_security_group_rule_with_bad_ethertype
tempest.api.network.test_security_groups_negative.NegativeSecGroupTest.test_create_security_group_rule_with_bad_protocol
tempest.api.network.test_security_groups_negative.NegativeSecGroupTest.test_create_security_group_rule_with_bad_remote_ip_prefix
tempest.api.network.test_security_groups_negative.NegativeSecGroupTest.test_create_security_group_rule_with_invalid_ports
tempest.api.network.test_security_groups_negative.NegativeSecGroupTest.test_create_security_group_rule_with_non_existent_remote_groupid
tempest.api.network.test_security_groups_negative.NegativeSecGroupTest.test_create_security_group_rule_with_non_existent_security_group
tempest.api.network.test_security_groups_negative.NegativeSecGroupTest.test_delete_non_existent_security_group
tempest.api.network.test_security_groups_negative.NegativeSecGroupTest.test_show_non_existent_security_group
tempest.api.network.test_security_groups_negative.NegativeSecGroupTest.test_show_non_existent_security_group_rule

Test preconditions
------------------

Neutron is available.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: Create a security group SG1, list all security groups, update the name and description
  of SG1, show details of SG1 and delete SG1
* **Test assertion 1:** SG1 is in the list, the name and description of SG1 equal to the ones used to
  update it, the name and description of SG1 shown in the details equal to the ones used to update it,
  and SG1's id is not found after deletion
* Test action 2: Create a security group SG1, and create a rule with protocol 'tcp',
  port_range_min and port_range_max
* **Test assertion 2:** The values returned in the response equal to the ones used to create the rule
* Test action 3: Create a security group SG1, and create a rule with protocol 'icmp' and icmp_type_codes
* **Test assertion 3:** The values returned in the response equal to the ones used to create the rule
* Test action 4: Create a security group SG1, and create a rule with protocol '17'
* **Test assertion 4:** The values returned in the response equal to the ones used to create the rule
* Test action 5: Create a security group SG1, and create a rule with protocol 'udp', port_range_min,
  port_range_max and remote_group_id
* **Test assertion 5:** The values returned in the response equal to the ones used to create the rule
* Test action 6: Create a security group SG1, and create a rule with protocol 'tcp', port_range_min,
  port_range_max and remote_ip_prefix
* **Test assertion 6:** The values returned in the response equal to the ones used to create the rule
* Test action 7: Create a security group SG1, create 3 rules with protocol 'tcp', 'udp' and 'icmp'
  respectively, show details of each rule, list all rules and delete all rules
* **Test assertion 7:** The values in the shown details equal to the ones used to create the rule,
  all rules are found in the list, and all rules are not found after deletion
* Test action 8: List all security groups
* **Test assertion 8:** There is one default security group in the list
* Test action 9: Create a security group whose name is 'default'
* **Test assertion 9:** Failed to create this security group because of name conflict
* Test action 10: Create a security group SG1, create a rule with protocol 'tcp', port_range_min
  and port_range_max, and create another tcp rule with the same parameters
* **Test assertion 10:** Failed to create this security group rule because of duplicate protocol
* Test action 11: Create a security group SG1, and create a rule with ethertype 'bad_ethertype'
* **Test assertion 11:** Failed to create this security group rule because of bad ethertype
* Test action 12: Create a security group SG1, and create a rule with protocol 'bad_protocol_name'
* **Test assertion 12:** Failed to create this security group rule because of bad protocol
* Test action 13: Create a security group SG1, and create a rule with remote_ip_prefix '92.168.1./24',
  '192.168.1.1/33', 'bad_prefix' and '256' respectively
* **Test assertion 13:** Failed to create these security group rules because of bad remote_ip_prefix
* Test action 14: Create a security group SG1, and create a tcp rule with (port_range_min, port_range_max)
  (-16, 80), (80, 79), (80, 65536), (None, 6) and (-16, 65536) respectively
* **Test assertion 14:** Failed to create these security group rules because of bad ports
* Test action 15: Create a security group SG1, and create a tcp rule with remote_group_id 'bad_group_id'
  and a random uuid respectively
* **Test assertion 15:** Failed to create these security group rules because of nonexistent remote_group_id
* Test action 16: Create a security group SG1, and create a rule with a random uuid as security_group_id
* **Test assertion 16:** Failed to create these security group rules because of nonexistent security_group_id
* Test action 17: Generate a random uuid and use this id to delete security group
* **Test assertion 17:** Failed to delete security group because of nonexistent security_group_id
* Test action 18: Generate a random uuid and use this id to show security group
* **Test assertion 18:** Failed to show security group because of nonexistent id of security group
* Test action 19: Generate a random uuid and use this id to show security group rule
* **Test assertion 19:** Failed to show security group rule because of nonexistent id of security group rule

Pass / Fail criteria
''''''''''''''''''''

These test cases evaluate the ability of Basic CRUD operations on security groups and security group rules.
Specifically it verifies that:

* Security groups can be created, list, updated, shown and deleted.
* Security group rules can be created with different parameters, list, shown and deleted.
* Cannot create an additional default security group.
* Cannot create a duplicate security group rules.
* Cannot create security group rules with bad ethertype, protocol, remote_ip_prefix, ports,
  remote_group_id and security_group_id.
* Cannot show or delete security groups or security group rules with nonexistent ids.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A

---------------------------------------------
Test Case 3 - CRUD operations on subnet pools
---------------------------------------------

Test case specification
-----------------------

tempest.api.network.test_subnetpools_extensions.SubnetPoolsTestJSON.test_create_list_show_update_delete_subnetpools

Test preconditions
------------------

Neutron is available.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: Create a subnetpool SNP1 with a specific name and get the name from the response body
* **Test assertion 1:** The name got from the body is the same as the name used to create SNP1
* Test action 2: Show SNP1 and get the name from the response body
* **Test assertion 2:** The name got from the body is the same as the name used to create SNP1
* Test action 3: Update the name of SNP1 and get the new name from the response body
* **Test assertion 3:** The name got from the body is the same as the name used to update SNP1
* Test action 4: Delete SNP1


Pass / Fail criteria
''''''''''''''''''''

These test cases evaluate the ability of Basic CRUD operations on subnetpools.
Specifically it verifies that:

* Subnetpools can be created, updated, shown and deleted.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A

----------------------------------------
Test Case 4 - CRUD operations on routers
----------------------------------------

Test case specification
-----------------------

tempest.api.network.test_routers.RoutersTest.test_add_multiple_router_interfaces
tempest.api.network.test_routers.RoutersTest.test_add_remove_router_interface_with_port_id
tempest.api.network.test_routers.RoutersTest.test_add_remove_router_interface_with_subnet_id
tempest.api.network.test_routers.RoutersTest.test_create_show_list_update_delete_router
tempest.api.network.test_routers.RoutersTest.test_update_delete_extra_route
tempest.api.network.test_routers.RoutersTest.test_update_router_admin_state
tempest.api.network.test_routers_negative.RoutersNegativeTest.test_add_router_interfaces_on_overlapping_subnets_returns_400
tempest.api.network.test_routers_negative.RoutersNegativeTest.test_delete_non_existent_router_returns_404
tempest.api.network.test_routers_negative.RoutersNegativeTest.test_router_add_gateway_invalid_network_returns_404
tempest.api.network.test_routers_negative.RoutersNegativeTest.test_router_add_gateway_net_not_external_returns_400
tempest.api.network.test_routers_negative.RoutersNegativeTest.test_router_remove_interface_in_use_returns_409
tempest.api.network.test_routers_negative.RoutersNegativeTest.test_show_non_existent_router_returns_404
tempest.api.network.test_routers_negative.RoutersNegativeTest.test_update_non_existent_router_returns_404

Test preconditions
------------------

Neutron is available.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: Create 2 networks NET1 and NET2, create SubNet1 of NET1 and SubNet2 with cidr of NET2,
  create a router R1, add SubNet1 and SubNet2 to be R1's interfaces and get port details
* **Test assertion 1:** The device_id and subnet_id of the port equals to the router id
  and subnet id getting from the creating response body
* Test action 2: Create a network NET1, create SubNet1 of NET1, create P1 of NET1, create a router R1,
  add P1 to be its interface, store the response body B1, show P1 and store the response body B2 and
  remove the interface with port id
* **Test assertion 2:** B1 includes keys 'subnet_id' and 'port_id', 'device_id' of B2 equals to router id
* Test action 3: Create a network NET1, create SubNet1 of NET1, create a router R1, add SubNet1 to be its
  interface, store the response body B1, show port details with 'port_id' in B1
* **Test assertion 3:** B1 includes keys 'subnet_id' and 'port_id', 'device_id' equals to router id
* Test action 4: Create a router R1 with name, admin_state_up False and external_network_id Ext-Net,
  store the request body B1, show R1 with 'id' in B1, list all routers, update R1's name
* **Test assertion 4:** 'name', 'admin_state_up' and 'network_id' in B1 equal to the name, False and Ext-Net,
  'name' in show details equals to 'name' in B1, 'network_id' in show details equals to Ext-Net,
  R1 is in the router list, the 'name' has been updated
* Test action 5: Create a router R1 with admin_state_up=True, create 4 networks and 4 subnets with different
  cidr, add these 4 subnets to R1 as its interfaces, update R1 by given routes and show R1, delete extra
  route of R1 and then show R1
* **Test assertion 5:** The number of routes queals to 4 and routes is empty after deletion
* Test action 6: Create a router R1, update 'admin_state_up' of R1 to be True
* **Test assertion 6:** 'admin_state_up' of R1 is False, 'admin_state_up' of R1 is True after updating
* Test action 7: Create 2 networks NET1 and NET2, create SubNet1 of NET1 and SubNet2 of NET2,
  create a router R1, add SubNet1 to be R1's interface and then trying to add SubNet2 to be R1's interface
* **Test assertion 7:** It raises a BadRequest exception when trying to add SubNet2
* Test action 8: Try to delete router with a random name
* **Test assertion 8:** It raises a NotFound exception when trying delete operation
* Test action 9: Create a router R1 and try to update it with wrong external_gateway_info
* **Test assertion 9:** It raises a NotFound exception when trying to update R1
* Test action 10: Create an internal network NET1, create SubNet1 with cidr of NET1,
  create a router R1 and try to update it with NET1 as external_gateway_info
* **Test assertion 10:** It raises a BadRequest exception when trying to update R1
* Test action 11: Create a network NET1, create SubNet1 of NET1, create a router R1, add SubNet1 to
  the interface of R1 and try to delete R1
* **Test assertion 11:** It raises a Conflict exception when trying to delete R1
* Test action 12: Try to show router with a random name
* **Test assertion 12:** It raises a NotFound exception when trying to show router
* Test action 13: Try to update router with a random name
* **Test assertion 13:** It raises a NotFound exception when trying to update router


Pass / Fail criteria
''''''''''''''''''''

These test cases evaluate the ability of Basic CRUD operations on routers.
Specifically it verifies that:

* Routers can be created, updated, shown and deleted.
* Can not show, update and delete non existent router.
* Can not remove interface in use.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A

----------------------------------------------
Test Case 5 - List versions within Network API
----------------------------------------------

Test case specification
-----------------------

tempest.api.network.test_versions.NetworksApiDiscovery.test_api_version_resources

Test preconditions
------------------

Neutron is available.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: List network API versions
* **Test assertion 1:** The network API version is 'v2.0'

Pass / Fail criteria
''''''''''''''''''''

This test case evaluates the ability of listing network API versions.
Specifically it verifies that:

* The network API version is 'v2.0'.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A
