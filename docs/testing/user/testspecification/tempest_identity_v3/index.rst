.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Ericsson AB

===========================================
Tempest Identity v3 test specification
===========================================


Scope
=====

The Tempest Identity v3 test area evaluates the ability of the System Under Test
(SUT) to create, list, delete and verify users through the life of a VNF.
The tests in this test area will evaluate IPv4 network runtime operations
functionality.

These runtime operations may include that create, list, verify and delete:

- credentials
- domains
- endpoints
- user groups
- policies
- regions
- roles
- services
- identities
- API versions

References
==========

`Identity API v3.0 <https://developer.openstack.org/api-ref/identity/v3/index.html>`_

System Under Test (SUT)
=======================

The system under test is assumed to be the NFVi and VIM in operation on a
Pharos compliant infrastructure.

Test Area Structure
===================

The test area is structured in individual tests as listed below.
For detailed information on the individual steps and assertions performed
by the tests, review the Python source code accessible via the following links:

All these test cases are included in the test case dovetail.tempest.identity_v3 of
OVP test suite.

- `Create, Get, Update and Delete Credentials <https://github.com/openstack/tempest/blob/12.2.0/tempest/api/identity/admin/v3/test_credentials.py#L21>`_
    - tempest.api.identity.admin.v3.test_credentials.CredentialsTestJSON.test_credentials_create_get_update_delete

- `Create and Verify Domain <https://github.com/openstack/tempest/blob/12.2.0/tempest/api/identity/admin/v3/test_domains.py#L159>`_
    - tempest.api.identity.admin.v3.test_domains.DefaultDomainTestJSON.test_default_domain_exists

- `Create, Update and Delete Domain <https://github.com/openstack/tempest/blob/12.2.0/tempest/api/identity/admin/v3/test_domains.py>`_
    - tempest.api.identity.admin.v3.test_domains.DomainsTestJSON.test_create_update_delete_domain

- `Create and Update endpoint <https://github.com/openstack/tempest/blob/12.2.0/tempest/api/identity/admin/v3/test_endpoints.py>`_
    - tempest.api.identity.admin.v3.test_endpoints.EndPointsTestJSON.test_update_endpoint

- `Create, List and Delete Group Users <https://github.com/openstack/tempest/blob/12.2.0/tempest/api/identity/admin/v3/test_groups.py>`_
    - tempest.api.identity.admin.v3.test_groups.GroupsV3TestJSON.test_group_users_add_list_delete

- `Update Policy <https://github.com/openstack/tempest/blob/12.2.0/tempest/api/identity/admin/v3/test_policies.py>`_
    - tempest.api.identity.admin.v3.test_policies.PoliciesTestJSON.test_create_update_delete_policy

- `Create a Region with a Specific Id <https://github.com/openstack/tempest/blob/12.2.0/tempest/api/identity/admin/v3/test_regions.py>`_
    - tempest.api.identity.admin.v3.test_regions.RegionsTestJSON.test_create_region_with_specific_id

- `Create, Update and Show Role List <https://github.com/openstack/tempest/blob/12.2.0/tempest/api/identity/admin/v3/test_roles.py>`_
    - tempest.api.identity.admin.v3.test_roles.RolesV3TestJSON.test_role_create_update_show_list

- `Create a Service <https://github.com/openstack/tempest/blob/12.2.0/tempest/api/identity/admin/v3/test_services.py>`_
    - tempest.api.identity.admin.v3.test_services.ServicesTestJSON.test_create_update_get_service

- `Create and List Trusts <https://github.com/openstack/tempest/blob/12.2.0/tempest/api/identity/admin/v3/test_trusts.py#L193>`_
    - tempest.api.identity.admin.v3.test_trusts.TrustsV3TestJSON.test_get_trusts_all

- `List API Versions <https://github.com/openstack/tempest/blob/18.0.0/tempest/api/identity/v3/test_api_discovery.py>`_
    - tempest.api.identity.v3.test_api_discovery.TestApiDiscovery.test_list_api_versions
