.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. SPDX-License-Identifier: CC-BY-4.0

.. _dovetail-releasenotes:

======================================================================
OPNFV Verification Program (OVP) 2020.r1 
======================================================================


OVP 2020.r1 Release
=====================

The OPNFV Verification Program (OVP) allows vendors and operators to obtain 'OPNFV Verified'
status based on an agreed upon set of compliance verification test cases that align to OPNFV
releases. The reference System under Test (SUT) is either the NFV components deployed in
accordance to CNTT requirements, where OVP 2020.r1 is based on the CNTT Baldy release, or a
VNF being on-boarded and orchestrated by the ONAP Frankfurt release. Participants of the
program can verify commercial or open source offerings against an OVP release. This implies
that the SUT used for verification has interfaces, components, functions, and behaviors that
align to the CNTT Reference Model, Reference Architecture, and ONAP deployments.

Approved test tools (OPNFV xTesting, ONAP VTP, and ONAP VVP)  work in conjunction with a web portal
interface dubbed the 'OVP web portal' to allow users to upload test results to a centralized community
repository. This facilitates user collaboration, result sharing, self-testing and community reviews.
It also serves as a hub for new participants to learn about the program and access key resources. The
link for these portals are at: `NFVI Verification Program <https://nfvi-verified.lfnetworking.org>`_ and
`VNF Verification Program <https://vnf-verified.lfnetworking.org>`_.

Use of the OVP web portal is open to all and only requires a valid Linux Foundation
ID to login. Users are welcome to use the portal to upload, inspect and share results in a private
manner. In order to submit results for official review, the first step is apply for acceptance
into the program with the participation form provided on the `OVP landing page`_.

NFVI Test Suites and Test Areas
-------------------------------

The OVP Infrastructure badge test requirements are defined within the CNTT RC1 documentation, with
traceability to the CNTT Reference Architecture and Reference Model documentation.   Testing is
is orchestrated by the OPNFV xTesting tool chain.

Test cases include a division into **'mandatory'** and **'optional'** in an overarching
categorization.

All the mandatory test cases are required to be executed with passing results for all inclusive
test cases for results to be reviewed and approved by the community made up of peer reviewers.
The optional test cases are not required to be executed for the official compliance verification
review in the OVP release. However, execution of these cases is encouraged, as some optional test
cases may become mandatory in future releases.

OPNFV Test Projects and Components
----------------------------------

The OPNFV test frameworks integrated into the xTesting framework that deliver test content are:

 - Functest (leverages OpenStack RefStack/Tempest projects in addition to supplying native test cases)

ONAP Test Projects and Components
---------------------------------

The ONAP test projects and components used with this OVP release to provide the test requirements
and test scripting are:

- VNFRQTS
- VNFSDK
- VVP

Acceptence and Marketing
------------------------

Upon successful community review of results for the program, the Linux Foundation Compliance &
Verification Committee (LFN CVC) on behalf of the Board of Directors can award a product 'OPNFV
Verified' status. Use of 'OPNFV Verified' Program Marks shall be awarded to the platform used
for compliance verification. The category label of 'Infrastructure' is used within the Program
Marks logo and limits the scope of this OVP release to a SUT consisting of NFVI and VIM components
using ETSI terminology. The release '2020.r1' corresponds to a reference SUT that aligns to the
CNTT Baldy and ONAP Frankfurt releases.

Organizations shall not use the Program Marks in any way that would associate it with any
individual or company logo or brand, beyond the association to the specific platform to which it
was awarded. While OpenStack RefStack interoperability and Tempest integration test cases are
executed as part of the OVP compliance & verification test suites, the OVP does not grant or
award OpenStack Marks in any fashion. 'OPNFV Verified' status does not assert readiness for
commercial deployment.

Please refer to the program governance guidelines and term & conditions documents for additional
details using the respective links:
* `Verification Program Page <https://www.lfnetworking.org/ovp/>`_
* `OVP Governance Guidelines <https://wiki.lfnetworking.org/download/attachments/8257540/LFN_CVP_Guidelines_1.1.0.docx>`_


Release Data
============

+--------------------------------------+---------------------------------------+
| **Project**                          | Dovetail                              |
|                                      |                                       |
+--------------------------------------+---------------------------------------+
| **Repo tag**                         | ovp-4.0.0                             |
|                                      |                                       |
+--------------------------------------+---------------------------------------+
| **Release designation**              | OPNFV Verification Program (OVP)      |
|                                      | 2020.r1                               |
+--------------------------------------+---------------------------------------+
| **Release date**                     | November 2020                         |
|                                      |                                       |
+--------------------------------------+---------------------------------------+
| **Purpose of the delivery**          | Support CNTT Baldy and ONAP Frankfurt |
|                                      | releases.                             |
+--------------------------------------+---------------------------------------+
| **Notes**                            | None                                  |
|                                      |                                       |
+--------------------------------------+---------------------------------------+


Deliverables
============

Software
--------

OPNFV Software
""""""""""""""

+-------------------------+-----------------------------------+----------------+
|  **Docker Container**   | **Docker Image**                  | **Tag**        |
+-------------------------+-----------------------------------+----------------+
|   dovetail              |    opnfv/dovetail                 |    ovp-3.0.0   |
+-------------------------+-----------------------------------+----------------+
|   functest              |    opnfv/functest-smoke           |    hunter      |
+-------------------------+-----------------------------------+----------------+
|   functest              |    opnfv/functest-healthcheck     |    hunter      |
+-------------------------+-----------------------------------+----------------+
|   functest              |    opnfv/functest-vnf             |    hunter      |
+-------------------------+-----------------------------------+----------------+
|   yardstick             |    opnfv/yardstick                |   opnfv-8.0.0  |
+-------------------------+-----------------------------------+----------------+
|   bottlenecks           |    opnfv/bottlenecks              |   8.0.1-latest |
+-------------------------+-----------------------------------+----------------+

**Docker images:**

- `Dovetail Docker images <https://hub.docker.com/r/opnfv/dovetail>`_
- `Functest-smoke Docker images <https://hub.docker.com/r/opnfv/functest-smoke/>`_
- `Functest-healthcheck  Docker images <https://hub.docker.com/r/opnfv/functest-healthcheck/>`_
- `Functest-vnf Docker images <https://hub.docker.com/r/opnfv/functest-vnf/>`_

ONAP Software
"""""""""""""

+-------------------------+----------------------------------------------------------------------------+
| **Item**                |  **Repo Link**                                                             |
+-------------------------+----------------------------------------------------------------------------+
| VTP/VNFSDK Test Scripts | `<https://gerrit.onap.org/r/admin/repos/vnfsdk/refrepo>`                   |
+-------------------------+----------------------------------------------------------------------------+
| VVP OVP Test Suite      | `<https://github.com/onap/vvp-test-engine/tree/frankfurt/ovp_testsuite>`   |
+-------------------------+----------------------------------------------------------------------------+

Documents
---------

- `System Preparation Guide <https://opnfv-dovetail.readthedocs.io/en/stable-hunter/testing/user/systempreparation/index.html>`_

- `NFVI User Guide <https://opnfv-dovetail.readthedocs.io/en/stable-hunter/testing/user/userguide/testing_guide.html>`_

- `VNF User Guide: <https://opnfv-dovetail.readthedocs.io/en/stable-hunter/testing/user/userguide/vnf_test_guide.html>`_

- `OVP NFVI Test Specifications <https://opnfv-dovetail.readthedocs.io/en/stable-hunter/testing/user/testspecification/index.html>`_

- `ONAP VNF Test Specifications <https://docs.onap.org/en/elalto/submodules/vnfrqts/testcases.git/docs/index.html>`_

- `Dovetail CLI Reference <https://opnfv-dovetail.readthedocs.io/en/stable-hunter/testing/user/userguide/cli_reference.html>`_

- `Dovetail RESTful API <https://opnfv-dovetail.readthedocs.io/en/stable-hunter/testing/user/userguide/api_testing_guide.html>`_

- `OVP Workflow <https://opnfv-dovetail.readthedocs.io/en/stable-hunter/testing/user/certificationworkflow/index.html>`_

- `OVP Reviewer Guide <https://opnfv-dovetail.readthedocs.io/en/stable-hunter/testing/user/reviewerguide/index.html>`_

Known Restrictions/Issues
================================

Please refer to the OPNFV and ONAP JIRA for known issues with each applicable project:

- `<https://jira.opnfv.org/projects/DOVETAIL>`_
- `<https://jira.onap.org/projects/VVP>`_
- `<https://jira.onap.org/projects/VNFSDK>`_


Useful Links
============

 - `NFVI Web Portal <https://nfvi-verified.lfnetworking.org>`_
 - `VNF Web Portal <https://vnf-verified.lfnetworking.org>`_
 - Dovetail IRC Channel: #opnfv-dovetail

.. References
.. _`OVP landing page`: https://www.lfnetworking.org/ovp/