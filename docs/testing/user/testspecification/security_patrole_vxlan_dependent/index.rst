.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) OPNFV

=====================================
Patrole Tempest Tests Depend on Vxlan
=====================================

Scope
=====

This test area includes some tempest role-based access control (RBAC) tests
which depend on vxlan physical networks.


References
================

- `OpenStack image service API reference <https://developer.openstack.org/api-ref/image/v2/index.html>`_
- `OpenStack metadata definitions service API reference <https://developer.openstack.org/api-ref/image/v2/metadefs-index.html>`_
- `OpenStack layer 2 networking service API reference <https://developer.openstack.org/api-ref/network/v2/index.html#layer-2-networking>`_
- `OpenStack layer 3 networking service API reference <https://developer.openstack.org/api-ref/network/v2/index.html#layer-3-networking>`_
- `OpenStack network security API reference <https://developer.openstack.org/api-ref/network/v2/index.html#security>`_
- `OpenStack resource management API reference <https://developer.openstack.org/api-ref/network/v2/index.html#resource-management>`_
- `OpenStack networking agents API reference <https://developer.openstack.org/api-ref/network/v2/index.html#networking-agents>`_


System Under Test (SUT)
=======================

The system under test is assumed to be the NFVI and VIM deployed on a Pharos
compliant infrastructure.


Test Area Structure
====================

The test area is structured in individual tests as listed below. Each test case
is able to run independently, i.e. irrelevant of the state created by a previous
test. For detailed information on the individual steps and assertions performed
by the tests, review the Python source code accessible via the following links.


**Network basic RBAC test:**

These tests cover the RBAC tests of network basic operations by creating a vxlan provider network.

Implementation:
`NetworksRbacTest <https://github.com/openstack/patrole/blob/0.2.0/patrole_tempest_plugin/tests/api/network/test_networks_rbac.py>`_

- patrole_tempest_plugin.tests.api.network.test_networks_rbac.NetworksRbacTest.test_create_network_provider_network_type
- patrole_tempest_plugin.tests.api.network.test_networks_rbac.NetworksRbacTest.test_create_network_provider_segmentation_id
