.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Intel Corporation, Ericsson AB, Huawei

====================================================================
Compliance and Verification Program - Guidelines Addendum for Danube
====================================================================

.. toctree::
   :maxdepth: 2


Introduction
============

This addendum provides a high-level description of the testing scope and pass/fail criteria used in the Compliance
Verification Program (CVP) for the OPNFV Danube release. This information is intended as an overview for CVP testers
and for the Dovetail Project to help guide test-tool and test-case development for Danube. Detailed information about
the test tool as well as test-cases can be found in Dovetail documents.
CVP testing focuses on establishing the ability of the SUT to perform NFVI operations and support Service Provider
oriented features that ensure manageable, resilient and secure networks.


Meaning of Compliance
=====================

OPNFV Compliance indicates adherence to NFV platform behavior defined as various platform capabilities or features
to prepare, instantiate and remove VNFs running on the NFVI. Danube compliance evaluates the ability of a platform
to support Service Provider network capabilities and workloads that are supported in the OPNFV platform as of this
release. Compliance test cases shall be designated as compulsory or optional based on the maturity of OPNFV
capabilities as well as industry expectations. Compulsory test cases may for example include NFVI management
capabilities whereas tests for certain high-availability features may be deemed as optional.

In the future the scope of compliance will include platform "usability" to ensure that Network Services can be
consistently managed. Test coverage is designed to ensure an acceptable level of compliance but not be so restrictive
as to disqualify variations in platform capabilities and features.


SUT Assumptions
===============

Assumptions about the System Under Test (SUT) include ...

  - The minimal specification of physical infrastructure, including controller nodes, compute nodes and networks,
    is defined by the Pharos specification.
  - The SUT is fully deployed and operational, i.e. SUT deployment tools are out of scope of testing.


Scope of Testing
================

The OPNFV CVP Guidelines [1], as approved by the Board of Directors, outlines the key objectives of
the CVP as follows:
  - Help build the market for
     - OPNFV based infrastructure
     - applications designed to run on that infrastructure
  - Reduce adoption risks for end-users
  - Decrease testing costs by verifying hardware and software platform interfaces and components
  - Enhance interoperability

The Guidelines further directs the scope to be constrained to "features, capabilities, components,
and interfaces included in an OPNFV release that are generally available in the industry (e.g.,
through adoption by an upstream community)". And compliance verification is evaluated using
"functional tests that focus on defined interfaces and/or behaviors without regard to the
underlying system under test". In the Danube release timeframe, these requirements put the
high level scope to be the NFVI and VIM only, because they have been the OPNFV community's main
focus so far.

In order to meet the above objectives for CVP, we first examined the pain points that a compliance
verification program could address from the end-users' perspective. From surveys and EUAG inputs,
the top-down expectations can be summarized in the following categories:
  - Interoperability, specifically (i) VNF portability among OPNFV-ready platforms, (ii) hardware
    on which compliant software is able to run with common configurations.
  - Common end-user RFP requirements, such as basic cloud capabilities, basic VNF management
    functions, and common use cases.
  - Carrier grade non-functional requirements such as availability, resilency and security.
  - Features that enable performance (but not benchmarking that is hard to define), performance
    monitoring and fault detection, as other carrier grade requirements.

End-users also expressed that the lack of an industry compliance verification program is a
major pain point in and of itself.

Based on these end-user requirements, and the functions and capabilities integrated and exposed
in the OPNFV Danube release, we seek to define the initial testing scope as the first step towards
meeting the CVP objectives:

1. OPNFV mainly supports Openstack as the VIM up to the Danube release. The portability of VNFs 
   requires commercial Openstack distributions to be compliant to a common specification. The CVP
   adopts Openstack community's Interop Working Group guidelines and Refstack test cases to define
   and verify compliance, respectively. This part of testing constitues the basic requirements of
   cloud management functions and VNF (as a VM) management, and is appropriate when the VIM is
   Openstack. The OPNFV CVP however goes beyond Openstack Interop requirements because the CVP
   requires that a Pharos compliant infrastructure must be the target NFVI when the test cases
   are executed. Different configurations of NFVI can significantly change a SUT's behaviors,
   not only hardware configurations, but also operating systems, hypervisors, data path
   acceleration methods, and underlay network controller choices, among many other aspects.
   In future CVP versions, we intend to closely align with its Interop guidelines and explore
   collaborative efforts in defining an NFV specific additions to the basic Interop suite.

2. With regard to hardware interoperability to compliant NFV software, this area has not been
   the OPNFV community's focus and we have therefore chosen to combine the hardware, NFVI and
   VIM in a single SUT. End-users, vendors and community members can however use the same CVP
   test suite to cross verify hardware/software interoperability. Similarly, other components
   of the NFVI, such as operating systems, hypervisors, data path acceleration methods and
   underlay network controller choices are not directly exposed by OPNFV. Testing of these
   components are indirect only, when they are used by the SUT.

3. End-users see use case level testing as a significant components in verifying OPNFV
   compliance because it validates use cases that NFV industry truly cares about, in
   partucular networking data path, control path and management functions. There are
   a lot of projects in OPNFV developing use cases and sample VNFs. Although most are still
   in early phase and require further enhancements, we see this category be very useful
   addition to the CVP. These use case test cases do not add new requirements to the SUT
   per se, but is very valuable in exercising aspects of the SUT's functionalities for
   OPNFV compliance.

4. NFV often has functional requirements beyond the basic common cloud capabilities, esp.
   in the networking area. Examples like SDNVPN, IPv6, SFC may be considered more
   critical in the NFV context than in general purpose cloud computing. These feature
   requirements expand beyond common Openstack requirements (or other VIM). OPNFV CVP
   will incorporate test cases to verify compliance in these areas as they become
   mature. Because these extensions impose new API demands, maturity and industry
   adoption must be prerequisite.

5. High availability is a common carrier grade requirement. Availability of a platform
   involves many aspects of the SUT, for example hardware or lower layer system failures
   or system overloads, and is also highly dependent on configurations. We can start
   with the high availability of controllers with common configurations adopted in the
   industry.

6. Resiliency is another aspect of the system behavior that is important to end-users
   but can be complex to qualify and validate. The OPNFV testing groups have some
   experiences so far up to the Danube release. We should strive to start resilency
   verification based on OPNFV community experience.

7. Security is among the top priorities as a carrier grade requirement by the end-users.
   Like most open source projects however, OPNFV has not been giving security testing
   sufficient attention and resources up to the time of Danube release. Good progress
   in the area of security scanning has already been made however, and can become
   a valuable addition to CVP if we put sufficient resource to the task. Additional
   end-user input in more specific requirements in security is also in need to understand
   the appropriate scope.

8. Performance testing is a difficult task because of the lack of objective clean
   definition of testing methodology and criteria. While it is very important to
   a lot of end-users, it may not be the most appropriate area for CVP. Some features
   in the SUT designed for enabling better performance, e.g. data path acceleration,
   can be a better substitute to the direct performance benchmarking. Another area is
   performance monitoring and fast fault detection that can also be valuable addition
   to the CVP. At the time of Danube release, these testing areas are out of scope
   but work is ongoing and encouraged to explore how to test performance enabling
   features or testing performance and fault management capabilities.

The Dovetail project, together with all related projects participated in Danube, also
took a bottom-up approach in analyzing what test cases developed in the OPNFV
community up to the Danube release are in scope and qualified.

Our combined analysis yields the following initial CVP scope, summarized in a table format.
These testd areas represent significant advancement in the direction to meet the CVP's
objectives and end-user expectations.

+---------------------+--------------+-----------------------+---------------------------------------------------------+
| Test Area           | Danube Scope | Reference Project/s   | Related Test Specifications                             |
+=====================+==============+=======================+=========================================================+
|                     |              |                       |                                                         |
| Cloud capabilities  | Included     | OpenStack             | Refstack (OpenStack interoperability testing)           |
|                     |              | OPNFV-Functest        |                                                         |
+---------------------+--------------+-----------------------+---------------------------------------------------------+
| VNF lifecycle       | Basic        | OpenStack             | Refstack (OpenStack interoperability testing)           |
| management          | functions    | OPNFV-Functest        | ETSI NFV-TST007 (Guidelines on Interoperability         |
|                     |              |                       | Testing for MANO)                                       |
+---------------------+--------------+-----------------------+---------------------------------------------------------+
| Networking          | Basic        |                       |                                                         |
| data path &         | functions    | OPNFV-Functest        |                                                         |
| use cases           |              | OPNFV-SDNVPN(optional)|                                                         |
|                     |              | OPNFV-IPv6 (optional) |                                                         |
+---------------------+--------------+-----------------------+---------------------------------------------------------|
| Carrier network     | Limited      | OPNFV-IPv6 (optional) | ETSI NFV-TST004 (Guidelines for Test plan               |
| capabilities        |              | OPNFV-SDNVPN          | for path implementation through NFVI)                   |
|                     |              | (optional)            | RFC4364, RFC 4659, RFC2547 (BGP VPN)                    |
|                     |              |                       | Openstack IPv6 Guide                                    |
|                     |              |                       | RFC2460 (IPv6)                                          |
+---------------------+--------------+-----------------------+---------------------------------------------------------+
| Service             | Limited      | OPNFV-HA              | ETSI NFV-REL001 (NFV Resiliency Requirements)           |
| Availability        |              | OPNFV-Yardstick       | OpenStack High Availability Guide                       |
|                     |              |                       |                                                         |
+---------------------+--------------+-----------------------+---------------------------------------------------------+
| Resilency           | Limited      | OPNFV-Bottleneck      |                                                         |
|                     |              | OPNFV-Yardstick       |                                                         |
|                     |              |                       |                                                         |
+---------------------+--------------+-----------------------+---------------------------------------------------------+

Note 1: While the current scope of compliance includes functional verification of certain performance-enhancing NFVI features,
no performance measurements or assessment of performance capabilities are included as of this release.

Note 2: The SUT is limited to NFVI and VIM functions. While testing MANO component capabilities is out of scope, certain
APIs exposed towards MANO are used by the current OPNFV compliance testing suite. MANO and other operational elements
may be part of the test infrastructure; for example used for workload deployment and provisioning.

Note 3: The following table lists test areas that are in scope and references related test specifications from OPNFV,
upstream projects and Industry Specification Groups. Dovetail documents include "Test Scope" which lists test areas
and respective test cases that are either compulsory or optional to include in a test run. Separate documents for each
test area specify detailed test cases with test steps and associated pass/fail criteria.

Criteria for Awarding Compliance
================================

This section provides guidance on compliance criteia for each test area. The criteria described here are
high-level, detailed pass/fail metrics are documented in Dovetail test specifications.

1. All mandatory test cases must pass.
2. Optional test cases are optional to run. Its test results, pass or fail, do not impact compliance.

References
==========

[1] The OPNFV CVP Guidelines v.16


