#!/usr/bin/env python
#
# grakiss.wanglei@huawei.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

import yaml
import os
import re


class DovetailConfig:

    COMPLIANCE_PATH = './compliance/'
    TESTCASE_PATH = './testcase/'
    # testsuite supported tuple, should adjust accordingly
    testsuite_supported = ('compliance_set', 'proposed_tests', 'debug')
    # testarea supported tuple, should adjust accordingly
    testarea_supported = ('vimops', 'nfvi', 'ipv6')

    dovetail_config = {}

    @classmethod
    def load_config_files(cls):
        curr_path = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(curr_path, 'dovetail_config.yml')) as f:
            cls.dovetail_config = yaml.safe_load(f)

        for extra_config_file in cls.dovetail_config['include_config']:
            with open(os.path.join(curr_path, extra_config_file)) as f:
                extra_config = yaml.safe_load(f)
                cls.dovetail_config.update(extra_config)

        path = os.path.join(curr_path, cls.dovetail_config['cli_file_name'])
        with open(path) as f:
            cmd_yml = yaml.safe_load(f)
            cls.dovetail_config['cli'] = cmd_yml[cmd_yml.keys()[0]]

    @classmethod
    def cmd_name_trans(cls, cmd_name):
        key = cmd_name.upper()
        if key == 'SUT_TYPE':
            key = 'INSTALLER_TYPE'
        if key == 'SUT_IP':
            key = 'INSTALLER_IP'
        return key

    @classmethod
    def update_envs(cls, options):
        for item in options:
            key = cls.cmd_name_trans(item)
            if not options[item] and key in os.environ:
                options[item] = os.environ[key]
            if options[item]:
                cls.update_config_envs('functest', key)
                cls.update_config_envs('yardstick', key)

    @classmethod
    def update_config_envs(cls, script_type, key):
        if key == 'DEBUG':
            os.environ['CI_DEBUG'] = os.environ[key]
        envs = cls.dovetail_config[script_type]['envs']
        old_value = re.findall(r'\s+%s=(.*?)(\s+|$)' % key, envs)
        if old_value == []:
            envs += ' -e ' + key + '=' + os.environ[key]
        else:
            envs = envs.replace(old_value[0][0], os.environ[key])
        cls.dovetail_config[script_type]['envs'] = envs
        return envs
