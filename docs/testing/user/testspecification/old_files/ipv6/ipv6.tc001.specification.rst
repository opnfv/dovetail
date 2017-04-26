.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) OPNFV

==================================================================================================
Dovetail IPv6 tc001 specification - Bulk Creation and Deletion of IPv6 Networks, Ports and Subnets
==================================================================================================


+-----------------------+----------------------------------------------------------------------------------------------------+
|test case name         |Bulk creation and deletion of IPv6 networks, ports and subnets                                      |
|                       |                                                                                                    |
+-----------------------+----------------------------------------------------------------------------------------------------+
|id                     |dovetail.ipv6.tc001                                                                                 |
+-----------------------+----------------------------------------------------------------------------------------------------+
|objective              |To verify that platform is able to create/delete networks, ports and subnets in bulk operation      |
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
|input specifications   |The parameters needed to execute Neutron network APIs.                                              |
|                       |Refer to Neutron Networking API v2.0 `[1]`_ `[2]`_                                                  |
+-----------------------+----------------------------------------------------------------------------------------------------+
|output specifications  |The responses after executing Network network APIs.                                                 |
|                       |Refer to Neutron Networking API v2.0 `[1]`_ `[2]`_                                                  |
+-----------------------+----------------------------------------------------------------------------------------------------+
|pass/fail criteria     |If normal response code 200 is returned, the test passes.                                           |
|                       |Otherwise, the test fails with various error codes.                                                 |
|                       |Refer to Neutron Networking API v2.0 `[1]`_ `[2]`_                                                  |
+-----------------------+----------------------------------------------------------------------------------------------------+
|test report            |TBD                                                                                                 |
+-----------------------+----------------------------------------------------------------------------------------------------+

.. _`[1]`: http://developer.openstack.org/api-ref/networking/v2/
.. _`[2]`: http://wiki.openstack.org/wiki/Neutron/APIv2-specification
