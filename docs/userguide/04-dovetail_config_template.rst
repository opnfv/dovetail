.. This work is licensed under a Creative Commons Attribution 4.0 International
.. License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) OPNFV, Huawei Technologies Co.,Ltd and others.

Config Template Syntax
======================

Dovetail uses Functest/Yardstick Docker container to run its testcases. So you need to give
configurations for building the container and the commands it needs to do. In dovetail,
all of these are defined in config yaml files ``dovetail/dovetail/conf/functest_config.yml``
and ``dovetail/dovetail/conf/yardstick_config.yml``.

Functest template syntax
------------------------

For example, you can define your ``functest_config.yml`` as:

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

First, you need to give the image that you want to use for building functest/yardstick container.
Besides, there also need some envirnment parameters such as ``INSTALLER_TYPE`` and ``INSTALLER_IP``
and the options for you container. Then the functest/yardstick container can be build with your
settings.

Second, there need three kinds of commands, ``pre_condition``, ``testcase`` and ``post_condition``.
If you want to do some cleanups or preparations, the commands can be put into ``pre_condition``
section orderly. All commands in this section will just be executed once in the begining.
The ``testcase`` section does the main jobs of the testing. All functest testcases will use the
container to execute these commands one by one. After finishing that, the test is accomplished
and the results are stored in files or uploaded to database. The ``post_condition`` section
does some work such as clean Docker images or something else after all testcases finished.
All commands in this section will just execute once.

Besides, there need a ``result`` section and it gives the directory of the functest/yardstick
results. The ``store_type`` should be the same with the cmds in ``testcase``. That means if the
test results are stored in files, then store_type need to be file and the file_path is also
needed. If the test results are uploaded to database, then a db_url is needed for acquiring the results.

Yardstick template syntax
-------------------------

The framework of ``yardstick_config.yml`` is almost the same as ``functest_config.yml``.

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

The main differences between ``yardstick_config.yml`` and ``functest_config.yml`` are the commands.

Jinja2 template syntax
----------------------

Note that you can use jinja2 template for your parameters such as ``{{script_testcase}}``. The
parameters are defined in ``dovetail/dovetail/conf/dovetail_config.yml``:

::

  parameters:
  - name: testcase
    path: '("name",)'
  - name: script_testcase
    path: '("scripts", "testcase")'

Here ``path`` is the path in testcase config files that you can find the value of parameters. Take
``script_testcase`` as the example. For testcase dovetail.ipv6.tc001:

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

The path ("scripts", "testcase") means 'testcase' subsection of 'scripts' section. So follow
the path ("scripts", "testcase") we can get the value of ``{{script_testcase}}`` that is
'tempest_smoke_serial'. 
