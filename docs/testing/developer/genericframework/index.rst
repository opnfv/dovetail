.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Huawei Technologies Co.,Ltd, and others

====================================
Dovetail as a Generic Test Framework
====================================

.. toctree::
   :maxdepth: 2


Overview
========

Dovetail is responsible for the technical realization of the OPNFV Verified
Program (OVP) and other compliance verification projects within the scope of
the Linux Foundation Networking (LFN) umbrella project.
Dovetail provides a generic framework for executing a specific set of test cases
which define the scope of a given compliance verification program, such as OVP.

This document aims at introducing what Dovetail generic framework looks like and
how to develop within this framework.


Introduction of Dovetail Framework
==================================

The following diagram illustrates Dovetail generic framework.

.. image:: ../../../images/dovetail_generic_framework.png
    :align: center
    :scale: 50%

- List

  - Sub list


Development with Dovetail Framework
===================================

For everyone who wants to do some developments with Dovetail framework to integrate
new upstream test cases, they will face the following 2 situations:

- **Adding test cases that belong to integrated projects**: There are already some
  projects integrated in Dovetail. The projects are coming from OPNFV (Open Platform
  for NFV) and ONAP (Open Network Automation Platform) communities. It will be
  much easier to add new test cases that belong to these projects.

- **Adding test cases that not belong to integrated projects**: The test cases
  may belong to other projects that haven't been integrated into Dovetail yet.
  The projects could be in OPNFV, ONAP or other communities. For this situation,
  it is a little more complicated than the first one.


Test cases belonging to integrated projects
-------------------------------------------

Dovetail framework already includes a large amount of test cases. All these test
cases are implemented by upstream projects in OPNFV and ONAP. The upstream
projects already integrated in Dovetail are FuncTest, Yardstick and Bottlenecks
from OPNFV and VNF SDK from ONAP.

If you want to add one new test case belonging to one of these projects, there
only need to add one test case configuration file which is in yaml format.
Following is the introduction about how to use the file to add one new test case.
Please refer to `Dovetail test case github
<https://github.com/opnfv/dovetail/tree/master/etc/testcase>`_
for all configuration files of all test cases.

.. code-block:: bash

   ---
   Test case name in Dovetail:
     name: Test case name in Dovetail
     objective: Test case description
     validate:
       type: Name of the project already integrated in Dovetail or Shell
       testcase: The test case name called in this project
       image_name: Name of the Docker image used to run this test
       pre_condition:
         - 'Commands needed to be executed before running this test'
         - 'e.g. cp src_file dest_file'
       pre_copy:
         src_file: sub_testcase_list.txt
         dest_path: /path/to/put/the/sub/test/list/
       cmds:
         - 'Commands used to run this test case'
       post_condition:
         - 'Commands needed to be executed after running this test case'
     report:
       source_archive_files:
         - test.log
       dest_archive_files:
         - path/to/archive/test.log
       check_results_file: results.json
       sub_testcase_list:
         - sub_test_1
         - sub_test_2
         - sub_test_3

This is the complete format of test case configuration file. Here gives some further
explanation.

- **Test case name in Dovetail**: All test cases should be named as 'xxx.yyy.zzz'.
  This is the name in Dovetail and has no relationship with its name in its own
  project.
  The first part is used to identify the project where this test case come
  from (e.g. functest, onap-vtp). The second part is used to classify the area
  of this test case (e.g. healthcheck, ha). Dovetail supports to run whole test
  cases in one test suite with the same area. Also the area is used to generate
  the summary report at the end of the test. The last part is special for this
  test case itself (e.g. image, haproxy, csar). It's better to keep the file
  name the same as the test case name to make it easier to find the config file
  according to this test case name in Dovetail.

- **validate**: This is the main section to define how to run this test case.

  - **type**: This is the type of this test case. It can be `shell` which means
    running this test case with Linux command within Dovetail container. Also it
    can be one of the projects already integrated in Dovetail. Then this type is
    used to map to its
    project configuration yaml file. For example, if you are planning to add a
    test case in OPNFV project FuncTest to Dovetail framework, the type here should
    be `functest`, and will map to `functest_config.yml` for more configurations
    in project level. Please refer to `Dovetail project config github
    <https://github.com/opnfv/dovetail/tree/master/etc/conf>`_ for more details.

  - **testcase**: This is the name defined in its own project.
    One test case can be uniquely identified by `type` and `testcase`. Take the
    test case `functest.vping.ssh` as an example. Its name in Dovetail is
    `functest.vping.ssh`, its type is `functest` and its name in FuncTest is
    `vping_ssh`. Users should only need to know that there is a test case named
    `functest.vping.ssh` in OVP compliance test scope. Dovetail Framework will
    run `vping_ssh` within FuncTest Docker container.

  - **image_name**: This is an optional section. If the type is `shell`, there is
    no need to give this. For other types, there are default docker images defined
    in their project configuration files. If this test case uses a different docker
    image, it needs to overwrite it by adding `image_name` here. The `image_name`
    here should only be the docker name without tag. The tag is defined in project's
    configuration file for all test cases belonging to this project.

  - **pre_condition**: This is an optional section. It's a list of all preparations
    needed by this test case. If the list is the same as the default one in its
    project configuration file, then there is no need to repeat it here. Otherwise,
    it's necessary to overwrite it. If its
    type is `shell`, then all commands in `pre_condition`, `cmds` and
    `post_condition` should be executable within Dovetail Ubuntu 14.04 Docker
    container.
    If its type is one of the Docker runner projects, then all commands should
    be executable within their own containers. For FuncTest, it's alpine 3.8. For
    Yardstick and Bottlenecks, it's Ubuntu 16.04. Also all these commands should
    not require network connection because some commercial platforms may be
    offline environment in private labs.

  - **pre_copy**: This is an optional section. It's only required when `testcase`
    is `tempest_custom` with
    `functest`. It will generate a test case list according to `sub_testcase_list`
    and copy it to functest container.

        - **src_file**: This is the file name of the generated test case list.
          and should be restricted by project FuncTest itself.

        - **dest_path**: This is the path where should put the test case list
          in FuncTest container.

  - **cmds**: This is an optional section with the same reason as `pre_condition`.
    It's a list of all commands used to run this test case.

  - **post_condition**: This is an optional section with the same reason as `cmds`
    and `pre_condition`. It's a list of all commands needed after executing this test
    case such as some clean up operations.

- **report**: This is the section for this test case to archive some log files and
  provide the result file for reporting PASS or FAIL.

  - **source_archive_files**: This is an optional section. If there is no need
    to archive any files, you can remove this section. Otherwise, this is a list
    of all source files needed to be
    archived. All files generated by all integrated projects will be put under
    `$DOVETAIL_HOME/results`. In order to classify and avoid overwriting them,
    it needs to rename some important files or move them to new directories.
    You can navigate directory `$DOVETAIL_HOME/results` to find out all files
    you plan to archive. The paths here should be relative ones according to
    `$DOVETAIL_HOME/results`.

  - **dest_archive_files**: This is an optional section relies on `source_archive_files`.
    This should be a list corresponding to the list of `source_archive_files`.
    Also all paths here should be relative ones according to `$DOVETAIL_HOME/results`.

  - **check_results_file**: This is the relative path of the result file generated
    when running this test case. Dovetail will crawl the results (PASS or FAIL)
    from this file.

  - **sub_testcase_list**: This section is almost only for Tempest tests in FuncTest.
    Take `functest.tempest.osinterop` as an example. The `sub_testcase_list` list
    here is an check list for this kind of tempest tests. Only when all sub test
    cases list here are passed, this test case can be taken as PASS. The other kind
    of tempest tests is `tempest_custom` such as `functest.tempest.image`. Besides
    take the `sub_testcase_list` as the check list, it's also used to generate an
    input file of FuncTest to define the list of sub test cases to be test.


Test cases not belonging to integrated projects
-----------------------------------------------

