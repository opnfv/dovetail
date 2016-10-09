.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) OPNFV

==============================================================
Dovetail VIM Operations tc002 specification - Images v2 delete
==============================================================

.. table::
   :class: longtable

+-----------------------+----------------------------------------------------------------------------------------------------+
|test case name         |Images v2 delete                                                                                    |
|                       |                                                                                                    |
+-----------------------+----------------------------------------------------------------------------------------------------+
|id                     |dovetail.vimops.tc002                                                                               |
+-----------------------+----------------------------------------------------------------------------------------------------+
|objective              |image deletion tests using the Glance v2 API                                                        |
+-----------------------+----------------------------------------------------------------------------------------------------+
|test items             |tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_delete_image                        |
|                       |{idempotent_id('f848bb94-1c6e-45a4-8726-39e3a5b23535')}                                             |
|                       |tempest.api.image.v2.test_images_negative.ImagesNegativeTest.test_delete_image_null_id              |
|                       |{idempotent_id('32248db1-ab88-4821-9604-c7c369f1f88c')}                                             |
|                       |tempest.api.image.v2.test_images_negative.ImagesNegativeTest.test_delete_non_existing_image         |
|                       |{idempotent_id('6fe40f1c-57bd-4918-89cc-8500f850f3de')}                                             |
|                       |tempest.api.image.v2.test_images_tags_negative.ImagesTagsNegativeTest.test_delete_non_existing_tag  |
|                       |{idempotent_id('39c023a2-325a-433a-9eea-649bf1414b19')}                                             |
+-----------------------+----------------------------------------------------------------------------------------------------+
|environmental          |                                                                                                    |
|requirements &         | environment can be deployed on bare metal of virtualized infrastructure                            |
|preconditions          | deployment can be HA or non-HA                                                                     |
|                       |                                                                                                    |
+-----------------------+----------------------------------------------------------------------------------------------------+
|scenario dependencies  | NA                                                                                                 |
+-----------------------+----------------------------------------------------------------------------------------------------+
|procedural             | Step 1: delete an image by image id                                                                |
|requirements           | Step 2: delete image with image_id=NULL                                                            |
|                       | Step 3: delete non-existent image                                                                  |
|                       | Step 4: delete non-existing tag                                                                    |
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
