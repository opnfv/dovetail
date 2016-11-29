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
import re
import os

import utils.dovetail_logger as dt_logger

from conf.dovetail_config import DovetailConfig as dt_config
from testcase import Testcase


def get_pass_str(passed):
    if passed:
        return 'PASS'
    else:
        return 'FAIL'


class Report:

    results = {'functest': {}, 'yardstick': {}, 'shell': {}}

    logger = None

    @classmethod
    def create_log(cls):
        cls.logger = dt_logger.Logger(__name__+'.Report').getLogger()

    @staticmethod
    def check_result(testcase, db_result):
        checker = CheckerFactory.create(testcase.script_type())
        if checker is not None:
            checker.check(testcase, db_result)

    @classmethod
    def generate_json(cls, testsuite_yaml, testarea):
        report_obj = {}
        report_obj['testsuite'] = testsuite_yaml['name']
        report_obj['testcases_list'] = []
        testarea_list = []
        for value in testsuite_yaml['testcases_list']:
            if value is not None and (testarea == 'full' or testarea in value):
                testarea_list.append(value)
        for testcase_name in testarea_list:
            testcase = Testcase.get(testcase_name)
            testcase_in_rpt = {}
            testcase_in_rpt['name'] = testcase_name
            if testcase is None:
                testcase_in_rpt['result'] = 'Undefined'
                testcase_in_rpt['objective'] = ''
                testcase_in_rpt['sub_testcase'] = []
                report_obj['testcases_list'].append(testcase_in_rpt)
                continue

            testcase_in_rpt['result'] = get_pass_str(testcase.passed())
            testcase_in_rpt['objective'] = testcase.objective()
            testcase_in_rpt['sub_testcase'] = []
            if testcase.sub_testcase() is not None:
                for sub_test in testcase.sub_testcase():
                    testcase_in_rpt['sub_testcase'].append({
                        'name': sub_test,
                        'result': get_pass_str(
                            testcase.sub_testcase_passed(sub_test))
                    })
            report_obj['testcases_list'].append(testcase_in_rpt)
        cls.logger.info(json.dumps(report_obj))
        return report_obj

    @classmethod
    def generate(cls, testsuite_yaml, testarea):
        rpt_data = cls.generate_json(testsuite_yaml, testarea)
        rpt_text = ''
        split_line = '+-----------------------------------------------------'
        split_line += '---------------------+\n'

        rpt_text += '\n\
+==========================================================================+\n\
|                                   report                                 |\n'
        rpt_text += split_line
        rpt_text += '|testsuite: %s\n' % rpt_data['testsuite']
        for testcase in rpt_data['testcases_list']:
            rpt_text += '|   [testcase]: %s\t\t\t\t[%s]\n' % \
                (testcase['name'], testcase['result'])
            rpt_text += '|   |-objective: %s\n' % testcase['objective']
            if 'sub_testcase' in testcase:
                for sub_test in testcase['sub_testcase']:
                    rpt_text += '|       |-%s \t\t [%s]\n' % \
                        (sub_test['name'], sub_test['result'])
            rpt_text += split_line

        cls.logger.info(rpt_text)
        cls.save(rpt_text)
        return rpt_text

    # save to disk as default
    @classmethod
    def save(cls, report):
        report_file_name = dt_config.dovetail_config['report_file']
        try:
            with open(os.path.join(dt_config.dovetail_config['result_dir'],
                      report_file_name), 'w') as report_file:
                report_file.write(report)
            cls.logger.info('save report to %s' % report_file_name)
        except Exception:
            cls.logger.error('Failed to save: %s' % report_file_name)

    @classmethod
    def get_result(cls, testcase):
        script_testcase = testcase.script_testcase()
        type = testcase.script_type()
        crawler = CrawlerFactory.create(type)
        if crawler is None:
            return None

        if script_testcase in cls.results[type]:
            return cls.results[type][script_testcase]

        result = crawler.crawl(script_testcase)

        if result is not None:
            cls.results[type][script_testcase] = result
            testcase.script_result_acquired(True)
            cls.logger.debug('testcase: %s -> result acquired' %
                             script_testcase)
        else:
            retry = testcase.increase_retry()
            cls.logger.debug('testcase: %s -> result acquired retry:%d' %
                             (script_testcase, retry))
        return result


class CrawlerFactory:

    @staticmethod
    def create(type):
        if type == 'functest':
            return FunctestCrawler()

        if type == 'yardstick':
            return YardstickCrawler()

        return None


class FunctestCrawler:

    logger = None

    def __init__(self):
        self.type = 'functest'

    @classmethod
    def create_log(cls):
        cls.logger = dt_logger.Logger(__name__+'.FunctestCrawler').getLogger()

    def crawl(self, testcase=None):
        store_type = \
            dt_config.dovetail_config[self.type]['result']['store_type']
        if store_type == 'file':
            return self.crawl_from_file(testcase)

        if store_type == 'url':
            return self.crawl_from_url(testcase)

    def crawl_from_file(self, testcase=None):
        dovetail_config = dt_config.dovetail_config
        file_path = \
            os.path.join(dovetail_config['result_dir'],
                         dovetail_config[self.type]['result']['file_path'])
        if not os.path.exists(file_path):
            self.logger.info('result file not found: %s' % file_path)
            return None

        try:
            with open(file_path, 'r') as myfile:
                output = myfile.read()
            error_logs = ""

            for match in re.findall('(.*?)[. ]*FAILED', output):
                error_logs += match

            criteria = 'PASS'
            failed_num = int(re.findall(' - Failed: (\d*)', output)[0])
            if failed_num != 0:
                criteria = 'FAIL'

            match = re.findall('Ran: (\d*) tests in (\d*)\.\d* sec.', output)
            num_tests, dur_sec_int = match[0]
            json_results = {'criteria': criteria, 'details': {"timestart": '',
                            "duration": int(dur_sec_int),
                            "tests": int(num_tests), "failures": failed_num,
                            "errors": error_logs}}
            self.logger.debug('Results: %s' % str(json_results))
            return json_results
        except Exception as e:
            self.logger.error('Cannot read content from the file: %s, '
                              'exception: %s' % (file_path, e))
            return None

    def crawl_from_url(self, testcase=None):
        url = \
            dt_config.dovetail_config[self.type]['result']['db_url'] % testcase
        self.logger.debug("Query to rest api: %s" % url)
        try:
            data = json.load(urllib2.urlopen(url))
            return data['results'][0]
        except Exception as e:
            self.logger.error("Cannot read content from the url: %s, "
                              "exception: %s" % (url, e))
            return None


class YardstickCrawler:

    logger = None

    def __init__(self):
        self.type = 'yardstick'

    @classmethod
    def create_log(cls):
        cls.logger = dt_logger.Logger(__name__+'.YardstickCrawler').getLogger()

    def crawl(self, testcase=None):
        store_type = \
            dt_config.dovetail_config[self.type]['result']['store_type']
        if store_type == 'file':
            return self.crawl_from_file(testcase)

        if store_type == 'url':
            return self.crawl_from_url(testcase)

    def crawl_from_file(self, testcase=None):
        file_path = os.path.join(dt_config.dovetail_config['result_dir'],
                                 testcase+'.out')
        if not os.path.exists(file_path):
            self.logger.info('result file not found: %s' % file_path)
            return None
        try:
            with open(file_path, 'r') as myfile:
                myfile.read()
            criteria = 'PASS'
            json_results = {'criteria': criteria}
            self.logger.debug('Results: %s' % str(json_results))
            return json_results
        except Exception as e:
            self.logger.error('Cannot read content from the file: %s, '
                              'exception: %s' % (file_path, e))
            return None

    def crawl_from_url(self, testcase=None):
        return None


class CheckerFactory:

    @staticmethod
    def create(type):
        if type == 'functest':
            return FunctestChecker()

        if type == 'yardstick':
            return YardstickChecker()

        return None


class ResultChecker:

    @staticmethod
    def check():
        return 'PASS'


class FunctestChecker:

    logger = None

    @classmethod
    def create_log(cls):
        cls.logger = dt_logger.Logger(__name__+'.FunctestChecker').getLogger()

    def check(self, testcase, db_result):
        sub_testcase_list = testcase.sub_testcase()

        if not db_result:
            if sub_testcase_list is not None:
                for sub_testcase in sub_testcase_list:
                    testcase.sub_testcase_passed(sub_testcase, False)
            return

        testcase.passed(db_result['criteria'] == 'PASS')

        if sub_testcase_list is None:
            return

        if testcase.testcase['passed'] is True:
            for sub_testcase in sub_testcase_list:
                testcase.sub_testcase_passed(sub_testcase, True)
            return

        all_passed = True
        for sub_testcase in sub_testcase_list:
            self.logger.debug('check sub_testcase:%s' % sub_testcase)
            if sub_testcase in db_result['details']['errors']:
                testcase.sub_testcase_passed(sub_testcase, False)
                all_passed = False
            else:
                testcase.sub_testcase_passed(sub_testcase, True)

        testcase.passed(all_passed)


class YardstickChecker:

    logger = None

    @classmethod
    def create_log(cls):
        cls.logger = dt_logger.Logger(__name__+'.YardstickChecker').getLogger()

    @staticmethod
    def check(testcase, result):
        if not result:
            testcase.passed(False)
        else:
            testcase.passed(result['criteria'] == 'PASS')
        return
