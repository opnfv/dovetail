.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Ericsson AB

===========================================
Tempest Identity v2 test specification
===========================================


Scope
=====

The Tempest Identity v2 test area evaluates the ability of the
System Under Test (SUT) create, list, delete and verify users through the
life of a VNF.
The tests in this test area will evaluate IPv4 network runtime operations
functionality.

These runtime operations includes:

- Create, List, Verify and Delete Services
- Create a user
- Tests for API discovery features

References
==========

`Identity API v2.0 <https://developer.openstack.org/api-ref/identity/v2-ext/index.html.`_

System Under Test (SUT)
=======================

The system under test is assumed to be the NFVi and VIM in operation on a
Pharos compliant infrastructure.


Test Area Structure
===================

The test area is structured in individual tests as listed below.
For detailed information on the individual steps and assertions performed
by the tests, review the Python source code accessible via the following links:

All these test cases are included in the test case dovetail.tempest.identity_v2 of
OVP test suite.

- `Create, List, Verify and Delete Services <https://github.com/openstack/tempest/blob/12.2.0/tempest/api/identity/admin/v2/test_services.py#L24>`_
    - tempest.api.identity.admin.v2.test_services.ServicesTestJSON.test_list_services

- `Create a user <https://github.com/openstack/tempest/blob/12.2.0/tempest/api/identity/admin/v2/test_users.py#L26>`_
    - tempest.api.identity.admin.v2.test_users.UsersTestJSON.test_create_user

- `Tests for API discovery features <https://github.com/openstack/tempest/blob/12.2.0/tempest/api/identity/v2/test_api_discovery.py#L20>`_
    - tempest.api.identity.v2.test_api_discovery.TestApiDiscovery.test_api_media_types
    - tempest.api.identity.v2.test_api_discovery.TestApiDiscovery.test_api_version_resources
    - tempest.api.identity.v2.test_api_discovery.TestApiDiscovery.test_api_version_statuses