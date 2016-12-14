#!/usr/bin/env python
#
# grakiss.wanglei@huawei.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

import os
import yaml

import utils.dovetail_logger as dt_logger

from parser import Parser
from utils.dovetail_config import DovetailConfig as dt_cfg
from test_runner import TestRunnerFactory


class Testcase(object):

    logger = None

    def __init__(self, testcase_yaml):
        self.testcase = testcase_yaml.values()[0]
        self.testcase['passed'] = False
        self.cmds = []
        self.sub_testcase_status = {}
        self.update_validate_testcase(self.validate_testcase())

    @classmethod
    def create_log(cls):
        cls.logger = dt_logger.Logger(__name__ + '.Testcase').getLogger()

    def prepare_cmd(self):
        try:
            for cmd in self.testcase['validate']['cmds']:
                cmd_lines = Parser.parse_cmd(cmd, self)
                if not cmd_lines:
                    return False
                # self.logger.debug('cmd_lines:%s', cmd_lines)
                self.cmds.append(cmd_lines)
            self.logger.debug('cmds:%s', self.cmds)
            if len(self.cmds) > 0:
                return True
            else:
                return False
        except KeyError:
            return False

    def __str__(self):
        return self.testcase

    def name(self):
        return self.testcase['name']

    def objective(self):
        return self.testcase['objective']

    def sub_testcase(self):
        try:
            return self.testcase['report']['sub_testcase_list']
        except KeyError:
            return []

    def sub_testcase_passed(self, name, passed=None):
        if passed is not None:
            self.logger.debug('sub_testcase_passed:%s %s', name, passed)
            self.sub_testcase_status[name] = passed
        return self.sub_testcase_status[name]

    def validate_type(self):
        return self.testcase['validate']['type']

    def validate_testcase(self):
        return self.testcase['validate']['testcase']

    def exceed_max_retry_times(self):
        # logger.debug('retry times:%d' % self.testcase['retry'])
        return self._exceed_max_retry_times(self.validate_testcase())

    def increase_retry(self):
        # self.testcase['retry'] = self.testcase['retry'] + 1
        # return self.testcase['retry']
        return self._increase_retry(self.validate_testcase())

    def passed(self, passed=None):
        if passed is not None:
            self.testcase['passed'] = passed
        return self.testcase['passed']

    def script_result_acquired(self, acquired=None):
        return self._result_acquired(self.validate_testcase(), acquired)

    def pre_condition(self):
        return self.pre_condition_cls(self.validate_type())

    def post_condition(self):
        return self.post_condition_cls(self.validate_type())

    def run(self):
        runner = TestRunnerFactory.create(self)
        try:
            runner.run()
        except AttributeError:
            pass

    # testcase in upstream testing project
    # validate_testcase_list = {'functest': {}, 'yardstick': {}, 'shell': {}}
    validate_testcase_list = {}
    # testcase in dovetail
    testcase_list = {}

    @classmethod
    def prepared(cls, prepared=None):
        if prepared is not None:
            cls.validate_testcase_list['prepared'] = prepared
        return cls.validate_testcase_list['prepared']

    @classmethod
    def cleaned(cls, cleaned=None):
        if cleaned is not None:
            cls.validate_testcase_list['cleaned'] = cleaned
        return cls.validate_testcase_list['cleaned']

    @staticmethod
    def pre_condition_cls(validate_type):
        return dt_cfg.dovetail_config[validate_type]['pre_condition']

    @staticmethod
    def post_condition_cls(validate_type):
        return dt_cfg.dovetail_config[validate_type]['post_condition']

    @classmethod
    def update_validate_testcase(cls, testcase_name):
        if testcase_name not in cls.validate_testcase_list:
            cls.validate_testcase_list[testcase_name] = \
                {'retry': 0, 'acquired': False}
            cls.validate_testcase_list['prepared'] = False
            cls.validate_testcase_list['cleaned'] = False

    @classmethod
    def _exceed_max_retry_times(cls, validate_testcase):
        retry = cls.validate_testcase_list[validate_testcase]['retry']
        return retry > 1

    @classmethod
    def _increase_retry(cls, validate_testcase):
        cls.validate_testcase_list[validate_testcase]['retry'] += 1
        return cls.validate_testcase_list[validate_testcase]['retry']

    @classmethod
    def _result_acquired(cls, testcase, acquired=None):
        if acquired is not None:
            cls.validate_testcase_list[testcase]['acquired'] = \
                acquired
        return cls.validate_testcase_list[testcase]['acquired']

    @classmethod
    def load(cls):
        for root, dirs, files in \
            os.walk(dt_cfg.dovetail_config['TESTCASE_PATH']):
            for testcase_file in files:
                with open(os.path.join(root, testcase_file)) as f:
                    testcase_yaml = yaml.safe_load(f)
                    case_type = testcase_yaml.values()[0]['validate']['type']
                    testcase = TestcaseFactory.create(case_type, testcase_yaml)
                    if testcase is not None:
                        cls.testcase_list[next(testcase_yaml.iterkeys())] = \
                            testcase
                    else:
                        cls.logger.error('failed to create testcase: %s',
                                         testcase_file)

    @classmethod
    def get(cls, testcase_name):
        if testcase_name in cls.testcase_list:
            return cls.testcase_list[testcase_name]
        return None


class FunctestTestcase(Testcase):

    validate_testcase_list = {}

    def __init__(self, testcase_yaml):
        super(FunctestTestcase, self).__init__(testcase_yaml)
        self.name = 'functest'

    def prepare_cmd(self):
        ret = super(FunctestTestcase, self).prepare_cmd()
        if not ret:
            for cmd in \
                dt_cfg.dovetail_config[self.name]['cmds']:
                cmd_lines = Parser.parse_cmd(cmd, self)
                if not cmd_lines:
                    return False
                self.logger.debug('cmd_lines:%s', cmd_lines)
                self.cmds.append(cmd_lines)
        return True


class YardstickTestcase(Testcase):

    validate_testcae_list = {}

    def __init__(self, testcase_yaml):
        super(YardstickTestcase, self).__init__(testcase_yaml)
        self.name = 'yardstick'


class ShellTestcase(Testcase):

    validate_testcase_list = {}

    def __init__(self, testcase_yaml):
        super(ShellTestcase, self).__init__(testcase_yaml)
        self.name = 'shell'


class TestcaseFactory(object):
    TESTCASE_TYPE_MAP = {
        'functest': FunctestTestcase,
        'yardstick': YardstickTestcase,
        'shell': ShellTestcase,
    }

    @classmethod
    def create(cls, testcase_type, testcase_yaml):
        try:
            return cls.TESTCASE_TYPE_MAP[testcase_type](testcase_yaml)
        except KeyError:
            return None


class Testsuite:

    logger = None

    def __init__(self, testsuite):
        self.testsuite = testsuite
        self.testcase_list = {}

    @classmethod
    def create_log(cls):
        cls.logger = dt_logger.Logger(__name__ + '.Testsuite').getLogger()

    def get_test(self, testcase_name):
        if testcase_name in self.testcase_list:
            return self.testcase_list[testcase_name]
        return None

    testsuite_list = {}

    @classmethod
    def load(cls):
        for root, dirs, files in \
            os.walk(dt_cfg.dovetail_config['COMPLIANCE_PATH']):
            for testsuite_yaml in files:
                with open(os.path.join(root, testsuite_yaml)) as f:
                    testsuite_yaml = yaml.safe_load(f)
                    cls.testsuite_list.update(testsuite_yaml)

        cls.logger.debug(cls.testsuite_list)

    @classmethod
    def get(cls, testsuite_name):
        if testsuite_name in cls.testsuite_list:
            return cls.testsuite_list[testsuite_name]
        return None
