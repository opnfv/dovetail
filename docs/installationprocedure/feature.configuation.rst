.. This work is licensed under a Creative Commons Attribution 4.0 International
.. License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) OPNFV, Huawei Technologies Co.,Ltd and others.

Testcase Template Syntax
=========================

The testcases certification are defined in ``dovetail/dovetail/testcase``.
Take testcase ``ipv6.tc001.yml`` as an example.

Basic template syntax
---------------------

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

The testcase needs at least three keys named as 'name', 'objective' and 'scripts'. The whole
dovetail project can just recognize testcases by the 'name' section, which here is
'dovetail.ipv6.tc001'. The 'objective' describes what exactly this testcase does. In the
'scripts' part, there are some subsections such as 'type', 'testcase' and 'sub_testcase_list'.
Dovetail now supports two kinds of types, functest and yardstick. If you define the type as
functest, then you need to give the functest testcase that you want to use. If the type is
yardstick, then a yardstick testcase is needed. The 'sub_testcase_list' lists the sub_testcases
that you put a high value on. Even though the whole testcase faild, we still think it passed
when all the sub_testcases pass. The sub_testcase_list is just available for functest. When
for yardstick testcase, retain 'sub_testcase_list' section and keep the content empty.

::

  sub_testcase_list:
    -

This is the definition of the dovetail testcases. They can just be tested by adding into
scenarios such as ``cert/basic.yml``.
