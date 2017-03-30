.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Ericsson AB

======================================================
Compliance and Verification program test specification
======================================================

.. toctree::
:maxdepth: 2

Version history
===============

+------------+----------+------------------+----------------------------------+
| **Date**   | **Ver.** | **Author**       | **Comment**                      |
|            |          |                  |                                  |
+------------+----------+------------------+----------------------------------+
| 2017-03-15 | 0.0.1    | Chris Price      | Draft version                    |
|            |          |                  |                                  |
+------------+----------+------------------+----------------------------------+


Introduction
============

This test specification provides a detailed outline of the prerequisites for performing evaluation
testing, testing methods and procedures used in the evaluation testing process and the tools provided
for running OPNFV evaluation testing.

A CVP system under test is assumed to be a stand alone cloud infrastructure running a virtualisation
software stack providing high availability, redundancy and resiliency.  OPNFV CVP testing covers the
combination of hardware and software that provide an NFV platform for running virtual workloads, approximately
the VIM & VNFi as defined by ETSI NFV ISG.

While the NFV platform is a composite system under test comprised of both hardware and software the VIM
& NFVi testing focuses on software evaluation where it is required and assumed the software is running on
a platform deemed to be Pharos compliant.  A "Pharos compliant" stand alone hardware system can be summarised
as a POD of at least 3 control and two compute blades to exercise the minimum set of compliance testing.
Pharos compliance is further defined, and expected to be implemented according to the `"Pharos specification"`_.


-------
Purpose
-------

This document is intended to be read by an engineer, intending to run or prepare a system for the evaluation
tests, prior to beginning the preparation for executing the evaluation tests.  The document is also useful as
a reference to learn more about OPNFV CVP testing, it's assumptions, targets, methods & tools and expected outcomes.

The engineer will be guided through configuring and populating an environment that is suitable for executing the
OPNFV compliance evaluation test suite.  This includes interpretations of the Pharos specification and assumptions
made by the toolchain on how those interpretations are evaluated.

In addition to system preparation the document provides a guide for working with the methods and tools associated
with the evaluation test procedure.

----------------
Scope of testing
----------------

The OPNFV CVP testing suite is implemented to evaluate the compliance of a virtualisation platform with standard
NFV, carrier and communications network, platform requirements.  Testing focuses on evaluating the software layer
in the platform in it's ability to provide OPNFV features and behaviours required to host communication and networking
industry applications.  This section will provide a brief overview of the target areas and scope addressed by the
testing suites

Features
--------

CVP testing addresses primarily features and capabilities of value to, and further developed by, the OPNFV community.
Target areas for CVP testing are to verify the presence and compliance of:
  * Validation of common cloud environment requirements inherited from key communities such as OpenStack and ETSI
  * Capabilities required to provide consistent application and workload on-boarding, lifecycle management, and scaling
  * Networking features required to address a carrier environment including VPN, service chaining, Trunking and peering
  * Others??

Resilience
----------

Availability of service and infrastructure are fundamental principals of carrier networking and as such form a
component of the compliance test suite aimed to establish the ability of a virtualisation infrastructure to identify
and recover from failures across the system.  The evaluation criteria specifically target control plane resilience
and the ability to identify, accommodate and recover from hardware failures in the system.

Security?
---------

https://jira.opnfv.org/browse/DOVETAIL-382

This section should outline the test strategy related to security,
representing the test cases and requirements on the SUT for security testing.

Scale
-----

The ability to scale is important for carrier networking infrastructure and applications.  The first iteration of the
compliance evaluation test suites address the need to scale however do not enforce strict requirements on how scale is
achieved.

Compliance to the Pharos specification is evaluated as a component of the test suite and provides an visibility into
the physical infrastructures ability to scale in accordance with OPNFV requirements.  The test suite itself does not
require and infrastructure that is running to be deployed at scale in order to pass the tests.  It is assumed the
compliance to Pharos provides enough infrastructure validation that the capability is inherent.

Characteristics
---------------

The OPNFV community invests heavily in ensuring the features and capabilities of the stack are able to run in the
most performant manner according to the needs of the workloads.  This can range from the ability to linearly scale
workloads to the ability to process traffic at line rates.

While each of these is a critical factor in evaluating the performance of a virtualisation infrastructure the CVP
suite does not at this time specify strict requirements on any given capability as part of the evaluation.  It is
expected that in future test suites concise performance metrics will be required to be achieved to achieve compliance
at this time the community has elected not to place pass/fail requirements on characteristics.


---------------------
Definitions and terms
---------------------

This document uses a number of acronyms and terms the reader may not be familiar with.  For a full glossary of
terms used in OPNFV, refer to the `OPNFV Glossary`_.

+------------+----------------------------------------------------------------+
| **Term**   | **Description**                                                |
|            |                                                                |
+------------+----------------------------------------------------------------+
| CVP        | The OPNFVCompliance and Verification Program                   |
|            |                                                                |
+------------+----------------------------------------------------------------+
| SUT        | System under test; the complete system targeted by the         |
|            | test cases, including software hardware and configuration.     |
|            |                                                                |
+------------+----------------------------------------------------------------+
| More       | Additional entries to be added to this table                   |
|            |                                                                |
+------------+----------------------------------------------------------------+


Overview
========

This section of the document will describe in details the processes and procedures required to perform OPNFV CVP
compliance testing.  The section is structured to address; planning and preparation, the approach to testing, the
scope of test activities including details of the test areas, methods and tools used in the testing and the result,
reporting & output of the test suites when run.

Test planning and preparation
=============================

https://jira.opnfv.org/browse/DOVETAIL-384

Give an outline of the planning phase.

--------------
Pre-requisites
--------------

Describe what needs to be in place before starting.

Required Infrastructure, connectivity needs, LF & CVP accounts and any additional security or peripheral needs.
Use sub-chapters for instance for any accounts etc that need to be created.

-------------------------------------------
Preparing the virtualisation infrastructure
-------------------------------------------

Briefly state what will be tested as an intro, then outline the required system state to be achieved prior to running the tests.

Preparing the test staging host system
--------------------------------------

https://jira.opnfv.org/browse/DOVETAIL-385

What is required from the system running the CVP test suites?

Required network configuration
-------------------------------

https://jira.opnfv.org/browse/DOVETAIL-386

VLAN configurations required for NFV deployments.  Non-VLAN configurations if needed.

Preparing your system for CVP testing
-------------------------------------

https://jira.opnfv.org/browse/DOVETAIL-387

Describe how to realise the "Pharos ready state" and the "Software ready state" in this section.

-------------------
Pre-test validation
-------------------

Describe how to evaluate test readiness here.
I suggest this be a process of doing a "dry run" and evaluating the results on the DB.  This should not
need to be reproduced later in the document.

Feature testing scope and approach
==================================

-------------
Test approach
-------------

Here we should describe the way we approach testing different areas.  API through RefStack, resilience through
ETSI test implementations, security is done in xyz way.  This should serve as an introduction to the following
feature test scope sections and provide common information not to be replicated further down.


------------------
Feature test scope
------------------

Included test areas
-------------------

CVP testing for the Danube release focuses on evaluating the ability of a platform to host basic carrier
networking related workloads.  The testing focuses on establishing the ability of the SUT to perform
basic NFVi operations such as managing images, instatiating workload & networking these workloads in a
secure and resiliant manner.

Many OPNFV features are derived from our target upstream communities resulting in the tests focusing
on exposing behaviour present through those development efforts.  This approach to OPNFV development
is reflected in our CVP testing where upstream validation procedures are leveraged to validate the
composite platform.  The OpenStack `RefStack <https://refstack.openstack.org/#/>`_ test suites are
leveraged in OPNFV for performing VIM validation according to expected behaviour in OPNFV.

OPNFV CVP testing has explicit requirements on hardware, control plane and compute topologies which
are assumed to be in place, these are covered in the `Preparing the virtualisation infrastructure`_
section of this document.  Tests may fail if the system is not prepared and configured in accordance
the prpeparation guidelines.

Excluded test areas
-------------------

The CVP testing procedure in Danube do not cover all aspects of the available OPNFV system, nor feature
suites.  To ensure the highest quality of evaluation that provides a trustworthy foundation for industry
compliance toward a common OPNFV standard tests and test areas are selected based on three key principals;
maturity of the test area and framework, availability of features and capabilities across OPNFV compositions,
relevance and value to the industry for evaluation.

In the Danube release of the CVP we have elected to esbalish an evaluation suite for only the common base
features of the platform.  Features areas that are optional or not yet mature in the platform are expluded.
This includes a number of optinal networking features such as BGP VPN networking and Service Chaining which
are intended to be included as optional evaluation areas in future CVP releases.

The Danube release of the OPNFV CVP testing suite in addition does not attempt to provide an evaluation criteria
for hardware.  Any hardware used in the evaluation testing must comply to the pre-resuities outlined in the
`Preparing the virtualisation infrastructure`_ section of this document.  Although the hardware is not tested
itself and no qualification metric has been established for the hardware in the Danube release.

Test criteria and reporting
---------------------------

https://jira.opnfv.org/browse/DOVETAIL-389

This section should specify the criteria to be used to decide whether a test item has passed or failed.
As each area may have differences it is important to ensure the user can react to a failure in accordance
with it's relevance to the overall test suites running.

Critical functions that are mandatory should be identified here. If any of these fail the system testing
should be halted.  If we can having a grading or sorts described here would be helpful as a "guide" for a
tester to know if they should submit, resolve an item in their stack, or try again at another time.


---------------------
Test design and tools
---------------------

This section needs to be done once we know the tools and areas covered by the CVP testing suites.  Parked for now.

VIM NBI testing
---------------

Describe the test areas addressed and how the tools are designed.  It is important to understand the behaviour
of the testing framework when running these tests.  Here we get into the details of behaviour for each of
the test frameworks we use, what they are testing and how the results are to be interpreted.

Outline the tool in detail, in this case RefStack.  How does it work, is it run to completion, is reporting
done per test case when do I as a user know I should do something?

Summarise the tests to be executed by this test framework and the purpose of those tests in the evaluation
of the CVP.  Are there dependancies between tests, does the tool expect a certain behaviour, do the test
cases have specific dependancies.  This provides the overall context of the evaluation performed by this
toolchain / suite and I would not want to be surprised by something when I run the tests after reading this.

Next test area
--------------

What is the test area, what tools, how do they work what does it mean to me as a tester?

Another test area
-----------------

Again what is the test area, what tools, how do they work what does it mean to me as a tester?


CVP test execution
==================

This section should identify the test procedure being executed. Include all people and
roles involved in the execution of a CVP test.  Include procedures, mailing lists, escalation, support
and periods of waiting for results.

The general workflow I assume should be something like this:

* Log into the CVP test case staging computer
* Open a Browser and Log into the CVP tool.
* Select the CVP suite to run, agree to the questions (there should be only 1 for now)
* Run the tests (we should be able to launch this from the Web UI if they are on the hosting machine)
* Wait for the tool to report completed.
* Review your results, refer to trouble shooting or support as needed
* Submit your results for CVP evaluation

------------
Test reports
------------

Describe the process of producing and accessing the test report.  This shoudl be a sub-section of CVP test execution I think.

how do I connect a test suite to my account to get a report?  How do I access the report when it is ready,
how do I identify one report from another in the toolchain?  We should go into all the details here and point
to the tool, referring to the "preparation" section of this document if needed for context.


References
==========

.. _`"Pharos specification"`: https://opnfv.org/
.. _`OPNFV Glossary`: http://docs.opnfv.org/en/latest/glossary/index.html

