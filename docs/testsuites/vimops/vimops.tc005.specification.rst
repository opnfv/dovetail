.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) OPNFV

==============================================================
Dovetail VIM Operations tc005 specification - Images v2 import
==============================================================

.. table::
   :class: longtable

+-----------------------+---------------------------------------------------------------------------------------------------------+
|test case name         |Images v2 import                                                                                         |
|                       |                                                                                                         |
+-----------------------+---------------------------------------------------------------------------------------------------------+
|id                     |dovetail.vimops.tc005                                                                                    |
+-----------------------+---------------------------------------------------------------------------------------------------------+
|objective              |Image registration tests using the Glance v2 API                                                         |
+-----------------------+---------------------------------------------------------------------------------------------------------+
|test items             |tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_register_upload_get_image_file           |
|                       |{idempotent_id('139b765e-7f3d-4b3d-8b37-3ca3876ee318')}                                                  |
|                       |tempest.api.image.v2.test_images_negative.ImagesNegativeTest.test_register_with_invalid_container_format |
|                       |{idempotent_id('292bd310-369b-41c7-a7a3-10276ef76753')}                                                  |
|                       |tempest.api.image.v2.test_images_negative.ImagesNegativeTest.test_register_with_invalid_disk_format      |
|                       |{idempotent_id('70c6040c-5a97-4111-9e13-e73665264ce1')}                                                  |
+-----------------------+---------------------------------------------------------------------------------------------------------+
|environmental          |                                                                                                         |
|requirements &         | environment can be deployed on bare metal of virtualized infrastructure                                 |
|preconditions          | deployment can be HA or non-HA                                                                          |
|                       |                                                                                                         |
+-----------------------+---------------------------------------------------------------------------------------------------------+
|scenario dependencies  | NA                                                                                                      |
+-----------------------+---------------------------------------------------------------------------------------------------------+
|procedural             | Step 1: Register image, upload the image file, get image and get image file api's                       |
|requirements           | Step 2: Negative tests for invalid data supplied to POST /images                                        |
|                       | Step 3: Negative tests for invalid disk format                                                          |
+-----------------------+---------------------------------------------------------------------------------------------------------+
|input specifications   |The parameters needed to execute Images APIs.                                                            |
|                       |Refer to Images API v2.0 [1]_                                                                            |
+-----------------------+---------------------------------------------------------------------------------------------------------+
|output specifications  |The responses after executing Images APIs.                                                               |
|                       |Refer to Images API v2.0 [1]_                                                                            |
+-----------------------+---------------------------------------------------------------------------------------------------------+
|pass/fail criteria     |If normal response code 200 is returned, the test passes.                                                |
|                       |Otherwise, the test fails with various error codes.                                                      |
|                       |Refer to Images API v2.0 [1]_                                                                            |
+-----------------------+---------------------------------------------------------------------------------------------------------+
|test report            |TBD                                                                                                      |
+-----------------------+---------------------------------------------------------------------------------------------------------+

.._[1]: http://developer.openstack.org/api-ref/image/v2/
