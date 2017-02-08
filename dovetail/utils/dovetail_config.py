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


class DovetailConfig(object):

    dovetail_config = {}

    CMD_NAME_TRANS = {
        'SUT_TYPE': 'INSTALLER_TYPE',
        'SUT_IP': 'INSTALLER_IP',
        'DEBUG': 'CI_DEBUG',
    }

    @classmethod
    def load_config_files(cls):
        curr_path = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(os.path.dirname(curr_path), 'conf')
        with open(os.path.join(config_path, 'dovetail_config.yml')) as f:
            cls.dovetail_config = yaml.safe_load(f)

        for extra_config_file in cls.dovetail_config['include_config']:
            with open(os.path.join(config_path, extra_config_file)) as f:
                extra_config = yaml.safe_load(f)
                cls.dovetail_config.update(extra_config)

        path = os.path.join(config_path, cls.dovetail_config['cli_file_name'])
        with open(path) as f:
            cmd_yml = yaml.safe_load(f)
            cls.dovetail_config['cli'] = cmd_yml[cmd_yml.keys()[0]]

    @classmethod
    def cmd_name_trans(cls, cmd_name):
        key = cmd_name.upper()
        return cls.CMD_NAME_TRANS.get(key, key)

    # Analyze the kind of the giving path,
    # return true for env path,
    # return false for non_env path.
    @classmethod
    def is_env_path(cls, path):
        if len(path) == 2:
            test_project = cls.dovetail_config['test_project']
            if path[0] in test_project and path[1] == 'envs':
                return True
        else:
            return False

    # update dovetail_config dict with the giving path.
    # if path is in the dovetail_config dict, its value will be replaced.
    # if path is not in the dict, it will be added as a new item of the dict.
    @classmethod
    def update_config(cls, config_dict):
        for key, value in config_dict.items():
            path_list = []
            for item in value['path']:
                path_list.append([(k.strip()) for k in item.split('/')])
            for path in path_list:
                if cls.is_env_path(path):
                    cls.update_envs(key, path, value['value'])
                else:
                    cls.update_non_envs(path, value['value'])

    @classmethod
    def update_envs(cls, key, path, value):
        key = cls.cmd_name_trans(key)
        if not value and key in os.environ:
            value = os.environ[key]
        if value:
            cls.update_config_envs(path[0], key, value)

    @classmethod
    def update_config_envs(cls, validate_type, key, value):
        envs = cls.dovetail_config[validate_type]['envs']
        old_value = re.findall(r'\s+%s=(.*?)(\s+|$)' % key, envs)
        if old_value == []:
            envs += ' -e ' + key + '=' + value
        else:
            envs = envs.replace(old_value[0][0], value)
        cls.dovetail_config[validate_type]['envs'] = envs
        return envs

    @staticmethod
    def set_leaf_dict(dic, path, value):
        for key in path[:-1]:
            dic = dic.setdefault(key, {})
        dic[path[-1]] = value

    @classmethod
    def update_non_envs(cls, path, value):
        if value:
            cls.set_leaf_dict(cls.dovetail_config, path, value)
