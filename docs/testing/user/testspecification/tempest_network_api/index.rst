.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Ericsson AB

===========================================
Tempest Network API test specification
===========================================


Scope
=====

The Tempest Network API test area tests the basic operations of the System Under
Test (SUT) through the life of a VNF.
The tests in this test area will evaluate IPv4 network runtime operations
functionality.

These runtime operations may include that create, list, verify or delete:

- Floating IP
- Network
- Subnet
- Port
- External Network Visibility
- Router
- Subnetpools
- API Version Resources

References
==========

`Networks: <https://developer.openstack.org/api-ref/network/v2/#networks>`_

- create network
- delete network

`Routers and interface: <https://developer.openstack.org/api-ref/networking/v2/index.html#routers-routers>`_

- create router
- update router
- delete router
- add interface to router

`Subnets: <https://developer.openstack.org/api-ref/networking/v2/index.html#subnets>`_

- create subnet
- update subnet
- delete subnet

`Subnetpools: <https://developer.openstack.org/api-ref/network/v2/#subnet-pools-extension-subnetpools>`_

- create subnetpool
- update subnetpool
- delete subnetpool

`Ports: <https://developer.openstack.org/api-ref/networking/v2/index.html#ports>`_

- create port
- update port
- delete port

`Floating IPs: <https://developer.openstack.org/api-ref/networking/v2/index.html#floating-ips-floatingips>`_

- create floating IP
- delete floating IP

`Api Versions <https://developer.openstack.org/api-ref/network/v2/#api-versions>`_

- list version
- show version

System Under Test (SUT)
=======================

The system under test is assumed to be the NFVi and VIM in operation on a
Pharos compliant infrastructure.

Test Area Structure
===================

The test area is structured in individual tests as listed below.
For detailed information on the individual steps and assertions performed
by the tests, review the Python source code accessible via the following links:

All these test cases are included in the test case dovetail.tempest.network of
OVP test suite.


`List, Show and Verify the Details of the Available Extensions <https://github.com/openstack/tempest/blob/master/tempest/api/network/test_extensions.py>`_
    - tempest.api.network.test_extensions.ExtensionsTestJSON.test_list_show_extensions

`Floating IP tests <https://github.com/openstack/tempest/blob/master/tempest/api/network/test_floating_ips.py>`_
    - Create a Floating IP
    - Update a Floating IP
    - Delete a Floating IP
    - List all Floating IPs
    - Show Floating IP Details
    - Associate a Floating IP with a Port and then Delete that Port
    - Associate a Floating IP with a Port and then with a Port on Another Router

- tempest.api.network.test_floating_ips.FloatingIPTestJSON.test_create_floating_ip_specifying_a_fixed_ip_address
- tempest.api.network.test_floating_ips.FloatingIPTestJSON.test_create_list_show_update_delete_floating_ip

`Network tests <https://github.com/openstack/tempest/blob/master/tempest/api/network/test_networks.py#L405>`_
    - Bulk Network Creation & Deletion
    - Bulk Subnet Create & Deletion
    - Bulk Port Creation & Deletion
    - List Project's Networks

- tempest.api.network.test_networks.BulkNetworkOpsTest.test_bulk_create_delete_network
- tempest.api.network.test_networks.BulkNetworkOpsTest.test_bulk_create_delete_port
- tempest.api.network.test_networks.BulkNetworkOpsTest.test_bulk_create_delete_subnet

`External Network Visibility test <https://github.com/openstack/tempest/blob/master/tempest/api/network/test_networks.py#L526>`_
    - tempest.api.network.test_networks.NetworksTest.test_external_network_visibility

`Create Port with No Security Groups test <https://github.com/openstack/tempest/blob/master/tempest/api/network/test_ports.py>`_
    - tempest.api.network.test_ports.PortsTestJSON.test_create_port_with_no_securitygroups

`Router test <https://github.com/openstack/tempest/blob/master/tempest/api/network/test_routers.py>`_
    - tempest.api.network.test_routers.RoutersTest.test_add_multiple_router_interfaces
    - tempest.api.network.test_routers.RoutersTest.test_add_remove_router_interface_with_port_id
    - tempest.api.network.test_routers.RoutersTest.test_add_remove_router_interface_with_subnet_id
    - tempest.api.network.test_routers.RoutersTest.test_create_show_list_update_delete_router

`Create, List, Show, Update and Delete Subnetpools <https://github.com/openstack/tempest/blob/master/tempest/api/network/test_subnetpools_extensions.py>`_
    - tempest.api.network.test_subnetpools_extensions.SubnetPoolsTestJSON.test_create_list_show_update_delete_subnetpools

`API Version Resources test <https://github.com/openstack/tempest/blob/master/tempest/api/network/test_versions.py>`_
    - tempest.api.network.test_versions.NetworksApiDiscovery.test_api_version_resources