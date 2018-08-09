.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. SPDX-License-Identifier: CC-BY-4.0

=======
License
=======

OPNFV Fraser release note for Dovetail Docs
are licensed under a Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this.
If not, see <http://creativecommons.org/licenses/by/4.0/>.

==================================================================
OPNFV Verified Program (OVP) 2018.08 / Dovetail 1.0.0 Release Note
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
| 2018-08-09 | 2.0.0    | Dovetail for OVP 2018.08 |
|            |          | Fraser release           |
+------------+----------+--------------------------+


OPNFV Danube Release
====================

The OPNFV Verified Program (OVP) allows vendors and operators to obtain 'OPNFV Verified'
status based on an agreed upon set of compliance verification test cases that align to OPNFV
releases. The reference System under Test (SUT) are the NFV components deployed by the OPNFV
installers for a given release, where OVP 2018.08 is based on the Fraser release. Participants
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
is at: `OPNFV Verified Program <https://verified.opnfv.org>`_.

Use of the OVP web portal is open to all and only requires a valid Linux Foundation or OpenStack
ID to login. Users are welcome to use the portal to upload, inspect and share results in a private
manner. In order to submit results for official review, the first step is apply for acceptance
into the program with the participation form provided in the link: `OPNFV Verified Program Participation Form <https://na3.docusign.net/Member/PowerFormSigning.aspx?PowerFormId=579ac00d-0a1f-4db3-82ea-ddd977769a60>`_

Test Suites & Test Areas
------------------------

OVP/Dovetail groups test cases into test suites and test areas. Test suites are currently a basic
categorization around releases for the most part. Executing the test suite 'ovp.2.0.0' without
further specification will run all the test cases in the OVP 2018.08 release. Test suites are
divided into test areas that can be executed separately.

Test areas include a division into **'mandatory'** and **'optional'** in an overarching categorization.
The mandatory test area is further subdivided into the following three test areas, which can
be executed independently:

Mandatory test area
 - Vping
 - Stress
 - Tempest Smoke
 - Patrole RBAC
 - High-availability

Optional test area
    - VNF
    - OPNFV SNAPS smoke
    - High-availability
    - Tempest (optional tests)
    - BGPVPN

All the mandatory test areas are required to be executed with passing results for all inclusive
test cases for results to be reviewed and approved by the community made up of peer reviewers.
The optional test areas are not required to be executed for the official compliance verification
review in the OVP 2018.08 release. However, execution of these areas is encouraged, as some
optional test areas may become mandatory in future releases.

Test Cases and Sub Test Cases
-----------------------------

Each test area consists of multiple test cases where each test case can be a single test or
broken down into sub test cases. A listing of test cases with the number of sub test cases noted
in parenthesis is shown below for the OVP 2018.08 release.

**Mandatory**

- dovetail.vping.userdata (1)
- dovetail.vping.ssh (1)
- dovetail.stress.ping
- dovetail.tempest.osinterop (204)
- dovetail.tempest.compute (12)
- dovetail.tempest.identity_v2 (5)
- dovetail.tempest.identity_v3 (11)
- dovetail.tempest.image (2)
- dovetail.tempest.network_api (14)
- dovetail.tempest.volume (2)
- dovetail.tempest.neutron_trunk_ports (43)
- dovetail.tempest.ipv6_api (21)
- dovetail.security.patrole (119)
- dovetail.ha.nova_api (1)
- dovetail.ha.neutron_server (1)
- dovetail.ha.keystone (1)
- dovetail.ha.glance_api (1)
- dovetail.ha.cinder_api (1)
- dovetail.ha.cpu_load (1)
- dovetail.ha.disk_load (1)
- dovetail.ha.haproxy (1)
- dovetail.ha.rabbitmq (1)
- dovetail.ha.database  (1)


There are a total of 445 mandatory test cases.

**Optional**

- functest.vnf.vims (1)
- functest.vnf.vepc (1)
- functest.snaps.smoke  (1)
- yardstick.ha.neutron_l3_agent  (1)
- yardstick.ha.controller_restart (1)
- functest.tempest.ipv6_scenario (8)
- functest.tempest.multi_node_scheduling (6)
- functest.tempest.network_security (6)
- functest.tempest.vm_lifecycle (12)
- functest.tempest.network_scenario (5)
- functest.tempest.bgpvpn (15)
- functest.bgpvpn.subnet_connectivity (1)
- functest.bgpvpn.tenant_separation (1)
- functest.bgpvpn.router_association (1)
- functest.bgpvpn.router_association_floating_ip (1)


There are a total of 61 optional test cases.

Further details on test area breakdown with expanded test and sub test case names is available at:
`Compliance and Verification program accepted test cases <https://docs.opnfv.org/en/stable-fraser/submodules/dovetail/docs/testing/developer/testscope/index.html>`_

OPNFV Test Projects and Components
----------------------------------

The OPNFV test frameworks integrated into the Dovetail framework that deliver test content are:

 * Functest (leverages OpenStack RefStack/Tempest projects in addition to supplying native test cases)
 * Yardstick

Other upstream components integrated into the Dovetail framework are:

 * TestAPI
 * MongoDB

.. The above components are part of the OPNFV test collection framework. Further information on how
.. this framework is used to collect test results can be found at:

.. http://docs.opnfv.org/en/stable-danube/submodules/functest/docs/testing/developer/devguide/#test-collection-framework

The test frameworks and components above are packaged as Docker containers for Dovetail to employ.
Dovetail creates OVP-specific containers for Functest and TestAPI, while it uses the default
Yardstick Danube container. Additionally, a generic container version of MongoDB is used.
Installation instructions for Dovetail and its dependent containers can be found in the user
guide at `Dovetail Testing Guide <https://docs.opnfv.org/en/stable-fraser/submodules/dovetail/docs/testing/user/userguide/testing_guide.html>`_.

Acceptence and Marketing
------------------------

Upon successful community review of results for OVP 2018.08, the OPNFV C&C Committee on behalf of
the Board of Directors can award a product 'OPNFV Verified' status. Use of 'OPNFV Verified'
Program Marks shall be awarded to the platform used for compliance verification. The category label
of 'Infrastructure' is used within the Program Marks logo and limits the scope of this OVP release
to a SUT consisting of NFVI and VIM components using ETSI terminology. It does not provide
compliance verification for specific VNFs in any fashion. The date '2018.08' corresponds to a
reference SUT that aligns to the OPNFV Fraser release and currently aligns to the Dovetail
framework version 2.0.0.

Organizations shall not use the Program Marks in any way that would associate it with any
individual or company logo or brand, beyond the association to the specific platform to which it
was awarded. While OpenStack RefStack interoperability and Tempest integration test cases are
executed as part of the OVP 2018.08 compliance verification test suites, the OVP does not grant or
award OpenStack Marks in any fashion. 'OPNFV Verified' status does not assert readiness for
commercial deployment.

Please refer to the program governance guidelines and term & conditions documents for additional
details using the respective links:

* `OVP Governance Guidelines <https://www.opnfv.org/wp-content/uploads/sites/12/2018/01/OVP-Governance-Guidelines-1.0.1-012218.pdf>`_
* `OVP Terms and Conditions <https://www.opnfv.org/wp-content/uploads/sites/12/2018/01/OVP-Terms-and-Conditions-011918.pdf>`_

Release Data
============

+--------------------------------------+---------------------------------------+
| **Project**                          | Dovetail                              |
|                                      |                                       |
+--------------------------------------+---------------------------------------+
| **Repo tag**                         | ovp.2.0.0                             |
|                                      |                                       |
+--------------------------------------+---------------------------------------+
| **Release designation**              | OPNFV Verified Program (OVP)          |
|                                      | 2018.08 (Fraser)                      |
+--------------------------------------+---------------------------------------+
| **Release date**                     | August xxxx 2018                      |
|                                      |                                       |
+--------------------------------------+---------------------------------------+
| **Purpose of the delivery**          | Support OVP 2018.08 release with      |
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
| dovetail        |  opnfv/dovetail      |  ovp.2.0.0  |
+-----------------+----------------------+-------------+
| functest        |  opnfv/functest      |  fraser     |
+-----------------+----------------------+-------------+
| yardstick       |  opnfv/yardstick     |  stable     |
+-----------------+----------------------+-------------+
| testapi         |  opnfv/testapi       |  ovp.2.0.0  |
+-----------------+----------------------+-------------+
| mongo           |  mongo               |  3.2.1      |
+-----------------+----------------------+-------------+

Docker images:

- `Dovetail Docker images <https://hub.docker.com/r/opnfv/dovetail>`_
- `Functest Docker images <https://hub.docker.com/r/opnfv/functest>`_
- `Yardstick Docker images <https://hub.docker.com/r/opnfv/yardstick>`_
- `TestAPI Docker images <https://hub.docker.com/r/opnfv/testapi>`_
- `MongoDB Docker images <https://hub.docker.com/_/mongo/>`_


Documents
---------

- `System Preparation Guide <http://docs.opnfv.org/en/stable-fraser/submodules/dovetail/docs/testing/user/systempreparation/index.html>`_

- `User Guide <http://docs.opnfv.org/en/stable-fraser/submodules/dovetail/docs/testing/user/userguide/testing_guide.html>`_

- `OPV Test Specifications <http://docs.opnfv.org/en/stable-fraser/submodules/dovetail/docs/testing/user/testspecification/index.html>`_

- `Dovetail CLI Reference <http://docs.opnfv.org/en/stable-fraser/submodules/dovetail/docs/testing/user/userguide/cli_reference.html>`_

- `OPV Workflow <http://docs.opnfv.org/en/stable-fraser/submodules/dovetail/docs/testing/user/certificationworkflow/index.html>`_

- `OPV Reviewer Guide <http://docs.opnfv.org/en/stable-fraser/submodules/dovetail/docs/testing/user/reviewerguide/index.html>`_


.. Version Change
.. ==============

.. This is the first major release of OVP/Dovetail. Please refer to the link below for minor
.. version changes during pre-release and beta phases.

..  * https://wiki.opnfv.org/display/dovetail/Running+history+for+the+dovetail+tool

Testing with OPNFV Fraser Installers ????????
====================================

OVP 2018.08 and Dovetail 2.0.0 are known to be have been tested with the following OPNFV
Fraser installer versions.

+-----------------+----------------------+
|   Installer     |      Version         |
+=================+======================+
|   Apex          |      fraser.x.x      |
+-----------------+----------------------+
|   Compass       |      fraser.x.x      |
+-----------------+----------------------+
|   Fuel          |      fraser.x.x      |
+-----------------+----------------------+


Fraser Known Restrictions/Issues ?????????
==================================

Please refer to the following link for known issues with the Dovetail Fraser release:

.. https://wiki.opnfv.org/display/dovetail/Running+history+for+the+dovetail+tool#Runninghistoryforthedovetailtool-4.KnownIssuesList

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

 - `OVP Web Portal <https://verified.opnfv.org>`_

 - `Wiki Project Page <https://wiki.opnfv.org/display/dovetail>`_

 - `Dovetail Repo <https://git.opnfv.org/dovetail/>`_

 - `Dovetail CI dashboard <https://build.opnfv.org/ci/view/dovetail/>`_

 - `JIRA dashboard <https://jira.opnfv.org/secure/RapidBoard.jspa?rapidView=149>`_

 - Dovetail IRC Channel: #opnfv-dovetail

 - `Dovetail Test Configuration <https://git.opnfv.org/dovetail/tree/dovetail/compliance/ovp.1.0.0.yml>`_
