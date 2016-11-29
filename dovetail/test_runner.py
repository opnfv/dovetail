#!/usr/bin/env python
#
# grakiss.wanglei@huawei.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

import utils.dovetail_utils as dt_utils
import utils.dovetail_logger as dt_logger

from container import Container


class DockerRunner(object):

    logger = None

    def __init__(self, testcase):
        self.testcase = testcase

    @classmethod
    def create_log(cls):
        cls.logger = dt_logger.Logger(__file__).getLogger()

    def run(self):
        Container.pull_image(self.testcase.validate_type())
        container_id = Container.create(self.testcase.validate_type())
        self.logger.debug('container id:%s' % container_id)

        if not self.testcase.prepared():
            cmds = self.testcase.pre_condition()
            if cmds:
                for cmd in cmds:
                    Container.exec_cmd(container_id, cmd)
            self.testcase.prepared(True)

        if not self.testcase.prepare_cmd():
            self.logger.error('failed to prepare testcase:%s',
                              self.testcase.name())
        else:
            for cmd in self.testcase.cmds:
                Container.exec_cmd(container_id, cmd)

        cmds = self.testcase.post_condition()
        if cmds:
            for cmd in cmds:
                Container.exec_cmd(container_id, cmd)
        self.testcase.cleaned(True)

        Container.clean(container_id)


class FunctestRunner(DockerRunner):

    def __init__(self, testcase):
        super(FunctestRunner, self).__init__(testcase)
        self.name = 'functest'


class YardstickRunner(DockerRunner):

    def __init__(self, testcase):
        super(YardstickRunner, self).__init__(testcase)
        self.name = 'yardstick'


class ShellRunner(object):

    logger = None

    @classmethod
    def create_log(cls):
        cls.logger = dt_logger.Logger(__file__).getLogger()

    def __init__(self, testcase):
        super(ShellRunner, self).__init__()
        self.testcase = testcase
        self.name = 'shell'

    def run(self):
        for cmd in self.testcase.cmds:
            dt_utils.exec_cmd(cmd, self.logger)


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
