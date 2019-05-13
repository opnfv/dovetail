.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Ericsson AB

======================
VPN test specification
======================

.. toctree::
   :maxdepth: 2

Scope
=====

The VPN test area evaluates the ability of the system under test to support VPN
networking for virtual workloads. This test area tests CRUD (Create, Read, Update,
Delete) operations of BGPVPN API.

References
==========

This test area evaluates the ability of the system to perform selected actions
defined in the following specifications. Details of specific features evaluated
are described in the test descriptions.

- RFC 4364 - BGP/MPLS IP Virtual Private Networks

  - https://tools.ietf.org/html/rfc4364

- RFC 4659 - BGP-MPLS IP Virtual Private Network

  - https://tools.ietf.org/html/rfc4659

- RFC 2547 - BGP/MPLS VPNs

  - https://tools.ietf.org/html/rfc2547


Definitions and abbreviations
=============================

The following terms and abbreviations are used in conjunction with this test
area

- BGP - Border gateway protocol
- NFVi - Network functions virtualization infrastructure
- VM - Virtual machine
- VPN - Virtual private network


System Under Test (SUT)
=======================

The system under test is assumed to be the NFVi and VIM in operation on a
Pharos compliant infrastructure.


Test Area Structure
===================

The test area is structured in several tempest tests which are executed
sequentially. The order of the tests is arbitrary as there are no dependencies
across the tests. Specifially, every test performs clean-up operations which
return the system to the same state as before the test.


Test Descriptions
=================

------------------------------------
Test Case 1 - Tempest API CRUD Tests
------------------------------------

Short Name
----------

functest.tempest.bgpvpn


Use case specification
----------------------

This test case combines multiple CRUD (Create, Read, Update, Delete) tests for
the objects defined by the BGPVPN API extension of Neutron.

These tests are implemented in the upstream `networking-bgpvpn project repository
<https://github.com/openstack/networking-bgpvpn>`_ as a Tempest plugin.


Test preconditions
------------------

The VIM is operational and the networking-bgpvpn service plugin for Neutron is
correctly configured and loaded. At least one compute node is available.


Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

List of test cases

* networking_bgpvpn_tempest.tests.api.test_create_bgpvpn
* networking_bgpvpn_tempest.tests.api.test_create_bgpvpn_as_non_admin_fail
* networking_bgpvpn_tempest.tests.api.test_delete_bgpvpn_as_non_admin_fail
* networking_bgpvpn_tempest.tests.api.test_show_bgpvpn_as_non_owner_fail
* networking_bgpvpn_tempest.tests.api.test_list_bgpvpn_as_non_owner_fail
* networking_bgpvpn_tempest.tests.api.test_show_netassoc_as_non_owner_fail
* networking_bgpvpn_tempest.tests.api.test_list_netassoc_as_non_owner_fail
* networking_bgpvpn_tempest.tests.api.test_associate_disassociate_network
* networking_bgpvpn_tempest.tests.api.test_update_route_target_non_admin_fail
* networking_bgpvpn_tempest.tests.api.test_create_bgpvpn_with_invalid_routetargets
* networking_bgpvpn_tempest.tests.api.test_update_bgpvpn_invalid_routetargets
* networking_bgpvpn_tempest.tests.api.test_associate_invalid_network
* networking_bgpvpn_tempest.tests.api.test_disassociate_invalid_network
* networking_bgpvpn_tempest.tests.api.test_associate_disassociate_router
* networking_bgpvpn_tempest.tests.api.test_attach_associated_subnet_to_associated_router

The tests include both positive tests and negative tests. The latter are
identified with the suffix "_fail" in their name.


Test execution
''''''''''''''

The tests are executed sequentially and a separate pass/fail result is recorded
per test.

In general, every test case performs the API operations indicated in its name
and asserts that the action succeeds (positive test) or a specific exception
is triggered (negative test). The following describes the test execution
per test in further detail.


networking_bgpvpn_tempest.tests.api.test_create_bgpvpn
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Create a BGPVPN as an admin.
* **Test assertion**: The API call succeeds.


networking_bgpvpn_tempest.tests.api.test_create_bgpvpn_as_non_admin_fail
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Attempt to create a BGPVPN as non-admin.
* **Test assertion**: Creating a BGPVPN as non-admin fails.


networking_bgpvpn_tempest.tests.api.test_delete_bgpvpn_as_non_admin_fail
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Create BGPVPN vpn1 as admin.
* Attempt to delete vpn1 as non-admin.
* **Test assertion**: The deletion of vpn1 as non-admin fails.


networking_bgpvpn_tempest.tests.api.test_show_bgpvpn_as_non_owner_fail
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Create a BGPVPN vpn1 as admin in project1.
* **Test assertion**: Attempting to retrieve detailed properties of vpn1
  in project2 fails.


networking_bgpvpn_tempest.tests.api.test_list_bgpvpn_as_non_owner_fail
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Create a BGPVPN vpn1 as admin in project1.
* Retrieve a list of all BGPVPNs in project2.
* **Test assertion**: The list of BGPVPNs retrieved in project2 does not
  include vpn1.


networking_bgpvpn_tempest.tests.api.test_show_netassoc_as_non_owner_fail
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Create BGPVPN vpn1 as admin in project1.
* Associate vpn1 with a Neutron network in project1
* **Test assertion**: Retrieving detailed properties of the network association
  fails in project2.


networking_bgpvpn_tempest.tests.api.test_list_netassoc_as_non_owner_fail
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Create BGPVPN vpn1 as admin in project1.
* Create network association net-assoc1 with vpn1 and Neutron network net1
  in project1.
* Retrieve a list of all network associations in project2.
* **Test assertion**: The retrieved list of network associations does not
  include network association net-assoc1.


networking_bgpvpn_tempest.tests.api.test_associate_disassociate_network
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Create a BGPVPN vpn1 as admin.
* Associate vpn1 with a Neutron network net1.
* **Test assertion**: The metadata of vpn1 includes the UUID of net1.
* Diassociate vpn1 from the Neutron network.
* **Test assertion**: The metadata of vpn1 does not include the UUID of net1.


networking_bgpvpn_tempest.tests.api.test_update_route_target_non_admin_fail
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Create a BGPVPN vpn1 as admin with specific route targets.
* Attempt to update vpn1 with different route targets as non-admin.
* **Test assertion**: The update fails.


networking_bgpvpn_tempest.tests.api.test_create_bgpvpn_with_invalid_routetargets
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Attempt to create a BGPVPN as admin with invalid route targets.
* **Test assertion**: The creation of the BGPVPN fails.


networking_bgpvpn_tempest.tests.api.test_update_bgpvpn_invalid_routetargets
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Create a BGPVPN vpn1 as admin with empty route targets.
* Attempt to update vpn1 with invalid route targets.
* **Test assertion**: The update of the route targets fails.


networking_bgpvpn_tempest.tests.api.test_associate_invalid_network
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Create BGPVPN vpn1 as admin.
* Attempt to associate vpn1 with a non-existing Neutron network.
* **Test assertion**: Creating the network association fails.


networking_bgpvpn_tempest.tests.api.test_disassociate_invalid_network
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Create BGPVPN vpn1 as admin.
* Create network association net-assoc1 with vpn1 and Neutron network net1.
* Attempt to delete net-assoc1 with an invalid network UUID.
* **Test assertion**: The deletion of the net-assoc fails.


networking_bgpvpn_tempest.tests.api.test_associate_disassociate_router
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Create a BGPVPN vpn1 as admin.
* Associate vpn1 with a Neutron router router1.
* **Test assertion**: The metadata of vpn1 includes the UUID of router1.
* Disassociate router1 from vpn1.
* **Test assertion**: The metadata of vpn1 does not include the UUID of router1.


networking_bgpvpn_tempest.tests.api.test_attach_associated_subnet_to_associated_router
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Create BGPVPN vpn1 as admin.
* Associate vpn1 with Neutron network net1.
* Create BGPVPN vpn2
* Associate vpn2 with Neutron router router1.
* Attempt to add the subnet of net1 to router1
* **Test assertion**: The association fails.



Pass / fail criteria
''''''''''''''''''''

This test validates that all supported CRUD operations (create, read, update,
delete) can be applied to the objects of the Neutron BGPVPN extension.  In
order to pass this test, all test assertions listed in the test execution above
need to pass.


Post conditions
---------------

N/A
