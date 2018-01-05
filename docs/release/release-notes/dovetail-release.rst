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
| 2018-01-08 | 1.0.0    | Dovetail for OVP 2018.01 |
|            |          | Danube release           |
+------------+----------+--------------------------+

OPNFV Danube Release
====================

The OPNFV Verified Program (OVP) allows cloud vendors and operators to obtain 'verified
marks' based on an agreed upon set of conformance/compliance test cases that align to OPNFV
releases. The reference System under Test (SUT) are the OPNFV installers for a given release.
Participants of the program can verify commercial or open-source systems against an OVP
release. This implies that the SUT used for official verification has interfaces, components,
functions and behaviors that align to OPNFV installer integrations.

Dovetail is the overall framework used to execute tests and collect results for OVP. Dovetail does
not deliver test content directly. Rather test content is developed in other OPNFV test projects
and upstream test communities such as OpenStack's refstack/tempest projects. Dovetail leverages
this upstream test content and provides a common set of test platform services for OVP.

Dovetail works in conjunction with a web portal interface dubbed the 'OVP web portal' to allow
users to upload test results to a centralized community repository. This facilitates user
collaboration, result sharing, self-testing and community reviews. It also serves as a hub for
new participants to learn about the program and access key resources. The link for this portal:

https://verified.opnfv.org

Use of the OVP web portal is open to all and only requires a valid Linux Foundation or OpenStack
ID to login. Users are welcome to use the portal to upload, inspect and share results in a private
manner. In order to submit results for official review, the first step is apply for acceptance
into the program with the application form provided in this link:

<Online application form here>

Test Suites & Test Areas
------------------------

OVP/Dovetail groups test cases into test suites and test areas. Test suites are currently a basic
categorization around releases for the most part. Executing the test suite 'ovp.1.0.0' without
further specification will run all the test cases in the OVP 2018.01 release. Test suites are
divided into test areas that can be executed separately.

Test areas include a division into 'mandatory' and 'optional' in an overarching categorization.
The mandatory test area is further subdivided into the following three test areas, which can
be executed independantly:

 * osinterop
 * ha
 * vping

The optional test area is further subdivided into the following three test areas:
 
 * ipv6
 * tempest
 * sdnvpn

All the mandatory test areas are required to be executed with passing results for all inclusive
test cases for results to be reviewed and approved by the community made up of peer reviewers. 

OPNFV Test Projects
-------------------

The OPNFV projects integrated into Dovetail framework are:

 * Functest
 * Yardstick
 * Testapi (not utilized for test content)

These test projects are packaged as Docker containers for Dovetail to employ. Dovetail creates
OVP-specific containers for Functest and Testapi, while it uses a default container to 
leverage Yardstick. Additionally, a generic container version of mongodb is also used.
Installation instructions for Dovetail and its dependent containers can be found in the user
guide at:

http://docs.opnfv.org/en/stable-danube/submodules/dovetail/docs/testing/user/userguide/testing_guide.html

Acceptence and Marketing
------------------------

Upon a successful community review of results for OVP 2018.01, the use of an 'OPNFV Verified'
marketing logo and associated text will be granted. The category label of 'Infrastructure' is
used within the logo. This label limits the scope of this OVP release to an SUT that
comprises a NFVi and VIM using ETSI terminology. It does not certify specific VNFs in any fashion.
The date 2018.01 corresponds to a reference SUT that aligns to the OPNFV Danube release of
installers and currently aligns to Dovetail version 1.0.0. 

<More detail TBA here>

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
| **Release date**                     | January 8th 2018                      |
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

 - Mongo Docker images: https://hub.docker.com/r/mongo 


Documents
---------

 - System Preparation Guide: http://docs.opnfv.org/en/stable-danube/submodules/dovetail/docs/testing/user/systempreparation/index.html

 - User Guide: http://docs.opnfv.org/en/stable-danube/submodules/dovetail/docs/testing/user/userguide/testing_guide.html

 - Test Specifications: http://docs.opnfv.org/en/stable-danube/submodules/dovetail/docs/testing/user/testspecification/index.html
 
 - Process Workflow: http://docs.opnfv.org/en/stable-danube/submodules/dovetail/docs/testing/user/certificationworkflow/index.html

 - Reviewer Guide: http://docs.opnfv.org/en/stable-danube/submodules/dovetail/docs/testing/user/reviewerguide/index.html



Version change
==============


- This is the first major release of OVP/Dovetail. Please refer to the link below for minor
version changes during pre-release and beta phases.

https://wiki.opnfv.org/display/dovetail/Running+history+for+the+dovetail+tool

Reference SUT Installer Test Matrix
===================================

For OPNFV Danube installers, Dovetail was tested with the following versions:
<Discuss whether we should include this section in Dovetail meeting>

Danube Known Restrictions/Issues
==================================

Please refer to the following link for known issues with the Dovetail Danube release:

https://wiki.opnfv.org/display/dovetail/Running+history+for+the+dovetail+tool#Runninghistoryforthedovetailtool-4.KnownIssuesList

Open JIRA tickets
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

 - Dovetail test configuration: https://git.opnfv.org/dovetail/tree/dovetail/compliance/ovp.1.0.0.yml
