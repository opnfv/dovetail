.. This work is licensed under a Creative Commons Attribution 4.0
.. International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) OPNFV

==============================================================
Dovetail VIM Operations tc006 specification - Images v2 update
==============================================================

Test Case Name
===============
Images v2 update

Test Case ID
=============
dovetail.vimops.tc006

Objective
==========
Verify the image update tests using the Glance v2 API

Functionality
=============
Function description or high-level test process

Test Item
=========

Test item 1
-----------

Update an image by image_id, reference:
tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_update_image:
{idempotent_id('f66891a7-a35c-41a8-b590-a065c2a1caa6')}

Test item 2
-----------

Update an image tag, reference:
tempest.api.image.v2.test_images_tags.ImagesTagsTest.test_update_delete_tags_for_image:
{idempotent_id('10407036-6059-4f95-a2cd-cbbbee7ed329')}

Test item 3
-----------

Update tag with non existing image, reference:
tempest.api.image.v2.test_images_tags_negative.ImagesTagsNegativeTest.
test_update_tags_for_non_existing_image:
{idempotent_id('8cd30f82-6f9a-4c6e-8034-c1b51fba43d9')}

Environmental requirements and precoditions
============================================

Environment can be deployed on bare metal of virtualized infrastructure.
Deployment can be HA or non-HA.

Scenario dependencies
=====================

NA

Preconditions and Procedural requirements
=========================================

NA

Input Specifications
====================

The parameters needed to execute Images APIs. Refer to Images API v2.0 '[1]'_

Output Specifications
=====================

The responses after executing Images APIs. Refer to Images API v2.0 '[1]'_

Pass/Fail criteria
==================

If normal response code 200 is returned the test passes, otherwise the test
case fails with various error codes. Refer to Images API v2.0 '[1]'_

Test Reporting
==============

The test report for this test case will be generated with links to relevant
data sources. This section can be updated once we have a template for the
report in place.

.._[1]: http://developer.openstack.org/api-ref/image/v2/
