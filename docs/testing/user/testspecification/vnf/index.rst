.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Ericsson AB

======================
VNF test specification
======================

.. toctree::
   :maxdepth: 2

Scope
=====

The VNF test area evaluates basic NFV capabilities of the system under test.
These capabilities include creating a small number of virtual machines,
establishing the SUT VNF, VNFs which are going to support the test activities
and an Orchestrator as well as verifying the proper behavior of the basic VNF.


References
==========

This test area references the following specifications and guides:

- Functest repo for detailed description of the vEPC testcase

  - https://github.com/opnfv/functest/blob/master/docs/testing/user/userguide/test_details.rst#juju_epc

- Functest repo for detailed description of the vIMS testcase

  - https://github.com/opnfv/functest/blob/master/docs/testing/user/userguide/test_details.rst#cloudify_ims

- 3GPP LTE

  - https://www.3gpp.org/technologies/keywords-acronyms/98-lte

- ETSI -  TS 24.301

  - https://www.etsi.org/deliver/etsi_ts/124300_124399/124301/10.03.00_60/ts_124301v100300p.pdf

- Cloudify clearwater: opnfv-cloudify-clearwater [1]

  - https://github.com/Orange-OpenSource/opnfv-cloudify-clearwater


Definitions and abbreviations
=============================

The following terms and abbreviations are used in conjunction with this test
area

- 3GPP - 3rd Generation Partnership Project
- EPC - Evolved Packet Core
- ETSI - European Telecommunications Standards Institute
- IMS - IP Multimedia Core Network Subsystem
- LTE - Long Term Evolution
- NFV - Network functions virtualization
- OAI - Open Air Interface
- TS - Technical Specifications
- VM - Virtual machine
- VNF - Virtual Network Function



System Under Test (SUT)
=======================

The system under test is assumed to be the VNF and VIM in operation on a
Pharos compliant infrastructure.


Test Area Structure
===================

The test area is structured in two separate tests which are executed
sequentially. The order of the tests is arbitrary as there are no dependencies
across the tests. Specifically, every test performs clean-up operations which
return the system to the same state as before the test.


Test Descriptions
=================

----------------------------------------------------------------
Test Case 1 - vEPC
----------------------------------------------------------------

Short name
----------

dovetail.vnf.vepc


Use case specification
----------------------

The Evolved Packet Core (EPC) is the main component of the System Architecture
Evolution (SAE) which forms the core of the 3GPP LTE specification.

vEPC has been integrated in Functest to demonstrate the capability to deploy
a complex mobility-specific NFV scenario on the OPNFV platform. The OAI EPC
supports most of the essential functions defined by the 3GPP Technical Specs;
hence the successful execution of functional tests on the OAI EPC provides a
good endorsement of the underlying NFV platform.


Test preconditions
------------------

At least one compute node is available. No further pre-configuration needed.


Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Methodology for verifying connectivity
''''''''''''''''''''''''''''''''''''''

This integration also includes ABot, a Test Orchestration system that enables
test scenarios to be defined in high-level DSL. ABot is also deployed as a VM
on the OPNFV platform; and this provides an example of the automation driver
and the Test VNF being both deployed as separate VNFs on the underlying OPNFV
platform.


Test execution
''''''''''''''
* Test action 1: Deploy Juju controller (VNF Manager) using Bootstrap command.
* Test action 2: Deploy ABot (Orchestrator) and OAI EPC as Juju charms.
  Configuration of ABot and OAI EPC components is handled through built-in Juju
  relations.
* Test action 3: Execution of ABot feature files triggered by Juju actions.
  This executes a suite of LTE signalling tests on the OAI EPC.
* Test action 4: ABot test results are parsed accordingly.
* Test action 5: The deployed VMs are deleted.


Pass / fail criteria
''''''''''''''''''''

The VNF Manager (juju) should be deployed successfully

Test executor (ABot), test Orchestration system is deployed and enables test
scenarios to be defined in high-level DSL

VMs which are act as VNFs (including the VNF that is the SUT for test case) are
following the 3GPP technical specifications accordingly.


Post conditions
---------------

The clean-up operations are run.

----------------------------------------------------------------
Test Case 2 - vIMS
----------------------------------------------------------------

Short name
----------

dovetail.vnf.vims

Use case specification
----------------------

The IP Multimedia Subsystem or IP Multimedia Core Network Subsystem (IMS) is
an architectural framework for delivering IP multimedia services.

vIMS test case is integrated to demonstrate the capability to deploy a
relatively complex NFV scenario on top of the OPNFV infrastructure.

Example of a real VNF deployment to show the NFV capabilities of the platform.
The IP Multimedia Subsytem is a typical Telco test case, referenced by ETSI.
It provides a fully functional VoIP System.

Test preconditions
------------------

Certain ubuntu server and cloudify images version refer to dovetail testing user guide.

At least 30G RAMs and 50 vcpu cores required.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

vIMS has been integrated in Functest to demonstrate the capability to deploy
a relatively complex NFV scenario on the OPNFV platform. The deployment of a
complete functional VNF allows the test of most of the essential functions
needed for a NFV platform.


Test execution
''''''''''''''
* Test action 1: Deploy a VNF orchestrator (Cloudify).
* Test action 2: Deploy a Clearwater vIMS (IP Multimedia Subsystem) VNF from
  this orchestrator based on a TOSCA blueprint defined in repository of
  opnfv-cloudify-clearwater [1].
* Test action 3: Run suite of signaling tests on top of this VNF
* Test action 4: Collect test results.
* Test action 5: The deployed VMs are deleted.


Pass / fail criteria
''''''''''''''''''''

The VNF orchestrator (Cloudify) should be deployed successfully.

The Clearwater vIMS (IP Multimedia Subsystem) VNF from this orchestrator
should be deployed successfully.

The suite of signaling tests on top of vIMS should be run successfully.

The test scenarios on the NFV platform should be executed successfully following
the ETSI standards accordingly.


Post conditions
---------------

All resources created during the test run have been cleaned-up
