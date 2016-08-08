.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Christopher Price (Ericsson AB) and others

*******************************
OPNFV IPv6 compliance test plan
*******************************

============
Introduction
============

The IPv6 compliance test plan outlines the method for testing IPv6 compliance to the OPNFV
platform behaviours and features of IPv6 enabled VNFi platforms.

Scope
-----

In this document, and throughout the test suite, the system under test (SUT) is defined as
the combination of the VNFi and VIM as defined by the ETSI NVF ISG (need reference).

===============================
Test suite scope and procedures
===============================

The IPv6 compliance test suite will evaluate the ability for a NVFi platform and VIM to provide
needed IPv6 features and functionality for use as an IPv6 enabled platform.

An IPv6 enabled platform needs to be able to demonstrate the ability to support for instance;
the ability to assign IPv6 addresses using SLAAC or stateful and stateless DHCPv6, the ability
to securely send a receive IPv6 traffic to an external network, support for multiple address
and dual stack interfaces.  For a complete list of the test cases refer to the 'test case specification [2]'_.

As the test suite runs as an external entity the system under test includes both the behaviours
and interfaces specified for the test.  It is expected that the system under test (SUT) interfaces
are compliant with the specifications or references supplied in the 'test case design [1]'_' document.
In addition the behaviours exhibited by the platform should comply to the referred standards
or behaviours as outlined in the 'test case design [1]'_' document.

====================
Test suite execution
====================

The test suite expects to interact with a system in an IPv6 enabled and ready state.  An IPv6
enabled system can be installed using an IPv6 enabled OPNFV scenario, or if you are not using
an OPNFV scenario ensure you have configured your system to use IPv6, in this case also pay
specific attention to the details of specific test preconditions captured in the
'test procedure specification [3]'_.

The test suite is designed to be run from an external server, the jump host, with access to the
control and network interfaces in order that it interacts with the SUT as an external entity.
The test suite will be executed by the test suite operator via scripts to be executed on the
jump host, or by leveraging the OPNFV infrastructure to execute an IPv6 compliance test job
from the jump host. Test cases may instantiate additional workloads on the SUT as part of the
test cases being executed, the system shall be returned to it's original state once the test
suite has completed.



.._'test case design [1]': http://www.opnfv.org
.._'test case specification [2]': http://www.opnfv.org
.._'test procedure specification [3]': http://www.opnfv.org

