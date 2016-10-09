.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) OPNFV

============================================================
Dovetail VIM Operations tc003 specification - Images v2 get
============================================================

.. table::
   :class: longtable

+-----------------------+----------------------------------------------------------------------------------------------------+
|test case name         |Images v2 get                                                                                       |
|                       |                                                                                                    |
+-----------------------+----------------------------------------------------------------------------------------------------+
|id                     |dovetail.vimops.tc003                                                                               |
+-----------------------+----------------------------------------------------------------------------------------------------+
|objective              |Image get tests using the Glance v2 API                                                             |
+-----------------------+----------------------------------------------------------------------------------------------------+
|test items             |tempest.api.image.v2.test_images.ListImagesTest.test_get_image_schema                               |
|                       |{idempotent_id('622b925c-479f-4736-860d-adeaf13bc371')}                                             |
|                       |tempest.api.image.v2.test_images.ListImagesTest.test_get_images_schema                              |
|                       |{idempotent_id('25c8d7b2-df21-460f-87ac-93130bcdc684')}                                             |
|                       |tempest.api.image.v2.test_images_negative.ImagesNegativeTest.test_get_delete_deleted_image          |
|                       |{idempotent_id('e57fc127-7ba0-4693-92d7-1d8a05ebcba9')}                                             |
|                       |tempest.api.image.v2.test_images_negative.ImagesNegativeTest.test_get_image_null_id                 |
|                       |{idempotent_id('ef45000d-0a72-4781-866d-4cb7bf2562ad')}                                             |
|                       |tempest.api.image.v2.test_images_negative.ImagesNegativeTest.test_get_non_existent_image            |
|                       |{idempotent_id('668743d5-08ad-4480-b2b8-15da34f81d9f')}                                             | 
+-----------------------+----------------------------------------------------------------------------------------------------+
|environmental          |                                                                                                    |
|requirements &         | environment can be deployed on bare metal of virtualized infrastructure                            |
|preconditions          | deployment can be HA or non-HA                                                                     |
|                       |                                                                                                    |
+-----------------------+----------------------------------------------------------------------------------------------------+
|scenario dependencies  | NA                                                                                                 |
+-----------------------+----------------------------------------------------------------------------------------------------+
|procedural             | Step 1: Test to get image schema                                                                   |
|requirements           | Step 2: Test to get images schema                                                                  |
|                       | Step 3: get and delete the deleted image                                                           |
|                       | Step 4: get image with image_id = NULL                                                             |
|                       | Step 5: get the non-existent image
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
