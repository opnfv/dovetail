.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) OPNFV

==============================================================
Dovetail VIM Operations tc006 specification - Images v2 update
==============================================================

.. table::
   :class: longtable

+-----------------------+---------------------------------------------------------------------------------------------------------------+
|test case name         |Images v2 update                                                                                               |
|                       |                                                                                                               |
+-----------------------+---------------------------------------------------------------------------------------------------------------+
|id                     |dovetail.vimops.tc006                                                                                          |
+-----------------------+---------------------------------------------------------------------------------------------------------------+
|objective              |Image update tests using the Glance v2 API                                                                     |
+-----------------------+---------------------------------------------------------------------------------------------------------------+
|test items             |tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_update_image                                   |
|                       |{idempotent_id('f66891a7-a35c-41a8-b590-a065c2a1caa6')}                                                        |
|                       |tempest.api.image.v2.test_images_tags.ImagesTagsTest.test_update_delete_tags_for_image                         |
|                       |{idempotent_id('10407036-6059-4f95-a2cd-cbbbee7ed329')}                                                        |
|                       |tempest.api.image.v2.test_images_tags_negative.ImagesTagsNegativeTest.test_update_tags_for_non_existing_image  |
|                       |{idempotent_id('8cd30f82-6f9a-4c6e-8034-c1b51fba43d9')}                                                        |
+-----------------------+---------------------------------------------------------------------------------------------------------------+
|environmental          |                                                                                                               |
|requirements &         | environment can be deployed on bare metal of virtualized infrastructure                                       |
|preconditions          | deployment can be HA or non-HA                                                                                |
|                       |                                                                                                               |
+-----------------------+---------------------------------------------------------------------------------------------------------------+
|scenario dependencies  | NA                                                                                                            |
+-----------------------+---------------------------------------------------------------------------------------------------------------+
|procedural             | Step 1: updates an image by image_id                                                                          |
|requirements           | Step 2: creating/deleting image tag and verify it                                                             |
|                       | Step 3: update tag with non existing image                                                                    |
+-----------------------+---------------------------------------------------------------------------------------------------------------+
|input specifications   |The parameters needed to execute Images APIs.                                                                  |
|                       |Refer to Images API v2.0 [1]_                                                                                  |
+-----------------------+---------------------------------------------------------------------------------------------------------------+
|output specifications  |The responses after executing Images APIs.                                                                     |
|                       |Refer to Images API v2.0 [1]_                                                                                  |
+-----------------------+---------------------------------------------------------------------------------------------------------------+
|pass/fail criteria     |If normal response code 200 is returned, the test passes.                                                      |
|                       |Otherwise, the test fails with various error codes.                                                            |
|                       |Refer to Images API v2.0 [1]_                                                                                  |
+-----------------------+---------------------------------------------------------------------------------------------------------------+
|test report            |TBD                                                                                                            |
+-----------------------+---------------------------------------------------------------------------------------------------------------+

.._[1]: http://developer.openstack.org/api-ref/image/v2/
