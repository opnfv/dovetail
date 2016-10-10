.. This work is licensed under a Creative Commons Attribution 4.0 International
.. License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) OPNFV, Huawei Technologies Co.,Ltd and others.

Testcase Template Syntax
=========================

The testcases certification are defined in ``dovetail/scripts/testcase``.
Take testcase ``feature.tc003.yml`` as an example.

Basic template syntax
---------------------

::

  dovetail.feature.tc003:
    name: dovetail.feature.tc003
    objective: testing for bulk network operations
    scripts:
      type: functest
      testcase: tempest_smoke_serial
      sub_testcase_list:
        - tempest.api.network.test_networks.BulkNetworkOpsTest.test_bulk_create_delete_network
        - tempest.api.network.test_networks.BulkNetworkOpsTest.test_bulk_create_delete_port

The testcase needs at least three keys named as 'name', 'objective' and 'scripts'. In the scripts
part, 'type' means the test project you want to use (i.e. functest or yardstick), and 'testcase'
needs to be existent in functest or yardstick. If you have the special sub_testcases that you
consider most, you can put them in the sub_testcase_list.
