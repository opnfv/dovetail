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

from pbr import version

import utils.dovetail_logger as dt_logger

from utils.dovetail_config import DovetailConfig as dt_cfg
import utils.dovetail_utils as dt_utils
from testcase import Testcase


class Report(object):

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
        report_obj['version'] = \
            version.VersionInfo('dovetail').version_string()
        report_obj['testsuite'] = testsuite_yaml['name']
        # TO DO: once dashboard url settled, adjust accordingly
        report_obj['dashboard'] = None
        report_obj['build_tag'] = dt_cfg.dovetail_config['build_tag']
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

            testcase_inreport['result'] = testcase.passed()
            testcase_inreport['objective'] = testcase.objective()
            testcase_inreport['sub_testcase'] = []
            if testcase.sub_testcase() is not None:
                for sub_test in testcase.sub_testcase():
                    testcase_inreport['sub_testcase'].append({
                        'name': sub_test,
                        'result': testcase.sub_testcase_passed(sub_test)
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
        report_txt += 'Build Tag: %s\n' % report_data['build_tag']
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

        testarea_scope = []
        for testcase in report_data['testcases_list']:
            pattern = re.compile(
                '|'.join(dt_cfg.dovetail_config['testarea_supported']))
            area = pattern.findall(testcase['name'])
            if not area:
                cls.logger.error("testcase %s not in supported testarea",
                                 testcase['name'])
                return None
            area = area[0]
            testarea_scope.append(area)
            sub_report[area] += '-%-25s %s\n' %\
                (testcase['name'], testcase['result'])
            if 'sub_testcase' in testcase:
                for sub_test in testcase['sub_testcase']:
                    sub_report[area] += '\t%-110s %s\n' %\
                        (sub_test['name'], sub_test['result'])
            testcase_num[area] += 1
            total_num += 1
            if testcase['result'] == 'PASS':
                testcase_passnum[area] += 1
                pass_num += 1
            elif testcase['result'] == 'SKIP':
                testcase_num[area] -= 1
                total_num -= 1

        if total_num != 0:
            pass_rate = pass_num / total_num
            report_txt += 'Pass Rate: %.2f%% (%s/%s)\n' %\
                (pass_rate * 100, pass_num, total_num)
            report_txt += 'Assessed test areas:\n'
        else:
            report_txt += \
                'no testcase or all testcases are skipped in this testsuite'

        for key in sub_report:
            if testcase_num[key] != 0:
                pass_rate = testcase_passnum[key] / testcase_num[key]
                report_txt += '-%-25s pass %.2f%%\n' %\
                    (key + ' results:', pass_rate * 100)
            elif key in testarea_scope:
                report_txt += '-%-25s all skipped\n' % key
        for key in sub_report:
            if testcase_num[key] != 0:
                pass_rate = testcase_passnum[key] / testcase_num[key]
                report_txt += '%-25s  pass rate %.2f%%\n' %\
                    (key + ':', pass_rate * 100)
                report_txt += sub_report[key]
            elif key in testarea_scope:
                report_txt += '%-25s  all skipped\n' % key
                report_txt += sub_report[key]

        cls.logger.info(report_txt)
        # cls.save(report_txt)
        return report_txt

    # save to disk as default
    @classmethod
    def save(cls, report):
        report_file_name = dt_cfg.dovetail_config['report_file']
        try:
            with open(os.path.join(dt_cfg.dovetail_config['result_dir'],
                      report_file_name), 'w') as report_file:
                report_file.write(report)
            cls.logger.info('save report to %s', report_file_name)
        except Exception:
            cls.logger.error('Failed to save: %s', report_file_name)

    @classmethod
    def get_result(cls, testcase):
        validate_testcase = testcase.validate_testcase()
        type = testcase.validate_type()
        crawler = CrawlerFactory.create(type)
        if crawler is None:
            cls.logger.error('crawler is None:%s', testcase.name())
            return None

        # if validate_testcase in cls.results[type]:
        #    return cls.results[type][validate_testcase]

        result = crawler.crawl(testcase)

        if result is not None:
            cls.results[type][validate_testcase] = result
            # testcase.script_result_acquired(True)
            cls.logger.debug('testcase: %s -> result acquired',
                             validate_testcase)
        else:
            retry = testcase.increase_retry()
            cls.logger.debug('testcase: %s -> result acquired retry:%d',
                             validate_testcase, retry)
        return result


class FunctestCrawler(object):

    logger = None

    def __init__(self):
        self.type = 'functest'
        self.logger.debug('create crawler:%s', self.type)

    @classmethod
    def create_log(cls):
        cls.logger = \
            dt_logger.Logger(__name__ + '.FunctestCrawler').getLogger()

    def crawl(self, testcase=None):
        report_dest = dt_cfg.dovetail_config['report_dest']
        if report_dest.lower() == 'file':
            return self.crawl_from_file(testcase)

        if report_dest.lower().startswith('http'):
            return self.crawl_from_url(testcase)

    def crawl_from_file(self, testcase=None):
        dovetail_config = dt_cfg.dovetail_config
        criteria = 'FAIL'
        details = {}
        timestart = 0
        timestop = 0
        duration = 0
        testcase_name = testcase.validate_testcase()
        build_tag = '%s-%s' % (dovetail_config['build_tag'], testcase.name())
        file_path = \
            os.path.join(dovetail_config['result_dir'],
                         dovetail_config[self.type]['result']['file_path'])
        if not os.path.exists(file_path):
            self.logger.info('result file not found: %s', file_path)
            return None
        if testcase_name in dt_cfg.dovetail_config['functest_testcase']:
            complex_testcase = False
        elif testcase_name in dt_cfg.dovetail_config['functest_testsuite']:
            complex_testcase = True
        else:
            self.logger.error("Wrong Functest test case %s.", testcase_name)
            return None
        with open(file_path, 'r') as f:
            for jsonfile in f:
                try:
                    data = json.loads(jsonfile)
                    if testcase_name == data['case_name'] and \
                        build_tag == data['build_tag']:
                        criteria = data['criteria']
                        timestart = data['start_date']
                        timestop = data['stop_date']
                        duration = dt_utils.get_duration(timestart, timestop,
                                                         self.logger)
                        if complex_testcase:
                            tests = data['details']['tests']
                            failed_num = data['details']['failures']
                            error_case = data['details']['errors']
                            skipped_case = data['details']['skipped']
                            details = {"tests": tests,
                                       "failures": failed_num,
                                       "errors": error_case,
                                       "skipped": skipped_case}
                except KeyError as e:
                    self.logger.error("Key error, exception: %s", e)
                    return None
                except ValueError:
                    continue

        json_results = {'criteria': criteria, 'timestart': timestart,
                        'timestop': timestop, 'duration': duration,
                        'details': details}

        self.logger.debug('Results: %s', str(json_results))
        return json_results

    def crawl_from_url(self, testcase=None):
        url = "%s/results?case=%s&last=1" % \
            (dt_cfg.dovetail_config['report_dest'],
             testcase.validate_testcase())
        self.logger.debug("Query to rest api: %s", url)
        try:
            data = json.load(urllib2.urlopen(url))
            return data['results'][0]
        except Exception as e:
            self.logger.error("Cannot read content from the url: %s, "
                              "exception: %s", url, e)
            return None


class YardstickCrawler(object):

    logger = None

    def __init__(self):
        self.type = 'yardstick'
        self.logger.debug('create crawler:%s', self.type)

    @classmethod
    def create_log(cls):
        cls.logger = \
            dt_logger.Logger(__name__ + '.YardstickCrawler').getLogger()

    def crawl(self, testcase=None):
        report_dest = dt_cfg.dovetail_config['report_dest']
        if report_dest.lower() == 'file':
            return self.crawl_from_file(testcase)

        if report_dest.lower().startswith('http'):
            return self.crawl_from_url(testcase)

    def crawl_from_file(self, testcase=None):
        file_path = os.path.join(dt_cfg.dovetail_config['result_dir'],
                                 testcase.validate_testcase() + '.out')
        if not os.path.exists(file_path):
            self.logger.info('result file not found: %s', file_path)
            return None
        criteria = 'FAIL'
        with open(file_path, 'r') as f:
            for jsonfile in f:
                data = json.loads(jsonfile)
                if 1 == data['status']:
                    criteria = 'PASS'
        json_results = {'criteria': criteria}
        self.logger.debug('Results: %s', str(json_results))
        return json_results

    def crawl_from_url(self, testcase=None):
        return None


class ShellCrawler(object):

    def __init__(self):
        self.type = 'shell'

    def crawl(self, testcase=None):
        return self.crawl_from_file(testcase)

    def crawl_from_file(self, testcase=None):
        file_path = os.path.join(dt_cfg.dovetail_config['result_dir'],
                                 testcase.name()) + '.out'
        if not os.path.exists(file_path):
            return None
        try:
            with open(file_path, 'r') as json_data:
                result = json.load(json_data)
            return result
        except Exception:
            return None


class CrawlerFactory(object):

    CRAWLER_MAP = {'functest': FunctestCrawler,
                   'yardstick': YardstickCrawler,
                   'shell': ShellCrawler}

    @classmethod
    def create(cls, type):
        try:
            return cls.CRAWLER_MAP[type]()
        except KeyError:
            return None


class ResultChecker(object):

    @staticmethod
    def check():
        return 'PASS'


class FunctestChecker(object):

    logger = None

    @classmethod
    def create_log(cls):
        cls.logger = \
            dt_logger.Logger(__name__ + '.FunctestChecker').getLogger()

    @staticmethod
    def get_sub_testcase(sub_testcase, result):
        if not result:
            return False
        reg = sub_testcase + '[\s+\d+]'
        find_reg = re.compile(reg)
        match = find_reg.findall(result)
        if match:
            return True
        return False

    def check(self, testcase, db_result):
        sub_testcase_list = testcase.sub_testcase()

        if not db_result:
            if sub_testcase_list is not None:
                for sub_testcase in sub_testcase_list:
                    testcase.sub_testcase_passed(sub_testcase, 'FAIL')
            return

        testcase.passed(db_result['criteria'])

        if sub_testcase_list is None:
            return

        testcase_passed = 'SKIP'
        for sub_testcase in sub_testcase_list:
            self.logger.debug('check sub_testcase:%s', sub_testcase)
            if self.get_sub_testcase(sub_testcase,
                                     db_result['details']['errors']):
                testcase.sub_testcase_passed(sub_testcase, 'FAIL')
                testcase_passed = 'FAIL'
                continue
            if self.get_sub_testcase(sub_testcase,
                                     db_result['details']['skipped']):
                testcase.sub_testcase_passed(sub_testcase, 'SKIP')
            else:
                testcase.sub_testcase_passed(sub_testcase, 'PASS')

        if testcase_passed == 'SKIP':
            for sub_testcase in sub_testcase_list:
                if testcase.sub_testcase_status[sub_testcase] == 'PASS':
                    testcase_passed = 'PASS'
                    break

        testcase.passed(testcase_passed)


class YardstickChecker(object):

    logger = None

    @classmethod
    def create_log(cls):
        cls.logger = \
            dt_logger.Logger(__name__ + '.YardstickChecker').getLogger()

    @staticmethod
    def check(testcase, result):
        if not result:
            testcase.passed('FAIL')
        else:
            testcase.passed(result['criteria'])
        return


class ShellChecker(object):

    @staticmethod
    def check(testcase, result):
        try:
            testcase.passed(result['pass'])
        except Exception:
            testcase.passed(False)


class CheckerFactory(object):

    CHECKER_MAP = {'functest': FunctestChecker,
                   'yardstick': YardstickChecker,
                   'shell': ShellChecker}

    @classmethod
    def create(cls, type):
        try:
            return cls.CHECKER_MAP[type]()
        except KeyError:
            return None
