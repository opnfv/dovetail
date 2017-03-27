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
        self.logger.debug('create runner: %s', self.type)

    @classmethod
    def create_log(cls):
        cls.logger = dt_logger.Logger(__name__ + '.DockerRunner').getLogger()

    def run(self):
        if dt_cfg.dovetail_config['offline']:
            exist = Container.check_image_exist(self.testcase.validate_type())
            if not exist:
                self.logger.error('%s image not exist offline running',
                                  self.testcase.validate_type())
                return
        else:
            if not Container.pull_image(self.testcase.validate_type()):
                self.logger.error("Failed to pull the image.")
                return
        container_id = Container.create(self.testcase.validate_type())
        if not container_id:
            self.logger.error('failed to create container')
            return

        self.logger.debug('container id:%s', container_id)

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
            self.logger.error('failed to prepare testcase:%s',
                              self.testcase.name())
        else:
            for cmd in self.testcase.cmds:
                ret, msg = Container.exec_cmd(container_id, cmd)
                if ret != 0:
                    self.logger.error('Failed to exec %s, ret:%d, msg:%s',
                                      cmd, ret, msg)
                    break

        cmds = self.testcase.post_condition()
        if cmds:
            for cmd in cmds:
                ret, msg = Container.exec_cmd(container_id, cmd)
        self.testcase.cleaned(True)

        Container.clean(container_id)


class FunctestRunner(DockerRunner):

    def __init__(self, testcase):
        self.type = 'functest'
        super(FunctestRunner, self).__init__(testcase)


class YardstickRunner(DockerRunner):

    def __init__(self, testcase):
        self.type = 'yardstick'
        super(YardstickRunner, self).__init__(testcase)


class ShellRunner(object):

    logger = None

    @classmethod
    def create_log(cls):
        cls.logger = dt_logger.Logger(__name__ + '.ShellRunner').getLogger()

    def __init__(self, testcase):
        super(ShellRunner, self).__init__()
        self.testcase = testcase
        self.type = 'shell'
        self.logger.debug('create runner:%s', self.type)

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
            self.logger.error('failed to prepare cmd:%s',
                              self.testcase.name())
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
        self.logger.debug('save result:%s', result_filename)
        try:
            with open(result_filename, 'w') as f:
                f.write(json.dumps(result))
        except Exception as e:
            self.logger.exception('Failed to write result into file:%s, \
                                   except:%s', result_filename, e)


class TestRunnerFactory(object):

    TEST_RUNNER_MAP = {
        "functest": FunctestRunner,
        "yardstick": YardstickRunner,
        "shell": ShellRunner,
    }

    @classmethod
    def create(cls, testcase):
        try:
            return cls.TEST_RUNNER_MAP[testcase.validate_type()](testcase)
        except KeyError:
            return None
