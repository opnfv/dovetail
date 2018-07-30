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

API Docs:
- http://snaps-provisioning.readthedocs.io/en/latest/


System Under Test (SUT)
=======================

The system under test is assumed to be the NFVi and VIM in operation on a
Pharos compliant infrastructure.


Test Area Structure
===================

The test area is structured in individual tests as listed below. 
For detailed information on the individual steps and assertions performed
by the tests, review the Python source code accessible via the following links:

**Dynamic creation of User/Project objects to be leveraged for the integration tests:**

- Create image tests 
  <https://github.com/opnfv/snaps/blob/stable/fraser/snaps/openstack/tests/create_image_tests.py>'

- Create Keypairs Cleanup tests 
  '<https://github.com/opnfv/snaps/blob/stable/fraser/snaps/openstack/tests/create_keypairs_tests.py>'

- Create Network Success tests 
  '<https://github.com/opnfv/snaps/blob/stable/fraser/snaps/openstack/tests/create_network_tests.py>'

- Create Router Success tests 
  '<https://github.com/opnfv/snaps/blob/stable/fraser/snaps/openstack/tests/create_router_tests.py>'

- Create QoS tests 
  '<https://github.com/opnfv/snaps/blob/stable/fraser/snaps/openstack/tests/create_qos_tests.py>'

- Create Volume Type Success tests
- Create Simple Volume Success tests
- Create Simple Volume Failure tests
- Create Volume With Type tests
- Create Volume With Image tests
  '<https://github.com/opnfv/snaps/blob/stable/fraser/snaps/openstack/tests/create_volume_tests.py>'

- Create Volume Type Complex tests 
  '<https://github.com/opnfv/snaps/blob/stable/fraser/snaps/openstack/tests/create_volume_type_tests.py>'

- Simple Health Check 
- Create Instance Two Net 
- Create Instance Simple 
- Create Instance Port Manipulation 
- Instance Security Group 
- Create Instance On Compute Host 
- Create Instance From Three Part Image 
- Create Instance Volume 
'<https://github.com/opnfv/snaps/blob/stable/fraser/snaps/openstack/tests/create_instance_tests.py>'

- Create Stack Success 
- Create Stack Volume 
- Create Stack Flavor 
- Create Stack Keypair 
- Create Stack Security Group 
- Create Stack Negative 
'<https://github.com/opnfv/snaps/blob/stable/fraser/snaps/openstack/tests/create_stack_tests.py>'

**Floating IP and Ansible provisioning:**

- Create Stack FloatingIp 
  '<https://github.com/opnfv/snaps/blob/stable/fraser/snaps/openstack/tests/create_stack_tests.py>'

- Ansible Provisioning 
  '<https://github.com/opnfv/snaps/blob/e6ec3766be49d69a44ca1e1348bbf5e6ed692c84/snaps/provisioning/tests/ansible_utils_tests.py>'