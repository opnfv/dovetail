.. This work is licensed under a Creative Commons Attribution 4.0 International
.. License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Intel and others

.. _dovetail-cvp_addendum:

====================================================================
Compliance Verification Program - Guidelines Addendum for Danube
====================================================================

.. toctree::
   :maxdepth: 2


Introduction
============

This addendum provides a high-level description of the testing scope and
pass/fail criteria used in the Compliance Verification Program (CVP) for the
OPNFV Danube release. This information is intended as an overview for CVP
testers and for the Dovetail Project to help guide test-tool and test-case
development for the OPNFV Danube release. The Dovetail project is responsible for documenting
test-case specifications as well as implementing the CVP tool-chain through collaboration
with the OPNFV testing community. CVP testing focuses on establishing the
ability of the System Under Test (SUT) to perform NFVI and VIM operations and support
Service Provider oriented features that ensure manageable, resilient and secure
networks.


Meaning of Compliance
=====================

OPNFV Compliance indicates adherence of an NFV platform to behaviors defined
through specific platform capabilities, allowing to prepare, instantiate,
operate and remove VNFs running on the NFVI. Danube compliance evaluates the
ability of a platform to support Service Provider network capabilities and
workloads that are supported in the OPNFV platform as of this release.
Compliance test cases are designated as compulsory or optional based on the
maturity of OPNFV capabilities as well as industry expectations. Compulsory
test cases may for example include NFVI management capabilities whereas tests
for certain high-availability features may be deemed as optional.

Test coverage and pass/fail criteria are
designed to ensure an acceptable level of compliance but not be so restrictive
as to disqualify variations in platform implementations, capabilities and features.


SUT Assumptions
===============

Assumptions about the System Under Test (SUT) include ...

- The minimal specification of physical infrastructure, including controller
  nodes, compute nodes and networks, is defined by the `Pharos specification`_.

- The SUT is fully deployed and operational, i.e. SUT deployment tools are
  out of scope of testing.


Scope of Testing
================

The `OPNFV CVP Guidelines`_, as approved by the Board of Directors, outlines
the key objectives of the CVP as follows:

- Help build the market for

  - OPNFV based infrastructure

  - applications designed to run on that infrastructure

- Reduce adoption risks for end-users

- Decrease testing costs by verifying hardware and software platform
  interfaces and components

- Enhance interoperability

The guidelines further directs the scope to be constrained to "features,
capabilities, components, and interfaces included in an OPNFV release that are
generally available in the industry (e.g., through adoption by an upstream
community)", and that compliance verification is evaluated using "functional tests
that focus on defined interfaces and/or behaviors without regard to the
the implementation of the underlying system under test".

OPNFV provides a broad range of capabilities, including the reference platform itself
as well as tools-chains and methodologies for building infrastructures, and
deploying and testing the platform.
Not all these aspects are in scope for CVP and not all functions and
components are tested in the initial version of CVP. For example, the deployment tools
for the SUT and CI/CD toolchain are currently out of scope.
Similarly, performance benchmarking related testing is also out of scope or
for further study. Newer functional areas such as MANO (outside of APIs in the NFVI and
VIM) are still developing and are for future considerations.


General Approach
----------------

In order to meet the above objectives for CVP, we aim to follow a general approach
by first identifying the overall requirements for all stake-holders,
then analyzing what OPNFV and the upstream communities can effectively test and verify
presently to derive an initial working scope for CVP, and to recommend what the
community should strive to achieve in future releases.

The overall requirements for CVP can be categorized by the basic cloud
capabilities representing common operations needed by basic VNFs, and additional
requirements for VNFs that go beyond the common cloud capabilities including
functional extensions, operational capabilities and additional carrier grade
requirements.

For the basic NFV requirements, we will analyze the required test cases,
leverage or improve upon existing test cases in OPNFV projects
and upstream projects whenever we can, and bridge the gaps when we must, to meet
these basic requirements.

We are not yet ready to include compliance requirements for capabilities such
as hardware portability, carrier grade performance, fault management and other
operational features, security, MANO and VNF verification.  These areas are
being studied for consideration in future CVP releases.

In some areas, we will start with a limited level of verification
initially, constrained by what community resources are able to support at this
time, but still serve a basic need that is not being fulfilled elsewhere.
In these areas, we bring significant value to the community we
serve by starting a new area of verification, breaking new ground and
expanding it in the future.

In other areas, the functions being verified have yet to reach
wide adoption but are seen as important requirements in NFV,
or features are only needed for specific NFV use cases but
an industry consensus about the APIs and behaviors is still deemed beneficial. In such
cases, we plan to incorporate the test areas as optional. An optional test
area will not have to be run or passed in order to achieve compliance.
Optional tests provide an opportunity for vendors to demonstrate compliance with specific OPNFV
features beyond the mandatory test scope.


Analysis of Scope
-----------------

In order to define the scope of the Danube-release of the compliance and
verification program, this section analyzes NFV-focused platform capabilities
with respect to the high-level objectives and the general approach outlined in
the previous section. The analysis determines which capabilities are suitable
for inclusion in this release of the CVP and which capabilities are to be
addressed in future releases.

1. Basic Cloud Capabilities

The intent of these tests is to verify that the SUT has the required
capabilities that a basic VNF needs, and these capabilities are implemented
in a way that enables this basic VNF to run on any OPNFV compliant
deployment.

A basic VNF can be thought of as a single virtual machine that is networked
and can perform the simplest network functions, for example, a simple forwarding
gateway, or a set of such virtual machines connected only by simple virtual network
services. Running such basic VNF leads to a set of common requirements, including:

- image management (Refstack testing Glance API)
- identity management (Refstack testing Keystone Identity API)
- virtual compute (Refstack testing Nova Compute API)
- virtual storage (Refstack testing Cinder API)
- virtual networks (Refstack testing Neutron Network API)
- forwarding packets through virtual networks in data path
- filtering packets based on security rules and port security in data path
- dynamic network runtime operations through the life of a VNF (e.g. attach/detach,
  enable/disable, read stats)
- correct behavior after common virtual machine life cycles events (e.g.
  suspend/resume, reboot, migrate)
- simple virtual machine resource scheduling on multiple nodes

OPNFV mainly supports OpenStack as the VIM up to the Danube release. The
VNFs used in the CVP program, and features in scope for the program which are
considered to be basic to all VNFs, require commercial OpenStack distributions
to support a common basic level of cloud capabilities, and to be compliant
to a common specification for these capabilities. This requirement significantly
overlaps with OpenStack community's Interop working group's goals, but they are not
identical. The CVP runs the OpenStack Refstack-Compute test cases to verify
compliance to the basic common API requirements of cloud
management functions and VNF (as a VM) management for OPNFV.
Additional NFV specific requirements are added in network data path validation,
packet filtering by security group rules and port security, life cycle runtime events of
virtual networks, multiple networks in a topology, validation
of VNF's functional state after common life-cycle events including reboot, pause,
suspense, stop/start and cold migration. In addition, the
basic requirement also verifies that the SUT can allocate VNF resources based
on simple anti-affinity rules.

The combined test cases help to ensure that these basic operations are always
supported by a compliant platform and they adhere to
a common standard to enable portability across OPNFV compliant platforms.

2. NFV specific functional requirements

NFV has functional requirements beyond the basic common cloud
capabilities, esp. in the networking area. Examples like SDNVPN, IPv6, SFC may
be considered additional NFV requirements beyond general purpose cloud
computing. These feature requirements expand beyond common OpenStack (or other
VIM) requirements. OPNFV CVP will incorporate test cases to verify
compliance in these areas as they become mature. Because these extensions
may impose new API demands, maturity and industry adoption is a prerequisite for
making them a mandatory requirement for OPNFV compliance. At the time of Danube,
we have not identified a new functional area that is mandatory for CVP.
In the meantime, CVP
intends to offer tests in some of these areas as an optional extension of the test
report to be submitted for review, noting that passing these tests will not be
required to pass OPNFV compliance verification.

SDNVPN is relevant due to the wide adoption of MPLS/BGP based VPNs in wide area
networks, which makes it necessary for data centers hosting VNFs to be able to
seamlessly interconnect with such networks. IPv6 is a high priority service provider
requirement to ease IP addressing and operational issues. SFC is also an important
NFV requirement, however its implementation has not yet been accepted or adopted
in the upstream at the time of Danube.

3. High availability

High availability is a common carrier grade requirement. Availability of a
platform involves many aspects of the SUT, for example hardware or lower layer
system failures or system overloads, and is also highly dependent on
configurations. The current OPNFV high availability verification focuses on
OpenStack control service failures and resource overloads, and verifies service
continuity when the system encounters such failures or resource overloads, and
also verifies the system heals after a failure episode within a reasonable time
window. These service HA capabilities are commonly adopted in the industry
and should be a mandatory requirement.

The current test cases in HA cover the basic area of failure and resource
overload conditions for a cloud platform's service availability, including all
of the basic cloud capability services, and basic compute and storage loads,
so it is a meaningful first step for CVP. We expect additional high availability
scenarios be extended in future releases.

4. Resiliency

Resiliency testing involves stressing the SUT and verifying its ability
to absorb stress conditions and still provide an acceptable level of service.
Resiliency is an important requirement for end-users.

The OPNFV testing projects have started testing
OPNFV system resiliency in
the Danube release that can be used to provide limited coverage in this area.
However, this is a relatively new test methodology in OPNFV, additional study
and testing experiences are still needed. We defer the resiliency testing to
future CVP releases.

5. Security

Security is among the top priorities as a carrier grade requirement by the
end-users. Some of the basic common functions, including virtual network isolation,
security groups, port security and role based access control are already covered as
part of the basic cloud capabilities that are verified in CVP. These test cases
however do not yet cover the basic required security capabilities expected of an end-user
deployment. It is an area that we should address in the near future, to define
a common set of requirements and develop test cases for verifying those
requirements.

Another common requirement is security vulnerability scanning.
While the OPNFV security project integrated tools for security vulnerability
scanning, this has not been fully analyzed or exercised in Danube release.
This area needs further work to identify the required level of security for the
purpose of OPNFV in order to be integrated into the CVP. End-user inputs on
specific requirements in security is needed.

6. Service assurance

Service assurance (SA) is a broad area of concern for reliability of the NFVI/VIM
and VNFs, and depends upon multiple subsystems of an NFV platform for essential
information and control mechanisms. These subsystems include telemetry, fault management
(e.g. alarms), performance management, audits, and control mechanisms such as security
and configuration policies.

The current Danube release implements some enabling capabilities in NFVI/VIM
such as telemetry, policy, and fault management. However, the specification of expected
system components, behavior and the test cases to verify them have not yet
been adequately developed. We will therefore not be testing this area at this time
but defer to future study.

7. Use case testing

Use-case test cases exercise multiple functional capabilities of a platform in
order to realize a larger end-to-end scenario.  Such end-to-end use cases do
not necessarily add new API requirements to the SUT per se, but exercise
aspects of the SUT's functional capabilities in more complex ways.  For
instance, they allow for verifying the complex interactions among multiple VNFs
and between VNFs and the cloud platform in a more realistic fashion.  End-users
consider use-case-level testing as a significant tool in verifying OPNFV
compliance because it validates design patterns and support for the types of
NFVI features that users care about.

There are a lot of projects in OPNFV developing use cases and sample VNFs,
however most are still in early phase and require further enhancements to
become useful additions to the CVP.  Examples such as vIMS, or those which are
not yet available in Danube release, e.g. vCPE, will be valuable additions to
the CVP. These use cases need to be widely accepted, and since they are more
complex, using these VNFs for CVP demands a higher level of community resources
to implement, analyze and document these VNFs.  Hence, use case testing is not
ready for CVP at the time of Danube, but can be incorporated in Euphrates or as
a future roadmap area.

8. Additional capabilities

In addition to the capabilities analyzed above, there are further system
aspects which are of importance for the CVP. These comprise operational and
management aspects such as platform in-place upgrades and platform operational
insights such as telemetry and logging. Further aspects include API backward
compatibility / micro-versioning, workload migration, multi-site federation and
interoperability with workload automation platforms, e.g. ONAP. Finally,
efficiency aspects such as the hardware and energy footprint of the platform
are worth considering in the CVP.

OPNFV is addressing these items on different levels of details in different
projects. However, the contributions developed in these projects are not yet
considered widely available in commercial systems in order to include them in
the CVP. Hence, these aspects are left for inclusion in future releases of the
CVP.



Scope of the Danube-release of the CVP
--------------------------------------

Summarizing the results of the analysis above, the scope of the Danube-release
of the CVP is as follows:

- Test Area: Basic cloud capabilities

  - **OpenStack interoperability test cases excluding object storage**\*
  - **OPNFV-Functest/vPing, including both user data and ssh**
  - *Port security and security groups*
  - *VM life-cycle events*
  - *VM networking*
  - *VM resource scheduling*
  - *Forwarding packets in the data path*

\* The OPNFV CVP utilizes the same set of test cases as the OpenStack
interoperability program *OpenStack Powered Compute*. Passing the OPNFV CVP
does **not** imply that the SUT is certified according to the *OpenStack Powered
Compute* program. *OpenStack Powered Compute* is a trademark of the OpenStack
foundation and the corresponding certification label can only be awarded by the
OpenStack foundation.



- Test Area: SDNVPN

  - *OPNFV-SDNVPN*


- Test Area: IPv6

  - *OPNFV-IPv6
    (Limited to overlay tests, v6Ping)*


- Test Area: High Availability

  - **OPNFV-Yardstick/HA**
    (Limited to service continuity verification of control services)

[Highlighting: **Mandatory test cases**, *Optional test cases*]


These tested areas represent significant advancement in the direction to meet
the CVP's objectives and end-user expectations, and is a good basis for the
initial phase of CVP.

Note: The SUT is limited to NFVI and VIM functions. While testing MANO
component capabilities is out of scope, certain APIs exposed towards MANO are
used by the current OPNFV compliance testing suite. MANO and other operational
elements may be part of the test infrastructure; for example used for workload
deployment and provisioning.


Scope considerations for future CVP releases
--------------------------------------------

Based on the previous analysis, the following items are outside the scope of
the Danube release of the CV but are being considered for inclusion in future
releases:

- service assurance
- use case testing
- platform in-place upgrade
- API backward compatibility / micro-versioning
- workload migration
- multi-site federation
- service function chaining
- platform operational insights, e.g. telemetry, logging
- efficiency, e.g. hardware and energy footprint of the platform
- interoperability with workload automation platforms e.g. ONAP
- resilience
- security and vulnerability scanning
- performance measurements


Criteria for Awarding Compliance
================================

This section provides guidance on compliance criteria for each test area. The
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

.. References
.. _`OPNFV CVP Guidelines`: https://wiki.opnfv.org/display/dovetail/CVP+document
.. _`Pharos specification`: https://wiki.opnfv.org/display/pharos/Pharos+Specification

