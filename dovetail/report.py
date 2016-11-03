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

from conf.dovetail_config import dovetail_config
from testcase import Testcase

logger = dt_logger.Logger('report.py').getLogger()


def get_pass_str(passed):
    if passed:
        return 'PASS'
    else:
        return 'FAIL'


class Report:

    results = {'functest': {}, 'yardstick': {}}

    @classmethod
    def check_result(cls, testcase, db_result):
        checker = CheckerFactory.create(testcase.script_type())
        checker.check(testcase, db_result)

    @classmethod
    def generate(cls, scenario_yaml):
        report = ''

        report += '\n\
+==========================================================================+\n\
|                                   report                                 |\n\
+--------------------------------------------------------------------------+\n'
        report += '|scenario: %s\n' % scenario_yaml['name']
        for testcase_name in scenario_yaml['testcase_list']:
            testcase = Testcase.get(testcase_name)
            if testcase is None:
                continue
            report += '|   [testcase]: %s\t\t\t\t[%s]\n' % \
                (testcase_name, get_pass_str(testcase.passed()))
            report += '|   |-objective: %s\n' % testcase.objective()
            if testcase.sub_testcase() is not None:
                for subtest in testcase.sub_testcase():
                    report += '|       |-%s \t\t [%s]\n' % \
                        (subtest,
                         get_pass_str(testcase.sub_testcase_passed(subtest)))
            report += '+-----------------------------------------------------'
            report += '---------------------+\n'

        logger.info(report)
        cls.save(report)
        return report

    # save to disk as default
    @classmethod
    def save(cls, report):
        report_file_name = dovetail_config['report_file']
        try:
            with open(os.path.join(dovetail_config['result_dir'],
                      report_file_name), 'w') as report_file:
                report_file.write(report)
            logger.info('save report to %s' % report_file_name)
        except Exception:
            logger.error('Failed to save: %s' % report_file_name)

    @classmethod
    def get_result(cls, testcase):
        script_testcase = testcase.script_testcase()
        type = testcase.script_type()
        crawler = CrawlerFactory.create(type)

        if script_testcase in cls.results[type]:
            return cls.results[type][script_testcase]

        result = crawler.crawl(script_testcase)

        if result is not None:
            cls.results[type][script_testcase] = result
            testcase.script_result_acquired(True)
            logger.debug('testcase: %s -> result acquired' % script_testcase)
        else:
            retry = testcase.increase_retry()
            logger.debug('testcase: %s -> result acquired retry:%d' %
                         (script_testcase, retry))
        return result


class CrawlerFactory:

    @classmethod
    def create(cls, type):
        if type == 'functest':
            return FunctestCrawler()

        if type == 'yardstick':
            return YardstickCrawler()

        return None


class FunctestCrawler:

    def __init__(self):
        self.type = 'functest'

    def crawl(self, testcase=None):
        store_type = dovetail_config[self.type]['result']['store_type']
        if store_type == 'file':
            return self.crawl_from_file(testcase)

        if store_type == 'url':
            return self.crawl_from_url(testcase)

    def crawl_from_file(self, testcase=None):
        file_path = \
            os.path.join(dovetail_config['result_dir'],
                         dovetail_config[self.type]['result']['file_path'])
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
            failed_num = int(re.findall(' - Failed: (\d*)', output)[0])
            if failed_num != 0:
                criteria = 'FAIL'

            match = re.findall('Ran: (\d*) tests in (\d*)\.\d* sec.', output)
            num_tests, dur_sec_int = match[0]
            json_results = {'criteria': criteria, 'details': {"timestart": '',
                            "duration": int(dur_sec_int),
                            "tests": int(num_tests), "failures": failed_num,
                            "errors": error_logs}}
            logger.debug('Results: %s' % str(json_results))
            return json_results
        except Exception as e:
            logger.error('Cannot read content from the file: %s, exception: %s'
                         % (file_path, e))
            return None

    def crawl_from_url(self, testcase=None):
        url = dovetail_config[self.type]['result']['db_url'] % testcase
        logger.debug("Query to rest api: %s" % url)
        try:
            data = json.load(urllib2.urlopen(url))
            return data['results'][0]
        except Exception as e:
            logger.error("Cannot read content from the url: %s, exception: %s"
                         % (url, e))
            return None


class YardstickCrawler:

    def __init__(self):
        self.type = 'yardstick'

    def crawl(self, testcase=None):
        store_type = dovetail_config[self.type]['result']['store_type']
        if store_type == 'file':
            return self.crawl_from_file(testcase)

        if store_type == 'url':
            return self.crawl_from_url(testcase)

    def crawl_from_file(self, testcase=None):
        file_path = os.path.join(dovetail_config['result_dir'],
                                 testcase+'.out')
        if not os.path.exists(file_path):
            logger.info('result file not found: %s' % file_path)
            return None
        try:
            with open(file_path, 'r') as myfile:
                myfile.read()
            criteria = 'PASS'
            json_results = {'criteria': criteria}
            logger.debug('Results: %s' % str(json_results))
            return json_results
        except Exception as e:
            logger.error('Cannot read content from the file: %s, exception: %s'
                         % (file_path, e))
            return None

    def crawl_from_url(self, testcase=None):
        return None


class CheckerFactory:

    @classmethod
    def create(cls, type):
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
            logger.debug('check sub_testcase:%s' % sub_testcase)
            if sub_testcase in db_result['details']['errors']:
                testcase.sub_testcase_passed(sub_testcase, False)
                all_passed = False
            else:
                testcase.sub_testcase_passed(sub_testcase, True)

        testcase.passed(all_passed)


class YardstickChecker:

    def check(cls, testcase, result):
        if not result:
            testcase.passed(False)
        else:
            testcase.passed(result['criteria'] == 'PASS')
        return
