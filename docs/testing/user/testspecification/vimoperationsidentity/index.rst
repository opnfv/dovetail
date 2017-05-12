s work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Ericsson AB and Huawei

==========================================
VIM identity operations test specification
==========================================

.. toctree::
   :maxdepth: 2

Scope
=====

The VIM identity test area evaluates the ability of the system under test to
support VIM identity operations. The tests in this area will evaluate 
API discovery operations within the Identity v3 API, auth operations within
the Identity API.

References
================

- Defcore test cases
  - https://github.com/openstack/interop/blob/master/2016.08.json
- Openstack interoperability
  - https://www.openstack.org/brand/interop/
- Defcore test cases listed using the Rest API from RefStack project
  - https://refstack.openstack.org/api/v1/guidelines/2016.08/tests?target=compute&type=required&alias=true&flag=false
- Refstack client
  - https://github.com/openstack/refstack-client

Definitions and abbreviations
=============================

The following terms and abbreviations are used in conjunction with this test area
- API - Application Programming Interface
- NFVi - Network Functions Virtualisation infrastructure
- VIM - Virtual Infrastructure Manager

System Under Test (SUT)
=======================

The system under test is assumed to be the NFVi in operation on an Pharos compliant infrastructure.

Test Area Structure
====================

The VIM identity operation test cases are a part of the DefCore tempest test
cases not flagged and required. According to
https://github.com/openstack/interop/blob/master/2016.08/procedure.rst,
some tests are still flagged due to outstanding bugs in the Tempest library,
particularly tests that require SSH. Refstack developers
are working on correcting these bugs upstream. Please note that although some tests
are flagged because of bugs, there is still an expectation that the capabilities
covered by the tests are available.

The approved guidelines (2016.08) are valid for Kilo, Liberty, Mitaka and Newton releases of OpenStack

The list can be generated using the Rest API from RefStack project:
https://refstack.openstack.org/api/v1/guidelines/2016.08/tests?target=compute&type=required&alias=true&flag=false

The VIM identity operation test cases include API discovery operations within
the Identity v3 API, Auth operations within the Identity API.

Test Descriptions
=================

----------------------------------------------------
API discovery operations within the Identity v3 API
----------------------------------------------------

Use case specification
-----------------------

tempest.api.identity.v3.TestApiDiscovery.test_api_version_resources
tempest.api.identity.v3.TestApiDiscovery.test_api_media_types
tempest.api.identity.v3.TestApiDiscovery.test_api_version_statuses
tempest.api.identity.v3.test_api_discovery.TestApiDiscovery.test_api_version_resources
tempest.api.identity.v3.test_api_discovery.TestApiDiscovery.test_api_media_types
tempest.api.identity.v3.test_api_discovery.TestApiDiscovery.test_api_version_statuses

note: the latter three test cases are the alias of the former three, respectively.

Test preconditions
-------------------

environment can be deployed on bare metal of virtualized infrastructure,
deployment can be HA or non-HA.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

* Test action 1: show indentity api description, keys 'id', 'links', 'media-types',
  'status', 'updated' should all in the identity api description keys.
* Test action 2: get identity api media types, api version 2 and version 3 should
  all in the identity api media types.
* Test action 3: show indentity api description, 'current', 'stable', 'experimental',
  'supported', 'deprecated' should all in the identity api 'status'.

The pass criteria for this test case is that all instructions are able to be carried out
according to the described behaviour without deviation.
A negative result will be generated if the above is not met in completion.

Post conditions
---------------

NA

------------------------------------------
Auth operations within the Identity API
------------------------------------------

Use case specification
-----------------------

tempest.api.identity.v3.test_tokens.TokensV3Test.test_create_token

Test preconditions
-------------------

environment can be deployed on bare metal of virtualized infrastructure,
deployment can be HA or non-HA.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

* Test action 1: get token should work
* Test action 2: the user id in get token reponse message
  should equal to the user id which is used to get token
* Test action 3: the user name in get token reponse message
  should equal to the user name which is used to get token
* Test action 4: methods in get token reponse message should
  equal to the password which is used to get token

The pass criteria for this test case is that all instructions are able to be carried out
according to the described behaviour without deviation.
A negative result will be generated if the above is not met in completion.

Post conditions
---------------

NA

