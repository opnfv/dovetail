.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Ericsson AB, Huawei Technologies Co.,Ltd

=======================================
VIM image operations test specification
=======================================

Scope
=====

The VIM image test area evaluates the ability of the system under test to support
VIM image operations. The test cases documented here are the Image API test cases
in the Openstack Interop guideline 2017.09 as implemented by the Refstack client.
These test cases will evaluate basic Openstack (as a VIM) image operations including
image creation, image list, image update and image deletion capabilities using Glance v2 API.

Definitions and abbreviations
=============================

The following terms and abbreviations are used in conjunction with this test area

- API - Application Programming Interface
- CRUD - Create, Read, Update, and Delete
- NFVi - Network Functions Virtualization infrastructure
- VIM - Virtual Infrastructure Manager

System Under Test (SUT)
=======================

The system under test is assumed to be the NFVi and VIM in operation on a
Pharos compliant infrastructure.

Test Area Structure
====================

The test area is structured based on VIM image operations. Each test case is able
to run independently, i.e. irrelevant of the state created by a previous test.

For brevity, the test cases in this test area are summarized together based on
the operations they are testing.

All these test cases are included in the test case dovetail.tempest.osinterop of
OVP test suite.

Test Descriptions
=================

----------------------
API Used and Reference
----------------------

Images: https://developer.openstack.org/api-ref/image/v2/

- create image
- delete image
- show image details
- show images
- show image schema
- show images schema
- upload binary image data
- add image tag
- delete image tag

---------------------------------------
Image get tests using the Glance v2 API
---------------------------------------

Test case specification
-----------------------

tempest.api.image.v2.test_images.ListUserImagesTest.test_get_image_schema
tempest.api.image.v2.test_images.ListUserImagesTest.test_get_images_schema
tempest.api.image.v2.test_images_negative.ImagesNegativeTest.test_get_delete_deleted_image
tempest.api.image.v2.test_images_negative.ImagesNegativeTest.test_get_image_null_id
tempest.api.image.v2.test_images_negative.ImagesNegativeTest.test_get_non_existent_image

Test preconditions
------------------

Glance is available.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: Create 6 images and store their ids in a created images list.
* Test action 2: Use image v2 API to show image schema and check the body of the response.
* **Test assertion 1:** In the body of the response, the value of the key 'name' is 'image'.
* Test action 3: Use image v2 API to show images schema and check the body of the response.
* **Test assertion 2:** In the body of the response, the value of the key 'name' is 'images'.
* Test action 4: Create an image with name 'test', container_formats 'bare' and
  disk_formats 'raw'. Delete this image with its id and then try to show it with
  its id. Delete this deleted image again with its id and check the API's response code.
* **Test assertion 3:** The operations of showing and deleting a deleted image with its id
  both get 404 response code.
* Test action 5: Use a null image id to show a image and check the API's response code.
* **Test assertion 4:** The API's response code is 404.
* Test action 6: Generate a random uuid and use it as the image id to show the image.
* **Test assertion 5:** The API's response code is 404.
* Test action 7: Delete the 6 images with the stored ids. Show all images and check
  whether the 6 images' ids are not in the show list.
* **Test assertion 6:** The 6 images' ids are not found in the show list.

Pass / fail criteria
''''''''''''''''''''

The first two test cases evaluate the ability to use Glance v2 API to show image
and images schema. The latter three test cases evaluate the ability to use Glance
v2 API to show images with a deleted image id, a null image id and a non-existing
image id. Specifically it verifies that:

* Glance image get API can show the image and images schema.
* Glance image get API can't show an image with a deleted image id.
* Glance image get API can't show an image with a null image id.
* Glance image get API can't show an image with a non-existing image id.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

None

--------------------------------------
CRUD image operations in Images API v2
--------------------------------------

Test case specification
-----------------------

tempest.api.image.v2.test_images.ListUserImagesTest.test_list_no_params

Test preconditions
------------------

Glance is available.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: Create 6 images and store their ids in a created images list.
* Test action 2: List all images and check whether the ids listed are in the created images list.
* **Test assertion 1:** The ids get from the list images API are in the created images list.

Pass / fail criteria
''''''''''''''''''''

This test case evaluates the ability to use Glance v2 API to list images.
Specifically it verifies that:

* Glance image API can show the images.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

None

----------------------------------------
Image list tests using the Glance v2 API
----------------------------------------

Test case specification
-----------------------

tempest.api.image.v2.test_images.ListUserImagesTest.test_list_images_param_container_format
tempest.api.image.v2.test_images.ListUserImagesTest.test_list_images_param_disk_format
tempest.api.image.v2.test_images.ListUserImagesTest.test_list_images_param_limit
tempest.api.image.v2.test_images.ListUserImagesTest.test_list_images_param_min_max_size
tempest.api.image.v2.test_images.ListUserImagesTest.test_list_images_param_size
tempest.api.image.v2.test_images.ListUserImagesTest.test_list_images_param_status
tempest.api.image.v2.test_images.ListUserImagesTest.test_list_images_param_visibility

Test preconditions
------------------

Glance is available.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: Create 6 images with a random size ranging from 1024 to 4096 and
  visibility 'private'; set their (container_format, disk_format) pair to be
  (ami, ami), (ami, ari), (ami, aki), (ami, vhd), (ami, vmdk) and (ami, raw);
  store their ids in a list and upload the binary images data.
* Test action 2: Use Glance v2 API to list all images whose container_format is 'ami'
  and store the response details in a list.
* **Test assertion 1:** The list is not empty and all the values of container_format
  in the list are 'ami'.
* Test action 3: Use Glance v2 API to list all images whose disk_format is 'raw'
  and store the response details in a list.
* **Test assertion 2:** The list is not empty and all the values of disk_format
  in the list are 'raw'.
* Test action 4: Use Glance v2 API to list one image by setting limit to be 1 and
  store the response details in a list.
* **Test assertion 3:** The length of the list is one.
* Test action 5: Use Glance v2 API to list images by setting size_min and size_max,
  and store the response images' sizes in a list. Choose the first image's size as
  the median, size_min is median-500 and size_max is median+500.
* **Test assertion 4:** All sizes in the list are no less than size_min and no more
  than size_max.
* Test action 6: Use Glance v2 API to show the first created image with its id and
  get its size from the response. Use Glance v2 API to list images whose size is equal
  to this size and store the response details in a list.
* **Test assertion 5:** All sizes of the images in the list are equal to the size
  used to list the images.
* Test action 7: Use Glance v2 API to list the images whose status is active and
  store the response details in a list.
* **Test assertion 6:** All status of images in the list are active.
* Test action 8: Use Glance v2 API to list the images whose visibility is private and
  store the response details in a list.
* **Test assertion 7:** All images' values of visibility in the list are private.
* Test action 9: Delete the 6 images with the stored ids. Show images and check whether
  the 6 ids are not in the show list.
* **Test assertion 8:** The stored 6 ids are not found in the show list.

Pass / fail criteria
''''''''''''''''''''

This test case evaluates the ability to use Glance v2 API to list images with
different parameters. Specifically it verifies that:

* Glance image API can show the images with the container_format.
* Glance image API can show the images with the disk_format.
* Glance image API can show the images by setting a limit number.
* Glance image API can show the images with the size_min and size_max.
* Glance image API can show the images with the size.
* Glance image API can show the images with the status.
* Glance image API can show the images with the visibility type.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

None

------------------------------------------
Image update tests using the Glance v2 API
------------------------------------------

Test case specification
-----------------------

tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_update_image
tempest.api.image.v2.test_images_tags.ImagesTagsTest.test_update_delete_tags_for_image
tempest.api.image.v2.test_images_tags_negative.ImagesTagsNegativeTest.test_update_tags_for_non_existing_image

Test preconditions
------------------

Glance is available.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: Create an image with container_formats 'ami', disk_formats 'ami'
  and visibility 'private' and store its id returned in the response. Check whether
  the status of the created image is 'queued'.
* **Test assertion 1:** The status of the created image is 'queued'.
* Test action 2: Use the stored image id to upload the binary image data and update
  this image's name. Show this image with the stored id. Check if the stored id and
  name used to update the image are equal to the id and name in the show list.
* **Test assertion 2:** The id and name returned in the show list are equal to
  the stored id and name used to update the image.
* Test action 3: Create an image with container_formats 'bare', disk_formats 'raw'
  and visibility 'private' and store its id returned in the response.
* Test action 4: Use the stored id to add a tag. Show the image with the stored id
  and check if the tag used to add is in the image's tags returned in the show list.
* **Test assertion 3:** The tag used to add into the image is in the show list.
* Test action 5: Use the stored id to delete this tag. Show the image with the
  stored id and check if the tag used to delete is not in the show list.
* **Test assertion 4:** The tag used to delete from the image is not in the show list.
* Test action 6: Generate a random uuid as the image id. Use the image id to add a tag
  into the image's tags.
* **Test assertion 5:** The API's response code is 404.
* Test action 7: Delete the images created in test action 1 and 3. Show the images
  and check whether the ids are not in the show list.
* **Test assertion 6:** The two ids are not found in the show list.

Pass / fail criteria
''''''''''''''''''''

This test case evaluates the ability to use Glance v2 API to update images with
different parameters. Specifically it verifies that:

* Glance image API can update image's name with the existing image id.
* Glance image API can update image's tags with the existing image id.
* Glance image API can't update image's tags with a non-existing image id.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

None

--------------------------------------------
Image deletion tests using the Glance v2 API
--------------------------------------------

Test case specification
-----------------------

tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_delete_image
tempest.api.image.v2.test_images_negative.ImagesNegativeTest.test_delete_image_null_id
tempest.api.image.v2.test_images_negative.ImagesNegativeTest.test_delete_non_existing_image
tempest.api.image.v2.test_images_tags_negative.ImagesTagsNegativeTest.test_delete_non_existing_tag

Test preconditions
------------------

Glance is available.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: Create an image with container_formats 'ami', disk_formats 'ami'
  and visibility 'private'. Use the id of the created image to delete the image.
  List all images and check whether this id is in the list.
* **Test assertion 1:** The id of the created image is not found in the list
  of all images after the deletion operation.
* Test action 2: Delete images with a null id and check the API's response code.
* **Test assertion 2:** The API's response code is 404.
* Test action 3: Generate a random uuid and delete images with this uuid as image id.
  Check the API's response code.
* **Test assertion 3:** The API's response code is 404.
* Test action 4: Create an image with container_formats 'bare', disk_formats 'raw'
  and visibility 'private'. Delete this image's tag with the image id and a random tag
  Check the API's response code.
* **Test assertion 4:** The API's response code is 404.
* Test action 5: Delete the images created in test action 1 and 4. List all images
  and check whether the ids are in the list.
* **Test assertion 5:** The two ids are not found in the list.

Pass / fail criteria
''''''''''''''''''''

The first three test cases evaluate the ability to use Glance v2 API to delete images
with an existing image id, a null image id and a non-existing image id. The last one
evaluates the ability to use the API to delete a non-existing image tag.
Specifically it verifies that:

* Glance image deletion API can delete the image with an existing id.
* Glance image deletion API can't delete an image with a null image id.
* Glance image deletion API can't delete an image with a non-existing image id.
* Glance image deletion API can't delete an image tag with a non-existing image tag.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

None
