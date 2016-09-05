.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Bin Hu (AT&T), Sridhar Gaddam (RedHat) and other contributors

==================================================
IPv6 Compliance Testing Methodology and Test Cases
==================================================

IPv6 Compliance Testing focuses on overlay IPv6 capabilities, i.e. to validate that
IPv6 capability is supported in tenant networks, subnets and routers. Both Tempest API
testing and Tempest Scenario testing are reused  as much as we can in IPv6 Compliance
Testing. In addition, Yardstick Test case 027 is also used to validate a specific use case
of using a Service VM as an IPv6 vRouter.

IPv6 Compliance Testing test cases are described as follows:

---------------------------------------------------------------
Test Case 1: Create and Delete an IPv6 Network, Port and Subnet
---------------------------------------------------------------

.. code-block:: bash

    tempest.api.network.test_networks.BulkNetworkOpsIpV6Test.test_bulk_create_delete_network
    tempest.api.network.test_networks.BulkNetworkOpsIpV6Test.test_bulk_create_delete_port
    tempest.api.network.test_networks.BulkNetworkOpsIpV6Test.test_bulk_create_delete_subnet

-----------------------------------------------------------------
Test Case 2: Create, Update and Delete an IPv6 Network and Subnet
-----------------------------------------------------------------

.. code-block:: bash

    tempest.api.network.test_networks.NetworksIpV6Test.test_create_update_delete_network_subnet
    tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_create_update_delete_network_subnet

----------------------------------------------
Test Case 3: Check External Network Visibility
----------------------------------------------

.. code-block:: bash

    tempest.api.network.test_networks.NetworksIpV6Test.test_external_network_visibility
    tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_external_network_visibility

-------------------------------------------------------
Test Case 4: List IPv6 Networks and Subnets of a Tenant
-------------------------------------------------------

.. code-block:: bash

    tempest.api.network.test_networks.NetworksIpV6Test.test_list_networks
    tempest.api.network.test_networks.NetworksIpV6Test.test_list_subnets
    tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_list_networks
    tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_list_subnets

-----------------------------------------------------------
Test Case 5: Show Information of an IPv6 Network and Subnet
-----------------------------------------------------------

.. code-block:: bash

    tempest.api.network.test_networks.NetworksIpV6Test.test_show_network
    tempest.api.network.test_networks.NetworksIpV6Test.test_show_subnet
    tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_show_network
    tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_show_subnet

------------------------------------------------------------
Test Case 6: Create an IPv6 Port in Allowed Allocation Pools
------------------------------------------------------------

.. code-block:: bash

    tempest.api.network.test_ports.PortsIpV6TestJSON.test_create_port_in_allowed_allocation_pools

--------------------------------------------------------
Test Case 7: Create an IPv6 Port without Security Groups
--------------------------------------------------------

.. code-block:: bash

    tempest.api.network.test_ports.PortsIpV6TestJSON.test_create_port_with_no_securitygroups

---------------------------------------------------
Test Case 8: Create, Update and Delete an IPv6 Port
---------------------------------------------------

.. code-block:: bash

    tempest.api.network.test_ports.PortsIpV6TestJSON.test_create_update_delete_port

----------------------------------------
Test Case 9: List IPv6 Ports of a Tenant
----------------------------------------

.. code-block:: bash

    tempest.api.network.test_ports.PortsIpV6TestJSON.test_list_ports

----------------------------------------------
Test Case 10: Show Information of an IPv6 Port
----------------------------------------------

.. code-block:: bash

    tempest.api.network.test_ports.PortsIpV6TestJSON.test_show_port

--------------------------------------------------------
Test Case 11: Add Multiple Interfaces for an IPv6 Router
--------------------------------------------------------

.. code-block:: bash

    tempest.api.network.test_routers.RoutersIpV6Test.test_add_multiple_router_interfaces

------------------------------------------------------------------
Test Case 12: Add and Remove an IPv6 Router Interface with port_id
------------------------------------------------------------------

.. code-block:: bash

    tempest.api.network.test_routers.RoutersIpV6Test.test_add_remove_router_interface_with_port_id

--------------------------------------------------------------------
Test Case 13: Add and Remove an IPv6 Router Interface with subnet_id
--------------------------------------------------------------------

.. code-block:: bash

    tempest.api.network.test_routers.RoutersIpV6Test.test_add_remove_router_interface_with_subnet_id

------------------------------------------------------------------
Test Case 14: Create, Update, Delete, List and Show an IPv6 Router
------------------------------------------------------------------

.. code-block:: bash

    tempest.api.network.test_routers.RoutersIpV6Test.test_create_show_list_update_delete_router

--------------------------------------------------------------------------
Test Case 15: Create, Update, Delete, List and Show an IPv6 Security Group
--------------------------------------------------------------------------

.. code-block:: bash

    tempest.api.network.test_security_groups.SecGroupIPv6Test.test_create_list_update_show_delete_security_group

----------------------------------------------------------
Test Case 16: Create, Delete and Show Security Group Rules
----------------------------------------------------------

.. code-block:: bash

    tempest.api.network.test_security_groups.SecGroupIPv6Test.test_create_show_delete_security_group_rule

--------------------------------------
Test Case 17: List All Security Groups
--------------------------------------

.. code-block:: bash

    tempest.api.network.test_security_groups.SecGroupIPv6Test.test_list_security_groups

--------------------------------------------------------
Test Case 18: IPv6 Address Assignment - DHCPv6 Stateless
--------------------------------------------------------

.. code-block:: bash

    tempest.scenario.test_network_v6.TestGettingAddress.test_dhcp6_stateless_from_os

--------------------------------------------------------------------
Test Case 19: IPv6 Address Assignment - Dual Stack, DHCPv6 Stateless
--------------------------------------------------------------------

.. code-block:: bash

    tempest.scenario.test_network_v6.TestGettingAddress.test_dualnet_dhcp6_stateless_from_os

---------------------------------------------------------------------------
Test Case 20: IPv6 Address Assignment - Multiple Prefixes, DHCPv6 Stateless
---------------------------------------------------------------------------

.. code-block:: bash

    tempest.scenario.test_network_v6.TestGettingAddress.test_multi_prefix_dhcpv6_stateless

---------------------------------------------------------------------------------------
Test Case 21: IPv6 Address Assignment - Dual Stack, Multiple Prefixes, DHCPv6 Stateless
---------------------------------------------------------------------------------------

.. code-block:: bash

    tempest.scenario.test_network_v6.TestGettingAddress.test_dualnet_multi_prefix_dhcpv6_stateless

---------------------------------------------
Test Case 22: IPv6 Address Assignment - SLAAC
---------------------------------------------

.. code-block:: bash

    tempest.scenario.test_network_v6.TestGettingAddress.test_slaac_from_os

---------------------------------------------------------
Test Case 23: IPv6 Address Assignment - Dual Stack, SLAAC
---------------------------------------------------------

.. code-block:: bash

    tempest.scenario.test_network_v6.TestGettingAddress.test_dualnet_slaac_from_os

----------------------------------------------------------------
Test Case 24: IPv6 Address Assignment - Multiple Prefixes, SLAAC
----------------------------------------------------------------

.. code-block:: bash

    tempest.scenario.test_network_v6.TestGettingAddress.test_multi_prefix_slaac

----------------------------------------------------------------------------
Test Case 25: IPv6 Address Assignment - Dual Stack, Multiple Prefixes, SLAAC
----------------------------------------------------------------------------

.. code-block:: bash

    tempest.scenario.test_network_v6.TestGettingAddress.test_dualnet_multi_prefix_slaac

-------------------------------------------
Test Case 26: Service VM as an IPv6 vRouter
-------------------------------------------

.. code-block:: bash

    # Refer to Yardstick Test Case 027
    # Instruction: http://artifacts.opnfv.org/ipv6/docs/configurationguide/index.html
    # Step 1: Set up Service VM as an IPv6 vRouter
    #    1.1: Install OPNFV and Preparation
    #    1.2: Disable Security Groups in OpenStack ML2 Setup
    #    1.3: Create IPv4 and IPv6 Neutron routers, networks and subnets
    #    1.4: Boot vRouter VM, and Guest VM1 and Guest VM2
    # Step 2: Verify IPv6 Connectivity
    #    2.1: ssh to Guest VM1
    #    2.2: Ping6 from Guest VM1 to Guest VM2
    #    2.3: Ping6 from Guest VM1 to vRouter VM
    #    2.4: Ping6 from Guest VM1 to Neutron IPv6 Router Namespace
    # Step 3: Tear down Setup
    #    3.1: Delete Guest VM1, Guest VM2 and vRouter VM
    #    3.2: Delete IPv4 and IPv6 Neutron routers, networks and subnets
    #    3.3: Enable Security Groups

