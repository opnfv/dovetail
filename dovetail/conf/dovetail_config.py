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

CERT_PATH = './cert/'
TESTCASE_PATH = './testcase/'
SCENARIO_NAMING_FMT = 'certification_%s'

curr_path = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(curr_path, 'dovetail_config.yml')) as f:
    dovetail_config = yaml.safe_load(f)

for extra_config_file in dovetail_config['include_config']:
    with open(os.path.join(curr_path, extra_config_file)) as f:
        extra_config = yaml.safe_load(f)
        dovetail_config.update(extra_config)

container_config = {}

container_config['functest'] = dovetail_config['functest']
container_config['yardstick'] = dovetail_config['yardstick']


with open(os.path.join(curr_path, 'cmd_config.yml')) as f:
    cmd_yml = yaml.safe_load(f)
    dovetail_config['cli'] = cmd_yml[cmd_yml.keys()[0]]


def cmd_name_trans(cmd_name):
    key = cmd_name.upper()
    if key == 'SUT_TYPE':
        key = 'INSTALLER_TYPE'
    if key == 'SUT_IP':
        key = 'INSTALLER_IP'
    return key


def update_envs(options):
    for item in options:
        if options[item] is not None:
            key = cmd_name_trans(item)
            os.environ[key] = options[item]
            update_config_envs('functest', key)
            update_config_envs('yardstick', key)


def update_config_envs(test_type, key):
    old_value = re.findall(r'\s+%s=(.*?)(\s+|$)' % key,
                           dovetail_config[test_type]['envs'])
    if old_value == []:
        dovetail_config[test_type]['envs'] += \
            ' -e ' + key + '=' + os.environ[key]
    else:
        dovetail_config[test_type]['envs'] = \
            dovetail_config[test_type]['envs'].replace(old_value[0][0],
                                                       os.environ[key])
