.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Huawei Technologies Co.,Ltd

===================================
Storage Security test specification
===================================

.. toctree::
   :maxdepth: 2

Scope
=====

The storage security test area evaluates the ability of the system under test
to support volume encryption.
The tests in this test area will evaluate functionality of encrypted cinder
volumes. These functionality includes creating an encryption type, creating a
volume type of that encryption type, creating an encrypted cinder volume,
attaching the encrypted volume to VM and detaching the encrypted volume from VM.

References
==========

- Data encryption

  - https://docs.openstack.org/security-guide/tenant-data/data-encryption.html

- Volume encryption

  - https://wiki.openstack.org/wiki/VolumeEncryption

Definitions and abbreviations
=============================

The following terms and abbreviations are used in conjunction with this test
area

- API - Application Programming Interface
- LUKS - Linux Unified Key Setup
- NFVi - Network Functions Virtualization infrastructure
- VIM - Virtual Infrastructure Manager
- VM - Virtual Machine

System Under Test (SUT)
=======================

The system under test is assumed to be the NFVi and VIM in operation on a
Pharos compliant infrastructure.

Test Area Structure
===================

The test area is structured based on the basic operations of cinder volumes.
Each test case is able to run independently, i.e. irrelevant of the state
created by a previous test. Specifically, every test performs clean-up
operations which return the system to the same state as before the test.

Test Descriptions
=================

API Used and Reference
----------------------

Image: https://developer.openstack.org/api-ref/image/v2/index.html#images

- create image
- delete image

Block storage: https://developer.openstack.org/api-ref/block-storage

- create encryption type
- delete encryption type
- create volume type
- delete volume type
- create volume
- delete volume
- attach volume to server
- detach volume from server

Servers: https://developer.openstack.org/api-ref/compute/

- create keypair
- delete keypair
- create server
- delete server

------------------------------------------------
Test Case 1 - Cryptsetup encryption types volume
------------------------------------------------

Test case specification
-----------------------

tempest.scenario.test_encrypted_cinder_volumes.TestEncryptedCinderVolumes.test_encrypted_cinder_volumes_cryptsetup

Test preconditions
------------------

* Block storage volume extension API
* Openstack nova, cinder, glance services are available

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: Create a glance image IMG1
* Test action 2: Create a keypair KEY1
* Test action 3: Create a server VM1 with IMG1 and KEY1
* Test action 4: Create a cinder 'cryptsetup' encryption type ETYP1
* Test action 5: Create a cinder volume type VTYP1 of encryption type ETYP1
* Test action 6: Create a cinder volume VOL1 with ETYP1 and VTYP1
* **Test assertion 1:** VOL1 can be attached to VM1 successfully and
  VOL1 can be detached from VM1 successfully
* Test action 6: Delete IMG1, KEY1, VM1, VOL1, ETYP1 and VTYP1

Pass / fail criteria
''''''''''''''''''''

This test evaluates the functionality of Cryptsetup type encrypted cinder volumes.
Specifically, the test verifies that:

* Cryptsetup encryption type cinder volume can be created correctly.

* Cryptsetup encryption type cinder volume can be attached to and detached from server successfully.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A

------------------------------------------
Test Case 2 - LUKS encryption types volume
------------------------------------------

Test case specification
-----------------------

tempest.scenario.test_encrypted_cinder_volumes.TestEncryptedCinderVolumes.test_encrypted_cinder_volumes_luks

Test preconditions
------------------

* Block storage volume extension API
* Openstack nova, cinder, glance services are available

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
''''''''''''''

* Test action 1: Create a glance image IMG1
* Test action 2: Create a keypair KEY1
* Test action 3: Create a server VM1 with IMG1 and KEY1
* Test action 4: Create a cinder 'LUKS' encryption type ETYP1
* Test action 5: Create a cinder volume type VTYP1 of encryption type ETYP1
* Test action 6: Create a cinder volume VOL1 with ETYP1 and VTYP1
* **Test assertion 1:** VOL1 can be attached to VM1 successfully and
  VOL1 can be detached from VM1 successfully
* Test action 6: Delete IMG1, KEY1, VM1, VOL1, ETYP1 and VTYP1

Pass / fail criteria
''''''''''''''''''''

This test evaluates the functionality of LUKS type encrypted cinder volumes.
Specifically, the test verifies that:

* LUKS encryption type cinder volume can be created correctly.

* LUKS encryption type cinder volume can be attached to and detached from server successfully.

In order to pass this test, all test assertions listed in the test execution above need to pass.

Post conditions
---------------

N/A
