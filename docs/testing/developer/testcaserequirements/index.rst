.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Ericsson AB

==========================================================
Compliance and Verification program test case requirements
==========================================================

.. toctree::
   :maxdepth: 2

CVP Test Suite Purpose and Goals
================================

The CVP test suite is intended to provide a method for validating the interfaces
and behaviors of an NFVi platform according to the expected capabilities exposed in
OPNFV.  The behavioral foundation evaluated in these tests should serve to provide
a functional baseline for VNF deployment and portability across NFVi instances.
All CVP tests are available in open source and are executed in open source test frameworks.

Test case requirements
======================

The following requirements are mandatory for test to be submitted for consideration in the
 CVP test suite:

- All test cases must be fully documented, in a common format

  - Clearly identifying the test procedure and expected results / metrics to determine a “pass” or “fail” result.

- Tests must be validated for purpose, tests should be run with both an expected positive and negative outcome.
- Tests should focus on functionality, not performance.

  - Performance test output could be built in as “for information only”, but must not carry pass/fail metrics.

- Test cases should favor implementation of a published standard interface for validation

  - Where no standard is available provide API support references
  - If a standard exists and is not followed, an exemption is required

- Test cases must pass on OPNFV reference deployments

  - Tests must not require a specific NFVi platform composition or installation tool

    - Tests and test tools must run independently of the method of platform installation and architecture.
    - Tests and tool must run independent of specific OPNFV components allowing different components such as storage backends or SDN controllers.

  - Tests must not require un-merged patches to the relevant upstream projects
  - Tests must not require features or code which are out of scope for the latest release of the OPNFV project
  - Tests must have a documented history of successful use in CI Functest for OPNFV scenarios that are both applicable and released.
  - Tests must be considered optional unless they have a documented history of successful use in CI Functest for ALL OPNFV scenarios that are both applicable and released.

- Tests must run against a fully deployed and operational system under test.
- Tests and test tools must support stand alone OPNFV and commercial derived OPNFV based solution

  - There can be no dependency on OPNFV resources or infrastructure.

- The following things must be documented for the test case:

  - Use case specification
  - Test preconditions
  - Basic test flow execution descriptor
  - Pass fail criteria

- The following things may be documented for the test case:

  - Parameter border test cases descriptions
  - Fault/Error test case descriptions
  - Post conditions where the system state may be left changed after completion

New test case proposals should complete a CVP test case worksheet to ensure that all
of these considerations are met before the test case is approved for inclusion in the
CVP test suite.

Dovetail Test Suite Naming Convention
=====================================

Test case naming and structure for dovetail needs to be done, it should consider:

- Identifying the test area
- Identifying the purpose of the test case

To be discussed, agreed and amended to this document.

