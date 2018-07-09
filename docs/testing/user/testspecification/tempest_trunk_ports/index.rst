.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) OPNFV

================================
Neutron Trunk Port Tempest Tests
================================

Scope
=====

This test area evaluates the ability of a system under test to support Neutron
trunk ports. The test area specifically validates port and sub-port API CRUD
operations, by means of both positive and negative tests.


References
================

- `OpenStack API reference <https://developer.openstack.org/api-ref/network/v2/#trunk-networking>`_


System Under Test (SUT)
=======================

The system under test is assumed to be the NFVI and VIM deployed on a Pharos
compliant infrastructure.


Test Area Structure
====================

The test area is structured in individual tests as listed below. Each test case
is able to run independently, i.e. irrelevant of the state created by a previous
test. For detailed information on the individual steps and assertions performed
by the tests, review the Python source code accessible via the following links:

- `Neutron Trunk API tests <https://github.com/openstack/neutron/blob/stable/pike/neutron/tests/tempest/api/test_trunk.py>`_
- `Neutron Trunk API negative tests <https://github.com/openstack/neutron/blob/stable/pike/neutron/tests/tempest/api/test_trunk_details.py>`_
- `Neutron Trunk API negative tests <https://github.com/openstack/neutron/blob/stable/pike/neutron/tests/tempest/api/test_trunk_negative.py>`_


**Trunk port and sub-port CRUD operations:**

These tests cover the CRUD (Create, Read, Update, Delete) life-cycle operations
of trunk ports and subports.

Implementation:
`TrunkTestInheritJSONBase <https://github.com/openstack/neutron/blob/stable/pike/neutron/tests/tempest/api/test_trunk.py#L228>`_
and
`TrunkTestJSON <https://github.com/openstack/neutron/blob/stable/pike/neutron/tests/tempest/api/test_trunk.py#L83>`_.


- neutron.tests.tempest.api.test_trunk.TrunkTestInheritJSONBase.test_add_subport
- neutron.tests.tempest.api.test_trunk.TrunkTestJSON.test_add_subport
- neutron.tests.tempest.api.test_trunk.TrunkTestJSON.test_create_show_delete_trunk
- neutron.tests.tempest.api.test_trunk.TrunkTestJSON.test_create_trunk_empty_subports_list
- neutron.tests.tempest.api.test_trunk.TrunkTestJSON.test_create_trunk_subports_not_specified
- neutron.tests.tempest.api.test_trunk.TrunkTestJSON.test_create_update_trunk
- neutron.tests.tempest.api.test_trunk.TrunkTestJSON.test_create_update_trunk_with_description
- neutron.tests.tempest.api.test_trunk.TrunkTestJSON.test_delete_trunk_with_subport_is_allowed
- neutron.tests.tempest.api.test_trunk.TrunkTestJSON.test_get_subports
- neutron.tests.tempest.api.test_trunk.TrunkTestJSON.test_list_trunks
- neutron.tests.tempest.api.test_trunk.TrunkTestJSON.test_remove_subport
- neutron.tests.tempest.api.test_trunk.TrunkTestJSON.test_show_trunk_has_project_id


**MTU-related operations:**

These tests validate that trunk ports and subports can be created and added
when specifying valid MTU sizes. These tests do not include negative tests
covering invalid MTU sizes.

Implementation:
`TrunkTestMtusJSON <https://github.com/openstack/neutron/blob/stable/pike/neutron/tests/tempest/api/test_trunk.py#L302>`_

- neutron.tests.tempest.api.test_trunk.TrunkTestMtusJSON.test_add_subport_with_mtu_equal_to_trunk
- neutron.tests.tempest.api.test_trunk.TrunkTestMtusJSON.test_add_subport_with_mtu_smaller_than_trunk
- neutron.tests.tempest.api.test_trunk.TrunkTestMtusJSON.test_create_trunk_with_mtu_equal_to_subport
- neutron.tests.tempest.api.test_trunk.TrunkTestMtusJSON.test_create_trunk_with_mtu_greater_than_subport


**API for listing query results:**

These tests verify that listing operations of trunk port objects work. This
functionality is required for CLI and UI operations.

Implementation:
`TrunksSearchCriteriaTest <https://github.com/openstack/neutron/blob/stable/pike/neutron/tests/tempest/api/test_trunk.py#L346>`_

- neutron.tests.tempest.api.test_trunk.TrunksSearchCriteriaTest.test_list_no_pagination_limit_0
- neutron.tests.tempest.api.test_trunk.TrunksSearchCriteriaTest.test_list_pagination
- neutron.tests.tempest.api.test_trunk.TrunksSearchCriteriaTest.test_list_pagination_page_reverse_asc
- neutron.tests.tempest.api.test_trunk.TrunksSearchCriteriaTest.test_list_pagination_page_reverse_desc
- neutron.tests.tempest.api.test_trunk.TrunksSearchCriteriaTest.test_list_pagination_page_reverse_with_href_links
- neutron.tests.tempest.api.test_trunk.TrunksSearchCriteriaTest.test_list_pagination_with_href_links
- neutron.tests.tempest.api.test_trunk.TrunksSearchCriteriaTest.test_list_pagination_with_marker
- neutron.tests.tempest.api.test_trunk.TrunksSearchCriteriaTest.test_list_sorts_asc
- neutron.tests.tempest.api.test_trunk.TrunksSearchCriteriaTest.test_list_sorts_desc


**Query trunk port details:**

These tests validate that all attributes of trunk port objects can be queried.

Implementation:
`TestTrunkDetailsJSON <https://github.com/openstack/neutron/blob/stable/pike/neutron/tests/tempest/api/test_trunk_details.py#L20>`_

- neutron.tests.tempest.api.test_trunk_details.TestTrunkDetailsJSON.test_port_resource_empty_trunk_details
- neutron.tests.tempest.api.test_trunk_details.TestTrunkDetailsJSON.test_port_resource_trunk_details_no_subports
- neutron.tests.tempest.api.test_trunk_details.TestTrunkDetailsJSON.test_port_resource_trunk_details_with_subport


**Negative tests:**

These group of tests comprise negative tests which verify that invalid operations
are handled correctly by the system under test.

Implementation:
`TrunkTestJSON <https://github.com/openstack/neutron/blob/stable/pike/neutron/tests/tempest/api/test_trunk_negative.py#L24>`_

- neutron.tests.tempest.api.test_trunk_negative.TrunkTestJSON.test_add_subport_duplicate_segmentation_details
- neutron.tests.tempest.api.test_trunk_negative.TrunkTestJSON.test_add_subport_passing_dict
- neutron.tests.tempest.api.test_trunk_negative.TrunkTestJSON.test_add_subport_port_id_disabled_trunk
- neutron.tests.tempest.api.test_trunk_negative.TrunkTestJSON.test_add_subport_port_id_uses_trunk_port_id
- neutron.tests.tempest.api.test_trunk_negative.TrunkTestJSON.test_create_subport_invalid_inherit_network_segmentation_type
- neutron.tests.tempest.api.test_trunk_negative.TrunkTestJSON.test_create_subport_missing_segmentation_id
- neutron.tests.tempest.api.test_trunk_negative.TrunkTestJSON.test_create_subport_nonexistent_port_id
- neutron.tests.tempest.api.test_trunk_negative.TrunkTestJSON.test_create_subport_nonexistent_trunk
- neutron.tests.tempest.api.test_trunk_negative.TrunkTestJSON.test_create_trunk_duplicate_subport_segmentation_ids
- neutron.tests.tempest.api.test_trunk_negative.TrunkTestJSON.test_create_trunk_nonexistent_port_id
- neutron.tests.tempest.api.test_trunk_negative.TrunkTestJSON.test_create_trunk_nonexistent_subport_port_id
- neutron.tests.tempest.api.test_trunk_negative.TrunkTestJSON.test_create_trunk_with_subport_missing_port_id
- neutron.tests.tempest.api.test_trunk_negative.TrunkTestJSON.test_create_trunk_with_subport_missing_segmentation_id
- neutron.tests.tempest.api.test_trunk_negative.TrunkTestJSON.test_create_trunk_with_subport_missing_segmentation_type
- neutron.tests.tempest.api.test_trunk_negative.TrunkTestJSON.test_delete_port_in_use_by_subport
- neutron.tests.tempest.api.test_trunk_negative.TrunkTestJSON.test_delete_port_in_use_by_trunk
- neutron.tests.tempest.api.test_trunk_negative.TrunkTestJSON.test_delete_trunk_disabled_trunk
- neutron.tests.tempest.api.test_trunk_negative.TrunkTestJSON.test_remove_subport_not_found
- neutron.tests.tempest.api.test_trunk_negative.TrunkTestJSON.test_remove_subport_passing_dict
- neutron.tests.tempest.api.test_trunk_negative.TrunkTestJSON.test_remove_subport_port_id_disabled_trunk
- neutron.tests.tempest.api.test_trunk_negative.TrunkTestMtusJSON.test_add_subport_with_mtu_greater_than_trunk
- neutron.tests.tempest.api.test_trunk_negative.TrunkTestMtusJSON.test_create_trunk_with_mtu_smaller_than_subport


**Scenario tests (tests covering more than one functionality):**

In contrast to the API tests above, these tests validate more than one specific
API capability. Instead they verify that a simple scenario (example workflow)
functions as intended. To this end, they boot up two VMs with trunk ports and
sub ports and verify connectivity between those VMs.

Implementation:
`TrunkTest <https://github.com/openstack/neutron/blob/stable/pike/neutron/tests/tempest/scenario/test_trunk.py#L45>`_

- neutron.tests.tempest.scenario.test_trunk.TrunkTest.test_subport_connectivity
- neutron.tests.tempest.scenario.test_trunk.TrunkTest.test_trunk_subport_lifecycle
