.. This work is licensed under a Creative Commons Attribution 4.0 International
.. License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) OPNFV, Huawei Technologies Co.,Ltd and others.

==================
Template Syntax
==================

Testcase Template Syntax
=========================

The testcases used for compliance and certification are defined in the ``dovetail/testcase`` directory,
which are defined in yaml format. Take the testcase ``ipv6.tc001.yml`` as an example, it is shown as:

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

- At least three sections named 'name', 'objective', 'scripts' must be included
- Section 'name' distinguishes different test cases used for compliance and certification,
  and should start with ``dovetail.``
- Section 'objective' describes what this testcase does
- Section 'scripts' has subsections such as 'type', 'testcase' and 'sub_testcase_list'
- Two kinds of 'type' is supported by now, functest and yardstick
- For functest, the 'testcase' represents the testcases in slicing/tier,
  'sub_testcase_list' represents the testcases in this slicing compliance and certification will use.
  For yardstick, since it is not sliced by now, 'sub_testcase_list' is not needed, only to edit the 'testcase' part
  such as ``yardstick_tc027``


Config Template Syntax
=======================

For Dovetail tool, the config files are located in ``dovetail/dovetail/conf``, which are written
in yaml format. As both functest and yardstick are utilized by Dovetail, their configuration files
should be configured as follows, within the ``functest_config.yml`` and ``yardstick_config.yml`` files,
respectively.

Functest config template syntax
-------------------------------

An example of functest configuration is shown as follows:

::

  functest:
    image_name: opnfv/functest
    docker_tag: latest
    envs: '-e INSTALLER_TYPE=compass -e INSTALLER_IP=192.168.200.2
           -e NODE_NAME=dovetail-pod -e DEPLOY_SCENARIO=ha_nosdn
           -e BUILD_TAG=dovetail -e CI_DEBUG=true -e DEPLOY_TYPE=baremetal'
    opts: '-id --privileged=true'
    pre_condition:
      cmds:
        - 'echo test for precondition'
    testcase:
      cmds:
        - 'python /home/opnfv/repos/functest/ci/prepare_env.py start'
        - 'python /home/opnfv/repos/functest/ci/run_tests.py -t {{script_testcase}} -r'
    post_condition:
      cmds:
        - ''
    result:
      dir: '/home/opnfv/functest/results'
      store_type: 'file'
      file_path: 'tempest/tempest.log'
      db_url: 'http://testresults.opnfv.org/test/api/v1/results?case=%s&last=1'

- ``image_name`` and ``docker_tag`` sections define the docker image pulled from the public dockerhub.
- ``envs`` should be correctly configed according to the SUT(System Under Test).
- ``pre_condition`` represents some cleanups or preparations.
  ``testcase`` represents the testcases running cmds.
  ``post_condition`` represents some cleanups needed after all testcases finished.
- ``result`` section gives the directory of the dovetail tool test result.
  ``db_url`` gives the database URL of the dovetail results to be stored.

Yardstick config template syntax
---------------------------------

The configuration in ``yardstick_config.yml`` is similiar to ``functest_config.yml``,
and an example is shown as follows:

::

  yardstick:
    image_name: opnfv/yardstick
    docker_tag: latest
    envs: '-e INSTALLER_TYPE=compass -e INSTALLER_IP=192.168.200.2
           -e NODE_NAME=dovetail-pod -e DEPLOY_SCENARIO=ha_nosdn
           -e BUILD_TAG=dovetail -e CI_DEBUG=true -e DEPLOY_TYPE=baremetal
           -e EXTERNAL_NETWORK=ext-net'
    opts: '-id --privileged=true'
    pre_condition:
      cmds:
        - 'source /home/opnfv/repos/yardstick/tests/ci/prepare_env.sh &&
           source /home/opnfv/repos/yardstick/tests/ci/clean_images.sh && cleanup'
        - 'source /home/opnfv/repos/yardstick/tests/ci/prepare_env.sh &&
           cd /home/opnfv/repos/yardstick && source tests/ci/load_images.sh'
    testcase:
      cmds:
        - 'mkdir -p /home/opnfv/yardstick/results/'
        - 'cd /home/opnfv/repos/yardstick && source tests/ci/prepare_env.sh &&
           yardstick task start tests/opnfv/test_cases/{{script_testcase}}.yaml
           --output-file /home/opnfv/yardstick/results/{{script_testcase}}.out &>
           /home/opnfv/yardstick/results/yardstick.log'
    post_condition:
      cmds:
        - ''
    result:
      dir: '/home/opnfv/yardstick/results'
      store_type: 'file'
      file_path: 'yardstick.log'
      db_url: 'http://testresults.opnfv.org/test/api/v1/results?case=%s&last=1'

The main differences between ``yardstick_config.yml`` and ``functest_config.yml``
are the ``cmds`` subsection.

Jinja2 template syntax
----------------------

Jinja2 module can be used to config the ``{{script_testcase}}``. The
parameters are defined in ``dovetail/dovetail/conf/dovetail_config.yml``:

::

  parameters:
  - name: testcase
    path: '("name",)'
  - name: script_testcase
    path: '("scripts", "testcase")'

Here ``path`` is the path defined in the testcase configuration files.
Take ``script_testcase`` as an example. For testcase ``dovetail.ipv6.tc001``:

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

The path ("scripts", "testcase") means 'testcase' is the subsection of 'scripts' section. From above,
by following the path ("scripts", "testcase") we can get the value of ``{{script_testcase}}`` is 'tempest_smoke_serial'.
