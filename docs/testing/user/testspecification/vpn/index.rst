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

The VPN test area evaluates the ability of the system under test to support VPN
networking for virtual workloads.  The tests in this suite will evaluate
establishing VPN networks, publishing and communication between endpoints using
BGP and tear down of the networks.

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

The following terms and abbreviations are used in conjunction with this test
suite

- BGP - Border gateway protocol
- eRT - Export route target
- IETF - Internet Engineering Task Force
- iRT - Import route target
- NFVi - Network functions virtualisation infrastructure
- Tenant - An isolated set of virtualised infrastructures
- VM - Virtual machine
- VPN - Virtual private network
- VLAN - Virtual local area network


System Under Test (SUT)
=======================

The system under test is assumed to be the NFVi in operation on an Pharos
compliant infrastructure.


Test Suite Structure
====================

The test suite is structured as three sequential tests with inherent
dependencies between each test in the suite.  The suite will evaluate the
ability of the SUT to establish connectivity between Virtual Machines (nodes)
using route targets, reconfigure the routing tables to disassociate the nodes,
then reestablish connectivity by re-association.


Test Descriptions
=================

----------------------------------------------------------------
Test Case 1 - VPN provides connectivity between Neutron subnets
----------------------------------------------------------------

Short name
----------

opnfv.sdnvpn.tc01.subnet_connectivity


Use case specification
----------------------

This test evaluates the instance where an NFVi tenant wants to use a BGPVPN to
provide connectivity between VMs on different Neutron networks and subnets that
reside on different hosts.


Test preconditions
------------------

2 compute nodes are available, denoted Node1 and Node2 in the following.


Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Methodology for verifying connectivity
''''''''''''''''''''''''''''''''''''''

Connectivity between VMs is tested by sending ICMP ping packets between
selected VMs. The target IPs are passed to the VMs sending pings by means of a
custom user data script. Whether or not a ping was successful is determined by
checking the console output of the source VMs.


Test execution
''''''''''''''

* Create Neutron network N1 and subnet SN1 with IP range 10.10.10.0/24
* Create Neutron network N2 and subnet SN2 with IP range 10.10.11.0/24

* Create VM1 on Node1 with a port in network N1
* Create VM2 on Node1 with a port in network N1
* Create VM1 on Node2 with a port in network N1
* Create VM4 on Node1 with a port in network N2
* Create VM5 on Node2 with a port in network N2

* Create VPN1 with eRT<>iRT and associate SN1 to it
* **Test action 1:** VM1 pings VM2, test passes if ping works
* **Test action 2:** VM1 pings VM3, test passes is ping works
* **Test action 3:** VM1 pings VM4, test passes if ping does not work

* Associate SN2 to VPN1
* **Test action 4:** VM4 pings VM5, test passes if ping works
* **Test action 5:** VM1 pings VM4, test passes if ping does not work
* **Test action 6:** VM1 pings VM5, test passes if ping does not work

* Configure iRT=eRT in VPN1
* **Test action 7:** VM1 pings VM4, test passes of ping works
* **Test action 8:** VM1 pings VM5, test passes if ping works


Pass / fail criteria
''''''''''''''''''''

The pass criteria for this test case is that all instructions are able to be
carried out according to the described behaviour without deviation.  A negative
result will be generated if the above is not met in completion.


Post conditions
---------------

TBD - should there be any other than the system is in the same state it started out as?



------------------------------------------------------------
Test Case 2 - VPNs ensure traffic separation between tenants
------------------------------------------------------------

Short Name
----------

opnfv.sdnvpn.tc2.tenant_separation


Use case specification
----------------------

This test evaluates if VPNs provide separation of traffic such that overlapping
IP ranges can be used.


Test preconditions
------------------

2 compute nodes are available, denoted Node1 and Node2 in the following.


Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Methodology for verifying connectivity
''''''''''''''''''''''''''''''''''''''

Connectivity between VMs is tested by establishing an SSH connection. Moreover,
the command "hostname" is executed at the remote VM in order to retrieve the
hostname of the remote VM.


Test execution
''''''''''''''

* Create Neutron network N1
* Create subnet SN1a of network N1 with IP range 10.10.10.0/24
* Create subnet SN1b of network N1 with IP range 10.10.11.0/24

* Create Neutron network N2
* Create subnet SN2a of network N2 with IP range 10.10.10.0/24
* Create subnet SN2b of network N2 with IP range 10.10.11.0/24

* Create VM1 on Node1 with a port in network N1 and IP 10.10.10.11.
* Create VM2 on Node1 with a port in network N1 and IP 10.10.10.12.
* Create VM3 on Node2 with a port in network N1 and IP 10.10.11.13.
* Create VM4 on Node1 with a port in network N2 and IP 10.10.10.12.
* Create VM5 on Node2 with a port in network N2 and IP 10.10.11.13.

* Create VPN V1 with iRT=eRT=RT1 and associate N1 to it

* **Test action 1:** VM1 connects to VM2 via SSH. The test passes if VM1 can retrieve the hostname of VM2 via SSH.
* **Test action 2:** VM1 connects to VM3 via SSH. The test passes if VM1 can retrieve the hostname of VM2 via SSH.

* **Test action 3:** VM1 connects to VM4 via SSH. The test passes if VM1 cannot retrieve the hostname of VM4 via SSH.
* **Test action 4:** VM1 connects to VM5 via SSH. The test passes if VM1 cannot retrieve the hostname of VM5 via SSH.

* Create VPN2 with iRT=eRT=RT2 and associate N2 to it
* **Test action 5:** VM4 connects to VM5 via SSH. The test passes if VM4 can retrieve the hostname of VM5 via SSH.
* **Test action 6:** VM4 connects to VM1 via SSH. The test passes if VM4 cannot retrieve the hostname of VM1 via SSH.
* **Test action 7:** VM4 connects to VM3 via SSH. The test passes if VM4 cannot retrieve the hostname of VM3 via SSH.


Pass / fail criteria
''''''''''''''''''''

The pass criteria for this test case is that all instructions are able to be
carried out according to the described behaviour without deviation.  A negative
result will be generated if the above is not met in completion.


Post conditions
---------------

TBD - should there be any other than the system is in the same state it started out as?


--------------------------------------------------------------------------------
Test Case 4 - VPN provides connectivity between subnets using router association
--------------------------------------------------------------------------------

Short Name
----------

opnfv.sdnvpn.tc04.router_association


Use case specification
----------------------

This test evaluates if a VPN provides connectivity between two subnets by
utilizing two different VPN association mechanisms: a router association and a
network association.

Specifically, the test network topology comprises two networks N1 and N2 with
corresponding subnets.  Additionally, network N1 is connected to a router R1.
This test verifies that a VPN V1 provides connectivity between both networks
when applying a router association to router R1 and a network association to
network N2.


Test preconditions
------------------

2 compute nodes are available, denoted Node1 and Node2 in the following.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Methodology for verifying connectivity
''''''''''''''''''''''''''''''''''''''

Connectivity between VMs is tested by sending ICMP ping packets between
selected VMs. The target IPs are passed to the VMs sending pings by means of a
custom user data script. Whether or not a ping was successful is determined by
checking the console output of the source VMs.


Test execution
''''''''''''''

* Create a network N1, a subnet SN1 with IP range 10.10.10.0/24 and a connected router R1
* Create a network N2, a subnet SN2 with IP range 10.10.11.0/24

* Create VM1 on Node1 with a port in network N1
* Create VM2 on Node1 with a port in network N1
* Create VM3 on Node2 with a port in network N1
* Create VM4 on Node1 with a port in network N2
* Create VM5 on Node2 with a port in network N2

* Create VPN1 with eRT<>iRT so that connected subnets should not reach each other and associate R1 to it
* **Test action 1:** VM1 pings VM2, the test passes if the ping works
* **Test action 2:** VM1 pings VM3, the test passes if the ping works
* **Test action 3:** VM1 pings VM4, the test passes if the ping does not work

* Associate SN2 to VPN1
* **Test action 4:** VM4 pings VM5, the test passes if the ping works
* **Test action 5:** VM1 pings VM4, the test passes if the ping does not work
* **Test action 6:** VM1 pings VM5, the test passes if the ping does not work

* Change VPN1 so that iRT=eRT
* **Test action 7:** VM1 pings VM4, the test passes if the ping works
* **Test action 8:** VM1 pings VM5, the test passes if the ping works


Pass / fail criteria
''''''''''''''''''''

The pass criteria for this test case is that all instructions are able to be
carried out according to the described behaviour without deviation.  A negative
result will be generated if the above is not met in completion.


Post conditions
---------------

TBD - should there be any other than the system is in the same state it started out as?



---------------------------------------------------------------------------------------------------
Test Case 8 - Verify interworking of router and network associations with floating IP functionality
---------------------------------------------------------------------------------------------------

Short Name
----------

opnfv.sdnvpn.tc08.router_association_floating_ip


Use case specification
----------------------

This test evaluates if both the router association and network association
mechanisms interwork with floating IP functionality.

Specifically, the test network topology comprises two networks N1 and N2 with
corresponding subnets.  Additionally, network N1 is connected to a router R1.
This test verifies that i) a VPN V1 provides connectivity between both networks
when applying a router association to router R1 and a network association to
network N2 and ii) a VM in network N1 is reachable externally by means of a
floating IP.


Test preconditions
------------------

At least one compute node is available.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Methodology for verifying connectivity
''''''''''''''''''''''''''''''''''''''

Connectivity between VMs is tested by sending ICMP ping packets between
selected VMs. The target IPs are passed to the VMs sending pings by means of a
custom user data script. Whether or not a ping was successful is determined by
checking the console output of the source VMs.


Test execution
''''''''''''''

* Create a network N1, a subnet SN1 with IP range 10.10.10.0/24 and a connected router R1
* Create a network N2 with IP range 10.10.20.0/24

* Create VM1 with a port in network N1
* Create VM2 with a port in network N2

* Create a VPN V1
* Create a router association between router R1 and VPN V1
* Create a network association between network N2 and VPN V1

* **Test action 1:** VM1 pings VM2, the test passes if the ping works

* Assign a floating IP to VM1
* **Test action 2:** Ping the floating IP of VM1 from the host running the test framework


Pass / fail criteria
''''''''''''''''''''

The pass criteria for this test case is that all instructions are able to be
carried out according to the described behaviour without deviation.  A negative
result will be generated if the above is not met in completion.


Post conditions
---------------

TBD - should there be any other than the system is in the same state it started out as?

