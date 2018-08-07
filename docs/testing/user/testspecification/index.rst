.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Ericsson AB, Huawei Technologies Co.,Ltd

.. _dovetail-test_case_specification:

==================================================
OPNFV Verified Program test specification
==================================================

Introduction
============

The OPNFV OVP provides a series or test areas aimed to evaluate the operation
of an NFV system in accordance with carrier networking needs.  Each test area
contains a number of associated test cases which are described in detail in the
associated test specification.

All tests in the OVP are required to fulfill a specific set of criteria in
order that the OVP is able to provide a fair assessment of the system under
test.  Test requirements are described in the :ref:dovetail-test_case_requirements
document.

All tests areas addressed in the OVP are covered in the following test
specification documents.

.. toctree::
   :maxdepth: 1

  ./highavailability/index.rst
  ./tempest_osinterop/index.rst
  ./vping/index.rst
  ./tempest_ipv6/index.rst
  ./tempest_network_security/index.rst
  ./tempest_network/network_scenario.rst
  ./tempest_vm_lifecycle/index.rst
  ./tempest_multi_node_scheduling/index.rst
  ./vpn/index.rst
  ./vnf/index.rst
  ./stress/index.rst
  ./snaps_smoke/index.rst
  ./tempest_compute/index.rst
  ./tempest_identity_v2/index.rst
  ./tempest_identity_v3/index.rst
  ./tempest_image/index.rst
  ./tempest_network/index.rst
  ./tempest_volume/index.rst