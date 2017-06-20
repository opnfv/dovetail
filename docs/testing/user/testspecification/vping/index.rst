.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Ericsson AB

========================
Vping test specification
========================

.. toctree::
   :maxdepth: 2

Scope
=====

The vping test area evaluates basic NFVi capabilities of the system under test.
These capabilities include creating a small number of virtual machines,
establishing basic L2 connectivity between them and verifying connectivity by
means of ICMP packets.


References
==========

TBD


Definitions and abbreviations
=============================

The following terms and abbreviations are used in conjunction with this test
area

- ICMP - Internet Control Message Protocol
- NFVi - Network functions virtualization infrastructure
- VM - Virtual machine


System Under Test (SUT)
=======================

The system under test is assumed to be the NFVi and VIM in operation on a
Pharos compliant infrastructure.


Test Area Structure
===================

The test area is structured in two separate tests which are executed
sequentially. The order of the tests is arbitrary as there are no dependencies
across the tests.


Test Descriptions
=================

-------------------------------------------------------
Test Case 1 - vPing using userdata via the config drive
-------------------------------------------------------

Short name
----------

opnfv.vping.userdata


Use case specification
----------------------

This test evaluates the use case where an NFVi tenant boots up a small number
of VMs and requires L2 connectivity between those VMs.


Test preconditions
------------------

At least one compute node is available. No further pre-configuration needed.


Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Methodology for verifying connectivity
''''''''''''''''''''''''''''''''''''''

Connectivity between VMs is tested by sending ICMP ping packets between
selected VMs. The target IPs are passed to the VMs sending pings by means of a
custom userdata script by means of the config driver mechanism provided by
Nova. Whether or not a ping was successful is determined by checking the
console output of the source VMs.


Test execution
''''''''''''''

* Create a test image in the Glance image store

* Create a Neutron network N

* Create security group allowing ICMP and SSH traffic

* Delete all VMs running on the system

* Create VM1 with a port in network N

* Create VM2 with a port in network N

* VM2 boots up and executes a script which is passed through the config drive.
  The script invokes ``ping`` with the IP address of VM1.

* **Test assertion:** Ping from VM2 to VM1 succeeds: ``ping`` exits with return
  code 0



Pass / fail criteria
''''''''''''''''''''

This test evaluates basic NFVi capabilities of the system under test.
Specifically, the test verifies that:

* The NFVi can boot up VMs with userdata

* VMs in the same Neutron subnet have IP connectivity.

In order to pass this test, all test assertions listed in the test execution
above need to pass.


Post conditions
---------------

The VMs VM1 and VM2 as well as the Neutron network remain on the system.



----------------------------------------------
Test Case 2 - vPing using SSH to a floating IP
----------------------------------------------

Short name
----------

opnfv.vping.ssh


Use case specification
----------------------

This test evaluates the use case where an NFVi tenant boots up a small number
of VMs and requires L2 connectivity between those VMs.


Test preconditions
------------------

At least one compute node is available. No further pre-configuration needed.


Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Methodology for verifying connectivity
''''''''''''''''''''''''''''''''''''''

Connectivity between VMs is tested by sending ICMP ping packets between
selected VMs. To this end, the test establishes a SSH connection from the host
running the test suite to a floating IP assiciates to VM2 and executes ``ping``
on VM2 with the IP of VM1 as target.


Test execution
''''''''''''''

* Create a test image in the Glance image store

* Create a Neutron network N

* Create security group allowing ICMP and SSH traffic

* Delete all VMs running on the system

* Create VM1 with a port in network N

* Create VM2 with a port in network N

* Associate a floating IP with VM2

* Copy a script ``ping.sh`` to VM2 via SSH and execute the script

* The script ``ping.sh`` invokes ``ping`` with the target IP of VM1

* **Test assertion:** Ping from VM2 to VM1 succeeds: ``ping`` exits with return
  code 0



Pass / fail criteria
''''''''''''''''''''

This test evaluates basic NFVi capabilities of the system under test.
Specifically, the test verifies that:

* The NFVi can boot up VMs

* Floating IPs can be associated with VMs

* SSH connectivity from the host running the test suite to VM2 via the floating
  IP is available.

* VMs in the same Neutron subnet have IP connectivity.

In order to pass this test, all test assertions listed in the test execution
above need to pass.


Post conditions
---------------

The VMs VM1 and VM2 as well as the Neutron network N remain on the system.

