.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) OPNFV

======================================================================================
Dovetail IPv6 tc001 specification - Create and Delete an IPv6 Network, Port and Subnet
======================================================================================

.. table::
   :class: longtable

+-----------------------+----------------------------------------------------------------------------------------------------+
|test case name         |Bulk creation and deletion of an IPv6 network, port and subnet                                      |
|                       |                                                                                                    |
+-----------------------+----------------------------------------------------------------------------------------------------+
|id                     |dovetail.ipv6.tc001                                                                                 |
+-----------------------+----------------------------------------------------------------------------------------------------+
|objective              |To verify that platform is able to create/delete networks, ports and subnets                        |
+-----------------------+----------------------------------------------------------------------------------------------------+
|dependent test project |tempest(openstack)/functest(OPNFV)                                                                  |
+-----------------------+----------------------------------------------------------------------------------------------------+
|test items             |tempest.api.network.test_networks.BulkNetworkOpsIpV6Test.test_bulk_create_delete_network            |
|                       |{idempotent_id('d4f9024d-1e28-4fc1-a6b1-25dbc6fa11e2')}                                             |
|                       |tempest.api.network.test_networks.BulkNetworkOpsIpV6Test.test_bulk_create_delete_port               |
|                       |{idempotent_id('48037ff2-e889-4c3b-b86a-8e3f34d2d060')}                                             |
|                       |tempest.api.network.test_networks.BulkNetworkOpsIpV6Test.test_bulk_create_delete_subnet             |
|                       |{idempotent_id('8936533b-c0aa-4f29-8e53-6cc873aec489')}                                             |
+-----------------------+----------------------------------------------------------------------------------------------------+
|environmental          |                                                                                                    |
|requirements &         | environment can be deployed on bare metal of virtualized infrastructure                            |
|preconditions          | deployment can be HA or non-HA                                                                     |
|                       |                                                                                                    |
+-----------------------+----------------------------------------------------------------------------------------------------+
|scenario dependencies  | NA                                                                                                 |
+-----------------------+----------------------------------------------------------------------------------------------------+
|procedural             |Step 1: create/delete network:                                                                      |
|requirements           |     create 2 networks in one request                                                               |
|                       |     asserting that the networks are found in the list after creation                               |
|                       |                                                                                                    |
|                       |Step 2: create/delete subnet:                                                                       |
|                       |     create 2 subnets in one request                                                                |
|                       |     asserting that the subnets are found in the list after creation                                |
|                       |                                                                                                    |
|                       |Step 3: create/delete port:                                                                         |
|                       |     create 2 ports in one request                                                                  |
|                       |     asserting that the ports are found in the list after creation                                  |
|                       |                                                                                                    |
+-----------------------+----------------------------------------------------------------------------------------------------+
|input specifications   |NA                                                                                                  |
+-----------------------+----------------------------------------------------------------------------------------------------+
|output specifications  |success/fail                                                                                        |
+-----------------------+----------------------------------------------------------------------------------------------------+
|pass/fail criteria     |success                                                                                             |
+-----------------------+----------------------------------------------------------------------------------------------------+
|test report            |TBD                                                                                                 |
+-----------------------+----------------------------------------------------------------------------------------------------+
