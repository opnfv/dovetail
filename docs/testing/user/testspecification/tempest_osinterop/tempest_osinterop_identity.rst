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

Definitions and abbreviations
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

All these test cases are included in the test case dovetail.tempest.osinterop of
OVP test suite.

Dependency Description
======================

The VIM identity operations test cases are a part of the OpenStack
interoperability tempest test cases. For Fraser based dovetail release, the
OpenStack interoperability guidelines (version 2017.09) is adopted, which is
valid for Mitaka, Newton, Ocata and Pike releases of Openstack.

Test Descriptions
=================

----------------------------------------------------
API discovery operations within the Identity v3 API
----------------------------------------------------

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

Pass / fail criteria
'''''''''''''''''''''

This test case passes if all test action steps execute successfully and all assertions
are affirmed. If any test steps fails to execute successfully or any of the assertions
is not met, the test case fails.

Post conditions
---------------

None

------------------------------------------
Auth operations within the Identity API
------------------------------------------

Use case specification
-----------------------

tempest.api.identity.v3.test_tokens.TokensV3Test.test_create_token

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

Pass / fail criteria
'''''''''''''''''''''

This test case passes if all test action steps execute successfully and all assertions
are affirmed. If any test steps fails to execute successfully or any of the assertions
is not met, the test case fails.

Post conditions
---------------

None

