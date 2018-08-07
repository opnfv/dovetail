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


`Attach Detach Volume to Instance <https://github.com/openstack/tempest/blob/master/tempest/api/volume/test_volumes_actions.py>`_
    - tempest.api.volume.test_volumes_actions.VolumesActionsTest.test_attach_detach_volume_to_instance


`Volume Boot Pattern test <https://github.com/openstack/tempest/blob/master/tempest/scenario/test_volume_boot_pattern.py>`_
    - Create in Cinder some bootable volume importing a Glance image
    - Boot an instance from the bootable volume
    - Write content to the volume
    - Delete an instance and Boot a new instance from the volume
    - Check written content in the instance
    - Create a volume snapshot while the instance is running
    - Boot an additional instance from the new snapshot based volume
    - Check written content in the instance booted from snapshot

- tempest.scenario.test_volume_boot_pattern.TestVolumeBootPattern.test_volume_boot_pattern