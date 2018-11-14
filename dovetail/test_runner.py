#!/usr/bin/env python
#
# Copyright (c) 2018 grakiss.wanglei@huawei.com and others.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

import json
import os

import jinja2
import jinja2.meta
import yaml

from container import Container
from dovetail import constants
from utils.dovetail_config import DovetailConfig as dt_cfg
import utils.dovetail_utils as dt_utils
import utils.dovetail_logger as dt_logger


class DockerRunner(object):

    logger = None

    def __init__(self, testcase):
        self.testcase = testcase
        self.logger.debug('Create runner: {}'.format(self.type))

    @classmethod
    def create_log(cls):
        cls.logger = dt_logger.Logger(__name__ + '.DockerRunner').getLogger()

    def pre_copy(self, container=None, dest_path=None,
                 src_file=None, exist_file=None):
        if not container:
            self.logger.error("Container instance is None.")
            return None
        if not dest_path:
            self.logger.error("There has no dest_path in {} config file."
                              .format(self.testcase.name()))
            return None
        if src_file:
            self.testcase.mk_src_file()
            file_path = dt_cfg.dovetail_config[self.type]['result']['dir']
            src_path = os.path.join(file_path, src_file)
        if exist_file:
            file_path = dt_cfg.dovetail_config[self.type]['config']['dir']
            src_path = os.path.join(file_path, 'pre_config', exist_file)

        container.copy_file(src_path, dest_path)
        return dest_path

    def run(self):
        container = Container(self.testcase)
        docker_image = container.get_docker_image()
        if dt_cfg.dovetail_config['offline']:
            exist = container.get_image_id(docker_image)
            if not exist:
                self.logger.error("{} image doesn't exist, can't run offline."
                                  .format(self.testcase.validate_type()))
                return
        else:
            if not container.pull_image(docker_image):
                self.logger.error("Failed to pull the image.")
                return

        container_id = container.create(docker_image)
        if not container_id:
            self.logger.error('Failed to create container.')
            return

        self.logger.debug('container id: {}'.format(container_id))

        dest_path = self.testcase.pre_copy_path('dest_path')
        src_file_name = self.testcase.pre_copy_path('src_file')
        exist_file_name = self.testcase.pre_copy_path('exist_src_file')

        if src_file_name or exist_file_name:
            if not self.pre_copy(container, dest_path, src_file_name,
                                 exist_file_name):
                return

        cmds = self.testcase.pre_condition()
        if cmds:
            for cmd in cmds:
                ret, msg = container.exec_cmd(cmd)
                if ret != 0:
                    self.logger.error('Failed to exec all pre_condition cmds.')
                    break

        if not self.testcase.prepare_cmd(self.type):
            self.logger.error(
                'Failed to prepare test case: {}'.format(self.testcase.name()))
        else:
            for cmd in self.testcase.cmds:
                ret, msg = container.exec_cmd(cmd)
                if ret != 0:
                    self.logger.error('Failed to exec {}, ret: {}, msg: {}'
                                      .format(cmd, ret, msg))
                    break

        cmds = self.testcase.post_condition()
        if cmds:
            for cmd in cmds:
                container.exec_cmd(cmd)

        if not dt_cfg.dovetail_config['noclean']:
            container.clean()

    def archive_logs(self):
        result_path = os.path.join(os.environ['DOVETAIL_HOME'], 'results')
        src_files = dt_utils.get_value_from_dict(
            'report.source_archive_files', self.testcase.testcase)
        dest_files = dt_utils.get_value_from_dict(
            'report.dest_archive_files', self.testcase.testcase)
        if not src_files and not dest_files:
            return True
        if not (src_files and dest_files) or len(src_files) != len(dest_files):
            self.logger.error("Can't find corresponding 'result_dest_files' "
                              "for 'result_source_files' with testcase {}"
                              .format(self.testcase.name()))
            return False
        res = True
        for index in range(0, len(src_files)):
            src_file_path = os.path.join(result_path, src_files[index])
            dest_file_path = os.path.join(result_path, dest_files[index])
            if os.path.isfile(src_file_path):
                os.renames(src_file_path, dest_file_path)
            else:
                self.logger.error("Can't find file {}.".format(src_file_path))
                res = False
        return res

    @staticmethod
    def _render(task_template, **kwargs):
        return jinja2.Template(task_template).render(**kwargs)

    @staticmethod
    def _add_testcase_info(testcase, config_item=None):
        if not config_item:
            config_item = {}
        config_item['validate_testcase'] = testcase.validate_testcase()
        config_item['testcase'] = testcase.name()
        config_item['os_insecure'] = os.getenv('OS_INSECURE')
        if 'DEPLOY_SCENARIO' in os.environ:
            config_item['deploy_scenario'] = os.environ['DEPLOY_SCENARIO']
        config_item['dovetail_home'] = os.getenv('DOVETAIL_HOME')
        config_item['debug'] = os.getenv('DEBUG')
        config_item['build_tag'] = dt_cfg.dovetail_config['build_tag']
        config_item['cacert'] = os.getenv('OS_CACERT')
        return config_item

    def _update_openstack_config(self, testcase):
        config_item = None
        pod_file = os.path.join(dt_cfg.dovetail_config['config_dir'],
                                dt_cfg.dovetail_config['pod_file'])
        config_file = os.path.join(constants.CONF_PATH, self.config_file_name)
        pod_info = dt_utils.read_yaml_file(pod_file, self.logger)
        task_template = dt_utils.read_plain_file(config_file, self.logger)
        if not task_template:
            return None
        if pod_info:
            try:
                process_info = pod_info['process_info']
            except KeyError as e:
                process_info = None
        else:
            process_info = None
        if process_info:
            for item in process_info:
                try:
                    if item['testcase_name'] == testcase.name():
                        config_item = self._add_testcase_info(testcase, item)
                        break
                except KeyError as e:
                    self.logger.error('Need key {} in {}'.format(e, item))
        if not config_item:
            config_item = self._add_testcase_info(testcase)
        full_task = self._render(task_template, **config_item)
        full_task_yaml = yaml.safe_load(full_task)
        dt_cfg.dovetail_config.update(full_task_yaml)
        return dt_cfg.dovetail_config


    def _update_config(self, testcase):
        config_file = os.path.join(constants.CONF_PATH, self.config_file_name)
        task_template = dt_utils.read_plain_file(config_file, self.logger)
        if not task_template:
            return None
        config_item = self._add_testcase_info(testcase)
        full_task = self._render(task_template, **config_item)
        full_task_yaml = yaml.safe_load(full_task)
        dt_cfg.dovetail_config.update(full_task_yaml)
        return dt_cfg.dovetail_config


class FunctestRunner(DockerRunner):

    config_file_name = 'functest_config.yml'

    def __init__(self, testcase):
        self.type = 'functest'
        super(FunctestRunner, self).__init__(testcase)
        endpoint_file = os.path.join(dt_cfg.dovetail_config['result_dir'],
                                     'endpoint_info.json')
        if not os.path.isfile(endpoint_file):
            dt_utils.get_openstack_info(self.logger)
        self._update_openstack_config(testcase)


class FunctestK8sRunner(DockerRunner):

    config_file_name = 'functest-k8s_config.yml'

    def __init__(self, testcase):
        self.type = 'functest-k8s'
        super(FunctestK8sRunner, self).__init__(testcase)
        self._update_config(testcase)


class YardstickRunner(DockerRunner):

    config_file_name = 'yardstick_config.yml'

    def __init__(self, testcase):
        self.type = 'yardstick'
        super(YardstickRunner, self).__init__(testcase)
        endpoint_file = os.path.join(dt_cfg.dovetail_config['result_dir'],
                                     'endpoint_info.json')
        if not os.path.isfile(endpoint_file):
            dt_utils.get_openstack_info(self.logger)
        self._update_openstack_config(testcase)


class BottlenecksRunner(DockerRunner):

    config_file_name = 'bottlenecks_config.yml'

    def __init__(self, testcase):
        self.type = 'bottlenecks'
        super(BottlenecksRunner, self).__init__(testcase)
        endpoint_file = os.path.join(dt_cfg.dovetail_config['result_dir'],
                                     'endpoint_info.json')
        if not os.path.isfile(endpoint_file):
            dt_utils.get_openstack_info(self.logger)
        self._update_openstack_config(testcase)


class ShellRunner(object):

    logger = None

    @classmethod
    def create_log(cls):
        cls.logger = dt_logger.Logger(__name__ + '.ShellRunner').getLogger()

    def __init__(self, testcase):
        super(ShellRunner, self).__init__()
        self.testcase = testcase
        self.type = 'shell'
        self.logger.debug('Create runner: {}'.format(self.type))

    def run(self):
        testcase_passed = 'PASS'
        result = {'pass': 'PASS', 'results': []}
        cmds = self.testcase.pre_condition()
        for cmd in cmds:
            ret, msg = dt_utils.exec_cmd(cmd, self.logger)
            result['results'].append((cmd, ret, msg))
            if ret != 0:
                self.logger.error('Failed to execute all pre_condition cmds.')
                break

        if not self.testcase.prepare_cmd(self.type):
            self.logger.error(
                'Failed to prepare cmd: {}'.format(self.testcase.name()))
        else:
            for cmd in self.testcase.cmds:
                ret, msg = dt_utils.exec_cmd(cmd, self.logger)
                result['results'].append((cmd, ret, msg))
                if ret != 0:
                    testcase_passed = 'FAIL'

        result['pass'] = testcase_passed

        cmds = self.testcase.post_condition()
        for cmd in cmds:
            ret, msg = dt_utils.exec_cmd(cmd, self.logger)
            result['results'].append((cmd, ret, msg))

        result_filename = os.path.join(dt_cfg.dovetail_config['result_dir'],
                                       self.testcase.name()) + '.out'
        self.logger.debug('Save result: {}'.format(result_filename))
        try:
            with open(result_filename, 'w') as f:
                f.write(json.dumps(result))
        except Exception as e:
            self.logger.exception('Failed to write result into file: {}, '
                                  'exception: {}'.format(result_filename, e))


class VnftestRunner(DockerRunner):

    def __init__(self, testcase):
        self.type = 'vnftest'
        super(VnftestRunner, self).__init__(testcase)


class TestRunnerFactory(object):

    TEST_RUNNER_MAP = {
        "functest": FunctestRunner,
        "yardstick": YardstickRunner,
        "bottlenecks": BottlenecksRunner,
        "shell": ShellRunner,
        "vnftest": VnftestRunner,
        "functest-k8s": FunctestK8sRunner
    }

    @classmethod
    def create(cls, testcase):
        try:
            return cls.TEST_RUNNER_MAP[testcase.validate_type()](testcase)
        except KeyError:
            return None
