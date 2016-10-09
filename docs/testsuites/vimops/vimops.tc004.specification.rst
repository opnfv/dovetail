.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) OPNFV

==============================================================
Dovetail VIM Operations tc004 specification - Images v2 list
==============================================================

.. table::
   :class: longtable

+-----------------------+----------------------------------------------------------------------------------------------------+
|test case name         |Images v2 list                                                                                      |
|                       |                                                                                                    |
+-----------------------+----------------------------------------------------------------------------------------------------+
|id                     |dovetail.vimops.tc004                                                                               |
+-----------------------+----------------------------------------------------------------------------------------------------+
|objective              |Image list tests using the Glance v2 API                                                            |
+-----------------------+----------------------------------------------------------------------------------------------------+
|test items             |tempest.api.image.v2.test_images.ListImagesTest.test_list_images_param_container_format             |
|                       |{idempotent_id('9959ca1d-1aa7-4b7a-a1ea-0fff0499b37e')}                                             |
|                       |tempest.api.image.v2.test_images.ListImagesTest.test_list_images_param_disk_format                  |
|                       |{idempotent_id('4a4735a7-f22f-49b6-b0d9-66e1ef7453eb')}                                             |
|                       |tempest.api.image.v2.test_images.ListImagesTest.test_list_images_param_limit                        |
|                       |{idempotent_id('e914a891-3cc8-4b40-ad32-e0a39ffbddbb')}                                             |
|                       |tempest.api.image.v2.test_images.ListImagesTest.test_list_images_param_min_max_size                 |
|                       |{idempotent_id('4ad8c157-971a-4ba8-aa84-ed61154b1e7f')}                                             |
|                       |tempest.api.image.v2.test_images.ListImagesTest.test_list_images_param_size                         |
|                       |{idempotent_id('cf1b9a48-8340-480e-af7b-fe7e17690876')}                                             |
|                       |tempest.api.image.v2.test_images.ListImagesTest.test_list_images_param_status                       |
|                       |{idempotent_id('7fc9e369-0f58-4d05-9aa5-0969e2d59d15')}                                             |
|                       |tempest.api.image.v2.test_images.ListImagesTest.test_list_images_param_visibility                   |
|                       |{idempotent_id('7a95bb92-d99e-4b12-9718-7bc6ab73e6d2')}                                             |
+-----------------------+----------------------------------------------------------------------------------------------------+
|environmental          |                                                                                                    |
|requirements &         | environment can be deployed on bare metal of virtualized infrastructure                            |
|preconditions          | deployment can be HA or non-HA                                                                     |
|                       |                                                                                                    |
+-----------------------+----------------------------------------------------------------------------------------------------+
|scenario dependencies  | NA                                                                                                 |
+-----------------------+----------------------------------------------------------------------------------------------------+
|procedural             | Step 1: Test to get all images with container_format='bare'                                        |
|requirements           | Step 2: Test to get all images with disk_format = raw                                              |
|                       | Step 3: Test to get images by limit                                                                |
|                       | Step 4: Test to get all images within a size scope                                                 |
|                       | Step 5: Test to get all images by size                                                             |
|                       | Step 6: Test to get all active images                                                              |
|                       | Step 7: Test to get all images with visibility = private                                           |
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
