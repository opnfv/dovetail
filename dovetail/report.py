#!/usr/bin/env python
#
# grakiss.wanglei@huawei.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#
from __future__ import division

import json
import urllib2
import re
import os
import datetime
import uuid

import utils.dovetail_logger as dt_logger

from conf.dovetail_config import DovetailConfig as dt_cfg
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
        cls.logger = dt_logger.Logger(__name__ + '.Report').getLogger()

    @staticmethod
    def check_result(testcase, db_result):
        checker = CheckerFactory.create(testcase.validate_type())
        if checker is not None:
            checker.check(testcase, db_result)

    @classmethod
    def generate_json(cls, testsuite_yaml, testarea, duration):
        report_obj = {}
        # TO DO: once version scheme settled, adjust accordingly
        report_obj['version'] = '1.0'
        report_obj['testsuite'] = testsuite_yaml['name']
        # TO DO: once dashboard url settled, adjust accordingly
        report_obj['dashboard'] = None
        report_obj['validation_ID'] = str(uuid.uuid4())
        report_obj['upload_date'] =\
            datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        report_obj['duration'] = duration

        report_obj['testcases_list'] = []
        testarea_list = []
        for value in testsuite_yaml['testcases_list']:
            if value is not None and (testarea == 'full' or testarea in value):
                testarea_list.append(value)
        for testcase_name in testarea_list:
            testcase = Testcase.get(testcase_name)
            testcase_inreport = {}
            testcase_inreport['name'] = testcase_name
            if testcase is None:
                testcase_inreport['result'] = 'Undefined'
                testcase_inreport['objective'] = ''
                testcase_inreport['sub_testcase'] = []
                report_obj['testcases_list'].append(testcase_inreport)
                continue

            testcase_inreport['result'] = get_pass_str(testcase.passed())
            testcase_inreport['objective'] = testcase.objective()
            testcase_inreport['sub_testcase'] = []
            if testcase.sub_testcase() is not None:
                for sub_test in testcase.sub_testcase():
                    testcase_inreport['sub_testcase'].append({
                        'name': sub_test,
                        'result': get_pass_str(
                            testcase.sub_testcase_passed(sub_test))
                    })
            report_obj['testcases_list'].append(testcase_inreport)
        cls.logger.info(json.dumps(report_obj))
        return report_obj

    @classmethod
    def generate(cls, testsuite_yaml, testarea, duration):
        report_data = cls.generate_json(testsuite_yaml, testarea, duration)
        report_txt = ''
        report_txt += '\n\nDovetail Report\n'
        report_txt += 'Version: %s\n' % report_data['version']
        report_txt += 'TestSuite: %s\n' % report_data['testsuite']
        report_txt += 'Result Dashboard: %s\n' % report_data['dashboard']
        report_txt += 'Validation ID: %s\n' % report_data['validation_ID']
        report_txt += 'Upload Date: %s\n' % report_data['upload_date']
        if report_data['duration'] == 0:
            report_txt += 'Duration: %s\n\n' % 'N/A'
        else:
            report_txt += 'Duration: %.2f s\n\n' % report_data['duration']

        total_num = 0
        pass_num = 0
        sub_report = {}
        testcase_num = {}
        testcase_passnum = {}
        for area in dt_cfg.dovetail_config['testarea_supported']:
            sub_report[area] = ''
            testcase_num[area] = 0
            testcase_passnum[area] = 0

        # TO DO: once version scheme settled, adjust accordingly
        spec_link = dt_cfg.dovetail_config['repo'] + 'dovetail/testcase'
        for testcase in report_data['testcases_list']:
            pattern = re.compile(
                '|'.join(dt_cfg.dovetail_config['testarea_supported']))
            area = pattern.findall(testcase['name'])[0]
            result_dir = dt_cfg.dovetail_config['result_dir']
            sub_report[area] += '- <%s> %s result: <%s>\n' %\
                (spec_link, testcase['name'], result_dir)
            testcase_num[area] += 1
            total_num += 1
            if testcase['result'] == 'PASS':
                testcase_passnum[area] += 1
                pass_num += 1

        if total_num != 0:
            pass_rate = pass_num / total_num
            report_txt += 'Pass Rate: %.2f%% (%s/%s)\n' %\
                (pass_rate * 100, pass_num, total_num)
            report_txt += 'Assessed test areas:\n'
        for key in sub_report:
            if testcase_num[key] != 0:
                pass_rate = testcase_passnum[key] / testcase_num[key]
                # TO DO: once version scheme settled, adjust accordingly
                doc_link = dt_cfg.dovetail_config['repo'] +\
                    ('docs/testsuites/%s' % key)
                report_txt += '- %s results: <%s> pass %.2f%%\n' %\
                    (key, doc_link, pass_rate * 100)
        for key in sub_report:
            if testcase_num[key] != 0:
                pass_rate = testcase_passnum[key] / testcase_num[key]
                report_txt += '%s: pass rate %.2f%%\n' % (key, pass_rate * 100)
                report_txt += sub_report[key]

        cls.logger.info(report_txt)
        cls.save(report_txt)
        return report_txt

    # save to disk as default
    @classmethod
    def save(cls, report):
        report_file_name = dt_cfg.dovetail_config['report_file']
        try:
            with open(os.path.join(dt_cfg.dovetail_config['result_dir'],
                      report_file_name), 'w') as report_file:
                report_file.write(report)
            cls.logger.info('save report to %s' % report_file_name)
        except Exception:
            cls.logger.error('Failed to save: %s' % report_file_name)

    @classmethod
    def get_result(cls, testcase):
        validate_testcase = testcase.validate_testcase()
        type = testcase.validate_type()
        crawler = CrawlerFactory.create(type)
        if crawler is None:
            return None

        if validate_testcase in cls.results[type]:
            return cls.results[type][validate_testcase]

        result = crawler.crawl(validate_testcase)

        if result is not None:
            cls.results[type][validate_testcase] = result
            testcase.script_result_acquired(True)
            cls.logger.debug('testcase: %s -> result acquired' %
                             validate_testcase)
        else:
            retry = testcase.increase_retry()
            cls.logger.debug('testcase: %s -> result acquired retry:%d' %
                             (validate_testcase, retry))
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
        cls.logger = \
            dt_logger.Logger(__name__ + '.FunctestCrawler').getLogger()

    def crawl(self, testcase=None):
        store_type = \
            dt_cfg.dovetail_config[self.type]['result']['store_type']
        if store_type == 'file':
            return self.crawl_from_file(testcase)

        if store_type == 'url':
            return self.crawl_from_url(testcase)

    def crawl_from_file(self, testcase=None):
        dovetail_config = dt_cfg.dovetail_config
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
            dt_cfg.dovetail_config[self.type]['result']['db_url'] % testcase
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
        cls.logger = \
            dt_logger.Logger(__name__ + '.YardstickCrawler').getLogger()

    def crawl(self, testcase=None):
        store_type = \
            dt_cfg.dovetail_config[self.type]['result']['store_type']
        if store_type == 'file':
            return self.crawl_from_file(testcase)

        if store_type == 'url':
            return self.crawl_from_url(testcase)

    def crawl_from_file(self, testcase=None):
        file_path = os.path.join(dt_cfg.dovetail_config['result_dir'],
                                 testcase + '.out')
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
        cls.logger = \
            dt_logger.Logger(__name__ + '.FunctestChecker').getLogger()

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
        cls.logger = \
            dt_logger.Logger(__name__ + '.YardstickChecker').getLogger()

    @staticmethod
    def check(testcase, result):
        if not result:
            testcase.passed(False)
        else:
            testcase.passed(result['criteria'] == 'PASS')
        return
