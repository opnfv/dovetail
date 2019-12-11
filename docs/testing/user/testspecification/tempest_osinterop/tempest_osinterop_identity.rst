.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) opnfv

==========================================
VIM identity operations test specification
==========================================

Scope
=====

The VIM identity test area evaluates the ability of the system under test to
support VIM identity operations. The tests in this area will evaluate
API discovery operations within the Identity v3 API, auth operations within
the Identity API.

Definitions and Abbreviations
=============================

The following terms and abbreviations are used in conjunction with this test area

- API - Application Programming Interface
- NFVi - Network Functions Virtualisation infrastructure
- VIM - Virtual Infrastructure Manager

System Under Test (SUT)
=======================

The system under test is assumed to be the NFVi and VIM in operation on an Pharos compliant infrastructure.

Test Area Structure
====================

The test area is structured based on VIM identity operations. Each test case
is able to run independently, i.e. irrelevant of the state created by a previous test.

All these test cases are included in the test case functest.tempest.osinterop of
OVP test suite.

Dependency Description
======================

The VIM identity operations test cases are a part of the OpenStack
interoperability tempest test cases. For Fraser based dovetail release, the
OpenStack interoperability guidelines (version 2018.11) is adopted, which is
valid for Mitaka, Newton, Ocata and Pike releases of Openstack.

Test Descriptions
=================

-----------------------------------------------------------------
Test Case 1 - API discovery operations within the Identity v3 API
-----------------------------------------------------------------

Use case specification
-----------------------

tempest.api.identity.v3.test_api_discovery.TestApiDiscovery.test_api_version_resources
tempest.api.identity.v3.test_api_discovery.TestApiDiscovery.test_api_media_types
tempest.api.identity.v3.test_api_discovery.TestApiDiscovery.test_api_version_statuses

Test preconditions
-------------------

None

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
'''''''''''''''

* Test action 1: Show the v3 identity api description, the test passes if keys
  'id', 'links', 'media-types', 'status', 'updated' are all included in the description
  response message.
* Test action 2: Get the value of v3 identity api 'media-types', the test passes if
  api version 2 and version 3 are all included in the response.
* Test action 3: Show the v3 indentity api description, the test passes if 'current',
  'stable', 'experimental', 'supported', 'deprecated' are all of the identity api 'status'
  values.

Pass / Fail criteria
'''''''''''''''''''''

This test case passes if all test action steps execute successfully and all assertions
are affirmed. If any test steps fails to execute successfully or any of the assertions
is not met, the test case fails.

Post conditions
---------------

None

-----------------------------------------------------
Test Case 2 - Auth operations within the Identity API
-----------------------------------------------------

Use case specification
-----------------------

tempest.api.identity.v3.test_tokens.TokensV3Test.test_create_token
tempest.api.identity.v3.test_tokens.TokensV3Test.test_validate_token

Test preconditions
-------------------

None

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
'''''''''''''''

* Test action 1: Get the token by system credentials, the test passes if
  the returned token_id is not empty and is string type.
* Test action 2: Get the user_id in getting token response message, the test
  passes if it is equal to the user_id which is used to get token.
* Test action 3: Get the user_name in getting token response message, the test
  passes if it is equal to the user_name which is used to get token.
* Test action 4: Get the method in getting token response message, the test
  passes if it is equal to the password which is used to get token.
* Test action 5: Get the token by system credentials and show the token,
  the test passes if the response bodies of the get and show operations are the same.
* Test action 6: Get the user_id in showing token response message, the test
  passes if it is equal to the user_id which is used to get token.
* Test action 7: Get the username in showing token response message, the test
  passes if it is equal to the username which is used to get token.
* Test action 8: Delete this token by non-admin compute client, the test passes
  if it raises a NotFound exception.

Pass / Fail criteria
'''''''''''''''''''''

This test case passes if all test action steps execute successfully and all assertions
are affirmed. If any test steps fails to execute successfully or any of the assertions
is not met, the test case fails.

Post conditions
---------------

None

--------------------------------------------------------
Test Case 3 - Catalog operations within the Identity API
--------------------------------------------------------

Use case specification
-----------------------

tempest.api.identity.v3.test_catalog.IdentityCatalogTest.test_catalog_standardization

Test preconditions
-------------------

None

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
'''''''''''''''

* Test action 1: Show all catalogs by non-admin catalog client, the test passes
  if the catalog types getting in the show response message equal to the
  standard service values. Standard catalog types of 'keystone', 'nova', 'glance' and
  'swift' should be 'identity', 'compute', 'image' and 'object-store' respectively.

Pass / Fail criteria
'''''''''''''''''''''

This test case passes if all test action steps execute successfully and all assertions
are affirmed. If any test steps fails to execute successfully or any of the assertions
is not met, the test case fails.

Post conditions
---------------

None
