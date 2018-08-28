.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Ericsson AB, and others

.. _dovetail-test_case_requirements:

==========================
OVP Test Case Requirements
==========================

.. toctree::
   :maxdepth: 2


OVP Test Suite Purpose and Goals
================================

The OVP test suite is intended to provide a method for validating the
interfaces and behaviors of an NFVI platform according to the expected
capabilities exposed in OPNFV. The behavioral foundation evaluated in these
tests should serve to provide a functional baseline for VNF deployment and
portability across NFVI instances. All OVP tests are available in open source
and are executed in open source test frameworks.


Test case requirements
======================

The following requirements are mandatory for a test to be submitted for
consideration in the OVP test suite:

- All test cases must be fully documented, in a common format. Please consider
  the existing :ref:`dovetail-test_case_specification` as examples.

  - Clearly identifying the test procedure and expected results / metrics to
    determine a “pass” or “fail” result.

- Tests must be validated for the purpose of OVP, tests should be run with both
  an expected positive and negative outcome.

- At the current stage of OVP, only functional tests are eligible, performance
  testing is out of scope.

  - Performance test output could be built in as “for information only”, but
    must not carry pass/fail metrics.

- Test cases should favor implementation of a published standard interface for
  validation.

  - Where no standard is available provide API support references.

  - If a standard exists and is not followed, an exemption is required. Such
    exemptions can be raised in the project meetings first, and if no consensus
    can be reached, escalated to the TSC.

- Test cases must pass on applicable OPNFV reference deployments and release
  versions.

  - Tests must not require a specific NFVI platform composition or installation
    tool.

    - Tests and test tools must run independently of the method of platform
      installation and architecture.

    - Tests and test tools must run independently of specific OPNFV components
      allowing different components such as storage backends or SDN
      controllers.

  - Tests must not require un-merged patches to the relevant upstream projects.

  - Tests must not require features or code which are out of scope for the
    latest release of the OPNFV project.

  - Tests must have a documented history of recent successful verification in
    OPNFV testing programs including CI, Functest, Yardstick, Bottlenecks,
    Dovetail, etc. (i.e., all testing programs in OPNFV that regularly validate
    tests against the release, whether automated or manual).

  - Tests must be considered optional unless they have a documented history for
    ALL OPNFV scenarios that are both

    - applicable, i.e., support the feature that the test exercises, and

    - released, i.e., in the OPNFV release supported by the OVP test suite
      version.

- Tests must run against a fully deployed and operational system under test.

- Tests and test implementations must support stand alone OPNFV and commercial
  OPNFV-derived solutions.

  - There can be no dependency on OPNFV resources or infrastructure.

  - Tests must not require external resources while a test is running, e.g.,
    connectivity to the Internet. All resources required to run a test, e.g.,
    VM and container images, are downloaded and installed as part of the system
    preparation and test tool installation.

- The following things must be documented for the test case:

  - Use case specification
  - Test preconditions
  - Basic test flow execution description and test assertions
  - Pass fail criteria

- The following things may be documented for the test case:

  - Parameter border test cases descriptions
  - Fault/Error test case descriptions
  - Post conditions where the system state may be left changed after completion

New test case proposals should complete a OVP test case worksheet to ensure
that all of these considerations are met before the test case is approved for
inclusion in the OVP test suite.


Dovetail Test Suite Naming Convention
=====================================

Test case naming and structuring must comply with the following conventions.
The fully qualified name of a test case must comprise three sections:

`<testproject>.<test_area>.<test_case_name>`

- **testproject**: The fully qualified test case name must identify the test
  project which developed and maintains the test case.

- **test_area**: The fully qualified test case name must identify the test case
  area. The test case area is a single word identifier describing the broader
  functional scope of a test case, such as ha (high-availability), tempest, vnf,
  etc.

- **test_case_name**: The fully qualified test case name must include a concise
  description of the purpose of the test case.

An example of a fully qualified test case name is `functest.tempest.compute`.

