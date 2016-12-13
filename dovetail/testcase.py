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
from conf.dovetail_config import DovetailConfig as dt_cfg


class Testcase:

    logger = None

    def __init__(self, testcase_yaml):
        self.testcase = testcase_yaml.values()[0]
        self.testcase['passed'] = False
        self.cmds = []
        self.sub_testcase_status = {}
        self.update_script_testcase(self.script_type(),
                                    self.script_testcase())

    @classmethod
    def create_log(cls):
        cls.logger = dt_logger.Logger(__name__ + '.Testcase').getLogger()

    def prepare_cmd(self):
        script_type = self.script_type()
        for cmd in dt_cfg.dovetail_config[script_type]['testcase']['cmds']:
            cmd_lines = Parser.parse_cmd(cmd, self)
            if not cmd_lines:
                return False
            self.cmds.append(cmd_lines)

        return True

    def __str__(self):
        return self.testcase

    def name(self):
        return self.testcase['name']

    def objective(self):
        return self.testcase['objective']

    def sub_testcase(self):
        return self.testcase['scripts']['sub_testcase_list']

    def sub_testcase_passed(self, name, passed=None):
        if passed is not None:
            self.logger.debug('sub_testcase_passed:%s %s' % (name, passed))
            self.sub_testcase_status[name] = passed
        return self.sub_testcase_status[name]

    def script_type(self):
        return self.testcase['scripts']['type']

    def script_testcase(self):
        return self.testcase['scripts']['testcase']

    def exceed_max_retry_times(self):
        # logger.debug('retry times:%d' % self.testcase['retry'])
        return self._exceed_max_retry_times(self.script_type(),
                                            self.script_testcase())

    def increase_retry(self):
        # self.testcase['retry'] = self.testcase['retry'] + 1
        # return self.testcase['retry']
        return self._increase_retry(self.script_type(), self.script_testcase())

    def passed(self, passed=None):
        if passed is not None:
            self.testcase['passed'] = passed
        return self.testcase['passed']

    def script_result_acquired(self, acquired=None):
        return self._result_acquired(self.script_type(),
                                     self.script_testcase(), acquired)

    def pre_condition(self):
        return self.pre_condition_cls(self.script_type())

    def post_condition(self):
        return self.post_condition_cls(self.script_type())

    # testcase in upstream testing project
    script_testcase_list = {'functest': {}, 'yardstick': {}}

    # testcase in dovetail
    testcase_list = {}

    @classmethod
    def prepared(cls, script_type, prepared=None):
        if prepared is not None:
            cls.script_testcase_list[script_type]['prepared'] = prepared
        return cls.script_testcase_list[script_type]['prepared']

    @classmethod
    def cleaned(cls, script_type, cleaned=None):
        if cleaned is not None:
            cls.scrpit_testcase_list[script_type]['cleaned'] = cleaned
        return cls.script_testcase_list[script_type]['cleaned']

    @staticmethod
    def pre_condition_cls(script_type):
        return dt_cfg.dovetail_config[script_type]['pre_condition']

    @staticmethod
    def post_condition_cls(script_type):
        return dt_cfg.dovetail_config[script_type]['post_condition']

    @classmethod
    def update_script_testcase(cls, script_type, script_testcase):
        if script_testcase not in cls.script_testcase_list[script_type]:
            cls.script_testcase_list[script_type][script_testcase] = \
                {'retry': 0, 'acquired': False}
            cls.script_testcase_list[script_type]['prepared'] = False
            cls.script_testcase_list[script_type]['cleaned'] = False

    @classmethod
    def _exceed_max_retry_times(cls, script_type, script_testcase):
        retry = cls.script_testcase_list[script_type][script_testcase]['retry']
        return retry > 1

    @classmethod
    def _increase_retry(cls, script_type, script_testcase):
        cls.script_testcase_list[script_type][script_testcase]['retry'] += 1
        return cls.script_testcase_list[script_type][script_testcase]['retry']

    @classmethod
    def _result_acquired(cls, script_type, testcase, acquired=None):
        if acquired is not None:
            cls.script_testcase_list[script_type][testcase]['acquired'] = \
                acquired
        return cls.script_testcase_list[script_type][testcase]['acquired']

    @classmethod
    def load(cls):
        for root, dirs, files in \
                 os.walk(dt_cfg.dovetail_config['TESTCASE_PATH']):
            for testcase_file in files:
                with open(os.path.join(root, testcase_file)) as f:
                    testcase_yaml = yaml.safe_load(f)
                    cls.testcase_list[testcase_yaml.keys()[0]] = \
                        cls(testcase_yaml)
        cls.logger.debug(cls.testcase_list)

    @classmethod
    def get(cls, testcase_name):
        if testcase_name in cls.testcase_list:
            return cls.testcase_list[testcase_name]
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
