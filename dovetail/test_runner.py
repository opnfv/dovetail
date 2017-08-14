#!/usr/bin/env python
#
# grakiss.wanglei@huawei.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

import os
import json
import utils.dovetail_utils as dt_utils
import utils.dovetail_logger as dt_logger
from utils.dovetail_config import DovetailConfig as dt_cfg

from container import Container


class DockerRunner(object):

    logger = None

    def __init__(self, testcase):
        self.testcase = testcase
        self.logger.debug('Create runner: {}'.format(self.type))

    @classmethod
    def create_log(cls):
        cls.logger = dt_logger.Logger(__name__ + '.DockerRunner').getLogger()

    def pre_copy(self, container_id=None, dest_path=None,
                 src_file=None, exist_file=None, tempest_dest_path=None):
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
        Container.pre_copy(container_id, src_path, dest_path)

        if tempest_dest_path:
            file_path = dt_cfg.dovetail_config[self.type]['config']['dir']
            file_name = dt_cfg.dovetail_config['tempest_conf']
            src_path = os.path.join(file_path, 'pre_config', file_name)
            Container.pre_copy(container_id, src_path, tempest_dest_path)

        return dest_path

    def run(self):
        if dt_cfg.dovetail_config['offline']:
            exist = Container.check_image_exist(self.testcase.validate_type())
            if not exist:
                self.logger.error("{} image doesn't exist, can't run offline."
                                  .format(self.testcase.validate_type()))
                return
        else:
            if not Container.pull_image(self.testcase.validate_type()):
                self.logger.error("Failed to pull the image.")
                return
        # for sdnvpn, there is a need to download needed images to config_dir
        # in dovetail_config.yml first.
        if 'sdnvpn' in str(self.testcase.name()):
            img_name = dt_cfg.dovetail_config['sdnvpn_image']
            img_file = os.path.join(dt_cfg.dovetail_config['config_dir'],
                                    img_name)
            if not os.path.isfile(img_file):
                self.logger.error('Image {} not found.'.format(img_name))
                return
        container_id = Container.create(self.testcase.validate_type(),
                                        self.testcase.name())
        if not container_id:
            self.logger.error('Failed to create container.')
            return

        self.logger.debug('container id: {}'.format(container_id))

        dest_path = self.testcase.pre_copy_path("dest_path")
        src_file_name = self.testcase.pre_copy_path("src_file")
        exist_file_name = self.testcase.pre_copy_path("exist_src_file")
        tempest_dest_path = self.testcase.pre_copy_path("tempest_config_path")

        if src_file_name or exist_file_name or tempest_dest_path:
            if not self.pre_copy(container_id, dest_path, src_file_name,
                                 exist_file_name, tempest_dest_path):
                return

        if not self.testcase.prepared():
            prepare_failed = False
            cmds = self.testcase.pre_condition()
            if cmds:
                for cmd in cmds:
                    ret, msg = Container.exec_cmd(container_id, cmd)
                    if ret != 0:
                        prepare_failed = True
                        break
            if not prepare_failed:
                self.testcase.prepared(True)

        if not self.testcase.prepare_cmd(self.type):
            self.logger.error(
                'Failed to prepare test case: {}'.format(self.testcase.name()))
        else:
            for cmd in self.testcase.cmds:
                ret, msg = Container.exec_cmd(container_id, cmd)
                if ret != 0:
                    self.logger.error('Failed to exec {}, ret: {}, msg: {}'
                                      .format(cmd, ret, msg))
                    break

        cmds = self.testcase.post_condition()
        if cmds:
            for cmd in cmds:
                ret, msg = Container.exec_cmd(container_id, cmd)
        self.testcase.cleaned(True)

        Container.clean(container_id, self.type)


class FunctestRunner(DockerRunner):

    def __init__(self, testcase):
        self.type = 'functest'
        super(FunctestRunner, self).__init__(testcase)


class YardstickRunner(DockerRunner):

    def __init__(self, testcase):
        self.type = 'yardstick'
        super(YardstickRunner, self).__init__(testcase)


class BottlenecksRunner(DockerRunner):

    def __init__(self, testcase):
        self.type = 'bottlenecks'
        super(BottlenecksRunner, self).__init__(testcase)


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
        prepare_failed = False
        result = {'pass': 'PASS', 'results': []}
        if not self.testcase.prepared():
            cmds = self.testcase.pre_condition()
            for cmd in cmds:
                ret, msg = dt_utils.exec_cmd(cmd, self.logger)
                result['results'].append((cmd, ret, msg))
                if ret != 0:
                    prepare_failed = True
                    break
            if not prepare_failed:
                self.testcase.prepared(True)

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


class TestRunnerFactory(object):

    TEST_RUNNER_MAP = {
        "functest": FunctestRunner,
        "yardstick": YardstickRunner,
        "bottlenecks": BottlenecksRunner,
        "shell": ShellRunner,
    }

    @classmethod
    def create(cls, testcase):
        try:
            return cls.TEST_RUNNER_MAP[testcase.validate_type()](testcase)
        except KeyError:
            return None
