.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Ericsson AB

===========================================
Tempest Volume test specification
===========================================


Scope
=====

This test area evaluates the ability of a system under test to manage volumes.

The test area specifically validates the creation, the deletion and
the attachment/detach volume operations.
tests.


References
==========

N/A

System Under Test (SUT)
=======================

The system under test is assumed to be the NFVi and VIM in operation on a
Pharos compliant infrastructure.

Test Area Structure
===================

The test area is structured in individual tests as listed below.
For detailed information on the individual steps and assertions performed
by the tests, review the Python source code accessible via the following links:

All these test cases are included in the test case dovetail.tempest.volume of
OVP test suite.


------------------------------------------------------------------------
Test Case 1 - `Attach Detach Volume to Instance <https://github.com/openstack/tempest/blob/master/tempest/api/volume/test_volumes_actions.py>`_
------------------------------------------------------------------------

Test case specification
-----------------------

tempest.api.volume.test_volumes_actions.VolumesActionsTest.test_attach_detach_volume_to_instance

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
* Test action 4: Detach VOL1 from VM1
* **Test assertion 3:** Verify detach volume VOL1 successfully

Pass / fail criteria
''''''''''''''''''''

This test evaluates the volume API ability of attaching a volume to a server
and detaching a volume from a server. Specifically, the test verifies that:

* Volumes can be attached and detached from servers.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A

------------------------------------------------------------------------
Test Case 2 - `Volume Boot Pattern test <https://github.com/openstack/tempest/blob/master/tempest/scenario/test_volume_boot_pattern.py>`_
------------------------------------------------------------------------

Test case specification
-----------------------

tempest.scenario.test_volume_boot_pattern.TestVolumeBootPattern.test_volume_boot_pattern

Test preconditions
------------------

* Volume extension API

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''
* Test action 1:Create in Cinder some bootable volume VOL1 importing a Glance image
* Test action 2:Boot an instance VM1 from the bootable volume VOL1
* Test action 3:Write content to the VOL1
* Test action 4:Delete VM1 and Boot a new instance VM2 from the volume VOL1
* Test action 5:Check written content in the instance
* **Test assertion 1:** Verify the content of written file in action 3
* Test action 6:Create a volume snapshot VOL2 while the instance VM2 is running
* Test action 7:Boot an additional instance VM3 from the new snapshot based volume VOL2
* Test action 8:Check written content in the instance booted from snapshot
* **Test assertion 2:** Verify the content of written file in action 3

Pass / fail criteria
''''''''''''''''''''

This test evaluates the volume storage consistency, Specifically, the test verifies that:

* The content of written file in the volume.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A
