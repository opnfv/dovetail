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

While the OPNFV reference platform provides a broad range of capabilities,
not all are represented in the CVP, or at least not at
this point. E.g., the deployment tools for the SUT is out of scope. Similarly,
performance benchmarking related testing is also out of scope or for further
study. Newer functional areas such as MANO (outside of APIs in the NFVI and
VIM) are still developing and are for future considerations.

In order to meet the above objectives for CVP, we aim to define the initial
scope of CVP to evaluate the following categories:

  - Common basic cloud capabilities, including VNF (VM) image management,
    compute resource management, virtual network management, identity
    management and basic data path validation.
  - Simple use cases that represent common operations needed by basic VNFs.
  - Functional requirements for NFV that go beyond the common cloud capabilities,
    such as SDNVPN and SFC.
  - Carrier grade non-functional requirements such as service availability.
  - Some level of system resilency under load.
  - Basic functional cloud constructs for supporting security.

Note that end-users also expressed additional priorities and
carrier grade requirements to CVP in the long term,
such as hardware portability, performance, fault management and other
operational features, security, MANO and VNF verification [2].
We are not yet ready to support all these areas at this time, but can start
to study for future roadmap considerations.

In some areas, we will start with a limited level of verification
initially, constrained on what community resources are able to support at this
time, but still serve a basic need that is not being fulfilled elsewhere.
In these areas, we bring significant value to the community we
serve by starting a new area of verification, breaking new ground and
expanding it in the future.

In other areas, the functions being verified have yet to reach
wide adoption but are seen as significant requirements in NFV. In such as
cases, we plan to incorporate the test areas as optional. An optional test
area will not have to be run or passed in order to obtain the "OPNFV ready" label.
It provides an opportunity for vendors to demonstrate compliance with specific OPNFV
features beyond the mandatory test scope.

End-users also expressed that the lack of an industry compliance verification
program is a major pain point in and of itself. The test areas with limited
scope and those that are optional are efforts by the community to start
to meet this need in a timely way.

Based on these high level objectives and the identified categories,
we seek to define the initial verification scope by analyzing each
category and aligning the category with what capabilities we have developed
in Danube release in the following enumerated sections:

1. Basic Cloud Capabilities and Interoperability

The intent of this category is to verify that the SUT has the required
capabilities that a basic VNF needs, and these capabilities are implemented
in a compliant way that enables this basic VNF to run on any compliant
systems.

A basic VNF can be thought of as a "bare-bone" virtual machine that is networked
and can perform the simplest network functions, for example, connecting to
more than one networks, forwarding packets between them, such as a ping,
and filtering packets based on some security rules. In addition, this basic
VNF will also have the same common needs of a virtual machine, including image
management, identity, virtual machine management, virtual storage, and virtual
networks.

OPNFV mainly supports Openstack as the VIM up to the Danube release. The
VNFs, and portability of VNFs, require commercial Openstack distributions
to support a common basic level of cloud capabilities, and to be compliant
to a common specification for these capabilities. This requirement significantly
overlaps with Openstack community's Interop working group's goals, but may not be fully
identical. The CVP runs the Openstack Refstack-Compute test cases to verify
compliance to the basic common requirements of cloud
management functions and VNF (as a VM) management for OPNFV. The test case
documentation for this teat area will summarize these test cases and their
coverage from the OPNFV's perspective.

These basic common requirements from Openstack are not sufficient for
OPNFV in several ways. The network data path validation is one area
that need additional test cases. OPNFV may also require additional network
capabilities other than those in Refstack,
and this basic validation requirement should be extended to all networks we support.

VNFs require validating more networking capabilities, such as connecting to
multiple networks in a topology, security group rules, dynamic network management.
The basic VNF will also go through its lifecycles and validation of its continued
functional state is another area of test cases.

This test area also helps to ensure that these basic operations adhere to
a common standard to ensure their portability across compliant platforms.

2. Use case testing

More complex interactions among multiple VNFs and between VNFs and the cloud
platform can be better exercised through selected simplified use cases.

End-users see use case level testing as a significant components in
verifying OPNFV compliance because it validates design patterns that users
care about. There are a lot of projects in OPNFV developing use cases
and sample VNFs. Although most are still in early phase and require further
enhancements, we see this category be very useful addition to the CVP.

Many of these test cases do not add new API requirements to the SUT per se, but
exercise aspects of the SUT's functional capabilities in more complex ways.
Other use cases, such as SDNVPN, will require additional API level extension,
and to clearly separate the two, we will discuss the latter in the next section
for NFV specific functional requirements.

Examples such as vIMS as part of Functest, or vCPE which are not yet available
in Danube release, will be valuable additions to the CVP. These use cases are
more complex to support and test and may demand higher level of community
resources to implement and document. Use cases that are not ready for CVP use at
time of Danube can be incorporated in Euphrates.

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

So far, we have covered functional requirements for a NFV platform from the
common and basic, to be OPNFV specific, and OPNFV functional extensions.
Next, we analyze common carrier grade requirements for NFV that are out of
the functional areas.

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

5. Resiliency with Load

Resilency testing involves long duration load testing and verifies the SUT's
ability to sustain the long duration load and continue to provide normal
service after the testing period. It is another aspect of the system requirement
that is common and important to end-users.

The OPNFV testing projects Bottleneck and Yardstick have started testing
OPNFV system resiliency with load in
the Danube release that can be used to provide limited coverage in this area.
[Editor's note: this test case has not yet been
proposed or documented yet, but is identified here from top-down analysis.]

6. Supporting Security

Security is among the top priorities as a carrier grade requirement by the
end-users. Some basic common functions such as virtual network isolations,
security groups and identify are a part of common capabilities and verified in CVP.

Another area of common requirement is security vulnerability scanning.
While the OPNFV security project integrated tools for security vulnerability
scanning, this has not been fully analyzed or exercised in Danube release.
This area needs further attention and analysis for future integration into CVP.

Additional gap analysis and additional end-user inputs on more
specific requirements in security is also needed.

Summary of Test Scope
---------------------

The above analysis concludes with the following scope summarized below.
These tested areas represent significant advancement in the
direction to meet the CVP's objectives and end-user expectations, and is a
good basis for the initial phase of CVP.

- Test Area: common cloud capabilities
  - Openstack Refstacki-compute test cases
    Image, Identity, Compute, Network, Storage
  - OPNFV-Functest/vPing, including both user data and ssh
  - [Editor's note: others to be added including testing security groups,
     VM lifecycle events, and networking cases.]
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

- Test Area: Resilency with Load
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

Exceptions to this rule may be legitimate, e.g. due to imperfect test tools or
reasonable circumstances that we can not foresee. These exceptions must be
documented and accepted by the reviewers.

2. Optional test cases are optional to run. Its test results, pass or fail,
   do not impact compliance.

Applicants who choose to run the optional test cases can include the results
of the optional test cases to highlight the additional compliance.

References
==========

[1] The OPNFV CVP Guidelines v.16 [Editor's note: link to be provided.]
[2] Pharos specification xxx [Editor's note: link to be provided.]

