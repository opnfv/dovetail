.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Huawei Technologies Co.,Ltd

===========================================================
Common virtual machine life cycle events test specification
===========================================================

.. toctree::
   :maxdepth: 2

Scope
=====

The common virtual machine life cycle events test area evaluates the ability of
the system under test to behave correctly after common virtual machine life
cycle events. The tests in this test area will evaluate:

- Stop/Start a server
- Reboot a server
- Rebuild a server
- Pause/Unpause a server
- Suspend/Resume a server
- Resize a server
- Resizing a volume-backed server
- Sequence suspend resume
- Shelve/Unshelve a server
- Cold migrate a server
- Live migrate a server

References
==========

- iSCSI

  - https://docs.openstack.org/liberty/config-reference/content/config-iscsi-storage.html

Definitions and abbreviations
=============================

The following terms and abbreviations are used in conjunction with this test area

- API - Application Programming Interface
- NFVi - Network Functions Virtualization infrastructure
- VIM - Virtual Infrastructure Manager
- VM - Virtual Machine

System Under Test (SUT)
=======================

The system under test is assumed to be the NFVi and VIM in operation on a
Pharos compliant infrastructure.

Test Area Structure
===================

The test area is structured based on common virtual machine life cycle events.
Each test case is able to run independently, i.e. irrelevant of the state
created by a previous test. Specifically, every test performs clean-up
operations which return the system to the same state as before the test.

All these test cases are included in the test case dovetail.tempest.vm_lifecycle of
OVP test suite.

Test Descriptions
=================

----------------------
API Used and Reference
----------------------

Block storage: https://developer.openstack.org/api-ref/block-storage

- create volume
- delete volume
- attach volume to server
- detach volume from server

Security Groups: https://developer.openstack.org/api-ref/network/v2/index.html#security-groups-security-groups

- create security group
- delete security group

Networks: https://developer.openstack.org/api-ref/networking/v2/index.html#networks

- create network
- delete network

Routers and interface: https://developer.openstack.org/api-ref/networking/v2/index.html#routers-routers

- create router
- delete router
- add interface to router

Subnets: https://developer.openstack.org/api-ref/networking/v2/index.html#subnets

- create subnet
- delete subnet

Servers: https://developer.openstack.org/api-ref/compute/

- create keypair
- create server
- show server
- delete server
- add/assign floating IP
- resize server
- revert resized server
- confirm resized server
- pause server
- unpause server
- start server
- stop server
- reboot server
- rebuild server
- suspend server
- resume suspended server
- shelve server
- unshelve server
- migrate server
- live-migrate server

Ports: https://developer.openstack.org/api-ref/networking/v2/index.html#ports

- create port
- delete port

Floating IPs: https://developer.openstack.org/api-ref/networking/v2/index.html#floating-ips-floatingips

- create floating IP
- delete floating IP

Availability zone: https://developer.openstack.org/api-ref/compute/

- get availability zone

------------------------------------
Test Case 1 - Minimum basic scenario
------------------------------------

Test case specification
-----------------------

tempest.scenario.test_minimum_basic.TestMinimumBasicScenario.test_minimum_basic_scenario

Test preconditions
------------------

* Nova, cinder, glance, neutron services are available
* One public network

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: Create an image IMG1
* Test action 2: Create a keypair KEYP1
* Test action 3: Create a server VM1 with IMG1 and KEYP1
* **Test assertion 1:** Verify VM1 is created successfully
* Test action 4: Create a volume VOL1
* **Test assertion 2:** Verify VOL1 is created successfully
* Test action 5: Attach VOL1 to VM1
* **Test assertion 3:** Verify VOL1's status has been updated after attached to VM1
* Test action 6: Create a floating IP FIP1 and assign FIP1 to VM1
* **Test assertion 4:** Verify VM1's addresses have been refreshed after associating FIP1
* Test action 7: Create and add security group SG1 to VM1
* **Test assertion 5:** Verify can SSH to VM1 via FIP1
* Test action 8: Reboot VM1
* **Test assertion 6:** Verify can SSH to VM1 via FIP1
* **Test assertion 7:** Verify VM1's disk count equals to 1
* Test action 9: Delete the floating IP FIP1 from VM1
* **Test assertion 8:** Verify VM1's addresses have been refreshed after disassociating FIP1
* Test action 10: Delete SG1, IMG1, KEYP1, VOL1, VM1 and FIP1

Pass / fail criteria
''''''''''''''''''''

This test evaluates a minimum basic scenario. Specifically, the test verifies that:

* The server can be connected before reboot.

* The server can be connected after reboot.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A

----------------------------
Test Case 2 - Cold migration
----------------------------

Test case specification
-----------------------

tempest.scenario.test_network_advanced_server_ops.TestNetworkAdvancedServerOps.test_server_connectivity_cold_migration

Test preconditions
------------------

* At least 2 compute nodes
* Nova, neutron services are available
* One public network

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: Create a keypair KEYP1
* Test action 2: Create a server VM1 with KEYP1
* Test action 3: Create a floating IP FIP1 and assign FIP1 to VM1
* Test action 4: Get VM1's host info SRC_HOST
* Test action 5: Wait for VM1 to reach 'ACTIVE' status
* **Test assertion 1:** Verify can ping FIP1 successfully and can SSH to VM1 via FIP1
* Test action 6: Cold migrate VM1
* Test action 7: Wait for VM1 to reach 'VERIFY_RESIZE' status
* Test action 8: Confirm resize VM1
* Test action 9: Wait for VM1 to reach 'ACTIVE' status
* **Test assertion 2:** Verify can ping FIP1 successfully and can SSH to VM1 via FIP1
* Test action 10: Get VM1's host info DST_HOST
* **Test assertion 3:** Verify SRC_HOST does not equal to DST_HOST
* Test action 11: Delete KEYP1, VM1 and FIP1

Pass / fail criteria
''''''''''''''''''''

This test evaluates the ability to cold migrate VMs. Specifically, the test verifies that:

* Servers can be cold migrated from one compute node to another computer node.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A

--------------------------------------
Test Case 3 - Pause and unpause server
--------------------------------------

Test case specification
-----------------------

tempest.scenario.test_network_advanced_server_ops.TestNetworkAdvancedServerOps.test_server_connectivity_pause_unpause

Test preconditions
------------------

* Nova, neutron services are available
* One public network

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: Create a keypair KEYP1
* Test action 2: Create a server VM1 with KEYP1
* Test action 3: Create a floating IP FIP1 and assign FIP1 to VM1
* Test action 4: Pause VM1
* Test action 5: Wait for VM1 to reach 'PAUSED' status
* **Test assertion 1:** Verify FIP1 status is 'ACTIVE'
* **Test assertion 2:** Verify ping FIP1 failed and SSH to VM1 via FIP1 failed
* Test action 6: Unpause VM1
* Test action 7: Wait for VM1 to reach 'ACTIVE' status
* **Test assertion 3:** Verify can ping FIP1 successfully and can SSH to VM1 via FIP1
* Test action 8: Delete KEYP1, VM1 and FIP1

Pass / fail criteria
''''''''''''''''''''

This test evaluates the ability to pause and unpause VMs. Specifically, the test verifies that:

* When paused, servers cannot be reached.

* When unpaused, servers can recover its reachability.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A

---------------------------
Test Case 4 - Reboot server
---------------------------

Test case specification
-----------------------

tempest.scenario.test_network_advanced_server_ops.TestNetworkAdvancedServerOps.test_server_connectivity_reboot

Test preconditions
------------------

* Nova, neutron services are available
* One public network

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: Create a keypair KEYP1
* Test action 2: Create a server VM1 with KEYP1
* Test action 3: Create a floating IP FIP1 and assign FIP1 to VM1
* Test action 4: Soft reboot VM1
* Test action 5: Wait for VM1 to reach 'ACTIVE' status
* **Test assertion 1:** Verify can ping FIP1 successfully and can SSH to VM1 via FIP1
* Test action 6: Delete KEYP1, VM1 and FIP1

Pass / fail criteria
''''''''''''''''''''

This test evaluates the ability to reboot servers. Specifically, the test verifies that:

* After reboot, servers can still be connected.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A

----------------------------
Test Case 5 - Rebuild server
----------------------------

Test case specification
-----------------------

tempest.scenario.test_network_advanced_server_ops.TestNetworkAdvancedServerOps.test_server_connectivity_rebuild

Test preconditions
------------------

* Nova, neutron services are available
* One public network

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: Create a keypair KEYP1
* Test action 2: Create a server VM1 with KEYP1
* Test action 3: Create a floating IP FIP1 and assign FIP1 to VM1
* Test action 4: Rebuild VM1 with another image
* Test action 5: Wait for VM1 to reach 'ACTIVE' status
* **Test assertion 1:** Verify can ping FIP1 successfully and can SSH to VM1 via FIP1
* Test action 6: Delete KEYP1, VM1 and FIP1

Pass / fail criteria
''''''''''''''''''''

This test evaluates the ability to rebuild servers. Specifically, the test verifies that:

* Servers can be rebuilt with specific image correctly.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A

---------------------------
Test Case 6 - Resize server
---------------------------

Test case specification
-----------------------

tempest.scenario.test_network_advanced_server_ops.TestNetworkAdvancedServerOps.test_server_connectivity_resize

Test preconditions
------------------

* Nova, neutron services are available
* One public network

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: Create a keypair KEYP1
* Test action 2: Create a server VM1 with KEYP1
* Test action 3: Create a floating IP FIP1 and assign FIP1 to VM1
* Test action 4: Resize VM1 with another flavor
* Test action 5: Wait for VM1 to reach 'VERIFY_RESIZE' status
* Test action 6: Confirm resize VM1
* Test action 7: Wait for VM1 to reach 'ACTIVE' status
* **Test assertion 1:** Verify can ping FIP1 successfully and can SSH to VM1 via FIP1
* Test action 8: Delete KEYP1, VM1 and FIP1

Pass / fail criteria
''''''''''''''''''''

This test evaluates the ability to resize servers. Specifically, the test verifies that:

* Servers can be resized with specific flavor correctly.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A

-----------------------------------
Test Case 7 - Stop and start server
-----------------------------------

Test case specification
-----------------------

tempest.scenario.test_network_advanced_server_ops.TestNetworkAdvancedServerOps.test_server_connectivity_stop_start

Test preconditions
------------------

* Nova, neutron services are available
* One public network

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: Create a keypair KEYP1
* Test action 2: Create a server VM1 with KEYP1
* Test action 3: Create a floating IP FIP1 and assign FIP1 to VM1
* Test action 4: Stop VM1
* Test action 5: Wait for VM1 to reach 'SHUTOFF' status
* **Test assertion 1:** Verify ping FIP1 failed and SSH to VM1 via FIP1 failed
* Test action 6: Start VM1
* Test action 7: Wait for VM1 to reach 'ACTIVE' status
* **Test assertion 2:** Verify can ping FIP1 successfully and can SSH to VM1 via FIP1
* Test action 8: Delete KEYP1, VM1 and FIP1

Pass / fail criteria
''''''''''''''''''''

This test evaluates the ability to stop and start servers. Specifically, the test verifies that:

* When stopped, servers cannot be reached.

* When started, servers can recover its reachability.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A

---------------------------------------
Test Case 8 - Suspend and resume server
---------------------------------------

Test case specification
-----------------------

tempest.scenario.test_network_advanced_server_ops.TestNetworkAdvancedServerOps.test_server_connectivity_suspend_resume

Test preconditions
------------------

* Nova, neutron services are available
* One public network

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: Create a keypair KEYP1
* Test action 2: Create a server VM1 with KEYP1
* Test action 3: Create a floating IP FIP1 and assign FIP1 to VM1
* Test action 4: Suspend VM1
* Test action 5: Wait for VM1 to reach 'SUSPENDED' status
* **Test assertion 1:** Verify ping FIP1 failed and SSH to VM1 via FIP1 failed
* Test action 6: Resume VM1
* Test action 7: Wait for VM1 to reach 'ACTIVE' status
* **Test assertion 2:** Verify can ping FIP1 successfully and can SSH to VM1 via FIP1
* Test action 8: Delete KEYP1, VM1 and FIP1

Pass / fail criteria
''''''''''''''''''''

This test evaluates the ability to suspend and resume servers. Specifically, the test verifies that:

* When suspended, servers cannot be reached.

* When resumed, servers can recover its reachability.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A

----------------------------------------------------
Test Case 9 - Suspend and resume server in sequence
----------------------------------------------------

Test case specification
-----------------------

tempest.scenario.test_server_advanced_ops.TestServerAdvancedOps.test_server_sequence_suspend_resume

Test preconditions
------------------

* Nova, neutron services are available
* One public network

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: Create a server VM1
* Test action 2: Suspend VM1
* Test action 3: Wait for VM1 to reach 'SUSPENDED' status
* **Test assertion 1:** Verify VM1's status is 'SUSPENDED'
* Test action 4: Resume VM1
* Test action 5: Wait for VM1 to reach 'ACTIVE' status
* **Test assertion 2:** Verify VM1's status is 'ACTIVE'
* Test action 6: Suspend VM1
* Test action 7: Wait for VM1 to reach 'SUSPENDED' status
* **Test assertion 3:** Verify VM1 status is 'SUSPENDED'
* Test action 8: Resume VM1
* Test action 9: Wait for VM1 to reach 'ACTIVE' status
* **Test assertion 4:** Verify VM1 status is 'ACTIVE'
* Test action 10: Delete KEYP1, VM1 and FIP1

Pass / fail criteria
''''''''''''''''''''

This test evaluates the ability to suspend and resume servers in sequence.
Specifically, the test verifies that:

* Servers can be suspend and resume in sequence correctly.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A

------------------------------------------
Test Case 10 - Resize volume backed server
------------------------------------------

Test case specification
-----------------------

tempest.scenario.test_server_advanced_ops.TestServerAdvancedOps.test_resize_volume_backed_server_confirm

Test preconditions
------------------

* Nova, neutron, cinder services are available
* One public network

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: Create a volume backed server VM1
* Test action 2: Resize VM1 with another flavor
* Test action 3: Wait for VM1 to reach 'VERIFY_RESIZE' status
* Test action 4: Confirm resize VM1
* Test action 5: Wait for VM1 to reach 'ACTIVE' status
* **Test assertion 1:** VM1's status is 'ACTIVE'
* Test action 6: Delete VM1

Pass / fail criteria
''''''''''''''''''''

This test evaluates the ability to resize volume backed servers.
Specifically, the test verifies that:

* Volume backed servers can be resized with specific flavor correctly.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A

-----------------------------------------
Test Case 11 - Shelve and unshelve server
-----------------------------------------

Test case specification
-----------------------

tempest.scenario.test_shelve_instance.TestShelveInstance.test_shelve_instance

Test preconditions
------------------

* Nova, neutron, image services are available
* One public network

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: Create a keypair KEYP1
* Test action 2: Create a security group SG1, which has rules for allowing
  incoming SSH and ICMP traffic
* Test action 3: Create a server with SG1 and KEYP1
* Test action 4: Create a timestamp and store it in a file F1 inside VM1
* Test action 5: Shelve VM1
* Test action 6: Unshelve VM1
* Test action 7: Wait for VM1 to reach 'ACTIVE' status
* Test action 8: Read F1 and compare if the read value and the previously written value
  are the same or not
* **Test assertion 1:** Verify the values written and read are the same
* Test action 9: Delete SG1, KEYP1 and VM1

Pass / fail criteria
''''''''''''''''''''

This test evaluates the ability to shelve and unshelve servers.
Specifically, the test verifies that:

* Servers can be shelved and unshelved correctly.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A

-------------------------------------------------------
Test Case 12 - Shelve and unshelve volume backed server
-------------------------------------------------------

Test case specification
-----------------------

tempest.scenario.test_shelve_instance.TestShelveInstance.test_shelve_volume_backed_instance

Test preconditions
------------------

* Nova, neutron, image, cinder services are available
* One public network

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: Create a keypair KEYP1
* Test action 2: Create a security group SG1, which has rules for allowing
  incoming and outgoing SSH and ICMP traffic
* Test action 3: Create a volume backed server VM1 with SG1 and KEYP1
* Test action 4: SSH to VM1 to create a timestamp T_STAMP1 and store it in a file F1 inside VM1
* Test action 5: Shelve VM1
* Test action 6: Unshelve VM1
* Test action 7: Wait for VM1 to reach 'ACTIVE' status
* Test action 8: SSH to VM1 to read the timestamp T_STAMP2 stored in F1
* **Test assertion 1:** Verify T_STAMP1 equals to T_STAMP2
* Test action 9: Delete SG1, KEYP1 and VM1

Pass / fail criteria
''''''''''''''''''''

This test evaluates the ability to shelve and unshelve volume backed servers.
Specifically, the test verifies that:

* Volume backed servers can be shelved and unshelved correctly.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A
