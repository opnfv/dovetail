.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) OPNFV

========================
IPv6 test specification
========================

Scope
=====

The IPv6 test area will evaluate the ability for a SUT to support IPv6
Tenant Network features and functionality. The tests in this test area will
evaluate,

- network, subnet, port, router API CRUD operations
- interface add and remove operations
- security group and security group rule API CRUD operations
- IPv6 address assignment with dual stack, dual net, multiprefix in mode DHCPv6 stateless or SLAAC

References
================

- upstream openstack API reference

  - http://developer.openstack.org/api-ref

- upstream openstack IPv6 reference

  - https://docs.openstack.org/newton/networking-guide/config-ipv6.html

Definitions and abbreviations
=============================

The following terms and abbreviations are used in conjunction with this test area

- API - Application Programming Interface
- CIDR - Classless Inter-Domain Routing
- CRUD - Create, Read, Update, and Delete
- DHCP - Dynamic Host Configuration Protocol
- DHCPv6 - Dynamic Host Configuration Protocol version 6
- ICMP - Internet Control Message Protocol
- NFVI - Network Functions Virtualization Infrastructure
- NIC - Network Interface Controller
- RA - Router Advertisements
- radvd - The Router Advertisement Daemon
- SDN - Software Defined Network
- SLAAC - Stateless Address Auto Configuration
- TCP - Transmission Control Protocol
- UDP - User Datagram Protocol
- VM - Virtual Machine
- vNIC - virtual Network Interface Card

System Under Test (SUT)
=======================

The system under test is assumed to be the NFVI and VIM deployed with a Pharos compliant infrastructure.

Test Area Structure
====================

The test area is structured based on network, port and subnet operations. Each test case
is able to run independently, i.e. irrelevant of the state created by a previous test.

Test Descriptions
=================

API Used and Reference
----------------------

Networks: https://developer.openstack.org/api-ref/networking/v2/index.html#networks

- show network details
- update network
- delete network
- list networks
- create netowrk
- bulk create networks

Subnets: https://developer.openstack.org/api-ref/networking/v2/index.html#subnets

- list subnets
- create subnet
- bulk create subnet
- show subnet details
- update subnet
- delete subnet

Routers and interface: https://developer.openstack.org/api-ref/networking/v2/index.html#routers-routers

- list routers
- create router
- show router details
- update router
- delete router
- add interface to router
- remove interface from router

Ports: https://developer.openstack.org/api-ref/networking/v2/index.html#ports

- show port details
- update port
- delete port
- list port
- create port
- bulk create ports

Security groups: https://developer.openstack.org/api-ref/networking/v2/index.html#security-groups-security-groups

- list security groups
- create security groups
- show security group
- update security group
- delete security group

Security groups rules: https://developer.openstack.org/api-ref/networking/v2/index.html#security-group-rules-security-group-rules

- list security group rules
- create security group rule
- show security group rule
- delete security group rule

Servers: https://developer.openstack.org/api-ref/compute/

- list servers
- create server
- create multiple servers
- list servers detailed
- show server details
- update server
- delete server

All IPv6 api and scenario test cases addressed in OVP are covered in the
following test specification documents.

.. toctree::
   :maxdepth: 2

   ipv6_api.rst
   ipv6_scenario.rst
