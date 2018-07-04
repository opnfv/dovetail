.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Ericsson AB, Huawei Technologies Co.,Ltd

=========================================
VIM compute operations test specification
=========================================

Scope
=====

The VIM compute operations test area evaluates the ability of the system under
test to support VIM compute operations. The test cases documented here are the
compute API test cases in the OpenStack Interop guideline 2017.09 as implemented
by the RefStack client. These test cases will evaluate basic OpenStack (as a VIM)
compute operations, including:

- Image management operations
- Basic support operations
- API version support operations
- Quotas management operations
- Basic server operations
- Volume management operations

Definitions and abbreviations
=============================

The following terms and abbreviations are used in conjunction with this test area

- API - Application Programming Interface
- NFVi - Network Functions Virtualization infrastructure
- SUT - System Under Test
- UUID - Universally Unique Identifier
- VIM - Virtual Infrastructure Manager
- VM - Virtual Machine

System Under Test (SUT)
=======================

The system under test is assumed to be the NFVi and VIM deployed with a Pharos compliant infrastructure.

Test Area Structure
====================

The test area is structured based on VIM compute API operations. Each test case is
able to run independently, i.e. irrelevant of the state created by a previous test.
Specifically, every test performs clean-up operations which return the system to
the same state as before the test.

For brevity, the test cases in this test area are summarized together based on
the operations they are testing.

All these test cases are included in the test case dovetail.tempest.osinterop of
OVP test suite.

Test Descriptions
=================

----------------------
API Used and Reference
----------------------

Servers: https://developer.openstack.org/api-ref/compute/

- create server
- delete server
- list servers
- start server
- stop server
- update server
- get server action
- set server metadata
- update server metadata
- rebuild server

- create image
- delete image

- create keypair
- delete keypair

Block storage: https://developer.openstack.org/api-ref/block-storage

- create volume
- delete volume
- attach volume to server
- detach volume from server

-----------------------------------------------------
Test Case 1 - Image operations within the Compute API
-----------------------------------------------------

Test case specification
-----------------------

tempest.api.compute.images.test_images_oneserver.ImagesOneServerTestJSON.test_create_delete_image
tempest.api.compute.images.test_images_oneserver.ImagesOneServerTestJSON.test_create_image_specify_multibyte_character_image_name

Test preconditions
------------------

* Compute server extension API

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: Create a server VM1 with an image IMG1 and wait for VM1 to reach 'ACTIVE' status
* Test action 2: Create a new server image IMG2 from VM1, specifying image name
  and image metadata. Wait for IMG2 to reach 'ACTIVE' status, and then delete IMG2
* **Test assertion 1:** Verify IMG2 is created with correct image name and image
  metadata; verify IMG1's 'minRam' equals to IMG2's 'minRam' and IMG2's 'minDisk' equals
  to IMG1's 'minDisk' or VM1's flavor disk size
* **Test assertion 2:** Verify IMG2 is deleted correctly
* Test action 3: Create another server IMG3 from VM1, specifying image name
  with a 3 byte utf-8 character
* **Test assertion 3:** Verify IMG3 is created correctly
* Test action 4: Delete VM1, IMG1 and IMG3

Pass / fail criteria
''''''''''''''''''''

This test evaluates the Compute API ability of creating image from server,
deleting image, creating server image with multi-byte character name.
Specifically, the test verifies that:

* Compute server create image and delete image APIs work correctly.
* Compute server image can be created with multi-byte character name.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A

-----------------------------------------------------
Test Case 2 - Action operation within the Compute API
-----------------------------------------------------

Test case specification
-----------------------

tempest.api.compute.servers.test_instance_actions.InstanceActionsTestJSON.test_get_instance_action
tempest.api.compute.servers.test_instance_actions.InstanceActionsTestJSON.test_list_instance_actions

Test preconditions
------------------

* Compute server extension API

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: Create a server VM1 and wait for VM1 to reach 'ACTIVE' status
* Test action 2: Get the action details ACT_DTL of VM1
* **Test assertion 1:** Verify ACT_DTL's 'instance_uuid' matches VM1's ID and
  ACT_DTL's 'action' matched 'create'
* Test action 3: Create a server VM2 and wait for VM2 to reach 'ACTIVE' status
* Test action 4: Delete server VM2 and wait for VM2 to reach termination
* Test action 5: Get the action list ACT_LST of VM2
* **Test assertion 2:** Verify ACT_LST's length is 2 and two actions are 'create' and 'delete'
* Test action 6: Delete VM1

Pass / fail criteria
''''''''''''''''''''

This test evaluates the Compute API ability of getting the action details
of a provided server and getting the action list of a deleted server.
Specifically, the test verifies that:

* Get the details of the action in a specified server.
* List the actions that were performed on the specified server.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A

--------------------------------------------------------------------------
Test Case 3 - Generate, import and delete SSH keys within Compute services
--------------------------------------------------------------------------

Test case specification
-----------------------

tempest.api.compute.servers.test_servers.ServersTestJSON.test_create_specify_keypair

Test preconditions
------------------

* Compute server extension API

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: Create a keypair KEYP1 and list all existing keypairs
* Test action 2: Create a server VM1 with KEYP1 and wait for VM1 to reach 'ACTIVE' status
* Test action 3: Show details of VM1
* **Test assertion 1:** Verify value of 'key_name' in the details equals to the name of KEYP1
* Test action 4: Delete KEYP1 and VM1

Pass / fail criteria
''''''''''''''''''''

This test evaluates the Compute API ability of creating a keypair, listing
keypairs and creating a server with a provided keypair.
Specifically, the test verifies that:

* Compute create keypair and list keypair APIs work correctly.
* While creating a server, keypair can be specified.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A

--------------------------------------------------------
Test Case 4 - List supported versions of the Compute API
--------------------------------------------------------

Test case specification
-----------------------

tempest.api.compute.test_versions.TestVersions.test_list_api_versions

Test preconditions
------------------

* Compute versions extension API

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: Get a List of versioned endpoints in the SUT
* **Test assertion 1:** Verify endpoints versions start at 'v2.0'

Pass / fail criteria
''''''''''''''''''''

This test evaluates the functionality of listing all available APIs to API consumers.
Specifically, the test verifies that:

* Compute list API versions API works correctly.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A

----------------------------------------------
Test Case 5 - Quotas management in Compute API
----------------------------------------------

Test case specification
-----------------------

tempest.api.compute.test_quotas.QuotasTestJSON.test_get_default_quotas
tempest.api.compute.test_quotas.QuotasTestJSON.test_get_quotas

Test preconditions
------------------

* Compute quotas extension API

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''
* Test action 1: Get the default quota set using the tenant ID
* **Test assertion 1:** Verify the default quota set ID matches tenant ID and
  the default quota set is complete
* Test action 2: Get the quota set using the tenant ID
* **Test assertion 2:** Verify the quota set ID matches tenant ID and the quota
  set is complete
* Test action 3: Get the quota set using the user ID
* **Test assertion 3:** Verify the quota set ID matches tenant ID and the quota
  set is complete

Pass / fail criteria
''''''''''''''''''''

This test evaluates the functionality of getting quota set.
Specifically, the test verifies that:

* User can get the default quota set for its tenant.
* User can get the quota set for its tenant.
* User can get the quota set using user ID.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A

--------------------------------------------------------
Test Case 6 - Basic server operations in the Compute API
--------------------------------------------------------

Test case specification
-----------------------

This test case evaluates the Compute API ability of basic server operations, including:

- Create a server with admin password
- Create a server with a name that already exists
- Create a server with a numeric name
- Create a server with a really long metadata
- Create a server with a name whose length exceeding 255 characters
- Create a server with an unknown flavor
- Create a server with an unknown image ID
- Create a server with an invalid network UUID
- Delete a server using a server ID that exceeds length limit
- Delete a server using a negative server ID
- Get a nonexistent server details
- Verify the instance host name is the same as the server name
- Create a server with an invalid access IPv6 address
- List all existent servers
- Filter the (detailed) list of servers by flavor, image, server name, server status or limit
- Lock a server and try server stop, unlock and retry
- Get and delete metadata from a server
- List and set metadata for a server
- Reboot, rebuild, stop and start a server
- Update a server's access addresses and server name

The reference is,

tempest.api.compute.servers.test_servers.ServersTestJSON.test_create_server_with_admin_password
tempest.api.compute.servers.test_servers.ServersTestJSON.test_create_with_existing_server_name
tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_numeric_server_name
tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_server_metadata_exceeds_length_limit
tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_server_name_length_exceeds_256
tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_with_invalid_flavor
tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_with_invalid_image
tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_with_invalid_network_uuid
tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_delete_server_pass_id_exceeding_length_limit
tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_delete_server_pass_negative_id
tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_get_non_existent_server
tempest.api.compute.servers.test_create_server.ServersTestJSON.test_host_name_is_same_as_server_name
tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_host_name_is_same_as_server_name
tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_invalid_ip_v6_address
tempest.api.compute.servers.test_create_server.ServersTestJSON.test_list_servers
tempest.api.compute.servers.test_create_server.ServersTestJSON.test_list_servers_with_detail
tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_list_servers
tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_list_servers_with_detail
tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_flavor
tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_image
tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_server_name
tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_server_status
tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_limit_results
tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_flavor
tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_image
tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_limit
tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_server_name
tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_active_status
tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filtered_by_name_wildcard
tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_changes_since_future_date
tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_changes_since_invalid_date
tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits_greater_than_actual_count
tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits_pass_negative_value
tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits_pass_string
tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_non_existing_flavor
tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_non_existing_image
tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_non_existing_server_name
tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_detail_server_is_deleted
tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_status_non_existing
tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_with_a_deleted_server
tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_lock_unlock_server
tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_delete_server_metadata_item
tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_get_server_metadata_item
tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_list_server_metadata
tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_set_server_metadata
tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_set_server_metadata_item
tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_update_server_metadata
tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_server_name_blank
tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_reboot_server_hard
tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_reboot_non_existent_server
tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_rebuild_server
tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_rebuild_deleted_server
tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_rebuild_non_existent_server
tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_stop_start_server
tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_stop_non_existent_server
tempest.api.compute.servers.test_servers.ServersTestJSON.test_update_access_server_address
tempest.api.compute.servers.test_servers.ServersTestJSON.test_update_server_name
tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_name_of_non_existent_server
tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_server_name_length_exceeds_256
tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_server_set_empty_name
tempest.api.compute.servers.test_create_server.ServersTestJSON.test_verify_created_server_vcpus
tempest.api.compute.servers.test_create_server.ServersTestJSON.test_verify_server_details
tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_verify_created_server_vcpus
tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_verify_server_details
tempest.api.compute.servers.test_delete_server.DeleteServersTestJSON.test_delete_active_server

Test preconditions
------------------

* Compute quotas extension API

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: Create a server VM1 with a admin password 'testpassword'
* **Test assertion 1:** Verify the password returned in the response equals to 'testpassword'
* Test action 2: Generate a VM name VM_NAME
* Test action 3: Create 2 servers VM2 and VM3 both with name VM_NAME
* **Test assertion 2:** Verify VM2's ID is not equal to VM3's ID, and VM2's name equal to VM3's name
* Test action 4: Create a server VM4 with a numeric name '12345'
* **Test assertion 3:** Verify creating VM4 failed
* Test action 5: Create a server VM5 with a long metadata '{'a': 'b' * 260}'
* **Test assertion 4:** Verify creating VM5 failed
* Test action 6: Create a server VM6 with name length exceeding 255 characters
* **Test assertion 5:** Verify creating VM6 failed
* Test action 7: Create a server VM7 with an unknown flavor '-1'
* **Test assertion 6:** Verify creating VM7 failed
* Test action 8: Create a server VM8 with an unknown image ID '-1'
* **Test assertion 7:** Verify creating VM8 failed
* Test action 9: Create a server VM9 with an invalid network UUID 'a-b-c-d-e-f-g-h-i-j'
* **Test assertion 8:** Verify creating VM9 failed
* Test action 10: Delete a server using a server ID that exceeds system's max integer limit
* **Test assertion 9:** Verify deleting server failed
* Test action 11: Delete a server using a server ID '-1'
* **Test assertion 10:** Verify deleting server failed
* Test action 12: Get a nonexistent server by using a random generated server ID
* **Test assertion 11:** Verify get server failed
* Test action 13: SSH into a provided server and get server's hostname
* **Test assertion 12:** Verify server's host name is the same as the server name
* Test action 14: SSH into a provided server and get server's hostname (manual disk configuration)
* **Test assertion 13:** Verify server's host name is the same as the server name (manual disk configuration)
* Test action 15: Create a server with an invalid access IPv6 address
* **Test assertion 14:** Verify creating server failed, a bad request error is returned in response
* Test action 16: List all existent servers
* **Test assertion 15:** Verify a provided server is in the server list
* Test action 17: List all existent servers in detail
* **Test assertion 16:** Verify a provided server is in the detailed server list
* Test action 18: List all existent servers (manual disk configuration)
* **Test assertion 17:** Verify a provided server is in the server list (manual disk configuration)
* Test action 19: List all existent servers in detail (manual disk configuration)
* **Test assertion 18:** Verify a provided server is in the detailed server list (manual disk configuration)
* Test action 20: List all existent servers in detail and filter the server list by flavor
* **Test assertion 19:** Verify the filtered server list is correct
* Test action 21: List all existent servers in detail and filter the server list by image
* **Test assertion 20:** Verify the filtered server list is correct
* Test action 22: List all existent servers in detail and filter the server list by server name
* **Test assertion 21:** Verify the filtered server list is correct
* Test action 23: List all existent servers in detail and filter the server list by server status
* **Test assertion 22:** Verify the filtered server list is correct
* Test action 24: List all existent servers in detail and filter the server list by display limit '1'
* **Test assertion 23:** Verify the length of filtered server list is 1
* Test action 25: List all existent servers and filter the server list by flavor
* **Test assertion 24:** Verify the filtered server list is correct
* Test action 26: List all existent servers and filter the server list by image
* **Test assertion 25:** Verify the filtered server list is correct
* Test action 27: List all existent servers and filter the server list by display limit '1'
* **Test assertion 26:** Verify the length of filtered server list is 1
* Test action 28: List all existent servers and filter the server list by server name
* **Test assertion 27:** Verify the filtered server list is correct
* Test action 29: List all existent servers and filter the server list by server status
* **Test assertion 28:** Verify the filtered server list is correct
* Test action 30: List all existent servers and filter the server list by server name wildcard
* **Test assertion 29:** Verify the filtered server list is correct
* Test action 31: List all existent servers and filter the server list by part of server name
* **Test assertion 30:** Verify the filtered server list is correct
* Test action 32: List all existent servers and filter the server list by a future change-since date
* **Test assertion 31:** Verify the filtered server list is empty
* Test action 33: List all existent servers and filter the server list by a invalid change-since date format
* **Test assertion 32:** Verify a bad request error is returned in the response
* Test action 34: List all existent servers and filter the server list by a
  display limit value greater than the length of the server list
* **Test assertion 33:** Verify the length of filtered server list equals to the length of server list
* Test action 35: List all existent servers and filter the server list by display limit '-1'
* **Test assertion 34:** Verify a bad request error is returned in the response
* Test action 36: List all existent servers and filter the server list by a string type limit value 'testing'
* **Test assertion 35:** Verify a bad request error is returned in the response
* Test action 37: List all existent servers and filter the server list by a nonexistent flavor
* **Test assertion 36:** Verify the filtered server list is empty
* Test action 38: List all existent servers and filter the server list by a nonexistent image
* **Test assertion 37:** Verify the filtered server list is empty
* Test action 39: List all existent servers and filter the server list by a nonexistent server name
* **Test assertion 38:** Verify the filtered server list is empty
* Test action 40: List all existent servers in detail and search the server list for a deleted server
* **Test assertion 39:** Verify the deleted server is not in the server list
* Test action 41: List all existent servers and filter the server list by a nonexistent server status
* **Test assertion 40:** Verify the filtered server list is empty
* Test action 42: List all existent servers in detail
* **Test assertion 41:** Verify a provided deleted server's id is not in the server list
* Test action 43: Lock a provided server VM10 and retrieve the server's status
* **Test assertion 42:** Verify VM10 is in 'ACTIVE' status
* Test action 44: Stop VM10
* **Test assertion 43:** Verify stop VM10 failed
* Test action 45: Unlock VM10 and stop VM10 again
* **Test assertion 44:** Verify VM10 is stopped and in 'SHUTOFF' status
* Test action 46: Start VM10
* **Test assertion 45:** Verify VM10 is in 'ACTIVE' status
* Test action 47: Delete metadata item 'key1' from a provided server
* **Test assertion 46:** Verify the metadata item is removed
* Test action 48: Get metadata item 'key2' from a provided server
* **Test assertion 47:** Verify the metadata item is correct
* Test action 49: List all metadata key/value pair for a provided server
* **Test assertion 48:** Verify all metadata are retrieved correctly
* Test action 50: Set metadata {'meta2': 'data2', 'meta3': 'data3'} for a provided server
* **Test assertion 49:** Verify server's metadata are replaced correctly
* Test action 51: Set metadata item nova's value to 'alt' for a provided server
* **Test assertion 50:** Verify server's metadata are set correctly
* Test action 52: Update metadata {'key1': 'alt1', 'key3': 'value3'} for a provided server
* **Test assertion 51:** Verify server's metadata are updated correctly
* Test action 53: Create a server with empty name parameter
* **Test assertion 52:** Verify create server failed
* Test action 54: Hard reboot a provided server
* **Test assertion 53:** Verify server is rebooted successfully
* Test action 55: Soft reboot a nonexistent server
* **Test assertion 54:** Verify reboot failed, an error is returned in the response
* Test action 56: Rebuild a provided server with new image, new server name and metadata
* **Test assertion 55:** Verify server is rebuilt successfully, server image, name and metadata are correct
* Test action 57: Create a server VM11
* Test action 58: Delete VM11 and wait for VM11 to reach termination
* Test action 59: Rebuild VM11 with another image
* **Test assertion 56:** Verify rebuild server failed, an error is returned in the response
* Test action 60: Rebuild a nonexistent server
* **Test assertion 57:** Verify rebuild server failed, an error is returned in the response
* Test action 61: Stop a provided server
* **Test assertion 58:** Verify server reaches 'SHUTOFF' status
* Test action 62: Start the stopped server
* **Test assertion 59:** Verify server reaches 'ACTIVE' status
* Test action 63: Stop a provided server
* **Test assertion 60:** Verify stop server failed, an error is returned in the response
* Test action 64: Create a server VM12 and wait it to reach 'ACTIVE' status
* Test action 65: Update VM12's IPv4 and IPv6 access addresses
* **Test assertion 61:** Verify VM12's access addresses have been updated correctly
* Test action 66: Create a server VM13 and wait it to reach 'ACTIVE' status
* Test action 67: Update VM13's server name with non-ASCII characters '\u00CD\u00F1st\u00E1\u00F1c\u00E9'
* **Test assertion 62:** Verify VM13's server name has been updated correctly
* Test action 68: Update the server name of a nonexistent server
* **Test assertion 63:** Verify update server name failed, an 'object not found' error is returned in the response
* Test action 69: Update a provided server's name with a 256-character long name
* **Test assertion 64:** Verify update server name failed, a bad request is returned in the response
* Test action 70: Update a provided server's server name with an empty string
* **Test assertion 65:** Verify update server name failed, a bad request error is returned in the response
* Test action 71: Get the number of vcpus of a provided server
* Test action 72: Get the number of vcpus stated by the server's flavor
* **Test assertion 66:** Verify that the number of vcpus reported by the server
  matches the amount stated by the server's flavor
* Test action 73: Create a server VM14
* **Test assertion 67:** Verify VM14's server attributes are set correctly
* Test action 74: Get the number of vcpus of a provided server (manual disk configuration)
* Test action 75: Get the number of vcpus stated by the server's flavor (manual disk configuration)
* **Test assertion 68:** Verify that the number of vcpus reported by the server
  matches the amount stated by the server's flavor (manual disk configuration)
* Test action 76: Create a server VM15 (manual disk configuration)
* **Test assertion 69:** Verify VM15's server attributes are set correctly (manual disk configuration)
* Test action 77: Create a server VM16 and then delete it when its status is 'ACTIVE'
* **Test assertion 70:** Verify VM16 is deleted successfully
* Test action 78: Delete all VMs created

Pass / fail criteria
''''''''''''''''''''

This test evaluates the functionality of basic server operations.
Specifically, the test verifies that:

* If an admin password is provided on server creation, the server's root password should be set to that password
* Create a server with a name that already exists is allowed
* Create a server with a numeric name or a name that exceeds the length limit is not allowed
* Create a server with a metadata that exceeds the length limit is not allowed
* Create a server with an invalid flavor, an invalid image or an invalid network UUID is not allowed
* Delete a server with a server ID that exceeds the length limit or a nonexistent server ID is not allowed
* Delete a server which status is 'ACTIVE' is allowed
* A provided server's host name is the same as the server name
* Create a server with an invalid IPv6 access address is not allowed
* A created server is in the (detailed) list of servers
* Filter the (detailed) list of servers by flavor, image, server name, server status,
  and display limit, respectively.
* Filter the list of servers by a future date
* Filter the list of servers by an invalid date format, a negative display limit or a string type
  display limit value is not allowed
* Filter the list of servers by a nonexistent flavor, image, server name or server status is not allowed
* Deleted servers are not in the list of servers
* Deleted servers do not show by default in list of servers
* Locked server is not allowed to be stopped by non-admin user
* Can get and delete metadata from servers
* Can list, set and update server metadata
* Create a server with name parameter empty is not allowed
* Hard reboot a server and the server should be power cycled
* Reboot, rebuild and stop a nonexistent server is not allowed
* Rebuild a server using the provided image and metadata
* Stop and restart a server
* A server's name and access addresses can be updated
* Update the name of a nonexistent server is not allowed
* Update name of a server to a name that exceeds the name length limit is not allowed
* Update name of a server to an empty string is not allowed
* The number of vcpus reported by the server matches the amount stated by the server's flavor
* The specified server attributes are set correctly

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A

-----------------------------------------------------------------
Test Case 7 - Retrieve volume information through the Compute API
-----------------------------------------------------------------

Test case specification
-----------------------

This test case evaluates the Compute API ability of attaching volume to a
specific server and retrieve volume information, the reference is,

tempest.api.compute.volumes.test_attach_volume.AttachVolumeTestJSON.test_attach_detach_volume
tempest.api.compute.volumes.test_attach_volume.AttachVolumeTestJSON.test_list_get_volume_attachments

Test preconditions
------------------

* Compute volume extension API

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: Create a server VM1 and a volume VOL1
* Test action 2: Attach VOL1 to VM1
* **Test assertion 1:** Stop VM1 successfully and wait VM1 to reach 'SHUTOFF' status
* **Test assertion 2:** Start VM1 successfully and wait VM1 to reach 'ACTIVE' status
* **Test assertion 3:** SSH into VM1 and verify VOL1 is in VM1's root disk devices
* Test action 3: Detach VOL1 from VM1
* **Test assertion 4:** Stop VM1 successfully and wait VM1 to reach 'SHUTOFF' status
* **Test assertion 5:** Start VM1 successfully and wait VM1 to reach 'ACTIVE' status
* **Test assertion 6:** SSH into VM1 and verify VOL1 is not in VM1's root disk devices
* Test action 4: Create a server VM2 and a volume VOL2
* Test action 5: Attach VOL2 to VM2
* Test action 6: List VM2's volume attachments
* **Test assertion 7:** Verify the length of the list is 1 and VOL2 attachment is in the list
* Test action 7: Retrieve VM2's volume information
* **Test assertion 8:** Verify volume information is correct
* Test action 8: Delete VM1, VM2, VOL1 and VOL2

Pass / fail criteria
''''''''''''''''''''

This test evaluates the functionality of retrieving volume information.
Specifically, the test verifies that:

* Stop and start a server with an attached volume work correctly.
* Retrieve a server's volume information correctly.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A

--------------------------------------------------------------------------
Test Case 8 - List Compute service availability zones with the Compute API
--------------------------------------------------------------------------

Test case specification
-----------------------

This test case evaluates the Compute API ability of listing availability zones
with a non admin user, the reference is,

tempest.api.compute.servers.test_availability_zone.AZV2TestJSON.test_get_availability_zone_list_with_non_admin_user

Test preconditions
------------------

* Compute volume extension API

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: List availability zones with a non admin user
* **Test assertion 1:** The list is not empty

Pass / fail criteria
''''''''''''''''''''

This test evaluates the functionality of listing availability zones with a non admin user.
Specifically, the test verifies that:

* Non admin users can list availability zones.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A

-------------------------------------------------
Test Case 9 - List Flavors within the Compute API
-------------------------------------------------

Test case specification
-----------------------

This test case evaluates the Compute API ability of listing flavors, the reference is,

tempest.api.compute.flavors.test_flavors.FlavorsV2TestJSON.test_list_flavors
tempest.api.compute.flavors.test_flavors.FlavorsV2TestJSON.test_list_flavors_with_detail

Test preconditions
------------------

* Compute volume extension API

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: List all flavors
* **Test assertion 1:** One given flavor is list in the all flavors' list
* Test action 2: List all flavors with details
* **Test assertion 2:** One given flavor is list in the all flavors' list

Pass / fail criteria
''''''''''''''''''''

This test evaluates the functionality of listing flavors within the Compute API.
Specifically, the test verifies that:

* Can list flavors with/without details within the Compute API.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A
