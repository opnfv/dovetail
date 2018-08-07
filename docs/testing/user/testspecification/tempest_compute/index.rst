.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Ericsson AB

===========================================
Tempest Compute test specification
===========================================


Scope
=====

The Tempest Compute test area evaluates the ability of the System Under Test (SUT)
to support dynamic network runtime operations through the life of a VNF.
The tests in this test area will evaluate IPv4 network runtime operations
functionality.

These runtime operations includes:

- Create, list and show flavors
- Create and list security group rules
- Create, delete and list security groups
- Create, delete, show and list interfaces; attach and deattach ports to servers
- List server addresses
- Individual version endpoints info works
- Servers Test Boot From Volume


References
==========

`Security Groups: <https://developer.openstack.org/api-ref/network/v2/index.html#security-groups-security-groups>`_

- create security group
- delete security group

`Networks: <https://developer.openstack.org/api-ref/networking/v2/index.html#networks>`_

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

`Servers: <https://developer.openstack.org/api-ref/compute/>`_

- create keypair
- create server
- delete server
- add/assign floating IP
- disassociate floating IP

`Ports: <https://developer.openstack.org/api-ref/networking/v2/index.html#ports>`_

- create port
- update port
- delete port

`Floating IPs: <https://developer.openstack.org/api-ref/networking/v2/index.html#floating-ips-floatingips>`_

- create floating IP
- delete floating IP


System Under Test (SUT)
=======================

The system under test is assumed to be the NFVi and VIM in operation on a
Pharos compliant infrastructure.


Test Area Structure
===================

The test area is structured in individual tests as listed below.
For detailed information on the individual steps and assertions performed
by the tests, review the Python source code accessible via the following links:

All these test cases are included in the test case dovetail.tempest.compute of
OVP test suite.


Test Area Structure
===================

The test area is structured in individual tests as listed below.
For detailed information on the individual steps and assertions performed
by the tests, review the Python source code accessible via the following links:



- `Flavor V2 test <https://github.com/openstack/tempest/blob/12.2.0/tempest/api/compute/flavors/test_flavors.py#L20>`_
    - tempest.api.compute.flavors.test_flavors.FlavorsV2TestJSON.test_get_flavor
    - tempest.api.compute.flavors.test_flavors.FlavorsV2TestJSON.test_list_flavors

- `Security Group Rules test <https://github.com/openstack/tempest/blob/master/tempest/api/compute/security_groups/test_security_group_rules.py#L20>`_
    - tempest.api.compute.security_groups.test_security_group_rules.SecurityGroupRulesTestJSON.test_security_group_rules_create
    - tempest.api.compute.security_groups.test_security_group_rules.SecurityGroupRulesTestJSON.test_security_group_rules_list

- `Security Groups test <https://github.com/openstack/tempest/blob/master/tempest/api/compute/security_groups/test_security_groups.py#L23>`_
    - tempest.api.compute.security_groups.test_security_groups.SecurityGroupsTestJSON.test_security_groups_create_list_delete

- `Attach Interfaces test <https://github.com/openstack/tempest/blob/master/tempest/api/compute/servers/test_attach_interfaces.py#L32>`_
    - tempest.api.compute.servers.test_attach_interfaces.AttachInterfacesTestJSON.test_add_remove_fixed_ip


- `Server Addresses test <https://github.com/openstack/tempest/blob/master/tempest/api/compute/servers/test_server_addresses.py#L21>`_
    - tempest.api.compute.servers.test_server_addresses.ServerAddressesTestJSON.test_list_server_addresses
    - tempest.api.compute.servers.test_server_addresses.ServerAddressesTestJSON.test_list_server_addresses_by_network


- `Test Versions <https://github.com/openstack/tempest/blob/master/tempest/api/compute/test_versions.py#L19>`_
    - tempest.api.compute.test_versions.TestVersions.test_get_version_details


- `Servers Test Boot From Volume <https://github.com/openstack/tempest/blob/master/tempest/api/compute/servers/test_create_server.py#L158>`_
    - tempest.api.compute.servers.test_create_server.ServersTestBootFromVolume.test_verify_server_details
    - tempest.api.compute.servers.test_create_server.ServersTestBootFromVolume.test_list_servers


- `Server Basic Operations test <https://github.com/openstack/tempest/blob/master/tempest/scenario/test_server_basic_ops.py#L30>`_
    - tempest.scenario.test_server_basic_ops.TestServerBasicOps.test_server_basic_ops
