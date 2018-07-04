.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) OPNFV

----------------------------------------------------------------------------
Test Case 1 - IPv6 Address Assignment - Dual Stack, SLAAC, DHCPv6 Stateless
----------------------------------------------------------------------------

Short name
----------

dovetail.tempest.ipv6_scenario.dhcpv6_stateless

Use case specification
----------------------

This test case evaluates IPv6 address assignment in ipv6_ra_mode 'dhcpv6_stateless'
and ipv6_address_mode 'dhcpv6_stateless'.
In this case, guest instance obtains IPv6 address from OpenStack managed radvd
using SLAAC and optional info from dnsmasq using DHCPv6 stateless. This test case then
verifies the ping6 available VM can ping the other VM's v4 and v6 addresses
as well as the v6 subnet's gateway ip in the same network, the reference is

tempest.scenario.test_network_v6.TestGettingAddress.test_dhcp6_stateless_from_os

Test preconditions
------------------

There should exist a public router or a public network.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
'''''''''''''''

* Test action 1: Create one network, storing the "id" parameter returned in the response
* Test action 2: Create one IPv4 subnet of the created network, storing the "id"
  parameter returned in the response
* Test action 3: If there exists a public router, use it as the router. Otherwise,
  use the public network to create a router
* Test action 4: Connect the IPv4 subnet to the router, using the stored IPv4 subnet id
* Test action 5: Create one IPv6 subnet of the network created in test action 1 in
  ipv6_ra_mode 'dhcpv6_stateless' and ipv6_address_mode 'dhcpv6_stateless',
  storing the "id" parameter returned in the response
* Test action 6: Connect the IPv6 subnet to the router, using the stored IPv6 subnet id
* Test action 7: Boot two VMs on this network, storing the "id" parameters returned in the response
* **Test assertion 1:** The vNIC of each VM gets one v4 address and one v6 address actually assigned
* **Test assertion 2:** Each VM can ping the other's v4 private address
* **Test assertion 3:** The ping6 available VM can ping the other's v6 address
  as well as the v6 subnet's gateway ip
* Test action 8: Delete the 2 VMs created in test action 7, using the stored ids
* Test action 9: List all VMs, verifying the ids are no longer present
* **Test assertion 4:** The two "id" parameters are not present in the VM list
* Test action 10: Delete the IPv4 subnet created in test action 2, using the stored id
* Test action 11: Delete the IPv6 subnet created in test action 5, using the stored id
* Test action 12: List all subnets, verifying the ids are no longer present
* **Test assertion 5:** The "id" parameters of IPv4 and IPv6 are not present in the list
* Test action 13: Delete the network created in test action 1, using the stored id
* Test action 14: List all networks, verifying the id is no longer present
* **Test assertion 6:** The "id" parameter is not present in the network list

Pass / fail criteria
'''''''''''''''''''''

This test evaluates the ability to assign IPv6 addresses in ipv6_ra_mode
'dhcpv6_stateless' and ipv6_address_mode 'dhcpv6_stateless',
and verify the ping6 available VM can ping the other VM's v4 and v6 addresses as well as
the v6 subnet's gateway ip in the same network. Specifically it verifies that:

* The IPv6 addresses in mode 'dhcpv6_stateless' assigned successfully
* The VM can ping the other VM's IPv4 and IPv6 private addresses as well as the v6 subnet's gateway ip
* All items created using create commands are able to be removed using the returned identifiers

Post conditions
---------------

None

--------------------------------------------------------------------------------------
Test Case 2 - IPv6 Address Assignment - Dual Net, Dual Stack, SLAAC, DHCPv6 Stateless
--------------------------------------------------------------------------------------

Short name
----------

dovetail.tempest.ipv6_scenario.dualnet_dhcpv6_stateless

Use case specification
----------------------

This test case evaluates IPv6 address assignment in ipv6_ra_mode 'dhcpv6_stateless'
and ipv6_address_mode 'dhcpv6_stateless'.
In this case, guest instance obtains IPv6 address from OpenStack managed radvd
using SLAAC and optional info from dnsmasq using DHCPv6 stateless. This test case then
verifies the ping6 available VM can ping the other VM's v4 address in one network
and v6 address in another network as well as the v6 subnet's gateway ip, the reference is

tempest.scenario.test_network_v6.TestGettingAddress.test_dualnet_dhcp6_stateless_from_os

Test preconditions
------------------

There should exists a public router or a public network.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
'''''''''''''''

* Test action 1: Create one network, storing the "id" parameter returned in the response
* Test action 2: Create one IPv4 subnet of the created network, storing the "id"
  parameter returned in the response
* Test action 3: If there exists a public router, use it as the router. Otherwise,
  use the public network to create a router
* Test action 4: Connect the IPv4 subnet to the router, using the stored IPv4 subnet id
* Test action 5: Create another network, storing the "id" parameter returned in the response
* Test action 6: Create one IPv6 subnet of network created in test action 5 in
  ipv6_ra_mode 'dhcpv6_stateless' and ipv6_address_mode 'dhcpv6_stateless',
  storing the "id" parameter returned in the response
* Test action 7: Connect the IPv6 subnet to the router, using the stored IPv6 subnet id
* Test action 8: Boot two VMs on these two networks, storing the "id" parameters returned in the response
* Test action 9: Turn on 2nd NIC of each VM for the network created in test action 5
* **Test assertion 1:** The 1st vNIC of each VM gets one v4 address assigned and
  the 2nd vNIC of each VM gets one v6 address actually assigned
* **Test assertion 2:** Each VM can ping the other's v4 private address
* **Test assertion 3:** The ping6 available VM can ping the other's v6 address
  as well as the v6 subnet's gateway ip
* Test action 10: Delete the 2 VMs created in test action 8, using the stored ids
* Test action 11: List all VMs, verifying the ids are no longer present
* **Test assertion 4:** The two "id" parameters are not present in the VM list
* Test action 12: Delete the IPv4 subnet created in test action 2, using the stored id
* Test action 13: Delete the IPv6 subnet created in test action 6, using the stored id
* Test action 14: List all subnets, verifying the ids are no longer present
* **Test assertion 5:** The "id" parameters of IPv4 and IPv6 are not present in the list
* Test action 15: Delete the 2 networks created in test action 1 and 5, using the stored ids
* Test action 16: List all networks, verifying the ids are no longer present
* **Test assertion 6:** The two "id" parameters are not present in the network list

Pass / fail criteria
''''''''''''''''''''

This test evaluates the ability to assign IPv6 addresses in ipv6_ra_mode 'dhcpv6_stateless'
and ipv6_address_mode 'dhcpv6_stateless', and verify the ping6 available VM can ping
the other VM's v4 address in one network and v6 address in another network as well as
the v6 subnet's gateway ip. Specifically it verifies that:

* The IPv6 addresses in mode 'dhcpv6_stateless' assigned successfully
* The VM can ping the other VM's IPv4 address in one network and IPv6 address in another
  network as well as the v6 subnet's gateway ip
* All items created using create commands are able to be removed using the returned identifiers

Post conditions
---------------

None

-----------------------------------------------------------------------------------------------
Test Case 3 - IPv6 Address Assignment - Multiple Prefixes, Dual Stack, SLAAC, DHCPv6 Stateless
-----------------------------------------------------------------------------------------------

Short name
----------

dovetail.tempest.ipv6_scenario.multiple_prefixes_dhcpv6_stateless

Use case specification
----------------------

This test case evaluates IPv6 address assignment in ipv6_ra_mode 'dhcpv6_stateless'
and ipv6_address_mode 'dhcpv6_stateless'.
In this case, guest instance obtains IPv6 addresses from OpenStack managed radvd
using SLAAC and optional info from dnsmasq using DHCPv6 stateless. This test case then
verifies the ping6 available VM can ping the other VM's one v4 address and two v6
addresses with different prefixes as well as the v6 subnets' gateway ips in the
same network, the reference is

tempest.scenario.test_network_v6.TestGettingAddress.test_multi_prefix_dhcpv6_stateless

Test preconditions
------------------

There should exist a public router or a public network.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
'''''''''''''''

* Test action 1: Create one network, storing the "id" parameter returned in the response
* Test action 2: Create one IPv4 subnet of the created network, storing the "id"
  parameter returned in the response
* Test action 3: If there exists a public router, use it as the router. Otherwise,
  use the public network to create a router
* Test action 4: Connect the IPv4 subnet to the router, using the stored IPv4 subnet id
* Test action 5: Create two IPv6 subnets of the network created in test action 1 in
  ipv6_ra_mode 'dhcpv6_stateless' and ipv6_address_mode 'dhcpv6_stateless',
  storing the "id" parameters returned in the response
* Test action 6: Connect the two IPv6 subnets to the router, using the stored IPv6 subnet ids
* Test action 7: Boot two VMs on this network, storing the "id" parameters returned in the response
* **Test assertion 1:** The vNIC of each VM gets one v4 address and two v6 addresses with
  different prefixes actually assigned
* **Test assertion 2:** Each VM can ping the other's v4 private address
* **Test assertion 3:** The ping6 available VM can ping the other's v6 addresses
  as well as the v6 subnets' gateway ips
* Test action 8: Delete the 2 VMs created in test action 7, using the stored ids
* Test action 9: List all VMs, verifying the ids are no longer present
* **Test assertion 4:** The two "id" parameters are not present in the VM list
* Test action 10: Delete the IPv4 subnet created in test action 2, using the stored id
* Test action 11: Delete two IPv6 subnets created in test action 5, using the stored ids
* Test action 12: List all subnets, verifying the ids are no longer present
* **Test assertion 5:** The "id" parameters of IPv4 and IPv6 are not present in the list
* Test action 13: Delete the network created in test action 1, using the stored id
* Test action 14: List all networks, verifying the id is no longer present
* **Test assertion 6:** The "id" parameter is not present in the network list

Pass / fail criteria
'''''''''''''''''''''

This test evaluates the ability to assign IPv6 addresses in ipv6_ra_mode 'dhcpv6_stateless'
and ipv6_address_mode 'dhcpv6_stateless',
and verify the ping6 available VM can ping the other VM's v4 address and two
v6 addresses with different prefixes as well as the v6 subnets' gateway ips in the same network.
Specifically it verifies that:

* The different prefixes IPv6 addresses in mode 'dhcpv6_stateless' assigned successfully
* The VM can ping the other VM's IPv4 and IPv6 private addresses as well as the v6 subnets' gateway ips
* All items created using create commands are able to be removed using the returned identifiers

Post conditions
---------------

None

---------------------------------------------------------------------------------------------------------
Test Case 4 - IPv6 Address Assignment - Dual Net, Multiple Prefixes, Dual Stack, SLAAC, DHCPv6 Stateless
---------------------------------------------------------------------------------------------------------

Short name
----------

dovetail.tempest.ipv6_scenario.dualnet_multiple_prefixes_dhcpv6_stateless

Use case specification
----------------------

This test case evaluates IPv6 address assignment in ipv6_ra_mode 'dhcpv6_stateless'
and ipv6_address_mode 'dhcpv6_stateless'.
In this case, guest instance obtains IPv6 addresses from OpenStack managed radvd
using SLAAC and optional info from dnsmasq using DHCPv6 stateless. This test case then
verifies the ping6 available VM can ping the other VM's v4 address in one network
and two v6 addresses with different prefixes in another network as well as the
v6 subnets' gateway ips, the reference is

tempest.scenario.test_network_v6.TestGettingAddress.test_dualnet_multi_prefix_dhcpv6_stateless

Test preconditions
------------------

There should exist a public router or a public network.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
'''''''''''''''

* Test action 1: Create one network, storing the "id" parameter returned in the response
* Test action 2: Create one IPv4 subnet of the created network, storing the "id"
  parameter returned in the response
* Test action 3: If there exists a public router, use it as the router. Otherwise,
  use the public network to create a router
* Test action 4: Connect the IPv4 subnet to the router, using the stored IPv4 subnet id
* Test action 5: Create another network, storing the "id" parameter returned in the response
* Test action 6: Create two IPv6 subnets of network created in test action 5 in
  ipv6_ra_mode 'dhcpv6_stateless' and ipv6_address_mode 'dhcpv6_stateless',
  storing the "id" parameters returned in the response
* Test action 7: Connect the two IPv6 subnets to the router, using the stored IPv6 subnet ids
* Test action 8: Boot two VMs on these two networks, storing the "id" parameters returned in the response
* Test action 9: Turn on 2nd NIC of each VM for the network created in test action 5
* **Test assertion 1:** The vNIC of each VM gets one v4 address and two v6 addresses
  with different prefixes actually assigned
* **Test assertion 2:** Each VM can ping the other's v4 private address
* **Test assertion 3:** The ping6 available VM can ping the other's v6 addresses
  as well as the v6 subnets' gateway ips
* Test action 10: Delete the 2 VMs created in test action 8, using the stored ids
* Test action 11: List all VMs, verifying the ids are no longer present
* **Test assertion 4:** The two "id" parameters are not present in the VM list
* Test action 12: Delete the IPv4 subnet created in test action 2, using the stored id
* Test action 13: Delete two IPv6 subnets created in test action 6, using the stored ids
* Test action 14: List all subnets, verifying the ids are no longer present
* **Test assertion 5:** The "id" parameters of IPv4 and IPv6 are not present in the list
* Test action 15: Delete the 2 networks created in test action 1 and 5, using the stored ids
* Test action 16: List all networks, verifying the ids are no longer present
* **Test assertion 6:** The two "id" parameters are not present in the network list

Pass / fail criteria
'''''''''''''''''''''

This test evaluates the ability to assign IPv6 addresses in ipv6_ra_mode 'dhcpv6_stateless'
and ipv6_address_mode 'dhcpv6_stateless',
and verify the ping6 available VM can ping the other VM's v4 address in one network and two
v6 addresses with different prefixes in another network as well as the v6 subnets'
gateway ips. Specifically it verifies that:

* The IPv6 addresses in mode 'dhcpv6_stateless' assigned successfully
* The VM can ping the other VM's IPv4 and IPv6 private addresses as well as the v6 subnets' gateway ips
* All items created using create commands are able to be removed using the returned identifiers

Post conditions
---------------

None

----------------------------------------------------------
Test Case 5 - IPv6 Address Assignment - Dual Stack, SLAAC
----------------------------------------------------------

Short name
----------

dovetail.tempest.ipv6_scenario.slaac

Use case specification
----------------------

This test case evaluates IPv6 address assignment in ipv6_ra_mode 'slaac' and
ipv6_address_mode 'slaac'.
In this case, guest instance obtains IPv6 address from OpenStack managed radvd
using SLAAC. This test case then verifies the ping6 available VM can ping the other
VM's v4 and v6 addresses as well as the v6 subnet's gateway ip in the
same network, the reference is

tempest.scenario.test_network_v6.TestGettingAddress.test_slaac_from_os

Test preconditions
------------------

There should exist a public router or a public network.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
'''''''''''''''

* Test action 1: Create one network, storing the "id" parameter returned in the response
* Test action 2: Create one IPv4 subnet of the created network, storing the "id"
  parameter returned in the response
* Test action 3: If there exists a public router, use it as the router. Otherwise,
  use the public network to create a router
* Test action 4: Connect the IPv4 subnet to the router, using the stored IPv4 subnet id
* Test action 5: Create one IPv6 subnet of the network created in test action 1 in
  ipv6_ra_mode 'slaac' and ipv6_address_mode 'slaac', storing the "id" parameter returned in the response
* Test action 6: Connect the IPv6 subnet to the router, using the stored IPv6 subnet id
* Test action 7: Boot two VMs on this network, storing the "id" parameters returned in the response
* **Test assertion 1:** The vNIC of each VM gets one v4 address and one v6 address actually assigned
* **Test assertion 2:** Each VM can ping the other's v4 private address
* **Test assertion 3:** The ping6 available VM can ping the other's v6 address
  as well as the v6 subnet's gateway ip
* Test action 8: Delete the 2 VMs created in test action 7, using the stored ids
* Test action 9: List all VMs, verifying the ids are no longer present
* **Test assertion 4:** The two "id" parameters are not present in the VM list
* Test action 10: Delete the IPv4 subnet created in test action 2, using the stored id
* Test action 11: Delete the IPv6 subnet created in test action 5, using the stored id
* Test action 12: List all subnets, verifying the ids are no longer present
* **Test assertion 5:** The "id" parameters of IPv4 and IPv6 are not present in the list
* Test action 13: Delete the network created in test action 1, using the stored id
* Test action 14: List all networks, verifying the id is no longer present
* **Test assertion 6:** The "id" parameter is not present in the network list

Pass / fail criteria
'''''''''''''''''''''

This test evaluates the ability to assign IPv6 addresses in ipv6_ra_mode 'slaac'
and ipv6_address_mode 'slaac',
and verify the ping6 available VM can ping the other VM's v4 and v6 addresses as well as
the v6 subnet's gateway ip in the same network. Specifically it verifies that:

* The IPv6 addresses in mode 'slaac' assigned successfully
* The VM can ping the other VM's IPv4 and IPv6 private addresses as well as the v6 subnet's gateway ip
* All items created using create commands are able to be removed using the returned identifiers

Post conditions
---------------

None

--------------------------------------------------------------------
Test Case 6 - IPv6 Address Assignment - Dual Net, Dual Stack, SLAAC
--------------------------------------------------------------------

Short name
----------

dovetail.tempest.ipv6_scenario.dualnet_slaac

Use case specification
----------------------

This test case evaluates IPv6 address assignment in ipv6_ra_mode 'slaac' and
ipv6_address_mode 'slaac'.
In this case, guest instance obtains IPv6 address from OpenStack managed radvd
using SLAAC. This test case then verifies the ping6 available VM can ping the other
VM's v4 address in one network and v6 address in another network as well as the
v6 subnet's gateway ip, the reference is

tempest.scenario.test_network_v6.TestGettingAddress.test_dualnet_slaac_from_os

Test preconditions
------------------

There should exist a public router or a public network.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
'''''''''''''''

* Test action 1: Create one network, storing the "id" parameter returned in the response
* Test action 2: Create one IPv4 subnet of the created network, storing the "id"
  parameter returned in the response
* Test action 3: If there exists a public router, use it as the router. Otherwise,
  use the public network to create a router
* Test action 4: Connect the IPv4 subnet to the router, using the stored IPv4 subnet id
* Test action 5: Create another network, storing the "id" parameter returned in the response
* Test action 6: Create one IPv6 subnet of network created in test action 5 in
  ipv6_ra_mode 'slaac' and ipv6_address_mode 'slaac', storing the "id" parameter returned in the response
* Test action 7: Connect the IPv6 subnet to the router, using the stored IPv6 subnet id
* Test action 8: Boot two VMs on these two networks, storing the "id" parameters returned in the response
* Test action 9: Turn on 2nd NIC of each VM for the network created in test action 5
* **Test assertion 1:** The 1st vNIC of each VM gets one v4 address assigned and
  the 2nd vNIC of each VM gets one v6 address actually assigned
* **Test assertion 2:** Each VM can ping the other's v4 private address
* **Test assertion 3:** The ping6 available VM can ping the other's v6 address
  as well as the v6 subnet's gateway ip
* Test action 10: Delete the 2 VMs created in test action 8, using the stored ids
* Test action 11: List all VMs, verifying the ids are no longer present
* **Test assertion 4:** The two "id" parameters are not present in the VM list
* Test action 12: Delete the IPv4 subnet created in test action 2, using the stored id
* Test action 13: Delete the IPv6 subnet created in test action 6, using the stored id
* Test action 14: List all subnets, verifying the ids are no longer present
* **Test assertion 5:** The "id" parameters of IPv4 and IPv6 are not present in the list
* Test action 15: Delete the 2 networks created in test action 1 and 5, using the stored ids
* Test action 16: List all networks, verifying the ids are no longer present
* **Test assertion 6:** The two "id" parameters are not present in the network list

Pass / fail criteria
'''''''''''''''''''''

This test evaluates the ability to assign IPv6 addresses in ipv6_ra_mode 'slaac'
and ipv6_address_mode 'slaac',
and verify the ping6 available VM can ping the other VM's v4 address in one network and
v6 address in another network as well as the v6 subnet's gateway ip. Specifically it verifies that:

* The IPv6 addresses in mode 'slaac' assigned successfully
* The VM can ping the other VM's IPv4 address in one network and IPv6 address
  in another network as well as the v6 subnet's gateway ip
* All items created using create commands are able to be removed using the returned identifiers

Post conditions
---------------

None

-----------------------------------------------------------------------------
Test Case 7 - IPv6 Address Assignment - Multiple Prefixes, Dual Stack, SLAAC
-----------------------------------------------------------------------------

Short name
----------

dovetail.tempest.ipv6_scenario.multiple_prefixes_slaac

Use case specification
----------------------

This test case evaluates IPv6 address assignment in ipv6_ra_mode 'slaac' and
ipv6_address_mode 'slaac'.
In this case, guest instance obtains IPv6 addresses from OpenStack managed radvd
using SLAAC. This test case then verifies the ping6 available VM can ping the other
VM's one v4 address and two v6 addresses with different prefixes as well as the v6
subnets' gateway ips in the same network, the reference is

tempest.scenario.test_network_v6.TestGettingAddress.test_multi_prefix_slaac

Test preconditions
------------------

There should exists a public router or a public network.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
'''''''''''''''

* Test action 1: Create one network, storing the "id" parameter returned in the response
* Test action 2: Create one IPv4 subnet of the created network, storing the "id
  parameter returned in the response
* Test action 3: If there exists a public router, use it as the router. Otherwise,
  use the public network to create a router
* Test action 4: Connect the IPv4 subnet to the router, using the stored IPv4 subnet id
* Test action 5: Create two IPv6 subnets of the network created in test action 1 in
  ipv6_ra_mode 'slaac' and ipv6_address_mode 'slaac', storing the "id" parameters returned in the response
* Test action 6: Connect the two IPv6 subnets to the router, using the stored IPv6 subnet ids
* Test action 7: Boot two VMs on this network, storing the "id" parameters returned in the response
* **Test assertion 1:** The vNIC of each VM gets one v4 address and two v6 addresses with
  different prefixes actually assigned
* **Test assertion 2:** Each VM can ping the other's v4 private address
* **Test assertion 3:** The ping6 available VM can ping the other's v6 addresses
  as well as the v6 subnets' gateway ips
* Test action 8: Delete the 2 VMs created in test action 7, using the stored ids
* Test action 9: List all VMs, verifying the ids are no longer present
* **Test assertion 4:** The two "id" parameters are not present in the VM list
* Test action 10: Delete the IPv4 subnet created in test action 2, using the stored id
* Test action 11: Delete two IPv6 subnets created in test action 5, using the stored ids
* Test action 12: List all subnets, verifying the ids are no longer present
* **Test assertion 5:** The "id" parameters of IPv4 and IPv6 are not present in the list
* Test action 13: Delete the network created in test action 1, using the stored id
* Test action 14: List all networks, verifying the id is no longer present
* **Test assertion 6:** The "id" parameter is not present in the network list

Pass / fail criteria
'''''''''''''''''''''

This test evaluates the ability to assign IPv6 addresses in ipv6_ra_mode 'slaac'
and ipv6_address_mode 'slaac',
and verify the ping6 available VM can ping the other VM's v4 address and two
v6 addresses with different prefixes as well as the v6 subnets' gateway ips in the same network.
Specifically it verifies that:

* The different prefixes IPv6 addresses in mode 'slaac' assigned successfully
* The VM can ping the other VM's IPv4 and IPv6 private addresses as well as the v6 subnets' gateway ips
* All items created using create commands are able to be removed using the returned identifiers

Post conditions
---------------

None

---------------------------------------------------------------------------------------
Test Case 8 - IPv6 Address Assignment - Dual Net, Dual Stack, Multiple Prefixes, SLAAC
---------------------------------------------------------------------------------------

Short name
----------

dovetail.tempest.ipv6_scenario.dualnet_multiple_prefixes_slaac

Use case specification
----------------------

This test case evaluates IPv6 address assignment in ipv6_ra_mode 'slaac' and
ipv6_address_mode 'slaac'.
In this case, guest instance obtains IPv6 addresses from OpenStack managed radvd
using SLAAC. This test case then verifies the ping6 available VM can ping the other
VM's v4 address in one network and two v6 addresses with different prefixes in another
network as well as the v6 subnets' gateway ips, the reference is

tempest.scenario.test_network_v6.TestGettingAddress.test_dualnet_multi_prefix_slaac

Test preconditions
------------------

There should exist a public router or a public network.

Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Test execution
'''''''''''''''

* Test action 1: Create one network, storing the "id" parameter returned in the response
* Test action 2: Create one IPv4 subnet of the created network, storing the "id"
  parameter returned in the response
* Test action 3: If there exists a public router, use it as the router. Otherwise,
  use the public network to create a router
* Test action 4: Connect the IPv4 subnet to the router, using the stored IPv4 subnet id
* Test action 5: Create another network, storing the "id" parameter returned in the response
* Test action 6: Create two IPv6 subnets of network created in test action 5 in
  ipv6_ra_mode 'slaac' and ipv6_address_mode 'slaac', storing the "id" parameters returned in the response
* Test action 7: Connect the two IPv6 subnets to the router, using the stored IPv6 subnet ids
* Test action 8: Boot two VMs on these two networks, storing the "id" parameters returned in the response
* Test action 9: Turn on 2nd NIC of each VM for the network created in test action 5
* **Test assertion 1:** The vNIC of each VM gets one v4 address and two v6 addresses
  with different prefixes actually assigned
* **Test assertion 2:** Each VM can ping the other's v4 private address
* **Test assertion 3:** The ping6 available VM can ping the other's v6 addresses
  as well as the v6 subnets' gateway ips
* Test action 10: Delete the 2 VMs created in test action 8, using the stored ids
* Test action 11: List all VMs, verifying the ids are no longer present
* **Test assertion 4:** The two "id" parameters are not present in the VM list
* Test action 12: Delete the IPv4 subnet created in test action 2, using the stored id
* Test action 13: Delete two IPv6 subnets created in test action 6, using the stored ids
* Test action 14: List all subnets, verifying the ids are no longer present
* **Test assertion 5:** The "id" parameters of IPv4 and IPv6 are not present in the list
* Test action 15: Delete the 2 networks created in test action 1 and 5, using the stored ids
* Test action 16: List all networks, verifying the ids are no longer present
* **Test assertion 6:** The two "id" parameters are not present in the network list

Pass / fail criteria
'''''''''''''''''''''

This test evaluates the ability to assign IPv6 addresses in ipv6_ra_mode 'slaac'
and ipv6_address_mode 'slaac',
and verify the ping6 available VM can ping the other VM's v4 address in one network and two
v6 addresses with different prefixes in another network as well as the v6 subnets' gateway ips.
Specifically it verifies that:

* The IPv6 addresses in mode 'slaac' assigned successfully
* The VM can ping the other VM's IPv4 and IPv6 private addresses as well as the v6 subnets' gateway ips
* All items created using create commands are able to be removed using the returned identifiers

Post conditions
---------------

None



