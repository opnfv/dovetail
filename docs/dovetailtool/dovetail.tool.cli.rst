.. This work is licensed under a Creative Commons Attribution 4.0 International
.. License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) OPNFV, Huawei Technologies Co.,Ltd and others.

Command Line Interface
======================

Dovetail supports modifying some parameters at the run-time by using the command
line interface (CLI). The parameters can be defined through a config file by
developers easily and then be used at the run-time.

The CLI now fits all three kinds of running: directly running the python script,
running after setup and running within Docker containers.

Define CLI with config file
---------------------------

For easy to be modified, Dovetail provides ``dovetail/dovetail/conf/cmd_config.yml``
to define CLI automatically.

::

  cli:
    arguments:
      config:
        # This is a simple example of arguments.
        # Dovetail has no need of this kind of parameters currently.
        # The arguments must be given orderly at the run-time.
        #
        # docker_tag:
        #   flags: 'docker_tag'
        #   path:
        #     - 'functest/docker_tag'
        #     - 'yardstick/docker_tag'
      control:

    options:
      config:
        SUT_TYPE:
          flags:
            - '--SUT_TYPE'
            - '-t'
          path:
            - 'functest/envs'
            - 'yardstick/envs'
          help: 'Installer type of the system under test (SUT).'
        yard_tag:
          flags:
            - '--yard_tag'
            - '-y'
          path:
            - 'yardstick/docker_tag'
          help: 'Overwrite tag for yardstick docker container (e.g. stable or latest)'
        func_tag:
          flags:
            - '--func_tag'
            - '-f'
          path:
            - 'functest/docker_tag'
          help: 'Overwrite tag for functest docker container (e.g. stable or latest)'
      control:
        testsuite:
          flags:
            - '--testsuite'
          default: 'compliance_set'
          help: 'compliance testsuite.'
        testarea:
          flags:
            - '--testarea'
          default: 'full'
          help: 'compliance testarea within testsuite'

Dovetail uses click module in python to parse parameters defined in the above
config file. The basic config file shown above contains two subsections:
**arguments** and **options** corresponding to two types of parameters in click.

Add options
+++++++++++

Just as the name suggested, option parameters can either be given or not by users
after adding into CLI.

Then how to add an option for developers?

For each option, it at least needs a key **flags** to give its name. Customarily,
each option has two names, full name and short name, and they are begin with '--'
and '-' respectively. All other keys should be consistent with click's keys.

Take option **scenario** as the example. Its full name is '--scenario', and its
short name is '-s'. Actually full name is necessary but short name is optional.
The full name '--scenario' should be the same with the block's name **scenario**.
**default** section gives the default value of this option if it doesn't given
by users. Without the **default** section, it will be set None. **help** section
offers its help message that will be shown when excute -h/--help command. For
more information about click, please refer to: http://click.pocoo.org/5/

Add arguments
+++++++++++++

Arguments must given orderly by users once they are defined in the config file.
The Dovetail tool doesn't need any argument parameters currently. However, here
just give a simple example for its format.

Arguments also need subsection **flags** to give its name. Each argument can just
have one name, and the name should be the same with the key of this section. Other
keys should also be consistent with the click module.

Config and control
++++++++++++++++++

All options/arguments are divided into two parts: **config** and **control**.
The config ones are used for updating functest or yardstick config files according
to the **path** given.  For example, functest's config file is
``dovetail/dovetail/conf/functest_config.yml``, following is a simple example:

::

  docker_tag: latest
  envs: '-e INSTALLER_TYPE=compass -e INSTALLER_IP=192.168.200.2
         -e NODE_NAME=dovetail-pod -e DEPLOY_SCENARIO=ha_nosdn
         -e BUILD_TAG=dovetail -e CI_DEBUG=true -e DEPLOY_TYPE=baremetal'

If running with the command ``python run.py --SUT_TYPE fuel -f stable``, then
the configs will be changed into

::

  docker_tag: stable
  envs: '-e INSTALLER_TYPE=fuel -e INSTALLER_IP=192.168.200.2
         -e NODE_NAME=dovetail-pod -e DEPLOY_SCENARIO=ha_nosdn
         -e BUILD_TAG=dovetail -e CI_DEBUG=true -e DEPLOY_TYPE=baremetal'

The config options/arguments can be added or deleted just by modifying
``cmd_config.yml`` rather than changing the source code. However, for control
command, besides adding it into ``cmd_config.yml``, some other operations about
the source code are also needed.

Run with CLI
------------

For users, they can use CLI to input their own envs at the run-time instead of
modifying the config files of functest or yardstick. So Dovetail can supports
different environments more flexible with CLI. Dovetail now can be run with three
methods, directly running ``run.py`` script, running after setup and running
in Docker containers. The uses of CLI are almost the same for these three methods
and here take the first one as the example.

All parameters offered by Dovetail can be listed by using help option ``--help``.

::

  root@90256c4efd05:~/dovetail/dovetail$ python run.py --help
  Usage: run.py [OPTIONS]

  Dovetail compliance test entry!

  Options:
    -t, --SUT_TYPE TEXT  Installer type of the system under test (SUT).
    -f, --func_tag TEXT  Overwrite tag for functest docker container (e.g.
                       stable or latest)
    -i, --SUT_IP TEXT    IP of the system under test (SUT).
    -y, --yard_tag TEXT  Overwrite tag for yardstick docker container (e.g.
                       stable or latest)
    -d, --DEBUG TEXT     DEBUG for showing debug log.
    --testarea TEXT      compliance testarea within testsuite
    --testsuite TEXT     compliance testsuite.
    -h, --help           Show this message and exit.

All options listed can be used to input special environment values at the run-time.
For example:

::

  python run.py --SUT_TYPE compass -y stable

There is no need to give all these options. If it is not given by CLI, it will
be set with the system's environment value. If it is not included in system's
environment variables, it will be set with the default value in functest/yardstick
config file.
