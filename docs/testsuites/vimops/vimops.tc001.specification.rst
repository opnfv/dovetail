.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) OPNFV

==============================================================
Dovetail VIM Operations tc001 specification - Images v2 index
==============================================================

.. table::
   :class: longtable

+-----------------------+----------------------------------------------------------------------------------------------------+
|test case name         |Images v2 index                                                                                     |
|                       |                                                                                                    |
+-----------------------+----------------------------------------------------------------------------------------------------+
|id                     |dovetail.vimops.tc001                                                                               |
+-----------------------+----------------------------------------------------------------------------------------------------+
|objective              |CRUD image operations in Images API v2                                                              |
+-----------------------+----------------------------------------------------------------------------------------------------+
|test items             |tempest.api.image.v2.test_images.ListImagesTest.test_list_no_params                                 |
|                       |{idempotent_id('1e341d7a-90a9-494c-b143-2cdf2aeb6aee')}                                             |
+-----------------------+----------------------------------------------------------------------------------------------------+
|environmental          |                                                                                                    |
|requirements &         | environment can be deployed on bare metal of virtualized infrastructure                            |
|preconditions          | deployment can be HA or non-HA                                                                     |
|                       |                                                                                                    |
+-----------------------+----------------------------------------------------------------------------------------------------+
|scenario dependencies  | NA                                                                                                 |
+-----------------------+----------------------------------------------------------------------------------------------------+
|procedural             | NA                                                                                                 |
|requirements           |                                                                                                    |
|                       |                                                                                                    |
+-----------------------+----------------------------------------------------------------------------------------------------+
|input specifications   |The parameters needed to execute Images APIs.                                                       |
|                       |Refer to Images API v2.0 [1]_                                                                       |
+-----------------------+----------------------------------------------------------------------------------------------------+
|output specifications  |The responses after executing Images APIs.                                                          |
|                       |Refer to Images API v2.0 [1]_                                                                       |
+-----------------------+----------------------------------------------------------------------------------------------------+
|pass/fail criteria     |If normal response code 200 is returned, the test passes.                                           |
|                       |Otherwise, the test fails with various error codes.                                                 |
|                       |Refer to Images API v2.0 [1]_                                                                       |
+-----------------------+----------------------------------------------------------------------------------------------------+
|test report            |TBD                                                                                                 |
+-----------------------+----------------------------------------------------------------------------------------------------+

.._[1]: http://developer.openstack.org/api-ref/image/v2/
