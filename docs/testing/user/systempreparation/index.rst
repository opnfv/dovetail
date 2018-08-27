.. This work is licensed under a Creative Commons Attribution 4.0 International
.. License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Huawei, and others

.. _dovetail-system_preparation_guide:

============================
OVP System Preparation Guide
============================

This document provides a general guide to hardware system prerequisites
and expectations for running OPNFV OVP testing. For detailed guide of
preparing software tools and configurations, and conducting the test,
please refer to the User Guide :ref:dovetail-testing_user_guide.

The OVP test tools expect that the hardware of the System Under Test (SUT)
is Pharos compliant `Pharos specification`_

The Pharos specification itself is a general guideline, rather than a set of
specific hard requirements at this time, developed by the OPNFV community. For
the purpose of helping OVP testers, we summarize the main aspects of hardware to
consider in preparation for OVP testing.

As described by the OVP Testing User Guide, the hardware systems involved in
OVP testing includes a Test Node, a System Under Test (SUT) system, and network
connectivity between them.

The Test Node can be a bare metal machine or a virtual machine that can support
Docker container environment. If it is a bare metal machine, it needs to be a
x86 based at this time. Detailed information of how to configure and prepare the
Test Node can be found in the User Guide.

The System Under Test (SUT) system is expected to consist of a set of general
purpose servers, storage devices or systems, and networking infrastructure
connecting them together.
The set of servers are expected to be of the same architecture, either x86-64 or
ARM-64. Mixing different architectures in the same SUT is not supported.

A minimum of 5 servers, 3 configured for controllers and 2 or more configured for compute
resource are expected. However this is not a hard requirement
at this phase. The OVP 1.0 mandatory test cases only require one compute server. At
lease two compute servers are required to pass some of the optional test cases
in the current OVP release. OVP control service high availability tests expect two
or more control nodes to pass, depending on the HA mechanism implemented by the
SUT.

The SUT is also expected to include components for persistent storage. The OVP
testing does not expect or impose significant storage size or performance requirements.

The SUT is expected to be connected with high performance networks. These networks
are expected in the SUT:

- A management network by which the Test Node can reach all identity, image, network,
and compute services in the SUT
- A data network that supports the virtual network capabilities and data path testing

Additional networks, such as Light Out Management or storage networks, may be
beneficial and found in the SUT, but they are not a requirement for OVP testing.

.. References
.. _`Pharos specification`: https://wiki.opnfv.org/display/pharos/Pharos+Specification

