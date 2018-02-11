.. This work is licensed under a Creative Commons Attribution 4.0 International
.. License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Ericsson and others

==============================================================
Exemption Process - Disabling Strict API Validation in Tempest
==============================================================

.. toctree::
   :maxdepth: 2


Introduction
============

In 2015, the OpenStack QA team introduced a validation mechanism for Nova API
responses in Tempest [1]_ with the goal of enforcing Nova API microversions.
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


Precedent in OpenStack
======================

In the OpenStack community, the OpenStack Interoperability Working Group
(Interop WG) [3]_ is maintaining multiple API interoperability compliance
programs [4]_. These programs utilize Tempest-based tests to determine if a
given commercial cloud is compliant to a selected set of OpenStack APIs. After
introduction of the strict API response validation, various cloud products
which previously passed the compliance program failed validation because of the
reasons outlined above.

In order to mitigate this situation, the Interop WG consulted with the broader
OpenStack community [5]_ and eventually introduced an "additional properties
waiver" for its API compliance programs in July 2016. The waiver was
created with a clearly defined validity period, covering roughly one year -
equivalent to three iterations of interoperability guidelines (2015.07,
2016.01, and 2016.08). The limited lifetime of the waiver was intended to give
cloud product vendors a transition period for adapting their products to
achieve full API compliance by the end of the exemption period. All details of
the waiver are listed in [6]_. Finally, the waiver was officially canceled in
October 2017 [7]_ after about 15 months.


Exemption process for additional properties in API responses in the OVP
=======================================================================

The details of the exemption process for disabling strict validation of API
responses is as follows:

#. The Dovetail tool provides a new command line option "--non-strict-api" for
   disabling strict API validation. This option needs to be explicitly given on
   the command line to disable strict API validation. If this command line
   option is omitted, the default behavior (i.e., strict API validation) is
   applied.

#. The test result data created by the Dovetail tool includes an explicit
   print-out stating whether or not strict API validation was disabled during
   the test run.

#. The OVP portal reads the uploaded result files and indicates for all
   uploaded test results whether or not strict API validation was disabled.

#. Together with the application for certification, a company can request an
   exemption from the requirement for strict API response checking. A rationale
   for requesting the exemption has to be provided. The request either granted
   or rejected by the C&C committee. The rationale provided must establish that
   the need for exemption is not in violation of the OVP's objectives.

#. An exemption has to be requested again for each following application (newer
   versions of OVP, new product versions). OPNFV expects OVP participants to
   aim for full compliance without requiring exemptions as soon as possible and
   may stop permitting exemptions for recurring applications.

#. The first release to which the exemption process applies is the first
   release following the initial 2018.01 release of OVP. The compliance badge
   remains valid also after the exemption phase. The same logo will be used
   regardless of being obtained under exemption or not.

The C&C committee will monitor the situation around exemptions and may decide
changes to the above process at any time, including the possibility to stop
issuing exemptions.


.. [1] https://review.openstack.org/#/c/156130/
.. [2] https://github.com/openstack/tempest/tree/master/tempest/lib/api_schema/response/compute
.. [3] https://wiki.openstack.org/wiki/Governance/InteropWG
.. [4] https://refstack.openstack.org/
.. [5] http://lists.openstack.org/pipermail/openstack-dev/2016-June/097349.html
.. [6] https://review.openstack.org/#/c/333067/
.. [7] https://review.openstack.org/#/c/512447/
