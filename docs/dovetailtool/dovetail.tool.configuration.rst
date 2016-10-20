.. This work is licensed under a Creative Commons Attribution 4.0 International
.. License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) OPNFV, Huawei Technologies Co.,Ltd and others.

=========================
Testcase Template Syntax
=========================

The testcases used for compliance&certification are defined in directory ``dovetail/dovetail/testcase``,
which are written in yaml format. Take the testcase ``ipv6.tc001.yml`` as an example, it is shown as

::

  dovetail.ipv6.tc001:
    name: dovetail.ipv6.tc001
    objective: VIM ipv6 operations, to create/delete network, port and subnet in bulk operation
    scripts:
      type: functest
      testcase: tempest_smoke_serial
      sub_testcase_list:
        - tempest.api.network.test_networks.BulkNetworkOpsIpV6Test.test_bulk_create_delete_network
        - tempest.api.network.test_networks.BulkNetworkOpsIpV6Test.test_bulk_create_delete_port
        - tempest.api.network.test_networks.BulkNetworkOpsIpV6Test.test_bulk_create_delete_subnet

- At least three sections named 'name', 'objective', 'scripts' should be included.
- Section 'name' distinguish different test cases used for compliance&certification, it should be started with ``dovetail.``.
- Section 'objective' describes what this testcase does.
- Section 'scripts' has subsections such as 'type', 'testcase' and 'sub_testcase_list'.
- Two kinds of 'type' is supported by now, functest and yardstick.
- Since upstream functest and yardstick have different testcase running CLI by now.
  For functest, the 'testcase' represents the testcases in slicing,
  'sub_testcase_list' represents the testcases in this slicing compliance&certification will use.
  For yardstick, since it is not sliced by now, 'sub_testcase_list' is not needed, only to edit the 'testcase' part
  such as ``yardstick_tc027``.
