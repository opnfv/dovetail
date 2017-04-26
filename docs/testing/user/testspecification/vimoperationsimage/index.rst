.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Ericsson AB

=======================================
VIM image operations test specification
=======================================

.. toctree::
   :maxdepth: 2

Each test case requires documentation according to:
* Use case specification
* Test preconditions
* Basic test flow execution descriptor
* Post conditions and pass fail criteria

tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_delete_image
tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_update_image
tempest.api.image.v2.test_images.ListImagesTest.test_get_image_schema
tempest.api.image.v2.test_images.ListImagesTest.test_get_images_schema
tempest.api.image.v2.test_images.ListImagesTest.test_index_no_params
tempest.api.image.v2.test_images.ListImagesTest.test_list_images_param_container_format
tempest.api.image.v2.test_images.ListImagesTest.test_list_images_param_disk_format
tempest.api.image.v2.test_images.ListImagesTest.test_list_images_param_limit
tempest.api.image.v2.test_images.ListImagesTest.test_list_images_param_min_max_size
tempest.api.image.v2.test_images.ListImagesTest.test_list_images_param_size
tempest.api.image.v2.test_images.ListImagesTest.test_list_images_param_status
tempest.api.image.v2.test_images.ListImagesTest.test_list_images_param_visibility
tempest.api.image.v2.test_images.ListImagesTest.test_list_no_params
tempest.api.image.v2.test_images.ListUserImagesTest.test_get_image_schema
tempest.api.image.v2.test_images.ListUserImagesTest.test_get_images_schema
tempest.api.image.v2.test_images.ListUserImagesTest.test_list_images_param_container_format
tempest.api.image.v2.test_images.ListUserImagesTest.test_list_images_param_disk_format
tempest.api.image.v2.test_images.ListUserImagesTest.test_list_images_param_limit
tempest.api.image.v2.test_images.ListUserImagesTest.test_list_images_param_min_max_size
tempest.api.image.v2.test_images.ListUserImagesTest.test_list_images_param_size
tempest.api.image.v2.test_images.ListUserImagesTest.test_list_images_param_status
tempest.api.image.v2.test_images.ListUserImagesTest.test_list_images_param_visibility
tempest.api.image.v2.test_images.ListUserImagesTest.test_list_no_params
tempest.api.image.v2.test_images_negative.ImagesNegativeTest.test_delete_image_null_id
tempest.api.image.v2.test_images_negative.ImagesNegativeTest.test_delete_non_existing_image
tempest.api.image.v2.test_images_negative.ImagesNegativeTest.test_get_delete_deleted_image
tempest.api.image.v2.test_images_negative.ImagesNegativeTest.test_get_image_null_id
tempest.api.image.v2.test_images_negative.ImagesNegativeTest.test_get_non_existent_image
tempest.api.image.v2.test_images_tags.ImagesTagsTest.test_update_delete_tags_for_image
tempest.api.image.v2.test_images_tags_negative.ImagesTagsNegativeTest.test_delete_non_existing_tag
tempest.api.image.v2.test_images_tags_negative.ImagesTagsNegativeTest.test_update_tags_for_non_existing_image
