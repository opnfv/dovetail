.. This work is licensed under a Creative Commons Attribution 4.0 International
.. License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Intel Corporation, Ericsson AB, Huawei

====================================================================
Compliance and Verification Program - Guidelines Addendum for Danube
====================================================================

.. toctree::
   :maxdepth: 2


Introduction
============

This addendum provides a high-level description of the testing scope and
pass/fail criteria used in the Compliance Verification Program (CVP) for the
OPNFV Danube release. This information is intended as an overview for CVP
testers and for the Dovetail Project to help guide test-tool and test-case
development for Danube. The Dovetail project is responsible for test-case
specifications as well as implementing the CVP tool-chain through collaboration
with the OPNFV testing community. CVP testing focuses on establishing the
ability of the SUT to perform NFVI and VIM operations and support
Service Provider oriented features that ensure manageable, resilient and secure
networks.


Meaning of Compliance
=====================

OPNFV Compliance indicates adherence to NFV platform behavior defined as
various platform capabilities or features to prepare, instantiate and remove
VNFs running on the NFVI. Danube compliance evaluates the ability of a platform
to support Service Provider network capabilities and workloads that are
supported in the OPNFV platform as of this release. Compliance test cases shall
be designated as compulsory or optional based on the maturity of OPNFV
capabilities as well as industry expectations. Compulsory test cases may for
example include NFVI management capabilities whereas tests for certain
high-availability features may be deemed as optional.

Test coverage and pass/fail criteria are
designed to ensure an acceptable level of compliance but not be so restrictive
as to disqualify variations in platform capabilities and features.


SUT Assumptions
===============

Assumptions about the System Under Test (SUT) include ...

  - The minimal specification of physical infrastructure, including controller
    nodes, compute nodes and networks, is defined by the Pharos specification
    [2].
  - The SUT is fully deployed and operational, i.e. SUT deployment tools are
    out of scope of testing.


Scope of Testing
================

The OPNFV CVP Guidelines [1], as approved by the Board of Directors, outlines
the key objectives of the CVP as follows:
  - Help build the market for
     - OPNFV based infrastructure
     - applications designed to run on that infrastructure
  - Reduce adoption risks for end-users
  - Decrease testing costs by verifying hardware and software platform
    interfaces and components
  - Enhance interoperability

The Guidelines further directs the scope to be constrained to "features,
capabilities, components, and interfaces included in an OPNFV release that are
generally available in the industry (e.g., through adoption by an upstream
community)", and that compliance verification is evaluated using "functional tests
that focus on defined interfaces and/or behaviors without regard to the
underlying system under test".

While the OPNFV community has broad activities in the Danube release,
given these guidelines, not all are represented in the CVP, or at least not at
this point. E.g., the deployment tools for the SUT is out of scope. Similarly,
performance benchmarking related testing is also out of scope or for further
study. Newer functional areas such as MANO (outside of APIs in the NFVI and
VIM) are still developing and are for future considerations.

In order to meet the above objectives for CVP, we aim to define the initial
scope of CVP to evaluate the following categories:

  - Interoperability, specifically VNF portability among OPNFV-ready platforms
    that adhere to common APIs.
  - Common end-user RFP requirements, such as basic cloud capabilities, basic
    VNF lifecycle management functions, and common data path validation use cases.
  - Carrier grade non-functional requirements such as service availability,
    resilency, and security.
  - Functional extensions often required for NFV.

Note that end-users also expressed additional priorities and
carrier grade requirements to CVP in the long term,
such as hardware portability, performance, fault management and other
operational features, security, MANO and VNF verification [2].
We are not yet ready to support all these areas at this time, but can start
to study for future roadmap considerations.

In some areas, we can only start with very limited level of verification
initially, constrained by what the commmunity has developed or automated so
far. In these areas, we can still bring significant value to the community we
serve by starting verification from a limited base and expand in future.

In other areas, the functions being verified have yet to reach
wide adoption but are seen as significant requirements in NFV. In such as
cases, we can incorporate the test areas as optional.

End-users also expressed that the lack of an industry compliance verification
program is a major pain point in and of itself.

Based on these high level objectives and the identified categories,
we seek to define the initial verification scope by analyzing each
category and aligning the category with what capabilities we have developed
in Danube release in the following enumerated sections:

1. VNF portability on compliant platforms

OPNFV mainly supports Openstack as the VIM up to the Danube release. The
portability of VNFs requires commercial Openstack distributions to be compliant
to a common specification. This requirement significantly overlaps with
Openstack community's Interop working group's goals, but may not be fully
identical. The CVP runs a subset of Openstack Refstack test cases to verify
compliance to the basic common requirements of cloud
management functions and VNF (as a VM) management for OPNFV. The test case
documentation summarizes these requirements from the OPNFV's perspective.

These basic common requirements from Openstack may not be suffient for
covering all of the OPNFV requirements. An extension set of test cases
for NFV may be necessary as a future work item. In Openstack Interop WG,
there is also an intention to develop test cases for the NFV vertical. We intend
to work collaboratively with the Openstack community in these efforts.

The OPNFV CVP also requires that a Pharos [2] compliant infrastructure
must be the target NFVI when the test cases are executed. Different
configurations of NFVI can significantly change a SUT's behaviors. We do
not have a good way to verify Pharos compliance at this time however. This
requirement will have to depend on documented SUT statements.

2. Use case testing

End-users see use case level testing as a significant components in
verifying OPNFV compliance because it validates use cases that NFV industry
truly cares about. There are a lot of projects in OPNFV developing use cases
and sample VNFs. Although most are still in early phase and require further
enhancements, we see this category be very useful addition to the CVP. These
use case test cases do not add new API requirements to the SUT per se, but is very
valuable in exercising aspects of the SUT's functional interactions for OPNFV
compliance.

Examples such as vPing in Functest, and IPv6 and v6Ping, are valuable
addition to the CVP. Other use cases may not be ready for CVP use at
time of Danube but can be incorporated in Euphrates.

3. NFV specific funtional requirements

NFV has functional requirements beyond the basic common cloud
capabilities, esp.  in the networking area. Examples like SDNVPN, IPv6, SFC may
be considered additional requirements in the NFV beyond general purpose cloud
computing. These feature requirements expand beyond common Openstack (or other
VIM) requirements. OPNFV CVP will incorporate test cases to verify
compliance in these areas as they become mature. Because these extensions
impose new API demands, maturity and industry adoption must be prerequisite for
making them a mandatory requirement for OPNFV compliance. In the meantime, CVP
intends to offer tests in these areas as an optional extension of the test
report to be submitted for review, noting that passing these tests will not be
required to pass OPNFV compliance verification.

4. High availability

High availability is a common carrier grade requirement. Availability of a
platform involves many aspects of the SUT, for example hardware or lower layer
system failures or system overloads, and is also highly dependent on
configurations. The current OPNFV high availability verification focuses on
Openstack control service failures and resource overloads, and verifies service
continuity when the system encounters such failures or resource overloads, and
also verifies the system heals after a failure episode within a reasonable time
window. Such service HA capabilities are supported by common
configurations adopted in the industry.

We expect additional high availability scenarios be extended in future
releases.

5. Resiliency

Resilency testing involves long duration load testing and verifies the SUT's
ability to sustain the long duration load and continue to provide normal
service after the testing period. It is another aspect of the system behavior
that is important to end-users but can be complex to qualify and validate.
The OPNFV testing projects have some experiences in the Danube release that
can be used to provide limited coverage in resilency.

6. Security is among the top priorities as a carrier grade requirement by the
end-users. Some basic common functions such as virtual network isolations and
security groups are a part of common capabilities and verified in CVP. Another
area that the OPNFV security project made progress on in security vulnerability
scanning but this area needs further attention and analysis for future
integration into CVP. Gap analysis and additional end-user input in more
specific requirements in security is also needed.

In summary, the above analysis concludes with the following initial CVP scope,
summarized below. These tested areas represent significant advancement in the
direction to meet the CVP's objectives and end-user expectations, and is a
good basis for the initial phase of CVP.

- Test Area: common cloud capabilities
  - Openstack Refstack test cases
  - OPNFV-Functest/vPing
  - Mandatory

- Test Area: VNF lifecycle management
  - Openstack Refstack
  - Mandatory

- Test Area: SDNVPN
  - OPNFV-SDNVPN
  - Optional

- Test Area: IPv6
  - OPNFV-IPv6
  - Limited to overlay tests, v6Ping
  - Optional

- Test Area: High Availability
  - OPNFV-HA
  - OPNFV-Yardstick
  - Limited to service continuity verification on control services
  - Mandatory

- Test Area: Resilency
  - OPNFV-Bottleneck
  - OPNFV-Yardstick
  - Limited to compute resource load testing
  - Optional

Note 1: While the current scope of compliance includes functional verification
of certain performance-enhancing NFVI features, no performance measurements or
assessment of performance capabilities are included as of this release.

Note 2: The SUT is limited to NFVI and VIM functions. While testing MANO
component capabilities is out of scope, certain APIs exposed towards MANO are
used by the current OPNFV compliance testing suite. MANO and other operational
elements may be part of the test infrastructure; for example used for workload
deployment and provisioning.

Criteria for Awarding Compliance
================================

This section provides guidance on compliance criteia for each test area. The
criteria described here are high-level, detailed pass/fail metrics are
documented in Dovetail test specifications.

1. All mandatory test cases must pass.
2. Optional test cases are optional to run. Its test results, pass or fail,
   do not impact compliance.

References
==========

[1] The OPNFV CVP Guidelines v.16 [Editor's note: link to be provided.]
[2] Pharos specification xxx [Editor's note: link to be provided.]

