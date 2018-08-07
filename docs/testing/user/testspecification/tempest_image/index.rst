.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Ericsson AB

===========================================
Tempest Image test specification
===========================================


Scope
=====

The Tempest Image test area tests the basic operations of Images of the System Under
Test (SUT) through the life of a VNF. The tests in this test area will evaluate IPv4
network runtime operations functionality.

References
==========

`Image Service API v2 <https://developer.openstack.org/api-ref/image/v2/index.html#images>`_

System Under Test (SUT)
=======================

The system under test is assumed to be the NFVi and VIM in operation on a
Pharos compliant infrastructure.

Test Area Structure
===================

The test area is structured in individual tests as listed below.
For detailed information on the individual steps and assertions performed
by the tests, review the Python source code accessible via the following links:

All these test cases are included in the test case dovetail.tempest.image of
OVP test suite.

- `Register, Upload, Get Image and Get Image File API's <https://github.com/openstack/tempest/blob/18.0.0/tempest/api/image/v2/test_images.py#L32>`_
    - tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_register_upload_get_image_file

- `List Versions <https://github.com/openstack/tempest/blob/18.0.0/tempest/api/image/v2/test_versions.py>`_
    - tempest.api.image.v2.test_versions.VersionsTest.test_list_versions