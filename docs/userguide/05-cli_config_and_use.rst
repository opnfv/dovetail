.. This work is licensed under a Creative Commons Attribution 4.0 International 
.. License.                                                                        
.. http://creativecommons.org/licenses/by/4.0                                      
.. (c) OPNFV, Huawei Technologies Co.,Ltd and others.

Command Line Interface
======================

Dovetail supports modifying some parameters at the run-time by using the
command line interface. The commands can be defined through a config file by
developers easily and be used when running certification manually. It now fits
three kinds of running, directly running the python script, running after setup
and running with docker container.

Define CLI with config file
---------------------------

For easy to be modified, dovetail provides ``dovetail/dovetail/conf/cmd_config.yml``
to define CLI dynamically.

::

  cli:                                                                               
    scenario:                                                                        
      flags:                                                                         
        - '--scenario'                                                               
      default: 'basic'                                                               
      help: 'certification scenario.'                                                
    SUT_TYPE:                                                                        
      flags:                                                                         
        - '--SUT_TYPE'                                                               
        - '-TYPE'                                                                    
      help: 'Give SUT_TYPE.'                                                         
    SUT_IP:                                                                          
      flags:                                                                         
        - '--SUT_IP'                                                                 
        - '-IP'                                                                      
      help: 'Give SUT_IP.' 

The basic yaml file shown above contains three commands named **scenario**,
**SUT_TYPE** and **SUT_IP**, and all of them are options. Dovetail uses click
module in python to parse these commands, so for each command its keys should
be consistent with click's keys with the exception of **flags**. There is a list
in **flags** such as ``['--SUT_TYPE', '-TYPE']`` defining the full name and
short name of the command. The full name is necessary but the short name is
optional. As you can see, the full name ``--SUT_TYPE`` should be the same with
this block's name **SUT_TYPE**. Other keys such as **default** and **help** are
the same as defined in python module click.

The first command **scenario** is used for choosing the scenario to be run, and
the cmd config file needs to include this command at least. All other commands
are the environment paramenters that will be used to run functest/yardstick
containers. For example, the default envs for functest container are given in
functest's config file ``dovetail/dovetail/conf/functest_config.yml``:

::

  envs: '-e INSTALLER_TYPE=compass -e INSTALLER_IP=192.168.200.2                   
         -e NODE_NAME=dovetail-pod -e DEPLOY_SCENARIO=ha_nosdn                     
         -e BUILD_TAG=dovetail -e CI_DEBUG=true -e DEPLOY_TYPE=baremetal'

If running with the command ``python run.py --SUT_TYPE fuel``, then the envs
will be changed into

::

  envs: '-e INSTALLER_TYPE=fuel -e INSTALLER_IP=192.168.200.2                   
         -e NODE_NAME=dovetail-pod -e DEPLOY_SCENARIO=ha_nosdn                     
         -e BUILD_TAG=dovetail -e CI_DEBUG=true -e DEPLOY_TYPE=baremetal'

The envs commands can be added or deleted just by modifying ``cmd_config.yml``
rather than changing the source code. Now it only can dynamically modify envs
commands. If there is a need for adding non-envs command, besides adding it into
``cmd_config.yml``, some other operations about the source code are also needed.

Run certification with CLI
--------------------------

For users, they can use CLI to input their own envs at the run-time instead of
modifying the config files of functest and yardstick. So dovetail can supports
different environments more flexible with CLI. Dovetail now can be run with three
methods, directly running ``run.py`` script, running after setup and running
in docker container. The uses of CLI are almost the same for these three methods
and here takes the first one as the example.

All commands offered by dovetail can be listed by using help command ``--help``.

::

  root@90256c4efd05:~/dovetail/dovetail$ python run.py --help
  Usage: run.py [OPTIONS]

  Dovetail certification test entry!

  Options:
    -TYPE, --SUT_TYPE TEXT  Give SUT_TYPE.
    --DEPLOY_SCENARIO TEXT  Give DEPLOY_SCENARIO.
    --DEPLOY_TYPE TEXT      Give DEPLOY_TYPE.
    -IP, --SUT_IP TEXT      Give SUT_IP.
    --CI_DEBUG TEXT         Give CI_DEBUG.
    --scenario TEXT         certification scenario.
    --help                  Show this message and exit.

All options listed can be used to input special environment values at the run-time.
For example:

::

  python run.py --SUT_TYPE compass --SUT_IP 192.168.200.2

There is no need to give all these commands. If it is not given by CLI, it will
be set with the system's environment value. If it is not included in system's
environment variables, it will be set with the default value in functest/yardstick
config file.
