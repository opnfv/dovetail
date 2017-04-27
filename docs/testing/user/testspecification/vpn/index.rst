.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Ericsson AB

======================
VPN test specification
======================

.. toctree::
   :maxdepth: 2

Scope
=====

The VPN test area evaluates the ability of the system under test to support VPN networking
for virtual workdloads.  The tests in this suite will evaluate establishing VPN networks,
publishing and communication between endpoints using BGP and tear down of the networks.

References
================

This test suite assumes support for the following specifications:

- RFC 4364 - BGP/MPLS IP Virtual Private Networks

  - https://tools.ietf.org/html/rfc4364

- RFC 4659 - BGP-MPLS IP Virtual Private Network

  - https://tools.ietf.org/html/rfc4659

- RFC 2547 - BGP/MPLS VPNs

  - https://tools.ietf.org/html/rfc2547

Definitions and abbreviations
=============================

The following terms and abreviations are used in conunction with this test suite

- BGP - Border gateway protocol
- IETF - Internet Engineering Task Force
- NFVi - Network functions virtualization infrastructure
- Tenant - An isolated set of virtualized infrastructures
- VPN - Virtual private network
- VLAN - Virtual local area network

System Under Test (SUT)
=======================

The system under test is assumed to be the NFVi in operation on an Pharos compliant infrastructure.

Test Suite Structure
====================

The test suite is structured in some way that I am unable to articulate at this time.

Test Descriptions
=================

----------------------------------------------------------------
Test Case 1 - VPN provides connectivity between Neutron subnets
----------------------------------------------------------------

Use case specification
----------------------

This test evaluate the instance where an NFVi tenant wants to use a BGPVPN to provide
connectivity between VMs on different Neutron networks and Subnets that reside on different hosts.

Test preconditions
------------------

2 compute nodes are available, denoted Node1 and Node 2 in the following.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Set up VM1 and VM2 on Node1 and VM3 on Node2, all having ports in the same Neutron Network N1
and all having 10.10.10/24 addresses (this subnet is denoted SN1 in the following).

Set up VM4 on Node1 and VM5 on Node2, both having ports in Neutron Network N2
and having 10.10.11/24 addresses (this subnet is denoted SN2 in the following).

* Create VPN1 with eRT<>iRT and associate SN1 to it
* Test action 1: SSH into VM1 and ping VM2, test passes if ping works
* Test action 2: SSH into VM1 and ping VM3, test passes is ping works
* Test action 3: SSH into VM1 and ping VM4, test passes if ping does not work
* Associate SN2 to VPN1
* Test action 4: Ping from VM4 to VM5 should work
* Test action 5: Ping from VM1 to VM4 should not work
* Test action 6: Ping from VM1 to VM5 should not work
* Configure iRT=eRT in VPN1
* Test action 7: Ping from VM1 to VM4 should work
* Test action 8: Ping from VM1 to VM5 should work

The pass criteria for this test case is that all instructions are able to be carried out
according to the described behaviour without deviation.
A negative result will be generated if the above is not met in completion.

Post conditions
---------------

TBD - should there be any other than the system is in the same state it started out as?
