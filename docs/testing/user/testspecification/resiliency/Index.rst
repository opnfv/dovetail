.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) OPNFV

=============================
Resiliency Test Specification
=============================

.. toctree::
:maxdepth: 2

Scope
=====

The resiliency test involves testing and verifying the ability of the SUT to withstand stress and other challenging
factors. Main purpose behind the testing is to make sure the SUT is able to absorb failures
while providing an acceptable level of service.


References
================

This test area references the following specifications, definitions and reviews:

- Upstream OpenStack NOVA Resiliency

  - https://wiki.openstack.org/wiki/NovaResiliency

- Stress Testing over OPNFV Platform

  - https://wiki.opnfv.org/display/bottlenecks/Stress+Testing+over+OPNFV+Platform


Definitions and Abbreviations
=============================

The following terms and abbreviations are used in conjunction with this test area

- API - Application Programming Interface
- iff - if and only if
- Monitor - Tools to tracking the system/component behaviors
- NFVI - Network Functions Virtualization Infrastructure
- NIC - Network Interface Controller
- Service Level - Measurable terms that describe the quality of the service provided by the SUT within a given time period
- SUT - system under test
- TCP - Transmission Control Protocol
- UDP - User Datagram Protocol
- VM - Virtual Machine
- vNIC - virtual Network Interface Card


System Under Test (SUT)
=======================

The system under test is assumed to be the NFVI and VIM in operation on a
Pharos compliant infrastructure.


Test Area Structure
====================

The resiliency test area is structured by test cases focusing on different
purposes or their combinations. Preceding test will affect the subsequent test
with high probability in terms of service level
unless the system has fully recovered from the preceding test.


Test Descriptions
=================

------------------------------------------------
Test Case 1 - Perform life-cycle events for ping
------------------------------------------------

Short name
----------

posca_stress_ping

Use case specification
----------------------

This test case verifies the ability of the SUT setting up VM pairs for different tenants
and providing acceptable capacity after the amount of VM pairs reaches certain quantity.
The connectivity between VMs in a VM pair for a tenant is validated through Ping test.
A life-cycle event is referred to a VM pair life-cycle consisting of spawning, pinging and
destroying.

Test preconditions
------------------

heat_template_version': '2013-05-23

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Methodology for validating capacity of the SUT
'''''''''''''''''''''''''''''''''''''''''''''
Validating capacity of the SUT based on life-cycle ping test generally involves
2 subtests which provides secondary validation for the SUT furnishing users with
acceptable amount of VMs without being crushed.

Let *N1*, *N2*, *N3* and *P1* be certain preset numbers, repectively. In subtest 1, the SUT concurrently
setting up *N1* VM pairs with each VM pair belonging to a different tenant. Then
VM1 in a VM pair pings VM2 for *P1* times. The connectivity could be validated iff
at least 1 time that VM1 successfully pings VM2.

Subtest 2 is executed after subtest 1 as the secondary validation of the capacity.
It follows the same workflow as subtest 1 does to set up *N2* VM pairs. Even if the SUT malfunctions after
subtest 1, subtest 2 should be executed anyway in order to characterize ability of the SUT.

Assume *S1* and *S2* be the numbers of VM pairs that are successfully created in
subtest 1 and subtest 2, respectively. If *min(S1,S2)>=N3*, then the SUT is considered a PASS.
Otherwise, we denote the SUT with FAIL.

Test execution
''''''''''''''
* Test action 1: Install the testing tools by pulling and running Bottlenecks docker
* Test action 2: Prepare the test by sourcing rc file, eliminating the environment constraints, i.e., Quota setting, setting up Yarstick docker, pulling and registering OS images and VM flavor 
* Test action 3: Call Yardstick to concurrently creating *N1* VM pairs for N1 tenants
* Test action 4: Do *P1* ping tests within each VM pair while recording the successful pings
* Test action 5: Mark the VM pairs with at least 1 successful ping as PASS and record the total number of PASS VM pairs as *S1*
* Test action 6: Detroy all the VM pairs
* Test action 7: Goto *Test action 3* and do the test again to create *N2* VM pairs with PASS VM pairs counted as *S2*
* Test action 8: Denote the secondary validated capacity by *min(S1, S2)*
* Test action 9 (Optional): Clean up Bottlencks and Yardstick docker

Pass / fail criteria
''''''''''''''''''''

Typical setting of *(N1, N2, N3, P1)* is *(20, 20, 20, 10)*.

The connectivity witin a VM pair is validated iff:

* At least 1 ping test is successful among P1 tests

The SUT is considered passing the test iff:

* min(S1,S2)>=N3

Post conditions
---------------

N/A