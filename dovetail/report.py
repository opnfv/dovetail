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
import re
import os
import datetime
import tarfile
import time

from pbr import version

import utils.dovetail_logger as dt_logger

from utils.dovetail_config import DovetailConfig as dt_cfg
import utils.dovetail_utils as dt_utils
from testcase import Testcase


class Report(object):

    results = {'functest': {}, 'yardstick': {},
               'bottlenecks': {}, 'shell': {}, 'vnftest': {}}

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
    def generate_json(cls, testcase_list, duration):
        report_obj = {}
        report_obj['version'] = \
            version.VersionInfo('dovetail').version_string()
        report_obj['build_tag'] = dt_cfg.dovetail_config['build_tag']
        report_obj['upload_date'] =\
            datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        report_obj['duration'] = duration

        report_obj['testcases_list'] = []
        if not testcase_list:
            return report_obj

        for testcase_name in testcase_list:
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
        cls.logger.debug(json.dumps(report_obj))
        return report_obj

    @classmethod
    def generate(cls, testcase_list, duration):
        report_data = cls.generate_json(testcase_list, duration)
        report_txt = ''
        report_txt += '\n\nDovetail Report\n'
        report_txt += 'Version: %s\n' % report_data['version']
        report_txt += 'Build Tag: %s\n' % report_data['build_tag']
        report_txt += 'Upload Date: %s\n' % report_data['upload_date']
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
                cls.logger.error("Test case {} not in supported testarea."
                                 .format(testcase['name']))
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
                'no testcase or all testcases are skipped in this testsuite\n'

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
        return report_txt

    @classmethod
    def save_logs(cls):
        file_suffix = time.strftime('%Y%m%d_%H%M', time.localtime())
        logs_gz = "logs_{}.tar.gz".format(file_suffix)
        result_dir = dt_cfg.dovetail_config['result_dir']

        cwd = os.getcwd()
        os.chdir(os.path.join(result_dir, '..'))
        tar_file = os.path.join(result_dir, '..', logs_gz)
        with tarfile.open(tar_file, "w:gz") as f_out:
            files = os.listdir(result_dir)
            for f in files:
                if f not in ['workspace']:
                    f_out.add(os.path.join('results', f))
        os.chdir(cwd)

    @classmethod
    def get_result(cls, testcase):
        validate_testcase = testcase.validate_testcase()
        type = testcase.validate_type()
        crawler = CrawlerFactory.create(type)
        if crawler is None:
            cls.logger.error('Crawler is None: {}'.format(testcase.name()))
            return None

        # if validate_testcase in cls.results[type]:
        #    return cls.results[type][validate_testcase]

        result = crawler.crawl(testcase)

        if result is not None:
            cls.results[type][validate_testcase] = result
            # testcase.script_result_acquired(True)
            cls.logger.debug(
                'Test case: {} -> result acquired'.format(validate_testcase))
        else:
            retry = testcase.increase_retry()
            cls.logger.debug('Test case: {} -> result acquired retry: {}'
                             .format(validate_testcase, retry))
        return result


class Crawler(object):

    def add_result_to_file(self, result):
        result_file = os.path.join(dt_cfg.dovetail_config['result_dir'],
                                   dt_cfg.dovetail_config['result_file'])
        try:
            with open(result_file, 'a') as f:
                f.write(json.dumps(result) + '\n')
                return True
        except Exception as e:
            self.logger.exception("Failed to add result to file {}, "
                                  "exception: {}".format(result_file, e))
            return False


class FunctestCrawler(Crawler):

    logger = None

    def __init__(self):
        self.type = 'functest'
        self.logger.debug('Create crawler: {}'.format(self.type))

    @classmethod
    def create_log(cls):
        cls.logger = \
            dt_logger.Logger(__name__ + '.FunctestCrawler').getLogger()

    def crawl(self, testcase=None):
        return self.crawl_from_file(testcase)

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
            self.logger.error('Result file not found: {}'.format(file_path))
            return None
        if testcase_name in dt_cfg.dovetail_config['functest_testcase']:
            complex_testcase = False
        elif testcase_name in dt_cfg.dovetail_config['functest_testsuite']:
            complex_testcase = True
        else:
            self.logger.error(
                "Wrong Functest test case {}.".format(testcase_name))
            return None
        with open(file_path, 'r') as f:
            for jsonfile in f:
                try:
                    data = json.loads(jsonfile)
                    if (testcase_name == data['case_name'] or
                        data['project_name'] == "sdnvpn") and \
                        build_tag == data['build_tag']:
                        self.add_result_to_file(data)
                        criteria = data['criteria']
                        timestart = data['start_date']
                        timestop = data['stop_date']
                        duration = dt_utils.get_duration(timestart, timestop,
                                                         self.logger)
                        if complex_testcase:
                            tests = data['details']['tests_number']
                            failed_num = data['details']['failures_number']
                            success_case = data['details']['success']
                            error_case = data['details']['failures']
                            skipped_case = data['details']['skipped']
                            details = {"tests": tests,
                                       "failures": failed_num,
                                       "success": success_case,
                                       "errors": error_case,
                                       "skipped": skipped_case}
                except KeyError as e:
                    self.logger.exception(
                        "Result data don't have key {}.".format(e))
                    return None
                except ValueError:
                    continue

        json_results = {'criteria': criteria, 'timestart': timestart,
                        'timestop': timestop, 'duration': duration,
                        'details': details}

        self.logger.debug('Results: {}'.format(str(json_results)))
        return json_results


class YardstickCrawler(Crawler):

    logger = None

    def __init__(self):
        self.type = 'yardstick'
        self.logger.debug('Create crawler: {}'.format(self.type))

    @classmethod
    def create_log(cls):
        cls.logger = \
            dt_logger.Logger(__name__ + '.YardstickCrawler').getLogger()

    def crawl(self, testcase=None):
        return self.crawl_from_file(testcase)

    def crawl_from_file(self, testcase=None):
        file_path = os.path.join(dt_cfg.dovetail_config['result_dir'],
                                 testcase.name() + '.out')
        if not os.path.exists(file_path):
            self.logger.error('Result file not found: {}'.format(file_path))
            return None
        criteria = 'FAIL'
        with open(file_path, 'r') as f:
            for jsonfile in f:
                data = json.loads(jsonfile)
                self.add_result_to_file(data, testcase.name())
                try:
                    criteria = data['result']['criteria']
                    if criteria == 'PASS':
                        valid_tc = testcase.validate_testcase()
                        details = data['result']['testcases'][valid_tc]
                        sla_pass = details['tc_data'][0]['data']['sla_pass']
                        if not 1 == sla_pass:
                            criteria = 'FAIL'
                except KeyError as e:
                    self.logger.exception('Pass flag not found {}'.format(e))
        json_results = {'criteria': criteria}
        self.logger.debug('Results: {}'.format(str(json_results)))
        return json_results

    def add_result_to_file(self, result, tc_name):
        build_tag = '{}-{}'.format(dt_cfg.dovetail_config['build_tag'],
                                   tc_name)
        result['build_tag'] = build_tag
        super(YardstickCrawler, self).add_result_to_file(result)


class BottlenecksCrawler(Crawler):

    logger = None

    def __init__(self):
        self.type = 'bottlenecks'
        self.logger.debug('Create crawler: {}'.format(self.type))

    @classmethod
    def create_log(cls):
        cls.logger = \
            dt_logger.Logger(__name__ + '.BottlenecksCrawler').getLogger()

    def crawl(self, testcase=None):
        return self.crawl_from_file(testcase)

    def crawl_from_file(self, testcase=None):
        file_path = os.path.join(dt_cfg.dovetail_config['result_dir'],
                                 testcase.name() + '.out')
        if not os.path.exists(file_path):
            self.logger.error('Result file not found: {}'.format(file_path))
            return None
        criteria = 'FAIL'
        with open(file_path, 'r') as f:
            for jsonfile in f:
                data = json.loads(jsonfile)
                try:
                    if 'PASS' == data["data_body"]["result"]:
                        criteria = 'PASS'
                    else:
                        criteria = 'FAIL'
                        break
                except KeyError as e:
                    self.logger.exception('Pass flag not found {}'.format(e))
        json_results = {'criteria': criteria}
        self.logger.debug('Results: {}'.format(str(json_results)))
        return json_results


class ShellCrawler(Crawler):

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


class VnftestCrawler(Crawler):

    logger = None

    def __init__(self):
        self.type = 'vnftest'
        self.logger.debug('Create crawler: {}'.format(self.type))

    @classmethod
    def create_log(cls):
        cls.logger = \
            dt_logger.Logger(__name__ + '.VnftestCrawler').getLogger()

    def crawl(self, testcase):
        return self.crawl_from_file(testcase)

    def crawl_from_file(self, testcase):

        file_path = os.path.join(dt_cfg.dovetail_config['result_dir'],
                                 testcase.name() + '.out')
        if not os.path.exists(file_path):
            self.logger.error('Result file not found: {}'.format(file_path))
            return None
        criteria = 'FAIL'
        with open(file_path, 'r') as f:
            for jsonfile in f:
                data = json.loads(jsonfile)
                try:
                    criteria = data['result']['criteria']
                except KeyError as e:
                    self.logger.exception('Pass flag not found {}'.format(e))
        json_results = {'criteria': criteria}
        self.logger.debug('Results: {}'.format(str(json_results)))
        return json_results


class CrawlerFactory(object):

    CRAWLER_MAP = {'functest': FunctestCrawler,
                   'yardstick': YardstickCrawler,
                   'bottlenecks': BottlenecksCrawler,
                   'vnftest': VnftestCrawler,
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
        sub_testcase = re.sub("\[.*?\]", "", sub_testcase)
        reg = sub_testcase + '[\s+\d+]'
        find_reg = re.compile(reg)
        for tc in result:
            match = find_reg.findall(tc)
            if match:
                return True
        reg = sub_testcase + '$'
        find_reg = re.compile(reg)
        for tc in result:
            match = find_reg.findall(tc)
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

        testcase_passed = 'PASS'
        for sub_testcase in sub_testcase_list:
            self.logger.debug('Check sub_testcase: {}'.format(sub_testcase))
            try:
                if self.get_sub_testcase(sub_testcase,
                                         db_result['details']['success']):
                    testcase.sub_testcase_passed(sub_testcase, 'PASS')
                    continue
                if self.get_sub_testcase(sub_testcase,
                                         db_result['details']['skipped']):
                    testcase.sub_testcase_passed(sub_testcase, 'SKIP')
                else:
                    testcase.sub_testcase_passed(sub_testcase, 'FAIL')
                testcase_passed = 'FAIL'
            except KeyError:
                testcase.sub_testcase_passed(sub_testcase, 'FAIL')
                testcase_passed = 'FAIL'

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


class BottlenecksChecker(object):

    logger = None

    @classmethod
    def create_log(cls):
        cls.logger = \
            dt_logger.Logger(__name__ + '.BottlenecksChecker').getLogger()

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


class VnftestChecker(object):

    logger = None

    @classmethod
    def create_log(cls):
        cls.logger = \
            dt_logger.Logger(__name__ + '.VnftestCheckers').getLogger()

    @staticmethod
    def check(testcase, result):
        if not result:
            testcase.passed('FAIL')
        else:
            testcase.passed(result['criteria'])
        return


class CheckerFactory(object):

    CHECKER_MAP = {'functest': FunctestChecker,
                   'yardstick': YardstickChecker,
                   'bottlenecks': BottlenecksChecker,
                   'shell': ShellChecker,
                   'vnftest': VnftestChecker}

    @classmethod
    def create(cls, type):
        try:
            return cls.CHECKER_MAP[type]()
        except KeyError:
            return None
