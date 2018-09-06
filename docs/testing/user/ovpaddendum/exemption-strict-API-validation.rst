.. This work is licensed under a Creative Commons Attribution 4.0 International
.. License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Ericsson and others

.. _dovetail-exemption_process_api_response_validation:

==========================================
Disabling Strict API Validation in Tempest
==========================================

.. toctree::
   :maxdepth: 2


Introduction
============

In 2015, the OpenStack QA team introduced a validation mechanism for Nova API
responses in Tempest [1]_ with the goal of enforcing Nova API micro-versions.
The API validation mechanism verifies that API responses only contain data
elements (properties) as explicitly defined in API response schemas [2]_. In
case additional data elements are found in Nova API responses, the
corresponding tests fail immediately without asserting whether or not the
particular API operation actually succeeded or not.

Independently, cloud vendors have extended their commercial OpenStack cloud
implementations with additional functionality which requires API extensions.
Consequently, such cloud implementations do not pass Tempest tests which
validate API responses despite actually implementing and providing the tested
functionality.

This document describes an exemption process for use within the OPNFV Verified
Program which

i) allows vendors to pass Tempest tests if the tested functionality is
   fully supported despite the presence of additional data elements in API
   responses, and

ii) makes the application of the exemption process transparently visible in
    test results.


Background and benefits for OVP
===============================

Vendors of commercial NFV products have extended OpenStack to provide
additional (NFV) functionality to their customers and to fill functional gaps
in OpenStack. These add-ons potentially extend the OpenStack API in two ways:

i) new API endpoints and

ii) additional attributes returned by existing API endpoints.

New API endpoints typically go unnoticed by OpenStack Tempest tests and hence
do not interfere with existing tests. In contrast, (Nova) Tempest tests
actively validate the responses returned by existing API endpoints against
pre-defined schemas. An API response is considered invalid if additional
attributes are present (see example below). Hence, this particular type of
functional extension of OpenStack causes existing Tempest tests to fail,
irrespective of whether or not the functionality which is supposed to be tested
is actually available. As a result, a Tempest test failing due to extended API
responses does not provide information about whether the tested functionality
is available or not.

The OPNFV Verified Program has inherited the policy to strictly validate API
responses from OpenStack by including a selection of Tempest tests in its
compliance test suite. However, it was never discussed if OVP should adopt this
policy as well. It turns out that this policy causes challenges for vendors of
commercial NFV offerings to pass the OVP test suite. The exemption process
outlined in this document aims at allowing to selectively disable strict API
response validation in order to enable vendors to adopt OVP **if** the tested
functionality is supported.

It must be clearly understood that this exemption targets **only** the scenario
in which additional attributes are included in API responses. It does not
provide a loophole for passing OVP tests if the OpenStack APIs have been
altered significantly as this is in conflict with the objective of OVP to
create industry alignment.

In conclusion, the exemption process described here is deemed beneficial for
both the broader industry as well as for OVP: Enabling adoption of OVP by
vendors which extended OpenStack API responses facilitates adoption of OVP in
the industry. The limited validity period of an exemption incentivizes eventual
alignment within the industry around a clearly specified set of APIs.


Example: additional attributes per VM for HA policy
---------------------------------------------------

This fictional example showcases the presence of an additional attribute in an
API response. The example shows that the 'server details' [3]_, i.e. the VM
metadata, includes an additional attribute 'ha-policy' which is used to
associate high-availability policies with a VM instance. This attribute is
utilized by a proprietary add-on component to manage VM migration and recovery
in case of compute host failures::

  {
    "server": {
      "accessIPv4": "1.2.3.4",
      "config_drive": "",
      "flavor": {...},
      "image": {...},
      "ha_policy": "migrate"       <-- additional attribute
      "name": "new-server-test",
      "status": "ACTIVE"
    }
  }



Precedent in OpenStack
======================

In the OpenStack community, the OpenStack Interoperability Working Group
(Interop WG) [4]_ is maintaining multiple API interoperability compliance
programs [5]_. These programs utilize Tempest-based tests to determine if a
given commercial cloud is compliant to a selected set of OpenStack APIs. After
introduction of the strict API response validation, various cloud products
which previously passed the compliance program failed validation because of the
reasons outlined above.

In order to mitigate this situation, the Interop WG consulted with the broader
OpenStack community [6]_ and eventually introduced an "additional properties
waiver" for its API compliance programs in July 2016. The waiver was
created with a clearly defined validity period, covering roughly one year -
equivalent to three iterations of interoperability guidelines (2015.07,
2016.01, and 2016.08). The limited lifetime of the waiver was intended to give
cloud product vendors a transition period for adapting their products to
achieve full API compliance by the end of the exemption period. All details of
the waiver are listed in [7]_. Finally, the waiver was officially canceled in
October 2017 [8]_ after about 15 months.


Exemption process for additional properties in API responses in the OVP
=======================================================================

The details of the exemption process for disabling strict validation of API
responses is as follows:

#. The Dovetail tool provides a new command line option "--no-api-validation" for
   disabling strict API validation. This option needs to be explicitly given on
   the command line to disable strict API validation. If this command line
   option is omitted, the default behavior (i.e., strict API validation) is
   applied.

#. The test results created by the Dovetail tool includes an explicit print-out
   stating if strict API validation was disabled during the test run or not.

#. The OVP portal reads the uploaded result files and indicates for all
   uploaded test results if strict API validation was disabled or not.

#. Together with the application for certification, a company can request an
   exemption from the requirement for strict API response checking. A rationale
   for requesting the exemption has to be provided. The request is either
   granted or rejected by the C&C committee. The rationale provided must
   establish that the need for exemption is not in violation of the OVP's
   objectives.

#. Compliance badges obtained under exemption are valid for one year.

#. OPNFV expects OVP participants to aim for full compliance without requiring
   exemptions as soon as possible. Hence, an exemption can only be requested
   twice for the same product (addressing new versions of OVP or new versions
   of the product).

#. The same logo will be used regardless of being obtained under exemption or
   not.

#. The exemption will be made available to participants of OVP as part of a
   service release of OVP 2018.01 and 2018.09.

#. The C&C committee will monitor the situation around exemptions and may
   decide changes to the above process at any time, including the possibility
   to stop issuing exemptions.


.. [1] https://review.openstack.org/#/c/156130/
.. [2] https://github.com/openstack/tempest/tree/master/tempest/lib/api_schema/response/compute
.. [3] https://developer.openstack.org/api-ref/compute/#show-server-details
.. [4] https://wiki.openstack.org/wiki/Governance/InteropWG
.. [5] https://refstack.openstack.org/
.. [6] http://lists.openstack.org/pipermail/openstack-dev/2016-June/097349.html
.. [7] https://review.openstack.org/#/c/333067/
.. [8] https://review.openstack.org/#/c/512447/
