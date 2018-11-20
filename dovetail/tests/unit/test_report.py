#!/usr/bin/env python
#
# Copyright (c) 2018 mokats@intracom-telecom.com and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##

import json
import os
import unittest
import yaml
from mock import patch, call, Mock

import dovetail.report as dt_report

__author__ = 'Stamatis Katsaounis <mokats@intracom-telecom.com>'


class ReportTesting(unittest.TestCase):

    def setUp(self):
        test_path = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(test_path, 'test_testcase.yaml')) as f:
            self.testcase_yaml = yaml.safe_load(f)

    def tearDown(self):
        pass

    def teardown_method(self, method):
        dt_report.FunctestCrawler.logger = None
        dt_report.YardstickCrawler.logger = None
        dt_report.BottlenecksCrawler.logger = None
        dt_report.VnftestCrawler.logger = None
        dt_report.FunctestChecker.logger = None
        dt_report.YardstickChecker.logger = None
        dt_report.BottlenecksChecker.logger = None
        dt_report.VnftestChecker.logger = None
        dt_report.Report.logger = None
        dt_report.Report.results = {
            'functest': {}, 'yardstick': {},
            'bottlenecks': {}, 'shell': {}, 'vnftest': {}}

    def _produce_report_initial_text(self, report_data):
        report_txt = ''
        report_txt += '\n\nDovetail Report\n'
        report_txt += 'Version: %s\n' % report_data['version']
        report_txt += 'Build Tag: %s\n' % report_data['build_tag']
        report_txt += 'Test Date: %s\n' % report_data['test_date']
        report_txt += 'Duration: %.2f s\n\n' % report_data['duration']
        return report_txt

    @patch('dovetail.report.dt_logger')
    def test_create_log(self, mock_logger):
        getlogger_obj = Mock()
        logger_obj = Mock()
        logger_obj.getLogger.return_value = getlogger_obj
        mock_logger.Logger.return_value = logger_obj

        dt_report.Report.create_log()

        self.assertEquals(getlogger_obj, dt_report.Report.logger)

    @patch('dovetail.report.os.path')
    @patch('dovetail.report.dt_cfg')
    @patch('dovetail.report.dt_utils')
    @patch.object(dt_report.Report, 'get_result')
    @patch.object(dt_report.Report, 'check_result')
    def test_check_tc_result(self, mock_check, mock_get, mock_utils,
                             mock_config, mock_path):
        report = dt_report.Report()
        logger_obj = Mock()
        report.logger = logger_obj
        testcase_obj = Mock()
        inner_testcase_obj = Mock()
        testcase_obj.testcase = inner_testcase_obj
        mock_config.dovetail_config = {'result_dir': 'result_dir'}
        mock_utils.get_value_from_dict.return_value = 'check_results_file'
        mock_path.join.return_value = 'results_file'
        mock_path.isfile.return_value = True
        mock_get.return_value = 'result'

        result = report.check_tc_result(testcase_obj)

        mock_utils.get_value_from_dict.assert_called_once_with(
            'report.check_results_file', inner_testcase_obj)
        mock_path.join.assert_called_once_with(
            'result_dir', 'check_results_file')
        mock_path.isfile.assert_called_once_with('results_file')
        logger_obj.info.assert_called_once_with(
            'Results have been stored with file results_file.')
        mock_get.assert_called_once_with(testcase_obj, 'results_file')
        mock_check.assert_called_once_with(testcase_obj, 'result')
        self.assertEquals('result', result)

    @patch('dovetail.report.os.path')
    @patch('dovetail.report.dt_cfg')
    @patch('dovetail.report.dt_utils')
    @patch.object(dt_report.Report, 'get_result')
    @patch.object(dt_report.Report, 'check_result')
    def test_check_tc_result_no_file(self, mock_check, mock_get, mock_utils,
                                     mock_config, mock_path):
        report = dt_report.Report()
        logger_obj = Mock()
        report.logger = logger_obj
        testcase_obj = Mock()
        inner_testcase_obj = Mock()
        testcase_obj.testcase = inner_testcase_obj
        mock_config.dovetail_config = {'result_dir': 'result_dir'}
        mock_utils.get_value_from_dict.return_value = 'check_results_file'
        mock_path.join.return_value = 'results_file'
        mock_path.isfile.return_value = False

        result = report.check_tc_result(testcase_obj)

        mock_utils.get_value_from_dict.assert_called_once_with(
            'report.check_results_file', inner_testcase_obj)
        mock_path.join.assert_called_once_with(
            'result_dir', 'check_results_file')
        mock_path.isfile.assert_called_once_with('results_file')
        logger_obj.error.assert_called_once_with(
            'Failed to store results with file results_file.')
        mock_check.assert_called_once_with(testcase_obj)
        self.assertEquals(None, result)

    @patch('dovetail.report.os.path')
    @patch('dovetail.report.dt_cfg')
    @patch('dovetail.report.dt_utils')
    @patch.object(dt_report.Report, 'get_result')
    @patch.object(dt_report.Report, 'check_result')
    def test_check_tc_result_no_check(self, mock_check, mock_get, mock_utils,
                                      mock_config, mock_path):
        report = dt_report.Report()
        logger_obj = Mock()
        report.logger = logger_obj
        testcase_obj = Mock()
        inner_testcase_obj = Mock()
        testcase_obj.testcase = inner_testcase_obj
        testcase_obj.name.return_value = 'name'
        mock_config.dovetail_config = {'result_dir': 'result_dir'}
        mock_utils.get_value_from_dict.return_value = None

        result = report.check_tc_result(testcase_obj)

        mock_utils.get_value_from_dict.assert_called_once_with(
            'report.check_results_file', inner_testcase_obj)
        logger_obj.error.assert_called_once_with(
            "Failed to get 'check_results_file' from config "
            "file of test case name")
        mock_check.assert_called_once_with(testcase_obj)
        self.assertEquals(None, result)

    @patch('dovetail.report.CheckerFactory')
    def test_check_result(self, mock_factory):
        testcase_obj = Mock()
        testcase_obj.validate_type.return_value = 'type'
        checker_obj = Mock()
        mock_factory.create.return_value = checker_obj

        dt_report.Report.check_result(testcase_obj)

        testcase_obj.validate_type.assert_called_once_with()
        mock_factory.create.assert_called_once_with('type')
        checker_obj.check.assert_called_once_with(testcase_obj, None)

    @patch('dovetail.report.Testcase')
    @patch('dovetail.report.datetime.datetime')
    @patch('dovetail.report.dt_cfg')
    def test_generate_json(self, mock_config, mock_datetime, mock_testcase):
        logger_obj = Mock()
        report = dt_report.Report()
        report.logger = logger_obj
        testcase_list = ['t_a', 't_b']
        duration = 42
        mock_config.dovetail_config = {
            'build_tag': 'build_tag'
        }
        utc_obj = Mock()
        utc_obj.strftime.return_value = '2018-01-13 13:13:13 UTC'
        mock_datetime.utcnow.return_value = utc_obj
        testcase_obj = Mock()
        testcase_obj.passed.return_value = 'PASS'
        testcase_obj.objective.return_value = 'objective'
        testcase_obj.is_mandatory = True
        testcase_obj.sub_testcase.return_value = ['subt_a']
        testcase_obj.sub_testcase_passed.return_value = 'PASS'
        mock_testcase.get.side_effect = [testcase_obj, None]

        result = report.generate_json(testcase_list, duration)
        expected = {
            'version': '2018.09',
            'build_tag': 'build_tag',
            'test_date': '2018-01-13 13:13:13 UTC',
            'duration': duration,
            'testcases_list': [
                {
                    'name': 't_a',
                    'result': 'PASS',
                    'objective': 'objective',
                    'mandatory': True,
                    'sub_testcase': [{
                        'name': 'subt_a',
                        'result': 'PASS'
                    }]
                },
                {
                    'name': 't_b',
                    'result': 'Undefined',
                    'objective': '',
                    'mandatory': False,
                    'sub_testcase': []
                }
            ]
        }

        logger_obj.debug.assert_called_once_with(json.dumps(expected))
        self.assertEquals(expected, result)

    @patch('dovetail.report.datetime.datetime')
    @patch('dovetail.report.dt_cfg')
    def test_generate_json_no_list(self, mock_config, mock_datetime):
        logger_obj = Mock()
        report = dt_report.Report()
        report.logger = logger_obj
        duration = 42
        mock_config.dovetail_config = {
            'build_tag': 'build_tag'
        }
        utc_obj = Mock()
        utc_obj.strftime.return_value = '2018-01-13 13:13:13 UTC'
        mock_datetime.utcnow.return_value = utc_obj

        result = report.generate_json([], duration)
        expected = {
            'version': '2018.09',
            'build_tag': 'build_tag',
            'test_date': '2018-01-13 13:13:13 UTC',
            'duration': duration,
            'testcases_list': []
        }

        self.assertEquals(expected, result)

    @patch('dovetail.report.dt_cfg')
    @patch.object(dt_report.Report, 'generate_json')
    @patch.object(dt_report.Report, 'save_json_results')
    def test_generate(self, mock_save, mock_generate, mock_config):
        logger_obj = Mock()
        report = dt_report.Report()
        report.logger = logger_obj
        testcase_list = ['t_a', 't_b']
        mock_config.dovetail_config = {
            'testarea_supported': testcase_list
        }
        duration = 42
        report_data = {
            'version': 'v2',
            'build_tag': '2.0.0',
            'test_date': '2018-01-13 13:13:13 UTC',
            'duration': 42.42,
            'testcases_list': [
                {
                    'name': 't_a',
                    'result': 'PASS',
                    'sub_testcase': [{
                        'name': 'subt_a',
                        'result': 'PASS'
                    }]
                },
                {
                    'name': 't_b',
                    'result': 'SKIP'
                }
            ]
        }
        mock_generate.return_value = report_data

        result = report.generate(testcase_list, duration)
        expected = self._produce_report_initial_text(report_data)
        expected += 'Pass Rate: 100.00% (1/1)\n'
        expected += '%-25s  pass rate %.2f%%\n' % ('t_a:', 100)
        expected += '-%-25s %s\n' % ('t_a', 'PASS')
        expected += '\t%-110s %s\n' % ('subt_a', 'PASS')
        expected += '%-25s  all skipped\n' % 't_b'
        expected += '-%-25s %s\n' % ('t_b', 'SKIP')

        mock_generate.assert_called_once_with(testcase_list, duration)
        mock_save.assert_called_once_with(report_data)
        report.logger.info.assert_called_once_with(expected)
        self.assertEquals(expected, result)

    @patch('dovetail.report.dt_cfg')
    @patch.object(dt_report.Report, 'generate_json')
    @patch.object(dt_report.Report, 'save_json_results')
    def test_generate_error(self, mock_save, mock_generate, mock_config):
        logger_obj = Mock()
        report = dt_report.Report()
        report.logger = logger_obj
        mock_config.dovetail_config = {
            'testarea_supported': []
        }
        testcase_list = ['t_a']
        duration = 42
        report_data = {
            'version': 'v2',
            'build_tag': '2.0.0',
            'test_date': '2018-01-13 13:13:13 UTC',
            'duration': 42.42,
            'testcases_list': [{
                'name': 't_a',
                'result': 'PASS'
            }]
        }
        mock_generate.return_value = report_data

        result = report.generate(testcase_list, duration)
        expected = None

        mock_generate.assert_called_once_with(testcase_list, duration)
        mock_save.assert_called_once_with(report_data)
        report.logger.error.assert_called_once_with(
            'Test case {} not in supported testarea.'
            .format(report_data['testcases_list'][0]['name']))
        self.assertEquals(expected, result)

    @patch('dovetail.report.dt_cfg')
    @patch.object(dt_report.Report, 'generate_json')
    @patch.object(dt_report.Report, 'save_json_results')
    def test_generate_no_cases(self, mock_save, mock_generate, mock_config):
        logger_obj = Mock()
        report = dt_report.Report()
        report.logger = logger_obj
        mock_config.dovetail_config = {
            'testarea_supported': []
        }
        duration = 42
        report_data = {
            'version': 'v2',
            'build_tag': '2.0.0',
            'test_date': '2018-01-13 13:13:13 UTC',
            'duration': 42.42,
            'testcases_list': []
        }
        mock_generate.return_value = report_data

        result = report.generate([], duration)
        expected = self._produce_report_initial_text(report_data) +\
            'no testcase or all testcases are skipped in this testsuite\n'

        mock_generate.assert_called_once_with([], duration)
        mock_save.assert_called_once_with(report_data)
        report.logger.info.assert_called_once_with(expected)
        self.assertEquals(expected, result)

    @patch('__builtin__.open')
    @patch('dovetail.report.json')
    @patch('dovetail.report.os.path')
    @patch('dovetail.report.dt_cfg')
    def test_save_json_results(self, mock_config, mock_path, mock_json,
                               mock_open):
        mock_config.dovetail_config = {
            'result_dir': 'a',
            'result_file': 'b'
        }
        mock_path.join.return_value = 'result_file'
        file_obj = Mock()
        mock_open.return_value.__enter__.return_value = file_obj
        mock_json.dumps.return_value = 'results text'

        report = dt_report.Report()
        report.save_json_results('results')

        mock_path.join.assert_called_once_with('a', 'b')
        mock_open.assert_called_once_with('result_file', 'w')
        mock_json.dumps.assert_called_once_with('results')
        file_obj.write.assert_called_once_with('results text\n')

    @patch('__builtin__.open')
    @patch('dovetail.report.json')
    @patch('dovetail.report.os.path')
    @patch('dovetail.report.dt_cfg')
    def test_save_json_results_exception(self, mock_config, mock_path,
                                         mock_json, mock_open):
        report = dt_report.Report()
        logger_obj = Mock()
        report.logger = logger_obj
        mock_config.dovetail_config = {
            'result_dir': 'a',
            'result_file': 'b'
        }
        mock_path.join.return_value = 'result_file'
        mock_open.return_value.__enter__.side_effect = Exception('error')

        report.save_json_results('results')

        mock_path.join.assert_called_once_with('a', 'b')
        mock_open.assert_called_once_with('result_file', 'w')
        report.logger.exception.assert_called_once_with(
            'Failed to add result to file result_file, exception: error')

    @patch('dovetail.report.dt_cfg')
    @patch('dovetail.report.time')
    @patch('dovetail.report.os')
    @patch('dovetail.report.tarfile')
    def test_save_logs(self, mock_tar, mock_os, mock_time, mock_config):
        mock_config.dovetail_config = {'result_dir': 'result_dir'}
        local_time_obj = Mock()
        mock_time.localtime.return_value = local_time_obj
        mock_time.strftime.return_value = '20180113_13:13'
        mock_os.getcwd.return_value = 'cwd'
        tar_obj = Mock()
        tar_file_obj = Mock()
        mock_tar.open.return_value.__enter__.return_value = tar_file_obj
        mock_os.path.join.side_effect = ['one', tar_obj, 'three']
        mock_os.listdir.return_value = ['file']

        dt_report.Report.save_logs()

        mock_time.localtime.assert_called_once_with()
        mock_time.strftime.assert_called_once_with('%Y%m%d_%H%M',
                                                   local_time_obj)
        mock_os.getcwd.assert_called_once_with()
        mock_os.path.join.assert_has_calls([
            call('result_dir', '..'),
            call('result_dir', '..', 'logs_20180113_13:13.tar.gz'),
            call('results', 'file')])
        mock_tar.open.assert_called_once_with(tar_obj, 'w:gz')
        mock_os.listdir.assert_called_once_with('result_dir')
        tar_file_obj.add.assert_called_once_with('three')
        mock_os.chdir.assert_has_calls([call('one'), call('cwd')])

    @patch('dovetail.report.CrawlerFactory')
    def test_get_result(self, mock_crawler):
        logger_obj = Mock()
        report = dt_report.Report()
        report.logger = logger_obj
        testcase_obj = Mock()
        crawler_obj = Mock()
        testcase_obj.validate_testcase.return_value = 'validate'
        testcase_obj.validate_type.return_value = 'functest'
        mock_crawler.create.return_value = crawler_obj
        crawler_obj.crawl.return_value = 'result'

        result = report.get_result(testcase_obj, 'check_results_file')

        testcase_obj.validate_testcase.assert_called_once_with()
        testcase_obj.validate_type.assert_called_once_with()
        mock_crawler.create.assert_called_once_with('functest')
        crawler_obj.crawl.assert_called_once_with(
            testcase_obj, 'check_results_file')
        logger_obj.debug.assert_called_once_with(
            'Test case: validate -> result acquired')
        self.assertEquals({'validate': 'result'},
                          dt_report.Report.results['functest'])
        self.assertEquals('result', result)

    @patch('dovetail.report.CrawlerFactory')
    def test_get_result_no_result(self, mock_crawler):
        logger_obj = Mock()
        report = dt_report.Report()
        report.logger = logger_obj
        testcase_obj = Mock()
        crawler_obj = Mock()
        testcase_obj.validate_testcase.return_value = 'validate'
        testcase_obj.validate_type.return_value = 'functest'
        testcase_obj.increase_retry.return_value = 'retry'
        mock_crawler.create.return_value = crawler_obj
        crawler_obj.crawl.return_value = None

        result = report.get_result(testcase_obj, 'check_results_file')

        testcase_obj.validate_testcase.assert_called_once_with()
        testcase_obj.validate_type.assert_called_once_with()
        mock_crawler.create.assert_called_once_with('functest')
        crawler_obj.crawl.assert_called_once_with(
            testcase_obj, 'check_results_file')
        testcase_obj.increase_retry.assert_called_once_with()
        logger_obj.debug.assert_called_once_with(
            'Test case: validate -> result acquired retry: retry')
        self.assertEquals(None, result)

    @patch('dovetail.report.CrawlerFactory')
    def test_get_result_no_crawler(self, mock_crawler):
        logger_obj = Mock()
        report = dt_report.Report()
        report.logger = logger_obj
        testcase_obj = Mock()
        testcase_obj.name.return_value = 'name'
        testcase_obj.validate_testcase.return_value = 'validate'
        testcase_obj.validate_type.return_value = 'functest'
        mock_crawler.create.return_value = None

        result = report.get_result(testcase_obj, 'check_results_file')

        testcase_obj.validate_testcase.assert_called_once_with()
        testcase_obj.validate_type.assert_called_once_with()
        mock_crawler.create.assert_called_once_with('functest')
        logger_obj.error.assert_called_once_with(
            'Crawler is None: name')
        self.assertEquals(None, result)

    @patch('dovetail.report.dt_logger')
    def test_functest_crawler_create_log(self, mock_logger):
        getlogger_obj = Mock()
        logger_obj = Mock()
        logger_obj.getLogger.return_value = getlogger_obj
        mock_logger.Logger.return_value = logger_obj

        dt_report.FunctestCrawler.create_log()

        self.assertEquals(getlogger_obj, dt_report.FunctestCrawler.logger)

    @patch('dovetail.report.dt_cfg')
    @patch('dovetail.report.os.path')
    def test_functest_crawler_crawl_not_exists(self, mock_path, mock_config):
        logger_obj = Mock()
        mock_config.dovetail_config = {'build_tag': 'tag'}
        dt_report.FunctestCrawler.logger = logger_obj
        mock_path.exists.return_value = False
        file_path = 'file_path'
        testcase_obj = Mock()
        testcase_obj.validate_testcase.return_value = 'validate'
        testcase_obj.name.return_value = 'name'

        crawler = dt_report.FunctestCrawler()
        result = crawler.crawl(testcase_obj, file_path)

        mock_path.exists.assert_called_once_with(file_path)
        testcase_obj.validate_testcase.assert_called_once_with()
        testcase_obj.name.assert_called_once_with()
        logger_obj.error.assert_called_once_with(
            'Result file not found: {}'.format(file_path))
        self.assertEquals(None, result)

    @patch('__builtin__.open')
    @patch('dovetail.report.json')
    @patch('dovetail.report.dt_cfg')
    @patch('dovetail.report.dt_utils')
    @patch('dovetail.report.os.path')
    def test_functest_crawler_crawl(self, mock_path, mock_utils, mock_config,
                                    mock_json, mock_open):
        logger_obj = Mock()
        mock_config.dovetail_config = {'build_tag': 'tag'}
        dt_report.FunctestCrawler.logger = logger_obj
        mock_path.exists.return_value = True
        file_path = 'file_path'
        testcase_obj = Mock()
        testcase_obj.validate_testcase.return_value = 'name'
        testcase_obj.name.return_value = 'name'
        testcase_obj.sub_testcase.return_value = ['subt_a']
        file_obj = Mock()
        mock_open.return_value.__enter__.return_value = [file_obj]
        data_dict = {
            'case_name': 'name',
            'build_tag': 'tag-name',
            'criteria': 'criteria',
            'start_date': 'start_date',
            'stop_date': 'stop_date',
            'details': {
                'tests_number': 'tests_number',
                'failures_number': 'failures_number',
                'success': 'success',
                'failures': 'failures',
                'skipped': 'skipped'
            }
        }
        mock_json.loads.return_value = data_dict
        mock_utils.get_duration.return_value = 'duration'

        crawler = dt_report.FunctestCrawler()
        result = crawler.crawl(testcase_obj, file_path)
        expected = {'criteria': 'criteria', 'timestart': 'start_date',
                    'timestop': 'stop_date', 'duration': 'duration',
                    'details': {
                        'tests': 'tests_number', 'failures': 'failures_number',
                        'success': 'success', 'errors': 'failures',
                        'skipped': 'skipped'}}

        mock_path.exists.assert_called_once_with(file_path)
        mock_open.assert_called_once_with(file_path, 'r')
        mock_json.loads.assert_called_once_with(file_obj)
        mock_utils.get_duration.assert_called_once_with(
            'start_date', 'stop_date', logger_obj)
        testcase_obj.set_results.assert_called_once_with(expected)
        testcase_obj.validate_testcase.assert_called_once_with()
        testcase_obj.sub_testcase.assert_called_once_with()
        testcase_obj.name.assert_called_once_with()
        self.assertEquals(expected, result)

    @patch('__builtin__.open')
    @patch('dovetail.report.json.loads')
    @patch('dovetail.report.dt_cfg')
    @patch('dovetail.report.dt_utils')
    @patch('dovetail.report.os.path')
    def test_functest_crawler_crawl_errors(self, mock_path, mock_utils,
                                           mock_config, mock_load, mock_open):
        logger_obj = Mock()
        mock_config.dovetail_config = {'build_tag': 'tag'}
        dt_report.FunctestCrawler.logger = logger_obj
        mock_path.exists.return_value = True
        file_path = 'file_path'
        testcase_obj = Mock()
        testcase_obj.validate_testcase.return_value = 'name'
        testcase_obj.name.return_value = 'name'
        testcase_obj.sub_testcase.return_value = ['subt_a']
        file_a = Mock()
        file_b = Mock()
        mock_open.return_value.__enter__.return_value = [file_a, file_b]
        mock_load.side_effect = [ValueError(), {}]
        mock_utils.get_duration.return_value = 'duration'

        crawler = dt_report.FunctestCrawler()
        result = crawler.crawl(testcase_obj, file_path)

        mock_path.exists.assert_called_once_with(file_path)
        mock_open.assert_called_once_with(file_path, 'r')
        mock_load.assert_has_calls([call(file_a), call(file_b)])
        testcase_obj.validate_testcase.assert_called_once_with()
        testcase_obj.sub_testcase.assert_called_once_with()
        testcase_obj.name.assert_called_once_with()
        logger_obj.exception.assert_called_once_with(
            "Result data don't have key 'case_name'.")
        self.assertEquals(None, result)

    @patch('dovetail.report.dt_logger')
    def test_yardstick_crawler_create_log(self, mock_logger):
        getlogger_obj = Mock()
        logger_obj = Mock()
        logger_obj.getLogger.return_value = getlogger_obj
        mock_logger.Logger.return_value = logger_obj

        dt_report.YardstickCrawler.create_log()

        self.assertEquals(getlogger_obj, dt_report.YardstickCrawler.logger)

    @patch('dovetail.report.os.path')
    def test_yardstick_crawler_crawl_not_exists(self, mock_path):
        logger_obj = Mock()
        dt_report.YardstickCrawler.logger = logger_obj
        mock_path.exists.return_value = False
        file_path = 'file_path'

        crawler = dt_report.YardstickCrawler()
        result = crawler.crawl(None, file_path)

        mock_path.exists.assert_called_once_with(file_path)
        logger_obj.error.assert_called_once_with(
            'Result file not found: {}'.format(file_path))
        self.assertEquals(None, result)

    @patch('__builtin__.open')
    @patch('dovetail.report.json.loads')
    @patch('dovetail.report.dt_utils')
    @patch('dovetail.report.os.path')
    def test_yardstick_crawler_crawl(self, mock_path, mock_utils, mock_loads,
                                     mock_open):
        dt_report.YardstickCrawler.logger = Mock()
        mock_path.exists.return_value = True
        file_path = 'file_path'
        testcase_obj = Mock()
        testcase_obj.validate_testcase.return_value = 'name'
        file_obj = Mock()
        mock_open.return_value.__enter__.return_value = [file_obj]
        data_dict = {
            'result': {
                'testcases': {
                    'name': {
                        'tc_data': [{
                            'data': {
                                'sla_pass': 0
                            }
                        }]
                    }
                }
            }
        }
        mock_loads.return_value = data_dict
        mock_utils.get_value_from_dict.return_value = 'PASS'

        crawler = dt_report.YardstickCrawler()
        result = crawler.crawl(testcase_obj, file_path)
        expected = {'criteria': 'FAIL'}

        mock_path.exists.assert_called_once_with(file_path)
        mock_open.assert_called_once_with(file_path, 'r')
        mock_loads.assert_called_once_with(file_obj)
        mock_utils.get_value_from_dict.assert_called_once_with(
            'result.criteria', data_dict)
        testcase_obj.validate_testcase.assert_called_once_with()
        testcase_obj.set_results.assert_called_once_with(expected)
        self.assertEquals(expected, result)

    @patch('__builtin__.open')
    @patch('dovetail.report.json.loads')
    @patch('dovetail.report.dt_utils')
    @patch('dovetail.report.os.path')
    def test_yardstick_crawler_crawl_key_error(self, mock_path, mock_utils,
                                               mock_loads, mock_open):
        logger_obj = Mock()
        dt_report.YardstickCrawler.logger = logger_obj
        mock_path.exists.return_value = True
        file_path = 'file_path'
        testcase_obj = Mock()
        testcase_obj.validate_testcase.return_value = 'name'
        file_obj = Mock()
        mock_open.return_value.__enter__.return_value = [file_obj]

        mock_loads.return_value = {}
        mock_utils.get_value_from_dict.return_value = 'PASS'

        crawler = dt_report.YardstickCrawler()
        result = crawler.crawl(testcase_obj, file_path)
        expected = {'criteria': 'PASS'}

        mock_path.exists.assert_called_once_with(file_path)
        mock_open.assert_called_once_with(file_path, 'r')
        mock_loads.assert_called_once_with(file_obj)
        mock_utils.get_value_from_dict.assert_called_once_with(
            'result.criteria', {})
        testcase_obj.validate_testcase.assert_called_once_with()
        testcase_obj.set_results.assert_called_once_with(expected)
        logger_obj.exception.assert_called_once_with(
            "Pass flag not found 'result'")
        self.assertEquals(expected, result)

    @patch('dovetail.report.dt_logger')
    def test_bottlenecks_crawler_create_log(self, mock_logger):
        getlogger_obj = Mock()
        logger_obj = Mock()
        logger_obj.getLogger.return_value = getlogger_obj
        mock_logger.Logger.return_value = logger_obj

        dt_report.BottlenecksCrawler.create_log()

        self.assertEquals(getlogger_obj, dt_report.BottlenecksCrawler.logger)

    @patch('dovetail.report.os.path')
    def test_bottlenecks_crawler_crawl_not_exists(self, mock_path):
        logger_obj = Mock()
        dt_report.BottlenecksCrawler.logger = logger_obj
        mock_path.exists.return_value = False
        file_path = 'file_path'

        crawler = dt_report.BottlenecksCrawler()
        result = crawler.crawl(None, file_path)

        mock_path.exists.assert_called_once_with(file_path)
        logger_obj.error.assert_called_once_with(
            'Result file not found: {}'.format(file_path))
        self.assertEquals(None, result)

    @patch('__builtin__.open')
    @patch('dovetail.report.json.loads')
    @patch('dovetail.report.os.path')
    def test_bottlenecks_crawler_crawl_pass(self, mock_path, mock_loads,
                                            mock_open):
        dt_report.BottlenecksCrawler.logger = Mock()
        mock_path.exists.return_value = True
        file_path = 'file_path'
        testcase_obj = Mock()
        file_obj = Mock()
        mock_open.return_value.__enter__.return_value = [file_obj]
        data_dict = {
            'data_body': {
                'result': 'PASS'
            }
        }
        mock_loads.return_value = data_dict

        crawler = dt_report.BottlenecksCrawler()
        result = crawler.crawl(testcase_obj, file_path)
        expected = {'criteria': 'PASS'}

        mock_path.exists.assert_called_once_with(file_path)
        mock_open.assert_called_once_with(file_path, 'r')
        mock_loads.assert_called_once_with(file_obj)
        testcase_obj.set_results.assert_called_once_with(expected)
        self.assertEquals(expected, result)

    @patch('__builtin__.open')
    @patch('dovetail.report.json.loads')
    @patch('dovetail.report.os.path')
    def test_bottlenecks_crawler_crawl_fail(self, mock_path, mock_loads,
                                            mock_open):
        dt_report.BottlenecksCrawler.logger = Mock()
        mock_path.exists.return_value = True
        file_path = 'file_path'
        testcase_obj = Mock()
        file_obj = Mock()
        mock_open.return_value.__enter__.return_value = [file_obj]
        data_dict = {
            'data_body': {
                'result': 'FAIL'
            }
        }
        mock_loads.return_value = data_dict

        crawler = dt_report.BottlenecksCrawler()
        result = crawler.crawl(testcase_obj, file_path)
        expected = {'criteria': 'FAIL'}

        mock_path.exists.assert_called_once_with(file_path)
        mock_open.assert_called_once_with(file_path, 'r')
        mock_loads.assert_called_once_with(file_obj)
        testcase_obj.set_results.assert_called_once_with(expected)
        self.assertEquals(expected, result)

    @patch('__builtin__.open')
    @patch('dovetail.report.json.loads')
    @patch('dovetail.report.os.path')
    def test_bottlenecks_crawler_crawl_key_error(self, mock_path, mock_loads,
                                                 mock_open):
        logger_obj = Mock()
        dt_report.BottlenecksCrawler.logger = logger_obj
        mock_path.exists.return_value = True
        file_path = 'file_path'
        testcase_obj = Mock()
        file_obj = Mock()
        mock_open.return_value.__enter__.return_value = [file_obj]

        mock_loads.return_value = {}

        crawler = dt_report.BottlenecksCrawler()
        result = crawler.crawl(testcase_obj, file_path)
        expected = {'criteria': 'FAIL'}

        mock_path.exists.assert_called_once_with(file_path)
        mock_open.assert_called_once_with(file_path, 'r')
        mock_loads.assert_called_once_with(file_obj)
        testcase_obj.set_results.assert_called_once_with(expected)
        logger_obj.exception.assert_called_once_with(
            "Pass flag not found 'data_body'")
        self.assertEquals(expected, result)

    @patch('dovetail.report.os.path')
    def test_shell_crawler_crawl_not_exists(self, mock_path):
        mock_path.exists.return_value = False
        file_path = 'file_path'

        crawler = dt_report.ShellCrawler()
        result = crawler.crawl(None, file_path)

        mock_path.exists.assert_called_once_with(file_path)
        self.assertEquals(None, result)

    @patch('__builtin__.open')
    @patch('dovetail.report.os.path')
    def test_shell_crawler_crawl_exception(self, mock_path, mock_open):
        mock_path.exists.return_value = True
        file_path = 'file_path'
        mock_open.return_value.__enter__.return_value = Exception()

        crawler = dt_report.ShellCrawler()
        result = crawler.crawl(None, file_path)

        mock_path.exists.assert_called_once_with(file_path)
        mock_open.assert_called_once_with(file_path, 'r')
        self.assertEquals(None, result)

    @patch('__builtin__.open')
    @patch('dovetail.report.json.load')
    @patch('dovetail.report.os.path')
    def test_shell_crawler_crawl(self, mock_path, mock_load,
                                 mock_open):
        mock_path.exists.return_value = True
        file_path = 'file_path'
        file_obj = Mock()
        mock_open.return_value.__enter__.return_value = file_obj
        mock_load.return_value = 'result'

        crawler = dt_report.ShellCrawler()
        result = crawler.crawl(None, file_path)

        mock_path.exists.assert_called_once_with(file_path)
        mock_open.assert_called_once_with(file_path, 'r')
        mock_load.assert_called_once_with(file_obj)
        self.assertEquals('result', result)

    @patch('dovetail.report.dt_logger')
    def test_vnftest_crawler_create_log(self, mock_logger):
        getlogger_obj = Mock()
        logger_obj = Mock()
        logger_obj.getLogger.return_value = getlogger_obj
        mock_logger.Logger.return_value = logger_obj

        dt_report.VnftestCrawler.create_log()

        self.assertEquals(getlogger_obj, dt_report.VnftestCrawler.logger)

    @patch('dovetail.report.os.path')
    def test_vnftest_crawler_crawl_not_exists(self, mock_path):
        logger_obj = Mock()
        dt_report.VnftestCrawler.logger = logger_obj
        mock_path.exists.return_value = False
        file_path = 'file_path'

        crawler = dt_report.VnftestCrawler()
        result = crawler.crawl(None, file_path)

        mock_path.exists.assert_called_once_with(file_path)
        logger_obj.error.assert_called_once_with(
            'Result file not found: {}'.format(file_path))
        self.assertEquals(None, result)

    @patch('__builtin__.open')
    @patch('dovetail.report.json.loads')
    @patch('dovetail.report.os.path')
    def test_vnftest_crawler_crawl(self, mock_path, mock_loads,
                                   mock_open):
        dt_report.VnftestCrawler.logger = Mock()
        mock_path.exists.return_value = True
        file_path = 'file_path'
        testcase_obj = Mock()
        file_obj = Mock()
        mock_open.return_value.__enter__.return_value = [file_obj]
        data_dict = {
            'result': {
                'criteria': 'PASS'
            }
        }
        mock_loads.return_value = data_dict

        crawler = dt_report.VnftestCrawler()
        result = crawler.crawl(testcase_obj, file_path)
        expected = {'criteria': 'PASS'}

        mock_path.exists.assert_called_once_with(file_path)
        mock_open.assert_called_once_with(file_path, 'r')
        mock_loads.assert_called_once_with(file_obj)
        self.assertEquals(expected, result)

    @patch('__builtin__.open')
    @patch('dovetail.report.json.loads')
    @patch('dovetail.report.os.path')
    def test_vnftest_crawler_crawl_key_error(self, mock_path, mock_loads,
                                             mock_open):
        logger_obj = Mock()
        dt_report.VnftestCrawler.logger = logger_obj
        mock_path.exists.return_value = True
        file_path = 'file_path'
        testcase_obj = Mock()
        file_obj = Mock()
        mock_open.return_value.__enter__.return_value = [file_obj]

        mock_loads.return_value = {}

        crawler = dt_report.VnftestCrawler()
        result = crawler.crawl(testcase_obj, file_path)
        expected = {'criteria': 'FAIL'}

        mock_path.exists.assert_called_once_with(file_path)
        mock_open.assert_called_once_with(file_path, 'r')
        mock_loads.assert_called_once_with(file_obj)
        logger_obj.exception.assert_called_once_with(
            "Pass flag not found 'result'")
        self.assertEquals(expected, result)

    def test_crawler_factory(self):
        result = dt_report.CrawlerFactory.create('shell')
        self.assertEquals(dt_report.ShellCrawler, result.__class__)

    def test_crawler_factory_none(self):
        self.assertEquals(None, dt_report.CrawlerFactory.create('other'))

    def test_result_checker(self):
        self.assertEquals('PASS', dt_report.ResultChecker.check())

    @patch('dovetail.report.dt_logger')
    def test_functest_checker_create_log(self, mock_logger):
        getlogger_obj = Mock()
        logger_obj = Mock()
        logger_obj.getLogger.return_value = getlogger_obj
        mock_logger.Logger.return_value = logger_obj

        dt_report.FunctestChecker.create_log()

        self.assertEquals(getlogger_obj, dt_report.FunctestChecker.logger)

    def test_functest_get_sub_testcase_no_result(self):
        self.assertEquals(
            False, dt_report.FunctestChecker.get_sub_testcase(None, None))

    def test_functest_get_sub_testcase_simple_match(self):
        self.assertEquals(
            True,
            dt_report.FunctestChecker.get_sub_testcase('subt_a',
                                                       ['subt_b', 'subt_a']))

    def test_functest_get_sub_testcase_extended_match(self):
        self.assertEquals(
            True,
            dt_report.FunctestChecker.get_sub_testcase('subt_a',
                                                       ['subt_b', 'subt_a+']))

    def test_functest_get_sub_no_match(self):
        self.assertEquals(
            False,
            dt_report.FunctestChecker.get_sub_testcase('subt_a',
                                                       ['subt_b']))

    def test_functest_check_no_db_results(self):
        testcase_obj = Mock()
        testcase_obj.sub_testcase.return_value = ['subt_a']

        checker = dt_report.FunctestChecker()
        checker.check(testcase_obj, None)

        testcase_obj.sub_testcase.assert_called_once_with()
        testcase_obj.sub_testcase_passed.assert_called_once_with(
            'subt_a', 'FAIL')

    def test_functest_check_no_subtestcases(self):
        testcase_obj = Mock()
        testcase_obj.sub_testcase.return_value = None

        checker = dt_report.FunctestChecker()
        checker.check(testcase_obj, {'criteria': 'PASS'})

        testcase_obj.sub_testcase.assert_called_once_with()
        testcase_obj.passed.assert_called_once_with('PASS')

    @patch.object(dt_report.FunctestChecker, 'get_sub_testcase')
    def test_functest_check(self, mock_get):
        testcase_obj = Mock()
        testcase_obj.sub_testcase.return_value = [
            'subt_a', 'subt_b', 'subt_c', 'subt_d']
        logger_obj = Mock()
        dt_report.FunctestChecker.logger = logger_obj
        db_result = {
            'criteria': 'PASS',
            'details': {
                'success': True,
                'skipped': False
            }
        }
        mock_get.side_effect = [True, False, True, False, False, KeyError()]

        checker = dt_report.FunctestChecker()
        checker.check(testcase_obj, db_result)

        testcase_obj.sub_testcase.assert_called_once_with()
        logger_obj.debug.assert_has_calls([
            call('Check sub_testcase: subt_a'),
            call('Check sub_testcase: subt_b'),
            call('Check sub_testcase: subt_c'),
            call('Check sub_testcase: subt_d')])
        testcase_obj.sub_testcase_passed.assert_has_calls([
            call('subt_a', 'PASS'),
            call('subt_b', 'SKIP'),
            call('subt_c', 'FAIL'),
            call('subt_d', 'FAIL')])
        testcase_obj.passed.assert_has_calls([call('PASS'), call('FAIL')])

    @patch('dovetail.report.dt_logger')
    def test_yardstick_checker_create_log(self, mock_logger):
        getlogger_obj = Mock()
        logger_obj = Mock()
        logger_obj.getLogger.return_value = getlogger_obj
        mock_logger.Logger.return_value = logger_obj

        dt_report.YardstickChecker.create_log()

        self.assertEquals(getlogger_obj, dt_report.YardstickChecker.logger)

    def test_yardstick_check_result(self):
        testcase_obj = Mock()
        result = {'criteria': 'PASS'}

        dt_report.YardstickChecker.check(testcase_obj, result)

        testcase_obj.passed.assert_called_once_with('PASS')

    def test_yardstick_check_result_none(self):
        testcase_obj = Mock()
        result = {}

        dt_report.YardstickChecker.check(testcase_obj, result)

        testcase_obj.passed.assert_called_once_with('FAIL')

    @patch('dovetail.report.dt_logger')
    def test_bottlenecks_checker_create_log(self, mock_logger):
        getlogger_obj = Mock()
        logger_obj = Mock()
        logger_obj.getLogger.return_value = getlogger_obj
        mock_logger.Logger.return_value = logger_obj

        dt_report.BottlenecksChecker.create_log()

        self.assertEquals(getlogger_obj, dt_report.BottlenecksChecker.logger)

    def test_bottlenecks_check_result(self):
        testcase_obj = Mock()
        result = {'criteria': 'PASS'}

        dt_report.BottlenecksChecker.check(testcase_obj, result)

        testcase_obj.passed.assert_called_once_with('PASS')

    def test_bottlenecks_check_result_none(self):
        testcase_obj = Mock()
        result = {}

        dt_report.BottlenecksChecker.check(testcase_obj, result)

        testcase_obj.passed.assert_called_once_with('FAIL')

    def test_shell_check_result(self):
        testcase_obj = Mock()
        result = {'pass': True}

        dt_report.ShellChecker.check(testcase_obj, result)

        testcase_obj.passed.assert_called_once_with(True)

    def test_shell_check_result_exception(self):
        testcase_obj = Mock()
        result = {}

        dt_report.ShellChecker.check(testcase_obj, result)

        testcase_obj.passed.assert_called_once_with(False)

    @patch('dovetail.report.dt_logger')
    def test_vnftest_checker_create_log(self, mock_logger):
        getlogger_obj = Mock()
        logger_obj = Mock()
        logger_obj.getLogger.return_value = getlogger_obj
        mock_logger.Logger.return_value = logger_obj

        dt_report.VnftestChecker.create_log()

        self.assertEquals(getlogger_obj, dt_report.VnftestChecker.logger)

    def test_vnftest_check_result(self):
        testcase_obj = Mock()
        result = {'criteria': 'PASS'}

        dt_report.VnftestChecker.check(testcase_obj, result)

        testcase_obj.passed.assert_called_once_with('PASS')

    def test_vnftest_check_result_none(self):
        testcase_obj = Mock()
        result = {}

        dt_report.VnftestChecker.check(testcase_obj, result)

        testcase_obj.passed.assert_called_once_with('FAIL')

    def test_checker_factory(self):
        result = dt_report.CheckerFactory.create('shell')
        self.assertEquals(dt_report.ShellChecker, result.__class__)

    def test_checker_factory_none(self):
        self.assertEquals(None, dt_report.CheckerFactory.create('other'))
