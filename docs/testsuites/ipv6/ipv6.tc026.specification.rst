.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) OPNFV

==============================================================
Dovetail IPv6 tc026 specification - Service VM as IPv6 vRouter
==============================================================


+-----------------------+--------------------------------------------------------------------------+
|test case name         |Service VM as IPv6 vRouter                                                |
|                       |                                                                          |
+-----------------------+--------------------------------------------------------------------------+
|id                     |dovetail.ipv6.tc026                                                       |
+-----------------------+--------------------------------------------------------------------------+
|objective              |IPv6 connnectivity, service VM as IPv6 vRouter                            |
+-----------------------+--------------------------------------------------------------------------+
|modules under test     |neutron, nova, etc                                                        |
+-----------------------+--------------------------------------------------------------------------+
|dependent test project |yardstick                                                                 |
+-----------------------+--------------------------------------------------------------------------+
|test items             |yardstick_tc027                                                           |
+-----------------------+--------------------------------------------------------------------------+
|environmental          | OpenStack-only environment                                               |
|requirements &         | environment can be deplyed on bare metal of virtualized infrastructure   |
|preconditions          | deployment can be HA or non-HA                                           |
|                       | test case image needs to be installed into Glance with ping6 included    |
+-----------------------+--------------------------------------------------------------------------+
|scenario dependencies  | nosdn                                                                    |
+-----------------------+--------------------------------------------------------------------------+
|procedural             |step 1: to setup IPv6 testing environment                                 |
|requirements           |     1.1 disable security group                                           |
|                       |     1.2 create (ipv6, ipv4) router, network and subnet                   |
|                       |     1.3 create vRouter, VM1, VM2                                         |
|                       |step 2: to run ping6 to verify IPv6 connectivity                          |
|                       |     2.1 ssh to VM1                                                       |
|                       |     2.2 ping6 to ipv6 router from VM1                                    |
|                       |     2.3 get the result and store the logs                                |
|                       |step 3: to teardown IPv6 testing environment                              |
|                       |     3.1 delete vRouter, VM1, VM2                                         |
|                       |     3.2 delete (ipv6, ipv4) router, network and subnet                   |
|                       |     3.3 enable security group                                            |
+-----------------------+--------------------------------------------------------------------------+
|input specifications   |packetsize: 56                                                            |
|                       |ping_count: 5                                                             |
|                       |                                                                          |
+-----------------------+--------------------------------------------------------------------------+
|output specifications  |output includes max_rtt, min_rtt, average_rtt                             |
+-----------------------+--------------------------------------------------------------------------+
|pass/fail criteria     |ping6 connectivity success, no SLA                                        |
+-----------------------+--------------------------------------------------------------------------+
|test report            | dovetail dashboard DB here                                               |
+-----------------------+--------------------------------------------------------------------------+

