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
networking for virtual workloads.  The tests in this test area will evaluate
establishing VPN networks, publishing and communication between endpoints using
BGP and tear down of the networks.

References
==========

This test area evaluates the ability of the system to perform selected actions
defined in the following specifications. Details of specific features evaluated
are described in the test descriptions.

- RFC 4364 - BGP/MPLS IP Virtual Private Networks

  - https://tools.ietf.org/html/rfc4364

- RFC 4659 - BGP-MPLS IP Virtual Private Network

  - https://tools.ietf.org/html/rfc4659

- RFC 2547 - BGP/MPLS VPNs

  - https://tools.ietf.org/html/rfc2547


Definitions and abbreviations
=============================

The following terms and abbreviations are used in conjunction with this test
area

- BGP - Border gateway protocol
- eRT - Export route target
- IETF - Internet Engineering Task Force
- iRT - Import route target
- NFVi - Network functions virtualization infrastructure
- Tenant - An isolated set of virtualized infrastructures
- VM - Virtual machine
- VPN - Virtual private network
- VLAN - Virtual local area network


System Under Test (SUT)
=======================

The system under test is assumed to be the NFVi and VIM in operation on a
Pharos compliant infrastructure.


Test Area Structure
===================

The test area is structured in four separate tests which are executed
sequentially. The order of the tests is arbitrary as there are no dependencies
across the tests. Specifially, every test performs clean-up operations which
return the system to the same state as before the test.

The test area evaluates the ability of the SUT to establish connectivity
between Virtual Machines using an appropriate route target configuration,
reconfigure the route targets to remove connectivity between the VMs, then
reestablish connectivity by re-association.


Test Descriptions
=================

----------------------------------------------------------------
Test Case 1 - VPN provides connectivity between Neutron subnets
----------------------------------------------------------------

Short name
----------

dovetail.sdnvpn.subnet_connectivity


Use case specification
----------------------

This test evaluates the use case where an NFVi tenant uses a BGPVPN to provide
connectivity between VMs on different Neutron networks and subnets that reside
on different hosts.


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
* Create VM3 on Node2 with a port in network N1
* Create VM4 on Node1 with a port in network N2
* Create VM5 on Node2 with a port in network N2

* Create VPN1 with eRT<>iRT
* Create network association between network N1 and VPN1

* VM1 sends ICMP packets to VM2 using ``ping``

* **Test assertion 1:** Ping from VM1 to VM2 succeeds: ``ping`` exits with return code 0

* VM1 sends ICMP packets to VM3 using ``ping``

* **Test assertion 2:** Ping from VM1 to VM3 succeeds: ``ping`` exits with return code 0

* VM1 sends ICMP packets to VM4 using ``ping``

* **Test assertion 3:** Ping from VM1 to VM4 fails: ``ping`` exits with a non-zero return code

* Create network association between network N2 and VPN1

* VM4 sends ICMP packets to VM5 using ``ping``

* **Test assertion 4:** Ping from VM4 to VM5 succeeds: ``ping`` exits with return code 0

* Configure iRT=eRT in VPN1

* VM1 sends ICMP packets to VM4 using ``ping``

* **Test assertion 5:** Ping from VM1 to VM4 succeeds: ``ping`` exits with return code 0

* VM1 sends ICMP packets to VM5 using ``ping``

* **Test assertion 6:** Ping from VM1 to VM5 succeeds: ``ping`` exits with return code 0

* Delete all instances: VM1, VM2, VM3, VM4 and VM5

* Delete all networks and subnets: networks N1 and N2 including subnets SN1 and SN2

* Delete all network associations and VPN1


Pass / fail criteria
''''''''''''''''''''

This test evaluates the capability of the NFVi and VIM to provide routed IP
connectivity between VMs by means of BGP/MPLS VPNs. Specifically, the test
verifies that:

* VMs in the same Neutron subnet have IP connectivity regardless of BGP/MPLS
  VPNs (test assertion 1, 2, 4)

* VMs in different Neutron subnets do not have IP connectivity by default - in
  this case without associating VPNs with the same import and export route
  targets to the Neutron networks (test assertion 3)

* VMs in different Neutron subnets have routed IP connectivity after
  associating both networks with BGP/MPLS VPNs which have been configured with
  the same import and export route targets (test assertion 5, 6). Hence,
  adjusting the ingress and egress route targets enables as well as prohibits
  routing.

In order to pass this test, all test assertions listed in the test execution
above need to pass.


Post conditions
---------------

N/A

------------------------------------------------------------
Test Case 2 - VPNs ensure traffic separation between tenants
------------------------------------------------------------

Short Name
----------

dovetail.sdnvpn.tenant_separation


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
hostname of the remote VM. The retrieved hostname is furthermore compared
against an expected value. This is used to verify tenant traffic separation,
i.e., despite overlapping IPs, a connection is made to the correct VM as
determined by means of the hostname of the target VM.



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

* Create VPN1 with iRT=eRT=RT1
* Create network association between network N1 and VPN1

* VM1 attempts to execute the command ``hostname`` on the VM with IP 10.10.10.12 via SSH.

* **Test assertion 1:** VM1 can successfully connect to the VM with IP
  10.10.10.12. via SSH and execute the remote command ``hostname``. The
  retrieved hostname equals the hostname of VM2.

* VM1 attempts to execute the command ``hostname`` on the VM with IP 10.10.11.13 via SSH.

* **Test assertion 2:** VM1 can successfully connect to the VM with IP
  10.10.11.13 via SSH and execute the remote command ``hostname``. The
  retrieved hostname equals the hostname of VM3.

* Create VPN2 with iRT=eRT=RT2
* Create network association between network N2 and VPN2

* VM4 attempts to execute the command ``hostname`` on the VM with IP 10.10.11.13 via SSH.

* **Test assertion 3:** VM4 can successfully connect to the VM with IP
  10.10.11.13 via SSH and execute the remote command ``hostname``. The
  retrieved hostname equals the hostname of VM5.

* VM4 attempts to execute the command ``hostname`` on the VM with IP 10.10.11.11 via SSH.

* **Test assertion 4:** VM4 cannot connect to the VM with IP 10.10.11.11 via SSH.

* Delete all instances: VM1, VM2, VM3, VM4 and VM5

* Delete all networks and subnets: networks N1 and N2 including subnets SN1a, SN1b, SN2a and SN2b

* Delete all network associations, VPN1 and VPN2


Pass / fail criteria
''''''''''''''''''''

This test evaluates the capability of the NFVi and VIM to provide routed IP
connectivity between VMs by means of BGP/MPLS VPNs. Specifically, the test
verifies that:

* VMs in the same Neutron subnet (still) have IP connectivity between each
  other when a BGP/MPLS VPN is associated with the network (test assertion 1).

* VMs in different Neutron subnets have routed IP connectivity between each
  other when BGP/MPLS VPNs with the same import and expert route targets are
  associated with both networks (assertion 2).

* VMs in different Neutron networks and BGP/MPLS VPNs with different import and
  export route targets can have overlapping IP ranges. The BGP/MPLS VPNs
  provide traffic separation (assertion 3 and 4).

In order to pass this test, all test assertions listed in the test execution
above need to pass.


Post conditions
---------------

N/A

--------------------------------------------------------------------------------
Test Case 3 - VPN provides connectivity between subnets using router association
--------------------------------------------------------------------------------

Short Name
----------

dovetail.sdnvpn.router_association


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

* Create VPN1 with eRT<>iRT so that connected subnets should not reach each other

* Create route association between router R1 and VPN1

* VM1 sends ICMP packets to VM2 using ``ping``

* **Test assertion 1:** Ping from VM1 to VM2 succeeds: ``ping`` exits with return code 0

* VM1 sends ICMP packets to VM3 using ``ping``

* **Test assertion 2:** Ping from VM1 to VM3 succeeds: ``ping`` exits with return code 0

* VM1 sends ICMP packets to VM4 using ``ping``

* **Test assertion 3:** Ping from VM1 to VM4 fails: ``ping`` exits with a non-zero return code

* Create network association between network N2 and VPN1

* VM4 sends ICMP packets to VM5 using ``ping``

* **Test assertion 4:** Ping from VM4 to VM5 succeeds: ``ping`` exits with return code 0

* Change VPN1 so that iRT=eRT

* VM1 sends ICMP packets to VM4 using ``ping``

* **Test assertion 5:** Ping from VM1 to VM4 succeeds: ``ping`` exits with return code 0

* VM1 sends ICMP packets to VM5 using ``ping``

* **Test assertion 6:** Ping from VM1 to VM5 succeeds: ``ping`` exits with return code 0

* Delete all instances: VM1, VM2, VM3, VM4 and VM5

* Delete all networks, subnets and routers: networks N1 and N2 including subnets SN1 and SN2, router R1

* Delete all network and router  associations and VPN1


Pass / fail criteria
''''''''''''''''''''

This test evaluates the capability of the NFVi and VIM to provide routed IP
connectivity between VMs by means of BGP/MPLS VPNs. Specifically, the test
verifies that:

* VMs in the same Neutron subnet have IP connectivity regardless of the import
  and export route target configuration of BGP/MPLS VPNs (test assertion 1, 2, 4)

* VMs in different Neutron subnets do not have IP connectivity by default - in
  this case without associating VPNs with the same import and export route
  targets to the Neutron networks or connected Neutron routers (test assertion 3).

* VMs in two different Neutron subnets have routed IP connectivity after
  associating the first network and a router connected to the second network
  with BGP/MPLS VPNs which have been configured with the same import and export
  route targets (test assertion 5, 6).  Hence, adjusting the ingress and egress
  route targets enables as well as prohibits routing.

* Network and router associations are equivalent methods for binding Neutron networks
  to VPN.

In order to pass this test, all test assertions listed in the test execution
above need to pass.


Post conditions
---------------

N/A

---------------------------------------------------------------------------------------------------
Test Case 4 - Verify interworking of router and network associations with floating IP functionality
---------------------------------------------------------------------------------------------------

Short Name
----------

dovetail.sdnvpn.router_association_floating_ip


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

* Create VPN1
* Create a router association between router R1 and VPN1
* Create a network association between network N2 and VPN1


* VM1 sends ICMP packets to VM2 using ``ping``

* **Test assertion 1:** Ping from VM1 to VM2 succeeds: ``ping`` exits with return code 0

* Assign a floating IP to VM1

* The host running the test framework sends ICMP packets to VM1 using ``ping``

* **Test assertion 2:** Ping from the host running the test framework to the
  floating IP of VM1 succeeds: ``ping`` exits with return code 0

* Delete floating IP assigned to VM1

* Delete all instances: VM1, VM2

* Delete all networks, subnets and routers: networks N1 and N2 including subnets SN1 and SN2, router R1

* Delete all network and router associations as well as VPN1


Pass / fail criteria
''''''''''''''''''''

This test evaluates the capability of the NFVi and VIM to provide routed IP
connectivity between VMs by means of BGP/MPLS VPNs. Specifically, the test
verifies that:

* VMs in the same Neutron subnet have IP connectivity regardless of the import
  and export route target configuration of BGP/MPLS VPNs (test assertion 1)

* VMs connected to a network which has been associated with a BGP/MPLS VPN are
  reachable through floating IPs.

In order to pass this test, all test assertions listed in the test execution
above need to pass.


Post conditions
---------------

N/A
