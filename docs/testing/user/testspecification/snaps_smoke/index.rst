.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Ericsson AB

==============================
SNAPS smoke test specification
==============================

.. toctree::
   :maxdepth: 2

Scope
=====

The SNAPS smoke test case contains tests that setup and destroy environments
with VMs with and without Floating IPs with a newly created user and project.

References
==========

This smoke test executes the Python Tests included with the SNAPS libraries
that exercise many of the OpenStack APIs within Keystone, Glance, Neutron,
and Nova.

- https://wiki.opnfv.org/display/PROJ/SNAPS-OO

System Under Test (SUT)
=======================

The SUT is assumed to be the NFVi and VIM in operation on a Pharos compliant infrastructure.


Test Area Structure
===================

The test area is structured in individual tests as listed below.
For detailed information on the individual steps and assertions performed
by the tests, review the Python source code accessible via the following links:

**Dynamic creation of User/Project objects to be leveraged for the integration tests:**

- `Create image tests <https://github.com/opnfv/snaps/blob/stable/fraser/snaps/openstack/tests/create_image_tests.py>`_
    - snaps.openstack.tests.create_image_tests.CreateImageSuccessTests
    - snaps.openstack.tests.create_image_tests.CreateImageNegativeTests
    - snaps.openstack.tests.create_image_tests.CreateMultiPartImageTests


- `Create Keypairs Cleanup tests <https://github.com/opnfv/snaps/blob/stable/fraser/snaps/openstack/tests/create_keypairs_tests.py>`_
    - snaps.openstack.tests.create_keypairs_tests.CreateKeypairsTests
    - snaps.openstack.tests.create_keypairs_tests.CreateKeypairsCleanupTests


- `Create Network Success tests <https://github.com/opnfv/snaps/blob/stable/fraser/snaps/openstack/tests/create_network_tests.py>`_
    - snaps.openstack.tests.create_network_tests.CreateNetworkSuccessTests


- `Create Router Success tests <https://github.com/opnfv/snaps/blob/stable/fraser/snaps/openstack/tests/create_router_tests.py>`_
    - snaps.openstack.tests.create_router_tests.CreateRouterSuccessTests
    - snaps.openstack.tests.create_router_tests.CreateRouterNegativeTests


- `Create QoS tests <https://github.com/opnfv/snaps/blob/stable/fraser/snaps/openstack/tests/create_qos_tests.py>`_
    - snaps.openstack.tests.create_qos_tests.CreateQoSTests


- `Create Volume tests <https://github.com/opnfv/snaps/blob/stable/fraser/snaps/openstack/tests/create_volume_tests.py>`_
    - snaps.openstack.tests.create_volume_tests.CreateSimpleVolumeSuccessTests
    - snaps.openstack.tests.create_volume_tests.CreateSimpleVolumeFailureTests
    - snaps.openstack.tests.create_volume_tests.CreateVolumeWithTypeTests
    - snaps.openstack.tests.create_volume_tests.CreateVolumeWithImageTests


- `Create Simple Volume Type Tests <https://github.com/opnfv/snaps/blob/stable/fraser/snaps/openstack/tests/create_volume_type_tests.py>`_
    - snaps.openstack.tests.create_volume_type_tests.CreateSimpleVolumeTypeSuccessTests
    - snaps.openstack.tests.create_volume_type_tests.CreateVolumeTypeComplexTests

- `Create Instance Tests <https://github.com/opnfv/snaps/blob/stable/fraser/snaps/openstack/tests/create_instance_tests.py>`_
    - snaps.openstack.tests.create_instance_tests.SimpleHealthCheck
    - snaps.openstack.tests.create_instance_tests.CreateInstanceTwoNetTests
    - snaps.openstack.tests.create_instance_tests.CreateInstanceSimpleTests
    - snaps.openstack.tests.create_instance_tests.CreateInstancePortManipulationTests
    - snaps.openstack.tests.create_instance_tests.InstanceSecurityGroupTests
    - snaps.openstack.tests.create_instance_tests.CreateInstanceOnComputeHost
    - snaps.openstack.tests.create_instance_tests.CreateInstanceFromThreePartImage
    - snaps.openstack.tests.create_instance_tests.CreateInstanceVolumeTests
    - snaps.openstack.tests.create_instance_tests.CreateInstanceSingleNetworkTests

- `Create Stack Tests <https://github.com/opnfv/snaps/blob/stable/fraser/snaps/openstack/tests/create_stack_tests.py>`_
    - snaps.openstack.tests.create_stack_tests.CreateStackSuccessTests
    - snaps.openstack.tests.create_stack_tests.CreateStackVolumeTests
    - snaps.openstack.tests.create_stack_tests.CreateStackFlavorTests
    - snaps.openstack.tests.create_stack_tests.CreateStackKeypairTests
    - snaps.openstack.tests.create_stack_tests.CreateStackSecurityGroupTests
    - snaps.openstack.tests.create_stack_tests.CreateStackNegativeTests


- `Create Security Group Tests <https://github.com/opnfv/snaps/blob/master/snaps/openstack/tests/create_security_group_tests.py>`_
    - snaps.openstack.tests.create_security_group_tests.CreateSecurityGroupTests


**Floating IP and Ansible provisioning:**

- `Create Stack FloatingIp <https://github.com/opnfv/snaps/blob/stable/fraser/snaps/openstack/tests/create_stack_tests.py>`_
    - snaps.openstack.tests.create_stack_tests.CreateStackFloatingIpTests


- `Ansible Provisioning <https://github.com/opnfv/snaps/blob/stable/fraser/snaps/provisioning/tests/ansible_utils_tests.py>`_
    - snaps.provisioning.tests.ansible_utils_tests.AnsibleProvisioningTests

