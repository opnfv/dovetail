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

logger = dt_logger.Logger(__file__).getLogger()


class TestRunnerFactory(object):

    @staticmethod
    def create(testcase):
        if testcase.script_type() == 'functest':
            return FunctestRunner(testcase)

        if testcase.script_type() == 'yardstick':
            return YardstickRunner(testcase)

        if testcase.script_type() == 'shell':
            return ShellRunner(testcase)

        return None


class DockerRunner(object):

    def __init__(self, testcase):
        self.testcase = testcase

    def run(self):
        Container.pull_image(self.testcase.script_type())
        container_id = Container.create(self.testcase.script_type())
        logger.debug('container id:%s' % container_id)

        if not self.testcase.prepared(self.testcase.script_type()):
            cmds = self.testcase.pre_condition()['cmds']
            if cmds:
                for cmd in cmds:
                    Container.exec_cmd(container_id, cmd)
            self.testcase.prepared(self.testcase.script_type(), True)

        if not self.testcase.prepare_cmd():
            logger.error('failed to prepare testcase:%s' %
                         self.testcase.name())
        else:
            for cmd in self.testcase.cmds:
                Container.exec_cmd(container_id, cmd)

        # testcase.post_condition()

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

    def __init__(self, testcase):
        super(ShellRunner, self).__init__()
        self.testcase = testcase
        self.name = 'shell'

    def run(self):
        for cmd in self.testcase.cmds:
            dt_utils.exec_cmd(cmd, logger)
