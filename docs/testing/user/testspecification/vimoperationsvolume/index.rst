.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Ericsson AB, Huawei Technologies Co.,Ltd

=========================================
VIM volume operations test specification
=========================================

.. toctree::
   :maxdepth: 2

Scope
=====

The VIM volume operations test area evaluates the ability of the system under
test to support VIM volume operations. The test cases documented here are the
volume API test cases in the OpenStack Interop guideline 2016.8 as implemented
by the RefStack client. These test cases will evaluate basic OpenStack (as a VIM)
volume operations, including:

- Volume attach and detach operations
- Volume service availability zone operations
- Volume cloning operations
- Image copy-to-volume operations
- Volume creation and deletion operations
- Volume service extension listing
- Volume metadata operations
- Volume snapshot operations

References
================

- OpenStack Governance/Interop

  - https://wiki.openstack.org/wiki/Governance/InteropWG

- OpenStack Interoperability guidelines (version 2016.08)

  - https://github.com/openstack/interop/blob/master/2016.08.json

- Refstack client

  - https://github.com/openstack/refstack-client

Definitions and abbreviations
=============================

The following terms and abbreviations are used in conjunction with this test area

- API - Application Programming Interface
- NFVi - Network Functions Virtualization infrastructure
- SUT - System Under Test
- VIM - Virtual Infrastructure Manager
- VM - Virtual Machine

System Under Test (SUT)
=======================

The system under test is assumed to be the NFVI and VIM deployed with a Pharos compliant infrastructure.

Test Area Structure
====================

The test area is structured based on VIM volume API operations. Each test case is
able to run independently, i.e. irrelevant of the state created by a previous test.
Specifically, every test performs clean-up operations which return the system to
the same state as before the test.

For brevity, the test cases in this test area are summarized together based on
the operations they are testing.

All these test cases are included in the test case dovetail.osinterop.tc001 of
cvp test suite.

Test Descriptions
=================

API Used and Reference
----------------------

Block storage: https://developer.openstack.org/api-ref/block-storage

- create volume
- delete volume
- update volume
- attach volume to server
- detach volume from server
- create volume metadata
- update volume metadata
- delete volume metadata
- list volume

- create snapshot
- update snapshot
- delete snapshot

------------------------------------------------------------------------
Test Case 1 - Volume attach and detach operations with the Cinder v2 API
------------------------------------------------------------------------

Test case specification
-----------------------

tempest.api.volume.test_volumes_actions.VolumesV2ActionsTest.test_attach_detach_volume_to_instance
tempest.api.volume.test_volumes_actions.VolumesV2ActionsTest.test_get_volume_attachment
tempest.api.volume.test_volumes_negative.VolumesV2NegativeTest.test_attach_volumes_with_nonexistent_volume_id
tempest.api.volume.test_volumes_negative.VolumesV2NegativeTest.test_detach_volumes_with_invalid_volume_id

Test preconditions
------------------

* Volume extension API

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''
* Test action 1: Create a server VM1
* Test action 2: Attach a provided VOL1 to VM1
* **Test assertion 1:** Verify VOL1 is in 'in-use' status
* Test action 3: Detach VOL1 from VM1
* **Test assertion 2:** Verify VOL1 is in 'available' status
* Test action 4: Create a server VM2
* Test action 5: Attach a provided VOL2 to VM2 and wait for VOL2 to reach 'in-use' status
* Test action 6: Retrieve VOL2's attachment information ATTCH_INFO
* **Test assertion 3:** Verify ATTCH_INFO is correct
* Test action 7: Create a server VM3 and wait for VM3 to reach 'ACTIVE' status
* Test action 8: Attach a non-existent volume to VM3
* **Test assertion 4:** Verify attach volume failed, a 'NOT FOUND' error is returned in the response
* Test action 9: Detach a volume from a server by using an invalid volume ID
* **Test assertion 5:** Verify detach volume failed, a 'NOT FOUND' error is returned in the response

Pass / fail criteria
''''''''''''''''''''

This test evaluates the volume API ability of attaching a volume to a server
and detaching a volume from a server. Specifically, the test verifies that:

* Volumes can be attached and detached from servers.
* Volume attachment information can be retrieved.
* Attach and detach a volume using an invalid volume ID is not allowed.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A

--------------------------------------------------------------------------------
Test Case 2 - Volume service availability zone operations with the Cinder v2 API
--------------------------------------------------------------------------------

Test case specification
-----------------------

tempest.api.volume.test_availability_zone.AvailabilityZoneV2TestJSON.test_get_availability_zone_list

tempest.api.volume.test_availability_zone.AvailabilityZoneTestJSON.test_get_availability_zone_list

Note: the second test case is the alias of the first one.
Alias should always be included so that the test run will be tempest version agnostic,
which can be used to test different version of Openstack.

Test preconditions
------------------

* Volume extension API

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''
* Test action 1: List all existent availability zones
* **Test assertion 1:** Verify the availability zone list length is greater than 0

Pass / fail criteria
''''''''''''''''''''

This test case evaluates the volume API ability of listing availability zones.
Specifically, the test verifies that:

* Availability zones can be listed.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A

--------------------------------------------------------------
Test Case 3 - Volume cloning operations with the Cinder v2 API
--------------------------------------------------------------

Test case specification
-----------------------

tempest.api.volume.test_volumes_get.VolumesV2GetTest.test_volume_create_get_update_delete_as_clone

tempest.api.volume.test_volumes_get.VolumesGetTest.test_volume_create_get_update_delete_as_clone

Note: the second test case is the alias of the first one.
Alias should always be included so that the test run will be tempest version agnostic,
which can be used to test different version of Openstack.

Test preconditions
------------------

* Volume extension API
* Cinder volume clones feature is enabled

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''
* Test action 1: Create a volume VOL1
* Test action 2: Create a volume VOL2 from source volume VOL1 with a specific name and metadata
* Test action 2: Wait for VOL2 to reach 'available' status
* **Test assertion 1:** Verify the name of VOL2 is correct
* Test action 3: Retrieve VOL2's detail information
* **Test assertion 2:** Verify the retrieved volume name, ID and metadata are the same as VOL2
* **Test assertion 3:** Verify VOL2's bootable flag is 'False'
* Test action 4: Update the name of VOL2 with the original value
* Test action 5: Update the name of VOL2 with a new value
* **Test assertion 4:** Verify the name of VOL2 is updated successfully
* Test action 6: Create a volume VOL3 with no name specified and a description contains characters '@#$%^*'
* **Test assertion 5:** Verify VOL3 is created successfully
* Test action 7: Update the name of VOL3 and description with the original value
* **Test assertion 6:** Verify VOL3's bootable flag is 'False'

Pass / fail criteria
''''''''''''''''''''

This test case evaluates the volume API ability of creating a cloned volume from a source volume,
getting cloned volume detail information and updating cloned volume attributes.

Specifically, the test verifies that:

* Cloned volume can be created from a source volume.
* Cloned volume detail information can be retrieved.
* Cloned volume detail information can be updated.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A

--------------------------------------------------------------------
Test Case 4 - Image copy-to-volume operations with the Cinder v2 API
--------------------------------------------------------------------

Test case specification
-----------------------

tempest.api.volume.test_volumes_actions.VolumesV2ActionsTest.test_volume_bootable
tempest.api.volume.test_volumes_get.VolumesV2GetTest.test_volume_create_get_update_delete_from_image

tempest.api.volume.test_volumes_get.VolumesActionsTest.test_volume_bootable
tempest.api.volume.test_volumes_get.VolumesGetTest.test_volume_create_get_update_delete_from_image

Note: the last 2 test cases are the alias of the former 2.
Alias should always be included so that the test run will be tempest version agnostic,
which can be used to test different version of Openstack.

Test preconditions
------------------

* Volume extension API

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''
* Test action 1: Set a provided volume VOL1's bootable flag to 'True'
* Test action 2: Retrieve VOL1's bootable flag
* **Test assertion 1:** Verify VOL1's bootable flag is 'True'
* Test action 3: Set a provided volume VOL1's bootable flag to 'False'
* Test action 4: Retrieve VOL1's bootable flag
* **Test assertion 2:** Verify VOL1's bootable flag is 'False'
* Test action 5: Create a bootable volume VOL2 from one image with a specific name and metadata
* Test action 6: Wait for VOL2 to reach 'available' status
* **Test assertion 3:** Verify the name of VOL2 name is correct
* Test action 7: Retrieve VOL2's information
* **Test assertion 4:** Verify the retrieved volume name, ID and metadata are the same as VOL2
* **Test assertion 5:** Verify VOL2's bootable flag is 'True'
* Test action 8: Update the name of VOL2 with the original value
* Test action 9: Update the name of VOL2 with a new value
* **Test assertion 6:** Verify the name of VOL2 is updated successfully
* Test action 10: Create a volume VOL3 with no name specified and a description contains characters '@#$%^*'
* **Test assertion 7:** Verify VOL3 is created successfully
* Test action 11: Update the name of VOL3 and description with the original value
* **Test assertion 8:** Verify VOL3's bootable flag is 'True'

Pass / fail criteria
''''''''''''''''''''

This test case evaluates the volume API ability of updating volume's bootable flag and creating
a bootable volume from an image, getting bootable volume detail information and updating bootable volume.

Specifically, the test verifies that:

* Volume bootable flag can be set and retrieved.
* Bootable volume can be created from a source volume.
* Bootable volume detail information can be retrieved.
* Bootable volume detail information can be updated.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A

----------------------------------------------------------------------------
Test Case 5 - Volume creation and deletion operations with the Cinder v2 API
----------------------------------------------------------------------------

Test case specification
-----------------------

tempest.api.volume.test_volumes_get.VolumesV2GetTest.test_volume_create_get_update_delete
tempest.api.volume.test_volumes_negative.VolumesV2NegativeTest.test_create_volume_with_invalid_size
tempest.api.volume.test_volumes_negative.VolumesV2NegativeTest.test_create_volume_with_nonexistent_source_volid
tempest.api.volume.test_volumes_negative.VolumesV2NegativeTest.test_create_volume_with_nonexistent_volume_type
tempest.api.volume.test_volumes_negative.VolumesV2NegativeTest.test_create_volume_with_out_passing_size
tempest.api.volume.test_volumes_negative.VolumesV2NegativeTest.test_create_volume_with_size_negative
tempest.api.volume.test_volumes_negative.VolumesV2NegativeTest.test_create_volume_with_size_zero

tempest.api.volume.test_volumes_get.VolumesGetTest.test_volume_create_get_update_delete
tempest.api.volume.test_volumes_negative.VolumesNegativeTest.test_create_volume_with_invalid_size
tempest.api.volume.test_volumes_negative.VolumesNegativeTest.test_create_volume_with_nonexistent_source_volid
tempest.api.volume.test_volumes_negative.VolumesNegativeTest.test_create_volume_with_nonexistent_volume_type

tempest.api.volume.test_volumes_negative.VolumesV2NegativeTest.test_create_volume_without_passing_size
tempest.api.volume.test_volumes_negative.VolumesNegativeTest.test_create_volume_without_passing_size

tempest.api.volume.test_volumes_negative.VolumesNegativeTest.test_create_volume_with_size_negative
tempest.api.volume.test_volumes_negative.VolumesNegativeTest.test_create_volume_with_size_zero

Note: test cases 8 to 11 are the alias of the fist 4 test cases, test cases 12 and 13 are both alias of
test case 5, and test cases 14 and 15 are the alias of the cases 6 and 7, respectively.
Alias should always be included so that the test run will be tempest version agnostic,
which can be used to test different version of OpenStack.

Test preconditions
------------------

* Volume extension API

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''
* Test action 1: Create a volume VOL1 with a specific name and metadata
* Test action 2: Wait for VOL1 to reach 'available' status
* **Test assertion 1:** Verify the name of VOL1 is correct
* Test action 3: Retrieve VOL1's information
* **Test assertion 2:** Verify the retrieved volume name, ID and metadata are the same as VOL1
* **Test assertion 3:** Verify VOL1's bootable flag is 'False'
* Test action 4: Update the name of VOL1 with the original value
* Test action 5: Update the name of VOL1 with a new value
* **Test assertion 4:** Verify the name of VOL1 is updated successfully
* Test action 6: Create a volume VOL2 with no name specified and a description contains characters '@#$%^*'
* **Test assertion 5:** Verify VOL2 is created successfully
* Test action 7: Update the name of VOL2 and description with the original value
* **Test assertion 6:** Verify VOL2's bootable flag is 'False'
* Test action 8: Create a volume with an invalid size '#$%'
* **Test assertion 7:** Verify create volume failed, a bad request error is returned in the response
* Test action 9: Create a volume with a nonexistent source volume
* **Test assertion 8:** Verify create volume failed, a 'Not Found' error is returned in the response
* Test action 10: Create a volume with a nonexistent volume type
* **Test assertion 9:** Verify create volume failed, a 'Not Found' error is returned in the response
* Test action 11: Create a volume without passing a volume size
* **Test assertion 10:** Verify create volume failed, a bad request error is returned in the response
* Test action 12: Create a volume with a negative volume size
* **Test assertion 11:** Verify create volume failed, a bad request error is returned in the response
* Test action 13: Create a volume with volume size '0'
* **Test assertion 12:** Verify create volume failed, a bad request error is returned in the response

Pass / fail criteria
''''''''''''''''''''

This test case evaluates the volume API ability of creating a volume, getting volume
detail information and updating volume, the reference is,
Specifically, the test verifies that:

* Volume can be created from a source volume.
* Volume detail information can be retrieved/updated.
* Create a volume with an invalid size is not allowed.
* Create a volume with a nonexistent source volume or volume type is not allowed.
* Create a volume without passing a volume size is not allowed.
* Create a volume with a negative volume size is not allowed.
* Create a volume with volume size '0' is not allowed.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A

--------------------------------------------------------------------------------
Test Case 6 - Volume service extension listing operations with the Cinder v2 API
--------------------------------------------------------------------------------

Test case specification
-----------------------

tempest.api.volume.test_extensions.ExtensionsV2TestJSON.test_list_extensions

tempest.api.volume.test_extensions.ExtensionsTestJSON.test_list_extensions

Note: the second test case is the alias of the first one.
Alias should always be included so that the test run will be tempest version agnostic,
which can be used to test different version of Openstack.

Test preconditions
------------------

* Volume extension API
* At least one Cinder extension is configured

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: List all cinder service extensions
* **Test assertion 1:** Verify all extensions are list in the extension list

Pass / fail criteria
''''''''''''''''''''

This test case evaluates the volume API ability of listing all existent volume service extensions.

* Cinder service extensions can be listed.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A

----------------------------------------------------------
Test Case 7 - Volume GET operations with the Cinder v2 API
----------------------------------------------------------

Test case specification
-----------------------

tempest.api.volume.test_volumes_negative.VolumesV2NegativeTest.test_get_invalid_volume_id
tempest.api.volume.test_volumes_negative.VolumesV2NegativeTest.test_get_volume_without_passing_volume_id
tempest.api.volume.test_volumes_negative.VolumesV2NegativeTest.test_volume_get_nonexistent_volume_id

tempest.api.volume.test_volumes_negative.VolumesNegativeTest.test_get_invalid_volume_id
tempest.api.volume.test_volumes_negative.VolumesNegativeTest.test_get_volume_without_passing_volume_id"
tempest.api.volume.test_volumes_negative.VolumesNegativeTest.test_volume_get_nonexistent_volume_id

Note: the latter 3 test cases is the alias of the first 3 ones.
Alias should always be included so that the test run will be tempest version agnostic,
which can be used to test different version of Openstack.

Test preconditions
------------------

* Volume extension API

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: Retrieve a volume with an invalid volume ID
* **Test assertion 1:** Verify retrieve volume failed, a 'Not Found' error is returned in the response
* Test action 2: Retrieve a volume with an empty volume ID
* **Test assertion 2:** Verify retrieve volume failed, a 'Not Found' error is returned in the response
* Test action 3: Retrieve a volume with a nonexistent volume ID
* **Test assertion 3:** Verify retrieve volume failed, a 'Not Found' error is returned in the response

Pass / fail criteria
''''''''''''''''''''

This test case evaluates the volume API ability of getting volumes.
Specifically, the test verifies that:

* Get a volume with an invalid/an empty/a nonexistent volume ID is not allowed.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A

--------------------------------------------------------------
Test Case 8 - Volume listing operations with the Cinder v2 API
--------------------------------------------------------------

Test case specification
-----------------------

tempest.api.volume.test_volumes_list.VolumesV2ListTestJSON.test_volume_list
tempest.api.volume.test_volumes_list.VolumesV2ListTestJSON.test_volume_list_by_name
tempest.api.volume.test_volumes_list.VolumesV2ListTestJSON.test_volume_list_details_by_name
tempest.api.volume.test_volumes_list.VolumesV2ListTestJSON.test_volume_list_param_display_name_and_status
tempest.api.volume.test_volumes_list.VolumesV2ListTestJSON.test_volume_list_with_detail_param_display_name_and_status
tempest.api.volume.test_volumes_list.VolumesV2ListTestJSON.test_volume_list_with_detail_param_metadata
tempest.api.volume.test_volumes_list.VolumesV2ListTestJSON.test_volume_list_with_details
tempest.api.volume.test_volumes_list.VolumesV2ListTestJSON.test_volume_list_with_param_metadata
tempest.api.volume.test_volumes_list.VolumesV2ListTestJSON.test_volumes_list_by_availability_zone
tempest.api.volume.test_volumes_list.VolumesV2ListTestJSON.test_volumes_list_by_status
tempest.api.volume.test_volumes_list.VolumesV2ListTestJSON.test_volumes_list_details_by_availability_zone
tempest.api.volume.test_volumes_list.VolumesV2ListTestJSON.test_volumes_list_details_by_status
tempest.api.volume.test_volumes_negative.VolumesV2NegativeTest.test_list_volumes_detail_with_invalid_status
tempest.api.volume.test_volumes_negative.VolumesV2NegativeTest.test_list_volumes_detail_with_nonexistent_name
tempest.api.volume.test_volumes_negative.VolumesV2NegativeTest.test_list_volumes_with_invalid_status
tempest.api.volume.test_volumes_negative.VolumesV2NegativeTest.test_list_volumes_with_nonexistent_name
tempest.api.volume.v2.test_volumes_list.VolumesV2ListTestJSON.test_volume_list_details_pagination
tempest.api.volume.v2.test_volumes_list.VolumesV2ListTestJSON.test_volume_list_details_with_multiple_params
tempest.api.volume.v2.test_volumes_list.VolumesV2ListTestJSON.test_volume_list_pagination

tempest.api.volume.test_volumes_list.VolumesListTestJSON.test_volume_list
tempest.api.volume.test_volumes_list.VolumesListTestJSON.test_volume_list_by_name
tempest.api.volume.test_volumes_list.VolumesListTestJSON.test_volume_list_details_by_name
tempest.api.volume.test_volumes_list.VolumesListTestJSON.test_volume_list_param_display_name_and_status
tempest.api.volume.test_volumes_list.VolumesListTestJSON.test_volume_list_with_detail_param_display_name_and_status
tempest.api.volume.test_volumes_list.VolumesListTestJSON.test_volume_list_with_detail_param_metadata
tempest.api.volume.test_volumes_list.VolumesListTestJSON.test_volume_list_with_details
tempest.api.volume.test_volumes_list.VolumesListTestJSON.test_volume_list_with_param_metadata
tempest.api.volume.test_volumes_list.VolumesListTestJSON.test_volume_list_by_availability_zone
tempest.api.volume.test_volumes_list.VolumesListTestJSON.test_volume_list_by_status
tempest.api.volume.test_volumes_list.VolumesListTestJSON.test_volume_list_details_by_availability_zone
tempest.api.volume.test_volumes_list.VolumesListTestJSON.test_volume_list_details_by_status
tempest.api.volume.test_volumes_negative.VolumesNegativeTest.test_list_volumes_detail_with_invalid_status
tempest.api.volume.test_volumes_negative.VolumesNegativeTest.test_list_volumes_detail_with_nonexistent_name
tempest.api.volume.test_volumes_negative.VolumesNegativeTest.test_list_volumes_with_invalid_status
tempest.api.volume.test_volumes_negative.VolumesNegativeTest.test_list_volumes_with_nonexistent_name
tempest.api.volume.v2.test_volumes_list.VolumesListTestJSON.test_volume_list_details_pagination
tempest.api.volume.v2.test_volumes_list.VolumesListTestJSON.test_volume_list_details_with_multiple_params
tempest.api.volume.v2.test_volumes_list.VolumesListTestJSON.test_volume_list_pagination

Note: the latter 19 test cases is the alias of the first 19 ones.
Alias should always be included so that the test run will be tempest version agnostic,
which can be used to test different version of Openstack.

Test preconditions
------------------

* Volume extension API
* The backing file for the volume group that Nova uses has space for at least 3 1G volumes

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: List all existent volumes
* **Test assertion 1:** Verify the volume list is complete
* Test action 2: List existent volumes and filter the volume list by volume name
* **Test assertion 2:** Verify the length of filtered volume list is 1 and the retrieved volume is correct
* Test action 3: List existent volumes in detail and filter the volume list by volume name
* **Test assertion 3:** Verify the length of filtered volume list is 1 and the retrieved volume is correct
* Test action 4: List existent volumes and filter the volume list by volume name and status 'available'
* **Test assertion 4:** Verify the name and status parameters of the fetched volume are correct
* Test action 5: List existent volumes in detail and filter the volume list by volume name and status 'available'
* **Test assertion 5:** Verify the name and status parameters of the fetched volume are correct
* Test action 6: List all existent volumes in detail and filter the volume list by volume metadata
* **Test assertion 6:** Verify the metadata parameter of the fetched volume is correct
* Test action 7: List all existent volumes in detail
* **Test assertion 7:** Verify the volume list is complete
* Test action 8: List all existent volumes and filter the volume list by volume metadata
* **Test assertion 8:** Verify the metadata parameter of the fetched volume is correct
* Test action 9: List existent volumes and filter the volume list by availability zone
* **Test assertion 9:** Verify the availability zone parameter of the fetched volume is correct
* Test action 10: List all existent volumes and filter the volume list by volume status 'available'
* **Test assertion 10:** Verify the status parameter of the fetched volume is correct
* Test action 11: List existent volumes in detail and filter the volume list by availability zone
* **Test assertion 11:** Verify the availability zone parameter of the fetched volume is correct
* Test action 12: List all existent volumes in detail and filter the volume list by volume status 'available'
* **Test assertion 12:** Verify the status parameter of the fetched volume is correct
* Test action 13: List all existent volumes in detail and filter the volume list by an invalid volume status 'null'
* **Test assertion 13:** Verify the filtered volume list is empty
* Test action 14: List all existent volumes in detail and filter the volume list by a non-existent volume name
* **Test assertion 14:** Verify the filtered volume list is empty
* Test action 15: List all existent volumes and filter the volume list by an invalid volume status 'null'
* **Test assertion 15:** Verify the filtered volume list is empty
* Test action 16: List all existent volumes and filter the volume list by a non-existent volume name
* **Test assertion 16:** Verify the filtered volume list is empty
* Test action 17: List all existent volumes in detail and paginate the volume list by desired volume IDs
* **Test assertion 17:** Verify only the desired volumes are listed in the filtered volume list
* Test action 18: List all existent volumes in detail and filter the volume list by volume status 'available' and display limit '2'
* Test action 19: Sort the filtered volume list by IDs in ascending order
* **Test assertion 18:** Verify the length of filtered volume list is 2
* **Test assertion 19:** Verify the status of retrieved volumes is correct
* **Test assertion 20:** Verify the filtered volume list is sorted correctly
* Test action 20: List all existent volumes in detail and filter the volume list by volume status 'available' and display limit '2'
* Test action 21: Sort the filtered volume list by IDs in descending order
* **Test assertion 21:** Verify the length of filtered volume list is 2
* **Test assertion 22:** Verify the status of retrieved volumes is correct
* **Test assertion 23:** Verify the filtered volume list is sorted correctly
* Test action 22: List all existent volumes and paginate the volume list by desired volume IDs
* **Test assertion 24:** Verify only the desired volumes are listed in the filtered volume list

Pass / fail criteria
''''''''''''''''''''

This test case evaluates the volume API ability of getting a list of volumes and filtering the volume list.
Specifically, the test verifies that:

* Get a list of volumes (in detail) successful.
* Get a list of volumes (in detail) and filter volumes by name/status/metadata/availability zone successful.
* Volume list pagination functionality is working.
* Get a list of volumes in detail using combined condition successful.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A

---------------------------------------------------------------
Test Case 9 - Volume metadata operations with the Cinder v2 API
---------------------------------------------------------------

Test case specification
-----------------------

tempest.api.volume.test_volume_metadata.VolumesV2MetadataTest.test_create_get_delete_volume_metadata
tempest.api.volume.test_volume_metadata.VolumesV2MetadataTest.test_update_volume_metadata_item

tempest.api.volume.test_volume_metadata.VolumesMetadataTest.test_crud_volume_metadata
tempest.api.volume.test_volume_metadata.VolumesV2MetadataTest.test_crud_volume_metadata

tempest.api.volume.test_volume_metadata.VolumesMetadataTest.test_update_volume_metadata_item
tempest.api.volume.test_volume_metadata.VolumesMetadataTest.test_update_show_volume_metadata_item

Note: Test case 3 and 4 are the alias of the first test case, and the last 2 test cases
are the alias of the second test case.
Alias should always be included so that the test run will be tempest version agnostic,
which can be used to test different version of OpenStack.

Test preconditions
------------------

* Volume extension API

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: Create metadata for a provided volume VOL1
* Test action 2: Get the metadata of VOL1
* **Test assertion 1:** Verify the metadata of VOL1 is correct
* Test action 3: Update the metadata of VOL1
* **Test assertion 2:** Verify the metadata of VOL1 is updated
* Test action 4: Delete one metadata item 'key1' of VOL1
* **Test assertion 3:** Verify the metadata item 'key1' is deleted
* Test action 5: Create metadata for a provided volume VOL2
* **Test assertion 4:** Verify the metadata of VOL2 is correct
* Test action 6: Update one metadata item 'key3' of VOL2
* **Test assertion 5:** Verify the metadata of VOL2 is updated

Pass / fail criteria
''''''''''''''''''''

This test case evaluates the volume API ability of creating metadata for a volume, getting the
metadata of a volume, updating volume metadata and deleting a metadata item of a volume.
Specifically, the test verifies that:

* Create metadata for volume successfully.
* Get metadata of volume successfully.
* Update volume metadata and metadata item successfully.
* Delete metadata item of a volume successfully.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A

---------------------------------------------------------------------------------
Test Case 10 - Verification of read-only status on volumes with the Cinder v2 API
---------------------------------------------------------------------------------

Test case specification
-----------------------

tempest.api.volume.test_volumes_actions.VolumesV2ActionsTest.test_volume_readonly_update

tempest.api.volume.test_volumes_actions.VolumesActionsTest.test_volume_readonly_update

Note: the second test case is the alias of the first one.
Alias should always be included so that the test run will be tempest version agnostic,
which can be used to test different version of Openstack.

Test preconditions
------------------

* Volume extension API

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: Update a provided volume VOL1's read-only access mode to 'True'
* **Test assertion 1:** Verify VOL1 is in read-only access mode
* Test action 2: Update a provided volume VOL1's read-only access mode to 'False'
* **Test assertion 2:** Verify VOL1 is not in read-only access mode

Pass / fail criteria
''''''''''''''''''''

This test case evaluates the volume API ability of setting and updating volume read-only access mode.
Specifically, the test verifies that:

* Volume read-only access mode can be set and updated.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A

-------------------------------------------------------------------
Test Case 11 - Volume reservation operations with the Cinder v2 API
-------------------------------------------------------------------

Test case specification
-----------------------

tempest.api.volume.test_volumes_actions.VolumesV2ActionsTest.test_reserve_unreserve_volume
tempest.api.volume.test_volumes_negative.VolumesV2NegativeTest.test_reserve_volume_with_negative_volume_status
tempest.api.volume.test_volumes_negative.VolumesV2NegativeTest.test_reserve_volume_with_nonexistent_volume_id
tempest.api.volume.test_volumes_negative.VolumesV2NegativeTest.test_unreserve_volume_with_nonexistent_volume_id

tempest.api.volume.test_volumes_actions.VolumesActionsTest.test_reserve_unreserve_volume
tempest.api.volume.test_volumes_negative.VolumesNegativeTest.test_reserve_volume_with_negative_volume_status
tempest.api.volume.test_volumes_negative.VolumesNegativeTest.test_reserve_volume_with_nonexistent_volume_id
tempest.api.volume.test_volumes_negative.VolumesNegativeTest.test_unreserve_volume_with_nonexistent_volume_id

Note: the last 4 test cases are the alias of the first 4 ones.
Alias should always be included so that the test run will be tempest version agnostic,
which can be used to test different version of Openstack.

Test preconditions
------------------

* Volume extension API

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: Update a provided volume VOL1 as reserved
* **Test assertion 1:** Verify VOL1 is in 'attaching' status
* Test action 2: Update VOL1 as un-reserved
* **Test assertion 2:** Verify VOL1 is in 'available' status
* Test action 3: Update a provided volume VOL2 as reserved
* Test action 4: Update VOL2 as reserved again
* **Test assertion 3:** Verify update VOL2 status failed, a bad request error is returned in the response
* Test action 5: Update VOL2 as un-reserved
* Test action 6: Update a non-existent volume as reserved by using an invalid volume ID
* **Test assertion 4:** Verify update non-existent volume as reserved failed, a 'Not Found' error is returned in the response
* Test action 7: Update a non-existent volume as un-reserved by using an invalid volume ID
* **Test assertion 5:** Verify update non-existent volume as un-reserved failed, a 'Not Found' error is returned in the response

Pass / fail criteria
''''''''''''''''''''

This test case evaluates the volume API ability of reserving and un-reserving volumes.
Specifically, the test verifies that:

* Volume can be reserved and un-reserved.
* Update a non-existent volume as reserved is not allowed.
* Update a non-existent volume as un-reserved is not allowed.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A

----------------------------------------------------------------------------------
Test Case 12 - Volume snapshot creation/deletion operations with the Cinder v2 API
----------------------------------------------------------------------------------

Test case specification
-----------------------

tempest.api.volume.test_snapshot_metadata.SnapshotV2MetadataTestJSON.test_create_get_delete_snapshot_metadata
tempest.api.volume.test_snapshot_metadata.SnapshotV2MetadataTestJSON.test_update_snapshot_metadata_item
tempest.api.volume.test_volumes_negative.VolumesV2NegativeTest.test_create_volume_with_nonexistent_snapshot_id
tempest.api.volume.test_volumes_negative.VolumesV2NegativeTest.test_delete_invalid_volume_id
tempest.api.volume.test_volumes_negative.VolumesV2NegativeTest.test_delete_volume_without_passing_volume_id
tempest.api.volume.test_volumes_negative.VolumesV2NegativeTest.test_volume_delete_nonexistent_volume_id
tempest.api.volume.test_volumes_snapshots.VolumesV2SnapshotTestJSON.test_snapshot_create_get_list_update_delete
tempest.api.volume.test_volumes_snapshots.VolumesV2SnapshotTestJSON.test_volume_from_snapshot
tempest.api.volume.test_volumes_snapshots.VolumesV2SnapshotTestJSON.test_snapshots_list_details_with_params
tempest.api.volume.test_volumes_snapshots.VolumesV2SnapshotTestJSON.test_snapshots_list_with_params
tempest.api.volume.test_volumes_snapshots_negative.VolumesV2SnapshotNegativeTestJSON.test_create_snapshot_with_nonexistent_volume_id
tempest.api.volume.test_volumes_snapshots_negative.VolumesV2SnapshotNegativeTestJSON.test_create_snapshot_without_passing_volume_id

tempest.api.volume.test_snapshot_metadata.SnapshotMetadataTestJSON.test_crud_snapshot_metadata
tempest.api.volume.test_snapshot_metadata.SnapshotV2MetadataTestJSON.test_crud_snapshot_metadata

tempest.api.volume.test_snapshot_metadata.SnapshotMetadataTestJSON.test_update_snapshot_metadata_item
tempest.api.volume.test_snapshot_metadata.SnapshotMetadataTestJSON.test_update_show_snapshot_metadata_item

tempest.api.volume.test_volumes_negative.VolumesNegativeTest.test_create_volume_with_nonexistent_snapshot_id
tempest.api.volume.test_volumes_negative.VolumesNegativeTest.test_delete_invalid_volume_id
tempest.api.volume.test_volumes_negative.VolumesNegativeTest.test_delete_volume_without_passing_volume_id
tempest.api.volume.test_volumes_negative.VolumesNegativeTest.test_volume_delete_nonexistent_volume_id
tempest.api.volume.test_volumes_snapshots.VolumesSnapshotTestJSON.test_snapshot_create_get_list_update_delete
tempest.api.volume.test_volumes_snapshots.VolumesSnapshotTestJSON.test_volume_from_snapshot

tempest.api.volume.test_volumes_snapshots_list.VolumesSnapshotListTestJSON.test_snapshots_list_details_with_params
tempest.api.volume.test_volumes_snapshots_list.VolumesV2SnapshotListTestJSON.test_snapshots_list_details_with_params

tempest.api.volume.test_volumes_snapshots_list.VolumesSnapshotListTestJSON.test_snapshots_list_with_params
tempest.api.volume.test_volumes_snapshots_list.VolumesV2SnapshotListTestJSON.test_snapshots_list_with_params

tempest.api.volume.test_volumes_snapshots_negative.VolumesSnapshotNegativeTestJSON.test_create_snapshot_with_nonexistent_volume_id
tempest.api.volume.test_volumes_snapshots_negative.VolumesSnapshotNegativeTestJSON.test_create_snapshot_without_passing_volume_id

Note: test case 13 and 14 are the alias of test case 1, test case 15 and 16 are the alias of test case 2,
test case 17 to 22 are the alias of test case 3 to 8 respectively, test case 23 and 24 are the alias of
test case 9, test case 25 and 26 are the alias of test case 10, and test case 27 and 28 are the alias of
test case 11 and 12 respectively.
Alias should always be included so that the test run will be tempest version agnostic,
which can be used to test different version of OpenStack.

Test preconditions
------------------

* Volume extension API

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: Create metadata for a provided snapshot SNAP1
* Test action 2: Get the metadata of SNAP1
* **Test assertion 1:** Verify the metadata of SNAP1 is correct
* Test action 3: Update the metadata of SNAP1
* **Test assertion 2:** Verify the metadata of SNAP1 is updated
* Test action 4: Delete one metadata item 'key3' of SNAP1
* **Test assertion 3:** Verify the metadata item 'key3' is deleted
* Test action 5: Create metadata for a provided snapshot SNAP2
* **Test assertion 4:** Verify the metadata of SNAP2 is correct
* Test action 6: Update one metadata item 'key3' of SNAP2
* **Test assertion 5:** Verify the metadata of SNAP2 is updated
* Test action 7: Create a volume with a nonexistent snapshot
* **Test assertion 6:** Verify create volume failed, a 'Not Found' error is returned in the response
* Test action 8: Delete a volume with an invalid volume ID
* **Test assertion 7:** Verify delete volume failed, a 'Not Found' error is returned in the response
* Test action 9: Delete a volume with an empty volume ID
* **Test assertion 8:** Verify delete volume failed, a 'Not Found' error is returned in the response
* Test action 10: Delete a volume with a nonexistent volume ID
* **Test assertion 9:** Verify delete volume failed, a 'Not Found' error is returned in the response
* Test action 11: Create a snapshot SNAP2 from a provided volume VOL1
* Test action 12: Retrieve SNAP2's detail information
* **Test assertion 10:** Verify SNAP2 is created from VOL1
* Test action 13: Update the name and description of SNAP2
* **Test assertion 11:** Verify the name and description of SNAP2 are updated in the response body of update snapshot API
* Test action 14: Retrieve SNAP2's detail information
* **Test assertion 12:** Verify the name and description of SNAP2 are correct
* Test action 15: Delete SNAP2
* Test action 16: Create a volume VOL2 with a volume size
* Test action 17: Create a snapshot SNAP3 from VOL2
* Test action 18: Create a volume VOL3 from SNAP3 with a bigger volume size
* Test action 19: Retrieve VOL3's detail information
* **Test assertion 13:** Verify volume size and source snapshot of VOL3 are correct
* Test action 20: List all snapshots in detail and filter the snapshot list by name
* **Test assertion 14:** Verify the filtered snapshot list is correct
* Test action 21: List all snapshots in detail and filter the snapshot list by status
* **Test assertion 15:** Verify the filtered snapshot list is correct
* Test action 22: List all snapshots in detail and filter the snapshot list by name and status
* **Test assertion 16:** Verify the filtered snapshot list is correct
* Test action 23: List all snapshots and filter the snapshot list by name
* **Test assertion 17:** Verify the filtered snapshot list is correct
* Test action 24: List all snapshots and filter the snapshot list by status
* **Test assertion 18:** Verify the filtered snapshot list is correct
* Test action 25: List all snapshots and filter the snapshot list by name and status
* **Test assertion 19:** Verify the filtered snapshot list is correct
* Test action 26: Create a snapshot from a nonexistent volume by using an invalid volume ID
* **Test assertion 20:** Verify create snapshot failed, a 'Not Found' error is returned in the response
* Test action 27: Create a snapshot from a volume by using an empty volume ID
* **Test assertion 21:** Verify create snapshot failed, a 'Not Found' error is returned in the response

Pass / fail criteria
''''''''''''''''''''

This test case evaluates the volume API ability of managing snapshot and snapshot metadata.
Specifically, the test verifies that:

* Create metadata for snapshot successfully.
* Get metadata of snapshot successfully.
* Update snapshot metadata and metadata item successfully.
* Delete metadata item of a snapshot successfully.
* Create a volume from a nonexistent snapshot is not allowed.
* Delete a volume using an invalid volume ID is not allowed.
* Delete a volume without passing the volume ID is not allowed.
* Delete a non-existent volume is not allowed.
* Create snapshot successfully.
* Get snapshot's detail information successfully.
* Update snapshot attributes successfully.
* Delete snapshot successfully.
* Creates a volume and a snapshot passing a size different from the source successfully.
* List snapshot details by display_name and status filters successfully.
* Create a snapshot from a nonexistent volume is not allowed.
* Create a snapshot from a volume without passing the volume ID is not allowed.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A

--------------------------------------------------------------
Test Case 13 - Volume update operations with the Cinder v2 API
--------------------------------------------------------------

Test case specification
-----------------------

tempest.api.volume.test_volumes_negative.VolumesV2NegativeTest.test_update_volume_with_empty_volume_id
tempest.api.volume.test_volumes_negative.VolumesV2NegativeTest.test_update_volume_with_invalid_volume_id
tempest.api.volume.test_volumes_negative.VolumesV2NegativeTest.test_update_volume_with_nonexistent_volume_id

tempest.api.volume.test_volumes_negative.VolumesNegativeTest.test_update_volume_with_empty_volume_id
tempest.api.volume.test_volumes_negative.VolumesNegativeTest.test_update_volume_with_invalid_volume_id
tempest.api.volume.test_volumes_negative.VolumesNegativeTest.test_update_volume_with_nonexistent_volume_id

Note: the last 3 test cases are the alias of the first 3 ones.
Alias should always be included so that the test run will be tempest version agnostic,
which can be used to test different version of Openstack.

Test preconditions
------------------

* Volume extension API

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: Update a volume by using an empty volume ID
* **Test assertion 1:** Verify update volume failed, a 'Not Found' error is returned in the response
* Test action 2: Update a volume by using an invalid volume ID
* **Test assertion 2:** Verify update volume failed, a 'Not Found' error is returned in the response
* Test action 3: Update a non-existent volume by using a random generated volume ID
* **Test assertion 3:** Verify update volume failed, a 'Not Found' error is returned in the response

Pass / fail criteria
''''''''''''''''''''

This test case evaluates the volume API ability of updating volume attributes.
Specifically, the test verifies that:

* Update a volume without passing the volume ID is not allowed.
* Update a volume using an invalid volume ID is not allowed.
* Update a non-existent volume is not allowed.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A
