.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Bin Hu (AT&T), Tim Irnich (Ericsson) and other contributors

======================================
L3VPN Any-to-Any Compliance Test Cases
======================================

The Compliance Test Cases for L3VPN Any-to-Any Scenario are as follows.
Please note that the test cases do not cover other L3VPN Scenarios such as
ECMP, Hub and Spoke etc.

----------------------------------
Test Case 1: Tempest Create BGPVPN
----------------------------------

.. code-block:: bash

    # Need to add Tempest API Tests

------------------------------------------------------
Test Case 2: VPN Provides Connectivity between Subnets
------------------------------------------------------

.. code-block:: bash

    # Note: Available in FuncTest
    # Description: VPNs provide connectivity across Neutron networks and subnets if configured accordingly.
    # Step 1: Test Setup
    #    1.1: Set up VM1 and VM2 on Node1 and VM3 on Node2
    #    1.1.1: All have ports in the same Neutron Network N1
    #    1.1.2: All have 10.10.10.0/24 addresses (this subnet is referred to as SN1 in the following steps)
    #    1.2: Set up VM4 on Node1 and VM5 on Node2
    #    1.2.1: Both have ports in Neutron Network N2
    #    1.2.2: Both have 10.10.11.0/24 addresses (this subnet is referred to as SN2 in the following steps)
    # Step 2: Test Execution
    #    2.1: Create VPN1 with eRT<>iRT (so that connected subnets should not reach each other) and associate SN1 to it
    #    2.2: Ping from VM1 to VM2 should work
    #    2.3: Ping from VM1 to VM3 should work
    #    2.4: Ping from VM1 to VM4 should not work
    #    2.5: Associate SN2 to VPN1
    #    2.6: Ping from VM4 to VM5 should work
    #    2.7: Ping from VM1 to VM4 should not work
    #    2.8: Ping from VM1 to VM5 should not work
    #    2.9: Change VPN 1 so that iRT=eRT
    #    2.10: Ping from VM1 to VM4 should work
    #    2.11: Ping from VM1 to VM5 should work

-----------------------------
Test Case 3: Tenant Isolation
-----------------------------

.. code-block:: bash

    # Note: Available in FuncTest
    # Description: Using VPNs to isolate tenants so that overlapping IP address ranges can be used
    # Step 1: Test Setup
    #    1.1: set up VM1 and VM2 on Node1 and VM3 on Node2
    #    1.1.1: All have ports in the same Neutron Network N1
    #    1.2: VM1 and VM2 have IP addresses in the subnet SN1a with range 10.10.10.0/24
    #    1.2.1: VM1: 10.10.10.11, running an HTTP server which returns "I am VM1" for any HTTP request
    #    1.2.2: VM2: 10.10.10.12, running an HTTP server which returns "I am VM2" for any HTTP request
    #    1.3: VM3 has an IP address in the subnet SN2a with range 10.10.11.0/24
    #    1.3.1: VM3: 10.10.11.13, running an HTTP server which returns "I am VM3" for any HTTP request
    #    1.4: Set up VM4 on Node1 and VM5 on Node2, both having ports in Neutron Network N2
    #    1.5: VM4 has an address in the subnet SN1b with range 10.10.10.0/24
    #    1.5.1: VM4: 10.10.10.12, running an HTTP server which returns "I am VM4" for any HTTP request
    #    1.5.2: Note VM4 has the same IP address as VM2
    #    1.6: VM5 has an address in the subnet SN2b with range 10.10.11/24
    #    1.6.1: VM5: 10.10.11.13, running an HTTP server which returns "I am VM5" for any HTTP request
    #    1.6.2: Note VM5 has the same IP address as VM3
    # Step 2: Test Execution
    #    2.1: Create VPN 1 with iRT=eRT=RT1 and associate N1 to it
    #    2.2: HTTP from VM1 to VM2 and VM3 should work
    #    2.2.1: It returns "I am VM2" and "I am VM3" respectively
    #    2.3: HTTP from VM1 to VM4 and VM5 should not work
    #    2.3.1: It never returns "I am VM4" or "I am VM5"
    #    2.4: Create VPN2 with iRT=eRT=RT2 and associate N2 to it
    #    2.5: HTTP from VM4 to VM5 should work
    #    2.5.1: It returns "I am VM5"
    #    2.6: HTTP from VM4 to VM1 and VM3 should not work
    #    2.6.1: It never returns "I am VM1" or "I am VM3"

