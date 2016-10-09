.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) OPNFV

==========================================
VIM operations test design specification
==========================================

This document outlines the approach and method for testing VIM operations in the OPNFV compliance test
suite.  Providing a brief outline of the features to be tested, the methodology for testing,
schema's and criteria.

Features to be tested
=====================

The VIM operations compliance test plan outlines the method for testing VIM operations compliance to the OPNFV
platform behaviours and features of VIM operations enabled NFVI platforms. VIM operations Compliance Testing
test cases are described as follows:

Test Case 1: VIM operations XXX
---------------------------------------------------------------------------

.. code-block:: bash

    XXX
    XXX


# ......


Test Case 6: Images v2 update
---------------------------------------------------------------------------

.. code-block:: bash

    tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_update_image
    tempest.api.image.v2.test_images_tags.ImagesTagsTest.test_update_delete_tags_for_image
    tempest.api.image.v2.test_images_tags_negative.ImagesTagsNegativeTest.test_update_tags_for_non_existing_image


# ......


Test Case XXX: VIM operations XXX
---------------------------------------------------------------------------

.. code-block:: bash

    XXX
    XXX


Test approach for VIM operations
===========================

The most common approach for testing VIM operations capabilities in the test suite is through interaction with the SUT.
In this instance the test framework will exercise the NBI provided by the VIM to configure and leverage VIM operations related
features in the platform, instantiate workloads, and invoke behaviours in the platform.  The suite may also interact directly with the
SUT to exercise platform capabilities and further invoke helper functions on the platform for the same purpose.

Test result analysis
=====================

All functional tests in the VIM operations test suite will provide a pass/fail result on completion of the test.  In addition test logs
and relevant additional information will be provided as part of the test log, available on test suite completion.

Some tests in the compliance suite measure such metrics as latency and performance.  At this time these tests are intended to
provide a feature based pass/fail metric not related to system performance.
These tests may however provide detailed results of performance and latency in the 'test report' document.

Test identification
===================

TBD:  WE need to identify the test naming scheme we will use in DoveTail in order that we can cross reference to the test
projects and maintain our suite effectively.  This naming scheme needs to be externally relevant to non-OPNFV consumers and as
such some consideration is required on the selection.

template
<dovetail><vimops><Images v2 update>
<dovetail>: the project name
<vimops>: the target test suite
<Images v2 update>: the specific use cases being tested


Pass/Fail Criteria
==================

For each specific use case, if normal response code 200 is returned the test passes，
otherwise the test fails with various error codes. Refer to Images API v2.0 [1]_

All the specific use cases can be run independently. If all the specific use cases in the test suite pass
the test suite passes, otherwise it fails.


.._[1]: http://developer.openstack.org/api-ref/image/v2/
