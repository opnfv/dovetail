.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Ericsson AB

========================
Vping test specification
========================

.. toctree::
   :maxdepth: 2

Scope
=====

The vping test area evaluates basic NFVi capabilities of the system under test.
These capabilities include creating a small number of virtual machines,
establishing basic L2 connectivity between them and verifying connectivity by
means of ICMP packets.


References
==========

- Neutron Client

  - https://docs.openstack.org/developer/python-neutronclient/usage/library.html

- Nova Client

  - https://docs.openstack.org/developer/python-novaclient/ref/v2/servers.html

- SSHClient

  - http://docs.paramiko.org/en/2.2/

- SCPClient

  - https://pypi.python.org/pypi/scp


Definitions and abbreviations
=============================

The following terms and abbreviations are used in conjunction with this test
area

- ICMP - Internet Control Message Protocol
- NFVi - Network functions virtualization infrastructure
- SCP - Secure Copy
- SSH - Secure Shell
- VM - Virtual machine


System Under Test (SUT)
=======================

The system under test is assumed to be the NFVi and VIM in operation on a
Pharos compliant infrastructure.


Test Area Structure
===================

The test area is structured in two separate tests which are executed
sequentially. The order of the tests is arbitrary as there are no dependencies
across the tests.


Test Descriptions
=================

-------------------------------------------------------
Test Case 1 - vPing using userdata via the config drive
-------------------------------------------------------

Short name
----------

opnfv.vping.userdata


Use case specification
----------------------

This test evaluates the use case where an NFVi tenant boots up two VMs and
requires L2 connectivity between those VMs.


Test preconditions
------------------

At least one compute node is available. No further pre-configuration needed.


Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Methodology for verifying connectivity
''''''''''''''''''''''''''''''''''''''

Connectivity between VMs is tested by sending ICMP ping packets between
selected VMs. The target IPs are passed to the VMs sending pings by means of a
custom userdata script by means of the config driver mechanism provided by
Nova. Whether or not a ping was successful is determined by checking the
console output of the source VMs.


Test execution
''''''''''''''

* Test action 1: create a private tenant network using neutron client, one subnet and one
  router are created in the network using neutron client, one interface is added between
  the subnet and router, one gateway is added to the router using neutron client,
  storing the network id returned in the response
* **Test assertion 1:** the network id, subnet id and router id can be found in the response
* Test action 2: create an security group using neutron client, storing the security group
  id parameter returned in the response
* **Test assertion 2:** the security group id can be found in the response
* Test action 3: boot VM1 using nova client with configured name, image, flavor, private tenant
  network created in test action 1, security group created in test action 2
* **Test assertion 3:** VM1 can be found in the response
* Test action 4: Ping script to be passed as userdata by the nova metadata server.
* Test action 5: boot VM2 using nova client with configured name, image, flavor, private tenant
  network created in test action 1, security group created in test action 2, userdata created
  in test action 4
* **Test assertion 4:** VM2 can be found in the response
* Test action 6: inside VM2, to execute the Ping script to ping VM1
* **Test assertion 5:** the return code from VM1 is 0, which means ping OK, after executing Ping script in VM2
* Test action 7: delete VM1, VM2
* **Test assertion 6:** VM1 and VM2 are not present in the VM list
* Test action 8: delete security group, gateway, interface, router, subnet and network
* **Test assertion 7:** the security group, gateway, interface, router, subnet and network are
  no longer present in the lists after deleting


Pass / fail criteria
''''''''''''''''''''

This test evaluates basic NFVi capabilities of the system under test.
Specifically, the test verifies that:

* neutron client network, subnet, router, interface create commands return valid "id" parameters
  which are shown in the create response message
* neutron client interface add command to add between subnet and router return success code
* neutron client gateway add command to add to router return success code
* neutron client security group create command returns valid "id" parameter which is shown in the response message
* nova client VM create command returns valid VM attributes response message
* nova metadata server can transfer userdata configuration at nova client VM booting time
* ping command from one VM to another in same private tenant network returns valid code
* All items created using neutron client or nova client create commands are able to be removed using the returned identifiers

In order to pass this test, all test assertions listed in the test execution
above need to pass.


Post conditions
---------------

None


----------------------------------------------
Test Case 2 - vPing using SSH to a floating IP
----------------------------------------------

Short name
----------

opnfv.vping.ssh


Use case specification
----------------------

This test evaluates the use case where an NFVi tenant boots up a small number
of VMs and requires L2 connectivity between those VMs.


Test preconditions
------------------

At least one compute node is available. There should exist an OpenStack external network
and can assign floating IP.


Basic test flow execution description and pass/fail criteria
------------------------------------------------------------

Methodology for verifying connectivity
''''''''''''''''''''''''''''''''''''''

Connectivity between VMs is tested by sending ICMP ping packets between
selected VMs. To this end, the test establishes a SSH connection from the host
running the test suite to a floating IP associates to VM2 and executes ``ping``
on VM2 with the IP of VM1 as target.


Test execution
''''''''''''''


* Test action 1: create a private tenant network using neutron client, one subnet and one
  router are created in the network using neutron client, one interface is added between
  the subnet and router, one gateway is added to the router using neutron client,
  storing the network id returned in the response
* **Test assertion 1:** the network id, subnet id and router id can be found in the response
* Test action 2: create an security group using neutron client, storing the security group
  id parameter returned in the response
* **Test assertion 2:** the security group id can be found in the response
* Test action 3: boot VM1 using nova client with configured name, image, flavor, private tenant
  network created in test action 1, security group created in test action 2
* **Test assertion 3:** VM1 can be found in the response
* Test action 4: boot VM2 using nova client with configured name, image, flavor, private tenant
  network created in test action 1, security group created in test action 2
* **Test assertion 4:** VM2 can be found in the response
* Test action 5: create one floating IP by using neutron client, storing the floating IP address
  returned in the response
* **Test assertion 5:** floating IP address can be found in the response
* Test action 6: assign the floating IP address created in test action 5 to VM2 using nova client
* **Test assertion 6:** the assigned floating IP can be found in the VM2 console log file
* Test action 7: establish SSH connection between VM1 and VM2 through the floating IP
* Test action 8: copy the Ping script to VM2 using SCPClient
* **Test assertion 7:** the Ping script can be found inside VM2
* Test action 9: inside VM2, to execute the Ping script to ping VM1
* **Test assertion 8:** the return code from VM1 is 0, which means ping OK, after executing Ping script in VM2
* Test action 10: delete VM1, VM2
* **Test assertion 9:** VM1 and VM2 are not present in the VM list
* Test action 11: delete security group, gateway, interface, router, subnet and network
* **Test assertion 10:** the security group, gateway, interface, router, subnet and network are
  no longer present in the lists after deleting

Pass / fail criteria
''''''''''''''''''''

This test evaluates basic NFVi capabilities of the system under test.
Specifically, the test verifies that:

* neutron client network, subnet, router, interface create commands return valid "id" parameters
  which are shown in the create response message
* neutron client interface add command to add between subnet and router return success code
* neutron client gateway add command to add to router return success code
* neutron client security group create command returns valid "id" parameter which is shown in the response message
* nova client VM create command returns valid VM attributes response message
* neutron client floating IP create command return valid floating IP address
* nova client add floating IP command returns valid response message
* SSH connection can be established using a floating IP
* ping command from one VM to another in same private tenant network returns valid code
* All items created using neutron client or nova client create commands are able to be removed using the returned identifiers

In order to pass this test, all test assertions listed in the test execution
above need to pass.


Post conditions
---------------

None

