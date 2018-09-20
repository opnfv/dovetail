.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. SPDX-License-Identifier: CC-BY-4.0

.. _dovetail-releasenotes:

==================================================================
OPNFV Verified Program (OVP) 2018.09 / Dovetail 2.0.0 Release Note
==================================================================


OPNFV 2018.09 Release
=====================

The OPNFV Verified Program (OVP) allows vendors and operators to obtain 'OPNFV Verified'
status based on an agreed upon set of compliance verification test cases that align to OPNFV
releases. The reference System under Test (SUT) are the NFV components deployed by the OPNFV
installers for a given release, where OVP 2018.09 is based on the Fraser release. Participants
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
into the program with the participation form provided in the link: `OPNFV Verified Program
Participation Form <https://na3.docusign.net/Member/PowerFormSigning.aspx?PowerFormId=579ac00d-0a1f-4db3-82ea-ddd977769a60>`_

Test Suites & Test Areas
------------------------

OVP/Dovetail groups test cases into test suites and test areas. Test suites are currently a basic
categorization around releases for the most part. Executing the test suite 'ovp.2018.09' without
further specification will run all the test cases in the OVP 2018.09 release. Test suites are
divided into test areas that can be executed separately.

Test areas include a division into **'mandatory'** and **'optional'** in an overarching
categorization.

All the mandatory test cases are required to be executed with passing results for all inclusive
test cases for results to be reviewed and approved by the community made up of peer reviewers.
The optional test cases are not required to be executed for the official compliance verification
review in the OVP 2018.09 release. However, execution of these cases is encouraged, as some
optional test cases may become mandatory in future releases.

Test Cases and Sub Test Cases
-----------------------------

Each test area consists of multiple test cases where each test case can be a single test or
broken down into sub test cases. A listing of test cases with the number of sub test cases noted
in parenthesis is shown below for the OVP 2018.09 release.

**Mandatory**

- functest.vping.userdata (1)
- functest.vping.ssh (1)
- bottlenecks.stress.ping (1)
- functest.tempest.osinterop (200)
- functest.tempest.compute (12)
- functest.tempest.identity_v3 (11)
- functest.tempest.image (2)
- functest.tempest.network_api (14)
- functest.tempest.volume (2)
- functest.tempest.neutron_trunk_ports (38)
- functest.tempest.ipv6_api (21)
- functest.security.patrole (119)
- yardstick.ha.nova_api (1)
- yardstick.ha.neutron_server (1)
- yardstick.ha.keystone (1)
- yardstick.ha.glance_api (1)
- yardstick.ha.cinder_api (1)
- yardstick.ha.cpu_load (1)
- yardstick.ha.disk_load (1)
- yardstick.ha.haproxy (1)
- yardstick.ha.rabbitmq (1)
- yardstick.ha.database  (1)


There are a total of 432 mandatory test cases.

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

OPNFV Test Projects and Components
----------------------------------

The OPNFV test frameworks integrated into the Dovetail framework that deliver test content are:

 * Functest (leverages OpenStack RefStack/Tempest projects in addition to supplying native test cases)
 * Yardstick
 * Bottlenecks


Acceptence and Marketing
------------------------

Upon successful community review of results for OVP 2018.09, the Linux Foundation Compliance
Verification Committee (LFN CVC) on behalf of the Board of Directors can award a product 'OPNFV
Verified' status. Use of 'OPNFV Verified' Program Marks shall be awarded to the platform used
for compliance verification. The category label of 'Infrastructure' is used within the Program
Marks logo and limits the scope of this OVP release to a SUT consisting of NFVI and VIM components
using ETSI terminology. It does not provide compliance verification for specific VNFs in any fashion.
The date '2018.09' corresponds to a reference SUT that aligns to the OPNFV Fraser release and
currently aligns to the Dovetail framework version 2.0.0.

Organizations shall not use the Program Marks in any way that would associate it with any
individual or company logo or brand, beyond the association to the specific platform to which it
was awarded. While OpenStack RefStack interoperability and Tempest integration test cases are
executed as part of the OVP 2018.09 compliance verification test suites, the OVP does not grant or
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
|                                      | 2018.09 (Fraser)                      |
+--------------------------------------+---------------------------------------+
| **Release date**                     | September 2018                        |
|                                      |                                       |
+--------------------------------------+---------------------------------------+
| **Purpose of the delivery**          | Support OVP 2018.09 release with      |
|                                      | OPNFV Fraser release as reference SUT |
+--------------------------------------+---------------------------------------+

Deliverables
============

Software
--------
+-------------------------+-----------------------------------+----------------+
|  **Docker Container**   | **Docker Image**                  | **Tag**        |
+-------------------------+-----------------------------------+----------------+
|   dovetail              |    opnfv/dovetail                 |    ovp.2.0.0   |
+-------------------------+-----------------------------------+----------------+
|   functest              |    opnfv/functest-smoke           |    opnfv-6.3.0 |
+-------------------------+-----------------------------------+----------------+
|   functest              |    opnfv/functest-healthcheck     |    opnfv-6.3.0 |
+-------------------------+-----------------------------------+----------------+
|   functest              |    opnfv/functest-features        |    opnfv-6.3.0 |
+-------------------------+-----------------------------------+----------------+
|   functest              |    opnfv/functest-vnf             |    opnfv-6.3.0 |
+-------------------------+-----------------------------------+----------------+
|   yardstick             |    opnfv/yardstick                |    ovp-2.0.0   |
+-------------------------+-----------------------------------+----------------+
|   bottlenecks           |    opnfv/bottlenecks              |    ovp-2.0.0   |
+-------------------------+-----------------------------------+----------------+


Docker images:

- `Dovetail Docker images <https://hub.docker.com/r/opnfv/dovetail>`_
- `Functest-smoke Docker images <https://hub.docker.com/r/opnfv/functest-smoke/>`_
- `Functest-healthcheck  Docker images <https://hub.docker.com/r/opnfv/functest-healthcheck/>`_
- `Functest-features Docker images <https://hub.docker.com/r/opnfv/functest-features/>`_
- `Functest-vnf Docker images <https://hub.docker.com/r/opnfv/functest-vnf/>`_
- `Yardstick Docker images <https://hub.docker.com/r/opnfv/yardstick/>`_
- `Bottlenecks Docker images <https://hub.docker.com/r/opnfv/bottlenecks/>`_



Documents
---------

- `System Preparation Guide <http://docs.opnfv.org/en/stable-fraser/submodules/dovetail/docs/testing/user/systempreparation/index.html>`_

- `User Guide <http://docs.opnfv.org/en/stable-fraser/submodules/dovetail/docs/testing/user/userguide/testing_guide.html>`_

- `OPV Test Specifications <http://docs.opnfv.org/en/stable-fraser/submodules/dovetail/docs/testing/user/testspecification/index.html>`_

- `Dovetail CLI Reference <http://docs.opnfv.org/en/stable-fraser/submodules/dovetail/docs/testing/user/userguide/cli_reference.html>`_

- `OPV Workflow <http://docs.opnfv.org/en/stable-fraser/submodules/dovetail/docs/testing/user/certificationworkflow/index.html>`_

- `OPV Reviewer Guide <http://docs.opnfv.org/en/stable-fraser/submodules/dovetail/docs/testing/user/reviewerguide/index.html>`_


Testing with OPNFV Fraser Installers
====================================

OVP 2018.09 and Dovetail 2.0.0 are known to be have been tested with the following OPNFV
Fraser installer versions.

+-----------------+----------------------+
|   Installer     |      Version         |
+=================+======================+
|   Apex          |      stable/fraser   |
+-----------------+----------------------+
|   Compass       |      stable/fraser   |
+-----------------+----------------------+
|   Fuel          |      stable/fraser   |
+-----------------+----------------------+


Fraser Known Restrictions/Issues
================================

Please refer to the Dovetail project JIRA for known issues with the Dovetail
Fraser release:

.. https://jira.opnfv.org/projects/DOVETAIL


Useful Links
============

 - `OVP Web Portal <https://verified.opnfv.org>`_

 - `Wiki Project Page <https://wiki.opnfv.org/display/dovetail>`_

 - `Dovetail Repo <https://git.opnfv.org/dovetail/>`_

 - `Dovetail CI dashboard <https://build.opnfv.org/ci/view/dovetail/>`_

 - `JIRA dashboard <https://jira.opnfv.org/secure/RapidBoard.jspa?rapidView=149>`_

 - Dovetail IRC Channel: #opnfv-dovetail

 - `Dovetail Test Configuration <https://git.opnfv.org/dovetail/tree/etc/compliance/ovp.2018.09.yaml>`_
