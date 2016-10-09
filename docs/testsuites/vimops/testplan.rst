.. This work is licensed under a Creative Commons Attribution 4.0
.. International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) OPNFV

====================================================
OPNFV VIM Operations Compliance Test Plan
====================================================

Introduction
============

The Virtualized Infrastructure Management (VIM) operations compliance test plan
outlines the method for testing VIM operations feature compliance with the
OPNFV platform. VIM operations operations are exercized directly on the exposed
VIM interfaces and verified through a combination of interface operations and
parallel validations from the toolchain.

Scope
-----

The tests comprising the VIM operations suite are intended to validate that
interactions with the VIM result in the realization of key functions expected
and required to provide an operational VIM operations management function. This
includes validating the VIM operations operations sufficiently exercise the
NFVI and NFVI events are accurately exposed at the VIM.

These test suites do not intend to validate the operations of any functions
instantiated on the NFVI, the methods of interaction between the VIM and NFVI,
nor the operations of the VIM outside the scope of the stated tests.

Test suite scope and procedures
===============================

This test suite is designed to be executed from a staging node, referred to as
the jump server, with operational/management access to the VIM control plane
nodes and network access to the NFVI compute nodes. All tests are designed to
interact with the system under test via the control plane interfaces exposed
by the VIM.  Interaction with the NFVI layer is purely to validate operations
requested by the VIM are exercising the NFVI as expected.

The test suites assume the operator, or automated test, has the necessary
authority to interact with and operate the VIM as required to perform the task
outlined in each specific test case.

A test case is structured in such a way that the test case should be exercised
in order from the first test to the last.  Where any operation required to
remove configuration or leverage previous operations is described within the
test case as a further step or operation of the overall test.  Each test case
should begin with the SUT in a stable and ready state, and once the test case
is complete the system should have been returned back to it's previous state.

All test cases provide a description of the expected outcomes of the test,
methods of validating the outcomes and the method of recording the results for
compliance validation.  Logs and traces should be kept and maintained for the
duration of the test activity and provided along with the documented test
results for evaluation.  Where test cases require multiple operations, the
failure of any one operation is not necessarily indicative of the test case
failing and the test case should be completed as documented for the results to
be evaluated.

Using the OPNFV automated self test compliance suite
----------------------------------------------------

The dovetail test suite provides an automated test suite able to perform VIM
operations operations compliance testing as described in this document. The
dovetail test tool should be run from the "jump host" provided for the staging
of the test cases.  The test tool will automatically source all required test
artefacts, maintain a log of events and provide a secure report of the results
of the tests as described in the OPNFV compliance and verification program
(CVP) documentation '[1]'_.

Third party labs for execution of the test suite
------------------------------------------------

If unable to establish a suitable SUT environment for the execution of the
tests you may contact the OPNFV CVP to identify if a third party lab may be
able to assist in the execution of the tests.

Test suite execution
====================

All tests are to be executed from the staging node, or jump host, as described
in the test specification.  Tests should be run as described in the test
specification, if possible with the automated dovetail test suite, in order
that the results can be accurately evaluated.

Details of the execution of each test case is provided in the test case
specification document for the tests. It is expected that all test
specifications should be executed as part of the compliance activity, if you
are unable to execute some parts of the test suite please provide an
explanation and motivation along with the test results for evaluation.

.._[1]: http://www.opnfv.org
