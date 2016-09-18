#!/usr/bin/env python
#
# grakiss.wanglei@huawei.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#
import json
import urllib2

import utils.dovetail_logger as dt_logger
import utils.dovetail_utils as dt_utils

logger = dt_logger.Logger('report.py').getLogger()

from conf.dovetail_config import *
from testcase import *

def get_pass_str(passed):
    if passed:
        return 'PASS'
    else:
        return 'FAIL'

class Report:

    results = {'functest':{},'yardstick':{}}

    @classmethod
    def check_result(cls, testcase, db_result):
        checker = CheckerFactory.create(testcase.script_type())
        checker.check(testcase, db_result)

    @classmethod
    def generate(cls, scenario_yaml):
        report = ''

        report += '\n\
+=============================================================================+\n\
|                                   report                                    | \n\
+-----------------------------------------------------------------------------+\n'
        report += '|scenario: %s\n' % scenario_yaml['name']
        for testcase_name in scenario_yaml['testcase_list']:
            testcase = Testcase.get(testcase_name)
            report += '|   [testcase]: %s\t\t\t\t[%s]\n' % (testcase_name, get_pass_str(testcase.passed()))
            report += '|   |-objective: %s\n' % testcase.objective()
            if testcase.sub_testcase() is not None:
                for subtest in testcase.sub_testcase():
                    report += '|       |-%s \t\t [%s]\n' % (subtest, get_pass_str(testcase.sub_testcase_passed(subtest)))
            report += '+-----------------------------------------------------------------------------+\n'

        logger.info(report)
        return report

    @classmethod
    def get_result(cls, testcase):
        script_testcase = testcase.script_testcase()
        type = testcase.script_type()

        if script_testcase in cls.results[type]:
            return cls.results[type][script_testcase]

        if dovetail_config[type]['result']['store_type'] == 'file':
            result = cls.get_results_from_file(type)
        else:
            result = cls.get_results_from_db(type, script_testcase)

        if result is not None:
            cls.results[type][script_testcase] = result
            testcase.script_result_acquired(True)
            logger.debug('testcase: %s -> result acquired' % script_testcase)
        else:
            retry = testcase.increase_retry()
            logger.debug('testcase: %s -> result acquired retry:%d' % (script_testcase, retry))
        return result

    @classmethod
    def get_results_from_db(cls, type, testcase):
        #url = 'http://testresults.opnfv.org/test/api/v1/results?case=%s&last=1' % testcase
        url = dovetail_config[type]['result']['db_url'] % testcase
        logger.debug("Query to rest api: %s" % url)
        try:
            data = json.load(urllib2.urlopen(url))
            return data['results'][0]
        except:
            logger.error("Cannot read content from the url: %s" % url)
            return None

    @classmethod
    def get_results_from_file(cls, type, testcase=None):
        file_path = os.path.join(dovetail_config[type]['result']['dir'],dovetail_config[type]['result']['file_path'])
        if not os.path.exists(file_path):
            logger.info('result file not found: %s' % file_path) 
            return None

        try:
            with open(file_path, 'r') as myfile:
                output = myfile.read()
            error_logs = ""

            for match in re.findall('(.*?)[. ]*FAILED', output):
                error_logs += match

            criteria = 'PASS'
            if error_logs:
                criteria = 'FAIL'

            json_results = {'criteria':criteria,'details':{"timestart": time_start, "duration": dur_sec_int,
                            "tests": int(num_tests), "failures": int(num_failures),
                            "errors": error_logs}}
            logger.debug('Results: %s' % str(json_results))
            return json_results 
        except:
            logger.error('Cannot read content from the file: %s' % file_path)
            return None

class CheckerFactory:

    @classmethod
    def create(cls,type):
        if type == 'functest':
            return FunctestChecker()

        if type == 'yardstick':
            return YardstickChecker()

        return None

class ResultChecker:

    def check(cls):
        return 'PASS'

class FunctestChecker:

    def check(cls, testcase, db_result):
        if not db_result:
            for sub_testcase in testcase.sub_testcase():
                testcase.sub_testcase_passed(sub_testcase,False)
            return

        testcase.passed(db_result['criteria'] == 'PASS')

        if testcase.sub_testcase() is None:
            return

        if testcase.testcase['passed'] == True:
            for sub_testcase in testcase.sub_testcase():
                testcase.sub_testcase_passed(sub_testcase, True)
            return

        all_passed = True
        for sub_testcase in testcase.sub_testcase():
            logger.debug('check sub_testcase:%s' % sub_testcase)
            if sub_testcase in db_result['details']['errors']:
                testcase.sub_testcase_passed(sub_testcase, False)
                all_passed = False
            else:
                testcase.sub_testcase_passed(sub_testcase, True)

        testcase.passed(all_passed)

class YardstickChecker:

    def check(cls, testcase, result):
        return 'PASS'


