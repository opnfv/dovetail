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

- `OpenStack API reference <https://docs.openstack.org/api-ref/network/v2/#trunk-networking>`_


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

- `Neutron Trunk API tests <https://github.com/openstack/neutron-tempest-plugin/blob/0.3.0/neutron_tempest_plugin/api/test_trunk.py>`_
- `Neutron Trunk API trunk details <https://github.com/openstack/neutron-tempest-plugin/blob/0.3.0/neutron_tempest_plugin/api/test_trunk_details.py>`_
- `Neutron Trunk API negative tests <https://github.com/openstack/neutron-tempest-plugin/blob/0.3.0/neutron_tempest_plugin/api/test_trunk_negative.py>`_


**Trunk port and sub-port CRUD operations:**

These tests cover the CRUD (Create, Read, Update, Delete) life-cycle operations
of trunk ports and subports.

Implementation:
`TrunkTestJSON <https://github.com/openstack/neutron-tempest-plugin/blob/0.3.0/neutron_tempest_plugin/api/test_trunk.py#L71>`_


- neutron_tempest_plugin.api.test_trunk.TrunkTestJSON.test_add_subports
- neutron_tempest_plugin.api.test_trunk.TrunkTestJSON.test_create_show_delete_trunk
- neutron_tempest_plugin.api.test_trunk.TrunkTestJSON.test_create_trunk_empty_subports_list
- neutron_tempest_plugin.api.test_trunk.TrunkTestJSON.test_create_trunk_subports_not_specified
- neutron_tempest_plugin.api.test_trunk.TrunkTestJSON.test_delete_trunk_with_subport_is_allowed
- neutron_tempest_plugin.api.test_trunk.TrunkTestJSON.test_get_subports
- neutron_tempest_plugin.api.test_trunk.TrunkTestJSON.test_list_trunks
- neutron_tempest_plugin.api.test_trunk.TrunkTestJSON.test_remove_subport


**API for listing query results:**

These tests verify that listing operations of trunk port objects work. This
functionality is required for CLI and UI operations.

Implementation:
`TrunksSearchCriteriaTest <https://github.com/openstack/neutron-tempest-plugin/blob/0.3.0/neutron_tempest_plugin/api/test_trunk.py#L306>`_

- neutron_tempest_plugin.api.test_trunk.TrunksSearchCriteriaTest.test_list_no_pagination_limit_0
- neutron_tempest_plugin.api.test_trunk.TrunksSearchCriteriaTest.test_list_pagination
- neutron_tempest_plugin.api.test_trunk.TrunksSearchCriteriaTest.test_list_pagination_page_reverse_asc
- neutron_tempest_plugin.api.test_trunk.TrunksSearchCriteriaTest.test_list_pagination_page_reverse_desc
- neutron_tempest_plugin.api.test_trunk.TrunksSearchCriteriaTest.test_list_pagination_with_marker
- neutron_tempest_plugin.api.test_trunk.TrunksSearchCriteriaTest.test_list_sorts_asc
- neutron_tempest_plugin.api.test_trunk.TrunksSearchCriteriaTest.test_list_sorts_desc


**Query trunk port details:**

These tests validate that all attributes of trunk port objects can be queried.

Implementation:
`TestTrunkDetailsJSON <https://github.com/openstack/neutron-tempest-plugin/blob/0.3.0/neutron_tempest_plugin/api/test_trunk_details.py#L20>`_

- neutron_tempest_plugin.api.test_trunk_details.TestTrunkDetailsJSON.test_port_resource_empty_trunk_details
- neutron_tempest_plugin.api.test_trunk_details.TestTrunkDetailsJSON.test_port_resource_trunk_details_no_subports
- neutron_tempest_plugin.api.test_trunk_details.TestTrunkDetailsJSON.test_port_resource_trunk_details_with_subport


**Negative tests:**

These group of tests comprise negative tests which verify that invalid operations
are handled correctly by the system under test.

Implementation:
`TrunkTestNegative <https://github.com/openstack/neutron-tempest-plugin/blob/0.3.0/neutron_tempest_plugin/api/test_trunk_negative.py#L27>`_

- neutron_tempest_plugin.api.test_trunk_negative.TrunkTestJSON.test_add_subport_duplicate_segmentation_details
- neutron_tempest_plugin.api.test_trunk_negative.TrunkTestJSON.test_add_subport_passing_dict
- neutron_tempest_plugin.api.test_trunk_negative.TrunkTestJSON.test_add_subport_port_id_disabled_trunk
- neutron_tempest_plugin.api.test_trunk_negative.TrunkTestJSON.test_add_subport_port_id_uses_parent_port_id
- neutron_tempest_plugin.api.test_trunk_negative.TrunkTestJSON.test_create_subport_missing_segmentation_id
- neutron_tempest_plugin.api.test_trunk_negative.TrunkTestJSON.test_create_subport_nonexistent_port_id
- neutron_tempest_plugin.api.test_trunk_negative.TrunkTestJSON.test_create_subport_nonexistent_trunk
- neutron_tempest_plugin.api.test_trunk_negative.TrunkTestJSON.test_create_trunk_duplicate_subport_segmentation_ids
- neutron_tempest_plugin.api.test_trunk_negative.TrunkTestJSON.test_create_trunk_nonexistent_port_id
- neutron_tempest_plugin.api.test_trunk_negative.TrunkTestJSON.test_create_trunk_nonexistent_subport_port_id
- neutron_tempest_plugin.api.test_trunk_negative.TrunkTestJSON.test_create_trunk_with_subport_missing_port_id
- neutron_tempest_plugin.api.test_trunk_negative.TrunkTestJSON.test_create_trunk_with_subport_missing_segmentation_id
- neutron_tempest_plugin.api.test_trunk_negative.TrunkTestJSON.test_create_trunk_with_subport_missing_segmentation_type
- neutron_tempest_plugin.api.test_trunk_negative.TrunkTestJSON.test_delete_port_in_use_by_subport
- neutron_tempest_plugin.api.test_trunk_negative.TrunkTestJSON.test_delete_port_in_use_by_trunk
- neutron_tempest_plugin.api.test_trunk_negative.TrunkTestJSON.test_delete_trunk_disabled_trunk
- neutron_tempest_plugin.api.test_trunk_negative.TrunkTestJSON.test_remove_subport_not_found
- neutron_tempest_plugin.api.test_trunk_negative.TrunkTestJSON.test_remove_subport_passing_dict
- neutron_tempest_plugin.api.test_trunk_negative.TrunkTestJSON.test_remove_subport_port_id_disabled_trunk


**Scenario tests (tests covering more than one functionality):**

In contrast to the API tests above, these tests validate more than one specific
API capability. Instead they verify that a simple scenario (example workflow)
functions as intended. To this end, they boot up two VMs with trunk ports and
sub ports and verify connectivity between those VMs.

Implementation:
`TrunkTest <https://github.com/openstack/neutron-tempest-plugin/blob/0.3.0/neutron_tempest_plugin/scenario/test_trunk.py#L41>`_

- neutron_tempest_plugin.scenario.test_trunk.TrunkTest.test_trunk_subport_lifecycle
