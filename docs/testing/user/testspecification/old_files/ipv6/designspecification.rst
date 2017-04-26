.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Christopher Price (Ericsson AB) and others

==============================
IPv6 test design specification
==============================

This document outlines the approach and method for testing IPv6 in the OPNFV compliance test
suite.  Providing a brief outline of the features to be tested, the methodology for testing,
schema's and criteria.

Features to be tested
=====================

The IPv6 compliance test plan outlines the method for testing IPv6 compliance to the OPNFV
platform behaviours and features of IPv6 enabled VNFi platforms.  The specific features to
be tested by the IPv6 compliance test suite is outlined in the following table.

.. table::
   :class: longtable

+-----------------------------------------------------------+-------------------+--------------------------------------------------------------------+
|Features / Requirements                                    |Tests available    | Test Cases                                                         |
+===========================================================+===================+====================================================================+
|All topologies work in a multi-tenant environment          |No                 |                                                                    |
|                                                           |                   |                                                                    |
|                                                           |                   |                                                                    |
|                                                           |                   |                                                                    |
|                                                           |                   |                                                                    |
|                                                           |                   |                                                                    |
+-----------------------------------------------------------+-------------------+--------------------------------------------------------------------+
|IPv6 VM to VM only                                         |No                 |                                                                    |
|                                                           |                   |                                                                    |
|                                                           |                   |                                                                    |
+-----------------------------------------------------------+-------------------+--------------------------------------------------------------------+
|IPv6 external L2 VLAN directly attached to a VM            |No                 |                                                                    |
|                                                           |                   |                                                                    |
+-----------------------------------------------------------+-------------------+--------------------------------------------------------------------+
|IPv6 subnet routed via L3 agent to an external IPv6 network|No                 |                                                                    |
|                                                           |                   |                                                                    |
|1. Both VLAN and overlay (e.g. GRE, VXLAN) subnet attached |                   |                                                                    |
|   to VMs;                                                 |                   |                                                                    |
|2. Must be able to support multiple L3 agents for a given  |                   |                                                                    |
|   external network to support scaling (neutron scheduler  |                   |                                                                    |
|   to assign vRouters to the L3 agents)                    |                   |                                                                    |
+-----------------------------------------------------------+-------------------+--------------------------------------------------------------------+
|Ability for a NIC to support both IPv4 and IPv6 (dual      |No                 |                                                                    |
|stack) address.                                            |                   |                                                                    |
|                                                           |                   |                                                                    |
|1. VM with a single interface associated with a network,   |                   |                                                                    |
|   which is then associated with two subnets.              |                   |                                                                    |
|2. VM with two different interfaces associated with two    |                   |                                                                    |
|   different networks and two different subnets.           |                   |                                                                    |
+-----------------------------------------------------------+-------------------+--------------------------------------------------------------------+
|Support IPv6 Address assignment modes.                     |No                 |                                                                    |
|                                                           |                   |                                                                    |
|1. SLAAC                                                   |                   |                                                                    |
|2. DHCPv6 Stateless                                        |                   |                                                                    |
|3. DHCPv6 Stateful                                         |                   |                                                                    |
+-----------------------------------------------------------+-------------------+--------------------------------------------------------------------+
|Ability to create a port on an IPv6 DHCPv6 Stateful subnet |No                 |                                                                    |
|and assign a specific IPv6 address to the port and have it |                   |                                                                    |
|taken out of the DHCP address pool.                        |                   |                                                                    |
+-----------------------------------------------------------+-------------------+--------------------------------------------------------------------+
|Full support for IPv6 matching (i.e., IPv6, ICMPv6, TCP,   |No                 |                                                                    |
|UDP) in security groups. Ability to control and manage all |                   |                                                                    |
|IPv6 security group capabilities via Neutron/Nova API (REST|                   |                                                                    |
|and CLI) as well as via Horizon.                           |                   |                                                                    |
+-----------------------------------------------------------+-------------------+--------------------------------------------------------------------+
|During network/subnet/router create, there should be an    |No                 |                                                                    |
|option to allow user to specify the type of address        |                   |                                                                    |
|management they would like. This includes all options      |                   |                                                                    |
|including those low priority if implemented (e.g., toggle  |                   |                                                                    |
|on/off router and address prefix advertisements); It must  |                   |                                                                    |
|be supported via Neutron API (REST and CLI) as well as via |                   |                                                                    |
|Horizon                                                    |                   |                                                                    |
+-----------------------------------------------------------+-------------------+--------------------------------------------------------------------+
|Security groups anti-spoofing: Prevent VM from using a     |No                 |                                                                    |
|source IPv6/MAC address which is not assigned to the VM    |                   |                                                                    |
+-----------------------------------------------------------+-------------------+--------------------------------------------------------------------+
|Protect tenant and provider network from rogue RAs         |No                 |                                                                    |
|                                                           |                   |                                                                    |
|                                                           |                   |                                                                    |
|                                                           |                   |                                                                    |
|                                                           |                   |                                                                    |
|                                                           |                   |                                                                    |
+-----------------------------------------------------------+-------------------+--------------------------------------------------------------------+
|Support the ability to assign multiple IPv6 addresses to   |No                 |                                                                    |
|an interface; both for Neutron router interfaces and VM    |                   |                                                                    |
|interfaces.                                                |                   |                                                                    |
+-----------------------------------------------------------+-------------------+--------------------------------------------------------------------+
|Ability for a VM to support a mix of multiple IPv4 and IPv6|No                 |                                                                    |
|networks, including multiples of the same type.            |                   |                                                                    |
+-----------------------------------------------------------+-------------------+--------------------------------------------------------------------+
|Support for IPv6 Prefix Delegation.                        |No                 |                                                                    |
+-----------------------------------------------------------+-------------------+--------------------------------------------------------------------+
|IPv6 First-Hop Security, IPv6 ND spoofing                  |No                 |                                                                    |
+-----------------------------------------------------------+-------------------+--------------------------------------------------------------------+
|IPv6 support in Neutron Layer3 High Availability           |No                 |                                                                    |
|(keepalived+VRRP).                                         |                   |                                                                    |
+-----------------------------------------------------------+-------------------+--------------------------------------------------------------------+


Test approach for IPv6
======================

The most common approach for testing IPv6 capabilities in the test suite is through interaction with the SUT control plane.
In this instance the test framework will exercise the NBI provided by the VIM to configure and leverage IPv6 related features
in the platform, instantiate workloads, and invoke behaviours in the platform.  The suite may also interact directly with the
data plane to exercise platform capabilities and further invoke helper functions on the platform for the same purpose.

Test result analysis
--------------------

All functional tests in the IPv6 test suite will provide a pass/fail result on completion of the test.  In addition test logs
and relevant additional information will be provided as part of the test log, available on test suite completion.

Some tests in the compliance suite measure such metrics as latency and performance.  At this time these tests are intended to
provide a feature based pass/fail metric not related to system performance.
These tests may however provide detailed results of performance and latency in the 'test report'_ document.

Test identification
===================

TBD:  WE need to identify the test naming scheme we will use in DoveTail in order that we can cross reference to the test
projects and maintain our suite effectively.  This naming scheme needs to be externally relevant to non-OPNFV consumers and as
such some consideration is required on the selection.

Pass Fail Criteria
==================

This section requires some further work with the test teams to identify how and where we generate, store and provide results.
