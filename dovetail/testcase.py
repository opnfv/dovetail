#!/usr/bin/env python
#
# grakiss.wanglei@huawei.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

import jinja2

import utils.dovetail_logger as dt_logger
import utils.dovetail_utils as dt_utils

from parser import *

logger = dt_logger.Logger('testcase.py').getLogger()

from conf.dovetail_config import *


class Testcase:

    def __init__(self, testcase_yaml):
        self.testcase = testcase_yaml.values()[0]
        self.testcase['passed'] = False
        self.cmds = []
        self.sub_testcase_status = {}
        Testcase.update_script_testcase(self.script_type(),
                                        self.script_testcase())

    def prepare_cmd(self):
        for cmd in dovetail_config[self.script_type()]['testcase']['cmds']:
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
            logger.debug('sub_testcase_passed:%s %s' % (name,  passed))
            self.sub_testcase_status[name] = passed
        return self.sub_testcase_status[name]

    def script_type(self):
        return self.testcase['scripts']['type']

    def script_testcase(self):
        return self.testcase['scripts']['testcase']

    def exceed_max_retry_times(self):
        #logger.debug('retry times:%d' % self.testcase['retry'])
        return Testcase._exceed_max_retry_times(self.script_type(),
                                                self.script_testcase())

    def increase_retry(self):
        #self.testcase['retry'] = self.testcase['retry'] + 1
        #return self.testcase['retry']
        return Testcase._increase_retry(self.script_type(),
                                        self.script_testcase())

    def passed(self, passed=None):
        if passed is not None:
            self.testcase['passed'] = passed
        return self.testcase['passed']

    def script_result_acquired(self, acquired=None):
        return Testcase._result_acquired(self.script_type(),
                                         self.script_testcase(), acquired)

    def pre_condition(self):
        return Testcase.pre_condition(self.script_type())

    def post_condition(self):
        return Testcase.post_condition(self.script_type())

    #testcase in upstream testing project
    script_testcase_list = {'functest': {}, 'yardstick': {}}

    #testcase in dovetail
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

    @classmethod
    def pre_condition(cls, script_type):
        return dovetail_config[script_type]['pre_condition']

    def post_condition(cls, script_type):
        return dovetail_config[script_type]['post_condition']

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
        for root, dirs, files in os.walk(TESTCASE_PATH):
            for testcase_file in files:
                with open(os.path.join(root, testcase_file)) as f:
                    testcase_yaml = yaml.safe_load(f)
                    cls.testcase_list[testcase_yaml.keys()[0]] = \
                        Testcase(testcase_yaml)
        logger.debug(cls.testcase_list)

    @classmethod
    def get(cls, testcase_name):
        if testcase_name in cls.testcase_list:
            return cls.testcase_list[testcase_name]
        return None


class Scenario:

    def __init__(self, scenario):
        self.scenario = scenario
        self.testcase_list = {}

    def get_test(self, testcase_name):
        if testcase_name in self.testcase_list:
            return self.testcase_list[testcase_name]
        return None

    scenario_list = {}

    @classmethod
    def load(cls):
        for root, dirs, files in os.walk(CERT_PATH):
            for scenario_yaml in files:
                with open(os.path.join(root, scenario_yaml)) as f:
                    scenario_yaml = yaml.safe_load(f)
                    cls.scenario_list.update(scenario_yaml)

        logger.debug(cls.scenario_list)

    @classmethod
    def get(cls, scenario_name):
        if scenario_name in cls.scenario_list:
            return cls.scenario_list[scenario_name]
        return None

