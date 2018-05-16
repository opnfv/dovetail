.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. SPDX-License-Identifier: CC-BY-4.0

=======
License
=======

OPNFV Danube release note for Dovetail Docs
are licensed under a Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this.
If not, see <http://creativecommons.org/licenses/by/4.0/>.

==================================================================
OPNFV Verified Program (OVP) 2018.01 / Dovetail 1.0.0 Release Note
==================================================================

Abstract
========

This document describes the release note of the OPNFV Verified Program and the Dovetail project.


Version History
===============

+------------+----------+--------------------------+
| **Date**   | **Ver.** | **Comment**              |
|            |          |                          |
+------------+----------+--------------------------+
| 2018-01-21 | 1.0.0    | Dovetail for OVP 2018.01 |
|            |          | Danube release           |
+------------+----------+--------------------------+

OPNFV Danube Release
====================

The OPNFV Verified Program (OVP) allows vendors and operators to obtain 'OPNFV Verified'
status based on an agreed upon set of compliance verification test cases that align to OPNFV
releases. The reference System under Test (SUT) are the NFV components deployed by the OPNFV
installers for a given release, where OVP 2018.01 is based on the Danube release. Participants
of the program can verify commercial or open source offerings against an OVP release. This implies
that the SUT used for verification has interfaces, components, functions and behaviors that align
to OPNFV installer integrations.

Dovetail is the overall framework used to execute tests and collect results for OVP. Dovetail does
not deliver test content directly. Rather, test content is developed in other OPNFV test frameworks
such as Functest and upstream test communities such as OpenStack's RefStack/Tempest projects.
Dovetail leverages this upstream test content and provides a common set of test platform services
for the OVP.

Dovetail works in conjunction with a web portal interface dubbed the 'OVP web portal' to allow
users to upload test results to a centralized community repository. This facilitates user
collaboration, result sharing, self-testing and community reviews. It also serves as a hub for
new participants to learn about the program and access key resources. The link for this portal
is at:

 * https://verified.opnfv.org

Use of the OVP web portal is open to all and only requires a valid Linux Foundation or OpenStack
ID to login. Users are welcome to use the portal to upload, inspect and share results in a private
manner. In order to submit results for official review, the first step is apply for acceptance
into the program with the participation form provided in the link:

 * https://na3.docusign.net/Member/PowerFormSigning.aspx?PowerFormId=579ac00d-0a1f-4db3-82ea-ddd977769a60

Test Suites & Test Areas
------------------------

OVP/Dovetail groups test cases into test suites and test areas. Test suites are currently a basic
categorization around releases for the most part. Executing the test suite 'ovp.1.0.0' without
further specification will run all the test cases in the OVP 2018.01 release. Test suites are
divided into test areas that can be executed separately.

Test areas include a division into 'mandatory' and 'optional' in an overarching categorization.
The mandatory test area is further subdivided into the following three test areas, which can
be executed independently:

 * osinterop
 * vping
 * ha

The optional test area is further subdivided into the following three test areas:

 * ipv6
 * tempest
 * sdnvpn

All the mandatory test areas are required to be executed with passing results for all inclusive
test cases for results to be reviewed and approved by the community made up of peer reviewers.
The optional test areas are not required to be executed for the official compliance verification
review in the OVP 2018.01 release. However, execution of these areas is encouraged, as some
optional test areas may become mandatory in future releases.

Test Cases and Sub Test Cases
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Each test area consists of multiple test cases where each test case can be a single test or
broken down into sub test cases. A listing of test cases with the number of sub test cases noted
in parenthesis is shown below for the OVP 2018.01 release.

**Mandatory**
 * dovetail.osinterop.tc001 (205)
 * dovetail.vping.tc001 (1)
 * dovetail.vping.tc002 (1)
 * dovetail.ha.tc001 (1)
 * dovetail.ha.tc002 (1)
 * dovetail.ha.tc003 (1)
 * dovetail.ha.tc004 (1)
 * dovetail.ha.tc005 (1)
 * dovetail.ha.tc006 (1)
 * dovetail.ha.tc007 (1)
 * dovetail.ha.tc008 (1)

There are a total of 215 mandatory test cases (osinterop: 205, vping: 2, ha: 8).

**Optional**
 * dovetail.ipv6.tc001 (3)
 * dovetail.ipv6.tc002 (1)
 * dovetail.ipv6.tc003 (1)
 * dovetail.ipv6.tc004 (2)
 * dovetail.ipv6.tc005 (2)
 * dovetail.ipv6.tc006 (1)
 * dovetail.ipv6.tc007 (1)
 * dovetail.ipv6.tc008 (1)
 * dovetail.ipv6.tc009 (1)
 * dovetail.ipv6.tc010 (1)
 * dovetail.ipv6.tc011 (1)
 * dovetail.ipv6.tc012 (1)
 * dovetail.ipv6.tc013 (1)
 * dovetail.ipv6.tc014 (1)
 * dovetail.ipv6.tc015 (1)
 * dovetail.ipv6.tc016 (1)
 * dovetail.ipv6.tc017 (1)
 * dovetail.ipv6.tc018 (1)
 * dovetail.ipv6.tc019 (1)
 * dovetail.ipv6.tc020 (1)
 * dovetail.ipv6.tc021 (1)
 * dovetail.ipv6.tc022 (1)
 * dovetail.ipv6.tc023 (1)
 * dovetail.ipv6.tc024 (1)
 * dovetail.ipv6.tc025 (1)
 * dovetail.tempest.tc001 (1)
 * dovetail.tempest.tc002 (6)
 * dovetail.tempest.tc003 (5)
 * dovetail.tempest.tc004 (12)
 * dovetail.tempest.tc005 (6)
 * dovetail.sdnvpn.tc001 (1)
 * dovetail.sdnvpn.tc002 (1)
 * dovetail.sdnvpn.tc004 (1)
 * dovetail.sdnvpn.tc008 (1)

There are a total of 63 optional test cases (ipv6: 29, tempest: 30, sdnvpn: 4).

Further details on test area breakdown with expanded test and sub test case names is available at:

 * http://docs.opnfv.org/en/stable-danube/submodules/dovetail/docs/testing/developer/testscope/index.html

OPNFV Test Projects and Components
----------------------------------

The OPNFV test frameworks integrated into the Dovetail framework that deliver test content are:

 * Functest (leverages OpenStack RefStack/Tempest projects in addition to supplying native test cases)
 * Yardstick

Other upstream components integrated into the Dovetail framework are:

 * TestAPI
 * MongoDB

The above components are part of the OPNFV test collection framework. Further information on how
this framework is used to collect test results can be found at:

 * http://docs.opnfv.org/en/stable-danube/submodules/functest/docs/testing/developer/devguide/#test-collection-framework

The test frameworks and components above are packaged as Docker containers for Dovetail to employ.
Dovetail creates OVP-specific containers for Functest and TestAPI, while it uses the default
Yardstick Danube container. Additionally, a generic container version of MongoDB is used.
Installation instructions for Dovetail and its dependent containers can be found in the user
guide at:

 * http://docs.opnfv.org/en/stable-danube/submodules/dovetail/docs/testing/user/userguide/testing_guide.html

Acceptence and Marketing
------------------------

Upon successful community review of results for OVP 2018.01, the OPNFV C&C Committee on behalf of
the Board of Directors can award a product 'OPNFV Verified' status. Use of 'OPNFV Verified'
Program Marks shall be awarded to the platform used for compliance verification. The category label
of 'Infrastructure' is used within the Program Marks logo and limits the scope of this OVP release
to a SUT consisting of NFVI and VIM components using ETSI terminology. It does not provide
compliance verification for specific VNFs in any fashion. The date '2018.01' corresponds to a
reference SUT that aligns to the OPNFV Danube release and currently aligns to the Dovetail
framework version 1.0.0.

Organizations shall not use the Program Marks in any way that would associate it with any
individual or company logo or brand, beyond the association to the specific platform to which it
was awarded. While OpenStack RefStack interoperability and Tempest integration test cases are
executed as part of the OVP 2018.01 compliance verification test suites, the OVP does not grant or
award OpenStack Marks in any fashion. 'OPNFV Verified' status does not assert readiness for
commercial deployment.

Please refer to the program governance guidelines and term & conditions documents for additional
details using the respective links:

 * https://www.opnfv.org/wp-content/uploads/sites/12/2018/01/OVP-Governance-Guidelines-1.0.1-012218.pdf
 * https://www.opnfv.org/wp-content/uploads/sites/12/2018/01/OVP-Terms-and-Conditions-011918.pdf

Release Data
============

+--------------------------------------+---------------------------------------+
| **Project**                          | Dovetail                              |
|                                      |                                       |
+--------------------------------------+---------------------------------------+
| **Repo tag**                         | ovp.1.0.0                             |
|                                      |                                       |
+--------------------------------------+---------------------------------------+
| **Release designation**              | OPNFV Verified Program (OVP)          |
|                                      | 2018.01 (Danube)                      |
+--------------------------------------+---------------------------------------+
| **Release date**                     | January 21st 2018                      |
|                                      |                                       |
+--------------------------------------+---------------------------------------+
| **Purpose of the delivery**          | Support OVP 2018.01 release with      |
|                                      | OPNFV Danube release as reference SUT |
+--------------------------------------+---------------------------------------+

Deliverables
============

Software
--------

+-----------------+----------------------+-------------+
|  Docker         | Docker Image         | Tag         |
|  Container      |                      |             |
+=================+======================+=============+
| dovetail        |  opnfv/dovetail      |  ovp.1.0.0  |
+-----------------+----------------------+-------------+
| functest        |  opnfv/functest      |  ovp.1.0.0  |
+-----------------+----------------------+-------------+
| yardstick       |  opnfv/yardstick     |  danube.3.2 |
+-----------------+----------------------+-------------+
| testapi         |  opnfv/testapi       |  ovp.1.0.0  |
+-----------------+----------------------+-------------+
| mongo           |  mongo               |  3.2.1      |
+-----------------+----------------------+-------------+


 - Dovetail Docker images: https://hub.docker.com/r/opnfv/dovetail

 - Functest Docker images: https://hub.docker.com/r/opnfv/functest

 - Yardstick Docker images: https://hub.docker.com/r/opnfv/yardstick

 - TestAPI Docker images: https://hub.docker.com/r/opnfv/testapi

 - MongoDB Docker images: https://hub.docker.com/r/mongo


Documents
---------

 - System Preparation Guide: http://docs.opnfv.org/en/stable-danube/submodules/dovetail/docs/testing/user/systempreparation/index.html

 - User Guide: http://docs.opnfv.org/en/stable-danube/submodules/dovetail/docs/testing/user/userguide/testing_guide.html

 - Test Specifications: http://docs.opnfv.org/en/stable-danube/submodules/dovetail/docs/testing/user/testspecification/index.html

 - Dovetail CLI Reference: http://docs.opnfv.org/en/stable-danube/submodules/dovetail/docs/testing/user/userguide/cli_reference.html

 - Process Workflow: http://docs.opnfv.org/en/stable-danube/submodules/dovetail/docs/testing/user/certificationworkflow/index.html

 - Reviewer Guide: http://docs.opnfv.org/en/stable-danube/submodules/dovetail/docs/testing/user/reviewerguide/index.html


Version Change
==============

This is the first major release of OVP/Dovetail. Please refer to the link below for minor
version changes during pre-release and beta phases.

 * https://wiki.opnfv.org/display/dovetail/Running+history+for+the+dovetail+tool

Testing with OPNFV Danube Installers
====================================

OVP 2018.01 and Dovetail 1.0.0 are known to be have been tested with the following OPNFV
Danube installer versions.

+-----------------+----------------------+
|   Installer     |      Version         |
+=================+======================+
|   Apex          |      danube.3.1      |
+-----------------+----------------------+
|   Compass       |      danube.3.1      |
+-----------------+----------------------+
|   Fuel          |      danube.3.0      |
+-----------------+----------------------+


Danube Known Restrictions/Issues
==================================

Please refer to the following link for known issues with the Dovetail Danube release:

 * https://wiki.opnfv.org/display/dovetail/Running+history+for+the+dovetail+tool#Runninghistoryforthedovetailtool-4.KnownIssuesList

Open JIRA Tickets
=================

+------------------+-----------------------------------------------+
|   JIRA           |         Description                           |
+==================+===============================================+
|                  |                                               |
|                  |                                               |
+------------------+-----------------------------------------------+

All blocking tickets have been fixed.


Useful Links
============

 - OVP Web Portal: https://verified.opnfv.org

 - Wiki Project Page: https://wiki.opnfv.org/display/dovetail

 - Dovetail Repo: https://git.opnfv.org/dovetail/

 - Dovetail CI dashboard: https://build.opnfv.org/ci/view/dovetail/

 - JIRA dashboard: https://jira.opnfv.org/secure/RapidBoard.jspa?rapidView=149

 - Dovetail IRC Channel: #opnfv-dovetail

 - Dovetail Test Configuration: https://git.opnfv.org/dovetail/tree/dovetail/compliance/ovp.1.0.0.yml
