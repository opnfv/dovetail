.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) OPNFV

=========================
Stress Test Specification
=========================

.. toctree::
   :maxdepth: 2

Scope
=====

The stress test involves testing and verifying the ability of the SUT to withstand
stress and other challenging factors. Main purpose behind the testing is to make sure
the SUT is able to absorb failures while providing an acceptable level of service.


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

- iff - if and only if
- NFVI - Network Functions Virtualization Infrastructure
- NaN - Not a Number
- Service Level - Measurable terms that describe the quality of the service provided by the SUT within a given time period
- SUT - System Under Test
- VM - Virtual Machine


System Under Test (SUT)
=======================

The system under test is assumed to be the NFVI and VIM in operation on a
Pharos compliant infrastructure.


Test Area Structure
====================

According to the testing goals stated in the test scope section,
preceding test will not affect the subsequent test
as long as the SUT is able to sustain the given stress
while providing an acceptable level of service.
Any FAIL result from a single test case will cause the SUT failing the whole test.


Test Descriptions
=================

----------------------------------------------------------------
Test Case 1 - Concurrent capacity based on life-cycle ping test
----------------------------------------------------------------

Short name
----------

dovetail.stress.ping

Use case specification
----------------------

This test case verifies the ability of the SUT concurrently setting up VM pairs
for different tenants (through different OpenStack related components) and
providing acceptable capacity under stressful conditions. The connectivity between
VMs in a VM pair for a tenant is validated through Ping test. A life-cycle event
in this test case is particularly referred to a VM pair life-cycle consisting of
spawning, pinging and destroying.

Test preconditions
------------------

* heat_template_version: 2013-05-23
* ElasticSearch Port: 5044
* LogStash Port: 5601
* Kibana Port: 9200
* Yardstick Port: 8888

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Methodology for validating capacity of the SUT
'''''''''''''''''''''''''''''''''''''''''''''
Validating capacity of the SUT based on life-cycle ping test generally involves
2 subtests which provides secondary validation for the SUT furnishing users with
reliable capacity without being crushed.

Let *N1*, *N2*, *N3* and *P1* be certain preset numbers, respectively.
In subtest 1, the SUT concurrently setting up *N1* VM pairs with each VM pair
belonging to a different tenant. Then VM1 in a VM pair pings VM2 for *P1* times
with *P1* packets. The connectivity could be validated iff VM1 successfully pings
VM2 with these *P1* packets.
Subtest 1 is finished iff all the concurrent (*N1*) requests for creating VM pairs
are fulfilled with returned values that indicate the statuses of the VM pairs creations.

Subtest 2 is executed after subtest 1 as secondary validation of the capacity.
It follows the same workflow as subtest 1 does to set up *N2* VM pairs.

Assume *S1* and *S2* be the numbers of VM pairs that are successfully created in
subtest 1 and subtest 2, respectively. If *min(S1,S2)>=N3*, then the SUT is considered as PASS.
Otherwise, we denote the SUT with FAIL.

Note that for subtest 1, if the number of successfully created VM pairs, i.e., *S1*,
is smaller than *N3*. Subtest 2 will not be executed and SUT will be marked with FAIL.

Test execution
''''''''''''''
* Test action 1: Install the testing tools by pulling and running the Bottlenecks Docker container
* Test action 2: Prepare the test by sourcing openstack credential file,
  eliminating the environment constraints, i.e., Quota setting, setting up
  Yardstick docker, pulling and registering OS images and VM flavor
* Test action 3: Call Yardstick to concurrently creating *N1* VM pairs for N1 tenants
* Test action 4: In each VM pair, VM1 pings VM2 for *P1* times with *P1* packets while recording the successful numbers
* Test action 5: Mark the VM pairs with *P1* successful pings as PASS and record the total number of PASS VM pairs as *S1*
* Test action 6: Destroy all the VM pairs
* Test action 7: If *S1<N3*, the SUT is marked with FAIL and the test return. Otherwise go to *Test action 8*
* Test action 8: Go to *Test action 3* and do the test again to create *N2* VM pairs with PASS VM pairs counted as *S2*
* Test action 9: If *S2<N3*, the SUT is marked with FAIL. Otherwise marked with PASS.

Pass / fail criteria
''''''''''''''''''''

Typical setting of *(N1, N2, N3, P1)* is *(5, 5, 5, 10)*.
The reference setting above is acquired based on the results from OPNFV CI jobs
and testing over commercial products.

The connectivity within a VM pair is validated iff:

* VM1 successfully pings VM2 for *P1* times with *P1* packets

The SUT is considered passing the test iff:

* *min(S1,S2)>=N3*

Note that after each subtest, the program will check if the successfully created number of VM pairs
is smaller than *N3*. If true, the program will return and the SUT will be marked with FAIL.
Then the passing criteria is equal to the equation above. When subtest 1 returns, *S2* here is denoted
by NaN.

Post conditions
---------------

The whole stress testing workflow will not proceed if the SUT is marked with FAIL.
That is, subsequent test cases do not need to be executed anymore.
The Bottlenecks and Yardstick dockers should be destroyed then.

