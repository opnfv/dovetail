.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Ericsson AB


=============================================================
Compliance and Verification Program Test Tool Developer Guide
=============================================================

.. toctree::
:maxdepth: 2

Version history
===============

+------------+----------+------------------+----------------------------------+
| **Date**   | **Ver.** | **Author**       | **Comment**                      |
|            |          |                  |                                  |
+------------+----------+------------------+----------------------------------+
| 2017-04-13 | 0.0.1    | Trevor Cooper    | Draft version                    |
|            |          |                  |                                  |
+------------+----------+------------------+----------------------------------+


Introduction
============

OPNFV Compliance defines required platform behavior which is a set of platform capabilities/features desirable
for setup, instantiate, scale and tear down of a Network Service on an NFV platform. In addition the User
(or Operator) Experience should be "good" which means that from a User perspective Network Services are easy
to instantiate and manage.


----------------
Document Purpose
----------------

The purpose of this document is to help guide development of the Dovetail test tool so that it will have the
required capabilities for executing test cases in the CVP Test Plan as well as for storing and reporting test
results in an appropriate manner to ensure test integrity and confidentiality.


------------------------------------
Objectives of the Dovetail Test Tool
------------------------------------

The scope and objectives of the CVP Program are described in the CVP Guidelines document authored and maintained
by the CVP committee which oversees governance and scope of the Program. Scope of testing is tied to an OPNFV
release and specified in an addendum to the CVP Guidelines document.

General objectives of the Dovetail tool are to provide automation of test setup and runs with minimal user
intervention. The tool should be easy to setup and configure as well as to run and report results. In addition
the tool should be self-contained with as few dependencies as possible. Any code dependencies should be documented
in the code as well as user instructions.

The following are non-objectives of the tools capabilities
	- Test API conformance
	- Test platform interoperability
	- Test performance (differed to Euphrates)
	- Test platform security (differed to Euphrates)


---------------------
Test Tool Assumptions
---------------------

	- The SUT is based on Open Stack
	- Assume that the SUT is running in a Pharos compliant "POD"
	- Tests must run in one or more of the "CVP scenarios" which are a subset of OPNFV release scenarios.
	- Each test case specifies which scenario/s will work with that test case and which features are required
	  to successfully run the test. For example HA is a feature that is included in many scenarios … the test
	  case however must state that HA is required to successfully pass that test case.
	- Every test case has a pass/fail (binary) result.
	- Each test case has an associated configuration file.


-------------------------------------------------------------------------
Dovetail Test Tool Requirements for Recording and Reporting Test  Results
-------------------------------------------------------------------------

	1. All test result are stored in persistent memory locally until they are either 1) successfully
	   transmitted 2) Tester hits "cancel test run".

	2. Each test run records
		a. Some platform identifier / metrics?
		b. Date of test run
		c. Name of entity doing testing (company doing self-testing or approved 3rd party test lab)
		d. Name of individual running the tests with contact details
		e. Physical location of SUT
		f. Total # tests run
		g. Total # tests passed
		h. Machine specs for each node (record as a POD descriptor)
		i. ?

	3. Each test case executed records
		a. Time test was run (start time, stop time)
		b. Test passed or failed
		c. Some info on why the test failed may be possible with some test cases
		d. Saves the Dovetail configuration file
		e. ?


---------------------------------------------------
Dovetail Test Tool Requirements for Executing Tests
---------------------------------------------------

	1. Requirements for testing Cloud capabilities and features
		- Relevant OPNFV feature/project
		- Relevant OPNFV scenario/s

	2. Requirements for testing VNF lifecycle management and scaling
		- Relevant OPNFV feature/project
		- Relevant OPNFV scenario/s

		○ VNF management
		○ Setup
		○ Instantiate
		○ Scale
		○ Tear down

	3. Requirements for testing Carrier network capabilities
		○ Relevant OPNFV feature/project
		○ Relevant OPNFV scenario/s

		- Virtual switching
			- IPV6
			- VxLAN / VLAN
	
	4. Requirements for testing Carrier grade features
		○ Relevant OPNFV feature/project
		○ Relevant OPNFV scenario/s

		○ High availability
		○ Resilience
		○ Fault management  / failure recovery
	
	5. Requirements for testing NFV Platform Security
		○ Relevant OPNFV feature/project
		○ Relevant OPNFV scenario/s

	6. Requirements for testing platform monitoring capabilities
		○ Relevant OPNFV feature/project
		○ Relevant OPNFV scenario/s




References
==========

.. _`"Pharos specification"`: https://opnfv.org/
.. _`OPNFV Glossary`: http://docs.opnfv.org/en/latest/glossary/index.html
