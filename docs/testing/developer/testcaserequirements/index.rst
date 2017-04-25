.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Ericsson AB

==========================================================
Compliance and Verification program test case requirements
==========================================================

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


CVP Test Suite Purpose and Goals
================================

The CVP test suite is intended to provide a method for validating the interfaces
and behaviors of an NFVi platform according to the expected capabilities exposed in
an OPNFV NVFi instance, and to provide a baseline of functionality to enable VNF
portability across different OPNFV NFVi instances. All CVP tests will be available
in open source and will be developed on readily available open source test frameworks.

Working with the ETSI NFV TST 001 reference:
http://www.etsi.org/deliver/etsi_gs/NFV-TST/001_099/001/01.01.01_60/gs_NFV-TST001v010101p.pdf

The CVP program focuses on tests validating a scope for a System Under Test
(SUT) associated with Chapter 4.9 - NFV Infrastructure + VIM Under Test, as adapted
for OPNFV (see figure below).  The test suite will also define preconditions and
assumptions about the state of any platform under evaluation. The test suite must
not require access to OPNFV infrastructre or resources in order to pass.

Test case requirements
======================

The following requirements should be fulfilled for all tests added to the CVP test suite:

    Test cases should favour implementation of a published standard interface for validation
        Where a compliance test suite exists for components of the SUT, this test suite should generally be considered as a baseline for CVP testing
        Where no standard is available provide API support references
        If a standard exists and is not followed, an exemption is required
    The following things must be documented for the test case:
        Use case specification
        Test preconditions
        Basic test flow execution descriptor
        Post conditions and pass fail criteria
    The following things may be documented for the test case:
        Parameter border test cases descriptions
        Fault/Error test case descriptions
    Test cases must pass on OPNFV reference deployments
        Tests must not require a specific NFVi platform composition or installation tool
        Tests must not require unmerged patches to the relevant upstream projects
        Tests must not require features or code which are out of scope for the latest release of the OPNFV project

New test case proposals should complete a CVP test case worksheet to ensure that all
of these considerations are met before the test case is approved for inclusion in the
CVP test suite.
