#!/usr/bin/env python

#
# Copyright (c) 2017 grakiss.wanglei@huawei.com and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

from __future__ import division

import collections
import json
import re
import os
import datetime
import tarfile
import time

import utils.dovetail_logger as dt_logger

from utils.dovetail_config import DovetailConfig as dt_cfg
import utils.dovetail_utils as dt_utils
from testcase import Testcase


class Report(object):

    results = {'functest': {}, 'yardstick': {}, 'functest-k8s': {},
               'bottlenecks': {}, 'shell': {}, 'vnftest': {}, 'onap-vtp': {}}

    logger = None

    @classmethod
    def create_log(cls):
        cls.logger = dt_logger.Logger(__name__ + '.Report').getLogger()

    def check_tc_result(self, testcase):
        result_path = dt_cfg.dovetail_config['result_dir']
        check_results_file = dt_utils.get_value_from_dict(
            'report.check_results_file', testcase.testcase)
        if not check_results_file:
            self.logger.error("Failed to get 'check_results_file' from config "
                              "file of test case {}".format(testcase.name()))
            self.check_result(testcase)
            return None
        result_file = os.path.join(result_path, check_results_file)
        if os.path.isfile(result_file):
            self.logger.info(
                'Results have been stored with file {}.'.format(result_file))
            result = self.get_result(testcase, result_file)
            self.check_result(testcase, result)
            return result
        else:
            self.logger.error(
                'Failed to store results with file {}.'.format(result_file))
            self.check_result(testcase)
            return None

    @staticmethod
    def check_result(testcase, db_result=None):
        checker = CheckerFactory.create(testcase.validate_type())
        if checker is not None:
            checker.check(testcase, db_result)

    def generate_json(self, testcase_list, duration):
        report_obj = {}
        # egeokun: using a hardcoded string instead of pbr version for
        # versioning the result file. The version of the results.json is
        # logically independent of the release of Dovetail.
        report_obj['version'] = '2018.09'
        report_obj['build_tag'] = dt_cfg.dovetail_config['build_tag']
        report_obj['test_date'] =\
            datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
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
                testcase_inreport['mandatory'] = False
                report_obj['testcases_list'].append(testcase_inreport)
                continue

            testcase_inreport['result'] = testcase.passed()
            testcase_inreport['objective'] = testcase.objective()
            testcase_inreport['mandatory'] = testcase.is_mandatory
            testcase_inreport['sub_testcase'] = []
            if testcase.sub_testcase() is not None:
                for sub_test in testcase.sub_testcase():
                    testcase_inreport['sub_testcase'].append({
                        'name': sub_test,
                        'result': testcase.sub_testcase_passed(sub_test)
                    })
            report_obj['testcases_list'].append(testcase_inreport)
        self.logger.debug(json.dumps(report_obj))
        return report_obj

    def generate(self, testcase_list, duration):
        report_data = self.generate_json(testcase_list, duration)
        self.save_json_results(report_data)

        report_txt = ''
        report_txt += '\n\nDovetail Report\n'
        report_txt += 'Version: %s\n' % report_data['version']
        report_txt += 'Build Tag: %s\n' % report_data['build_tag']
        report_txt += 'Test Date: %s\n' % report_data['test_date']
        report_txt += 'Duration: %.2f s\n\n' % report_data['duration']

        total_num = 0
        pass_num = 0
        sub_report = collections.OrderedDict()
        testcase_num = {}
        testcase_passnum = {}
        for area in dt_cfg.dovetail_config['testarea_supported']:
            sub_report[area] = ''
            testcase_num[area] = 0
            testcase_passnum[area] = 0

        testarea_scope = []
        for testcase in report_data['testcases_list']:
            supported_areas = dt_cfg.dovetail_config['testarea_supported']
            pattern = re.compile('|'.join(supported_areas))
            area = pattern.findall(testcase['name'])
            if not supported_areas or not area:
                self.logger.error('Test case {} not in supported testarea.'
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
        else:
            report_txt += \
                'no testcase or all testcases are skipped in this testsuite\n'

        for key in sub_report:
            if testcase_num[key] != 0:
                pass_rate = testcase_passnum[key] / testcase_num[key]
                report_txt += '%-25s  pass rate %.2f%%\n' %\
                    (key + ':', pass_rate * 100)
                report_txt += sub_report[key]
            elif key in testarea_scope:
                report_txt += '%-25s  all skipped\n' % key
                report_txt += sub_report[key]

        self.logger.info(report_txt)
        return report_txt

    def save_json_results(self, results):
        result_file = os.path.join(dt_cfg.dovetail_config['result_dir'],
                                   dt_cfg.dovetail_config['result_file'])

        try:
            with open(result_file, 'w') as f:
                f.write(json.dumps(results) + '\n')
        except Exception as e:
            self.logger.exception('Failed to add result to file {}, '
                                  'exception: {}'.format(result_file, e))

    @staticmethod
    def save_logs():
        file_suffix = time.strftime('%Y%m%d_%H%M', time.localtime())
        logs_gz = 'logs_{}.tar.gz'.format(file_suffix)
        result_dir = dt_cfg.dovetail_config['result_dir']

        cwd = os.getcwd()
        os.chdir(os.path.join(result_dir, '..'))
        tar_file = os.path.join(result_dir, '..', logs_gz)
        with tarfile.open(tar_file, 'w:gz') as f_out:
            files = os.listdir(result_dir)
            for f in files:
                if f not in ['workspace']:
                    f_out.add(os.path.join('results', f))
        os.chdir(cwd)

    def get_result(self, testcase, check_results_file):
        validate_testcase = testcase.validate_testcase()
        type = testcase.validate_type()
        crawler = CrawlerFactory.create(type)
        if crawler is None:
            self.logger.error('Crawler is None: {}'.format(testcase.name()))
            return None

        result = crawler.crawl(testcase, check_results_file)

        if result is not None:
            self.results[type][validate_testcase] = result
            self.logger.debug(
                'Test case: {} -> result acquired'.format(validate_testcase))
        else:
            retry = testcase.increase_retry()
            self.logger.debug('Test case: {} -> result acquired retry: {}'
                              .format(validate_testcase, retry))
        return result


class Crawler(object):
    pass


class FunctestCrawler(Crawler):

    logger = None

    def __init__(self):
        self.type = 'functest'
        self.logger.debug('Create crawler: {}'.format(self.type))

    @classmethod
    def create_log(cls):
        cls.logger = \
            dt_logger.Logger(__name__ + '.FunctestCrawler').getLogger()

    def crawl(self, testcase, file_path):
        return self.crawl_from_file(testcase, file_path)

    def crawl_from_file(self, testcase, file_path):
        dovetail_config = dt_cfg.dovetail_config
        criteria = 'FAIL'
        details = {}
        timestart = 0
        timestop = 0
        duration = 0
        testcase_name = testcase.validate_testcase()
        build_tag = '%s-%s' % (dovetail_config['build_tag'], testcase.name())
        if not os.path.exists(file_path):
            self.logger.error('Result file not found: {}'.format(file_path))
            return None

        sub_testcase_list = testcase.sub_testcase()
        complex_testcase = True if sub_testcase_list else False

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
                            tests = data['details']['tests_number']
                            failed_num = data['details']['failures_number']
                            success_case = data['details']['success']
                            error_case = data['details']['failures']
                            skipped_case = data['details']['skipped']
                            details = {'tests': tests,
                                       'failures': failed_num,
                                       'success': success_case,
                                       'errors': error_case,
                                       'skipped': skipped_case}
                except KeyError as e:
                    self.logger.exception(
                        "Result data don't have key {}.".format(e))
                    return None
                except ValueError:
                    continue

        json_results = {'criteria': criteria, 'timestart': timestart,
                        'timestop': timestop, 'duration': duration,
                        'details': details}

        testcase.set_results(json_results)
        return json_results


class FunctestK8sCrawler(FunctestCrawler):

    logger = None

    def __init__(self):
        self.type = 'functest-k8s'
        self.logger.debug('Create crawler: {}'.format(self.type))

    @classmethod
    def create_log(cls):
        cls.logger = \
            dt_logger.Logger(__name__ + '.FunctestK8sCrawler').getLogger()


class YardstickCrawler(Crawler):

    logger = None

    def __init__(self):
        self.type = 'yardstick'
        self.logger.debug('Create crawler: {}'.format(self.type))

    @classmethod
    def create_log(cls):
        cls.logger = \
            dt_logger.Logger(__name__ + '.YardstickCrawler').getLogger()

    def crawl(self, testcase, file_path):
        return self.crawl_from_file(testcase, file_path)

    def crawl_from_file(self, testcase, file_path):
        if not os.path.exists(file_path):
            self.logger.error('Result file not found: {}'.format(file_path))
            return None
        criteria = 'FAIL'
        with open(file_path, 'r') as f:
            for jsonfile in f:
                data = json.loads(jsonfile)
                try:
                    criteria = dt_utils.get_value_from_dict('result.criteria',
                                                            data)
                    if criteria == 'PASS':
                        valid_tc = testcase.validate_testcase()
                        details = data['result']['testcases'][valid_tc]
                        sla_pass = details['tc_data'][0]['data']['sla_pass']
                        if not 1 == sla_pass:
                            criteria = 'FAIL'
                except KeyError as e:
                    self.logger.exception('Pass flag not found {}'.format(e))
        json_results = {'criteria': criteria}

        testcase.set_results(json_results)
        return json_results


class BottlenecksCrawler(Crawler):

    logger = None

    def __init__(self):
        self.type = 'bottlenecks'
        self.logger.debug('Create crawler: {}'.format(self.type))

    @classmethod
    def create_log(cls):
        cls.logger = \
            dt_logger.Logger(__name__ + '.BottlenecksCrawler').getLogger()

    def crawl(self, testcase, file_path):
        return self.crawl_from_file(testcase, file_path)

    def crawl_from_file(self, testcase, file_path):
        if not os.path.exists(file_path):
            self.logger.error('Result file not found: {}'.format(file_path))
            return None
        criteria = 'FAIL'
        with open(file_path, 'r') as f:
            for jsonfile in f:
                data = json.loads(jsonfile)
                try:
                    if 'PASS' == data['data_body']['result']:
                        criteria = 'PASS'
                    else:
                        criteria = 'FAIL'
                        break
                except KeyError as e:
                    self.logger.exception('Pass flag not found {}'.format(e))
        json_results = {'criteria': criteria}

        testcase.set_results(json_results)
        return json_results


class ShellCrawler(Crawler):

    def __init__(self):
        self.type = 'shell'

    def crawl(self, testcase, file_path):
        return self.crawl_from_file(testcase, file_path)

    def crawl_from_file(self, testcase, file_path):
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

    def crawl(self, testcase, file_path):
        return self.crawl_from_file(testcase, file_path)

    def crawl_from_file(self, testcase, file_path):
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
        return json_results


class OnapVtpCrawler(Crawler):

    logger = None

    def __init__(self):
        self.type = 'onap-vtp'
        self.logger.debug('Create crawler: {}'.format(self.type))

    @classmethod
    def create_log(cls):
        cls.logger = dt_logger.Logger(__name__ + '.OnapVtpCrawler').getLogger()

    def crawl(self, testcase, file_path):
        return self.crawl_from_file(testcase, file_path)

    # The pass result looks like
    # {
    #   "results": [
    #     {"property": "results", "value": "{value=SUCCESS}"},
    #     {"property": "build_tag", "value": "test"},
    #     {"property": "criteria", "value": "PASS"}
    #   ]
    # }
    # The fail result looks like
    # {
    #   "results": [
    #     {"property": "results", "value": "{value=file doesn't exists}"},
    #     {"property": "build_tag", "value": "test"},
    #     {"property": "criteria", "value": "FAILED"}
    #   ]
    # }
    def crawl_from_file(self, testcase, file_path):
        if not os.path.exists(file_path):
            self.logger.error('Result file not found: {}'.format(file_path))
            return None
        criteria = 'FAIL'
        with open(file_path, 'r') as f:
            for jsonfile in f:
                try:
                    data = json.loads(jsonfile)
                    for item in data['results']:
                        if 'criteria' == item['property']:
                            if 'PASS' == item['value']:
                                criteria = 'PASS'
                            break
                    else:
                        self.logger.error('There is no property criteria.')
                except KeyError as e:
                    self.logger.exception('Pass flag not found {}'.format(e))
                except ValueError:
                    continue
        json_results = {'criteria': criteria}

        testcase.set_results(json_results)
        return json_results


class CrawlerFactory(object):

    CRAWLER_MAP = {'functest': FunctestCrawler,
                   'yardstick': YardstickCrawler,
                   'bottlenecks': BottlenecksCrawler,
                   'vnftest': VnftestCrawler,
                   'shell': ShellCrawler,
                   'functest-k8s': FunctestK8sCrawler,
                   'onap-vtp': OnapVtpCrawler}

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
        sub_testcase = re.sub(r"\[.*?\]", "", sub_testcase)
        reg = sub_testcase + r'[\s+\d+]'
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


class FunctestK8sChecker(FunctestChecker):

    logger = None

    @classmethod
    def create_log(cls):
        cls.logger = \
            dt_logger.Logger(__name__ + '.FunctestK8sChecker').getLogger()


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


class OnapVtpChecker(object):

    logger = None

    @classmethod
    def create_log(cls):
        cls.logger = dt_logger.Logger(__name__ + '.OnapVtpChecker').getLogger()

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
                   'vnftest': VnftestChecker,
                   'functest-k8s': FunctestK8sChecker,
                   'onap-vtp': OnapVtpChecker}

    @classmethod
    def create(cls, type):
        try:
            return cls.CHECKER_MAP[type]()
        except KeyError:
            return None
