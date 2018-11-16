#!/usr/bin/env python
#
# Copyright (c) 2018 mokats@intracom-telecom.com and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##

import os
import unittest
import yaml
from mock import patch, call, Mock
from _pytest.monkeypatch import MonkeyPatch

from dovetail.utils.dovetail_config import DovetailConfig
import click  # noqa: F401

monkeypatch = MonkeyPatch()
conf_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__)))
file_path = os.path.join(os.path.dirname(__file__), 'cmd_config.yml')
with open(file_path) as f:
    extra_config = yaml.safe_load(f)
monkeypatch.setattr(DovetailConfig, 'load_config_files', Mock())
monkeypatch.setattr(DovetailConfig, 'dovetail_config', extra_config)
from dovetail import run as dt_run  # noqa: E402
monkeypatch.undo()

__author__ = 'Stamatis Katsaounis <mokats@intracom-telecom.com>'


class RunTesting(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch('dovetail.run.dt_testcase.Testsuite')
    def test_load_testsuite(self, mock_testsuite):
        mock_testsuite.get.return_value = 'suite_a'

        result = dt_run.load_testsuite('testsuite')

        mock_testsuite.load.assert_called_once_with()
        mock_testsuite.get.assert_called_once_with('testsuite')
        self.assertEquals('suite_a', result)

    @patch('dovetail.run.dt_report.Report')
    def test_run_test_no_list(self, mock_report):
        logger = Mock()
        mock_report.return_value = Mock()

        dt_run.run_test([], False, logger)
        logger.warning.assert_called_once_with(
            "No test case will be executed.")

    @patch('dovetail.run.dt_cfg')
    @patch('dovetail.run.dt_report.Report')
    @patch('dovetail.run.dt_testcase.Testcase')
    @patch('dovetail.run.time')
    def test_run_test(self, mock_time, mock_testcase, mock_report,
                      mock_config):
        logger = Mock()
        report_obj = Mock()
        mock_report.return_value = report_obj
        mock_time.time.side_effect = [42, 84]
        testcase_name = 'testcase'
        testcase_obj = Mock()
        mock_testcase.get.return_value = testcase_obj
        mock_config.dovetail_config = {'stop': True}
        report_obj.check_tc_result.return_value = {'criteria': 'PASS'}

        dt_run.run_test([testcase_name], True, logger)

        mock_time.time.assert_has_calls([call(), call()])
        logger.info.assert_called_once_with(
            '>>[testcase]: {}'.format(testcase_name))
        mock_testcase.get.assert_called_once_with(testcase_name)
        testcase_obj.run.assert_called_once_with()
        report_obj.check_tc_result.assert_called_once_with(testcase_obj)
        report_obj.generate.assert_called_once_with([testcase_name], 42)
        report_obj.save_logs.assert_called_once_with()

    @patch('dovetail.run.dt_cfg')
    @patch('dovetail.run.dt_report.Report')
    @patch('dovetail.run.dt_testcase.Testcase')
    @patch('dovetail.run.time')
    def test_run_test_fail(self, mock_time, mock_testcase, mock_report,
                           mock_config):
        logger = Mock()
        report_obj = Mock()
        mock_report.return_value = report_obj
        testcase_name = 'testcase'
        testcase_obj = Mock()
        mock_testcase.get.return_value = testcase_obj
        mock_config.dovetail_config = {'stop': True}
        report_obj.check_tc_result.return_value = {'criteria': 'FAIL'}

        dt_run.run_test([testcase_name], True, logger)

        mock_time.time.assert_called_once_with()
        logger.info.assert_has_calls([
            call('>>[testcase]: {}'.format(testcase_name)),
            call('Stop because {} failed'.format(testcase_name))])
        mock_testcase.get.assert_called_once_with(testcase_name)
        testcase_obj.run.assert_called_once_with()
        report_obj.check_tc_result.assert_called_once_with(testcase_obj)

    @patch('dovetail.run.dt_cfg')
    @patch('dovetail.run.dt_report.Report')
    @patch('dovetail.run.dt_testcase.Testcase')
    @patch('dovetail.run.time')
    def test_run_test_fail_key_error(self, mock_time, mock_testcase,
                                     mock_report, mock_config):
        logger = Mock()
        report_obj = Mock()
        mock_report.return_value = report_obj
        mock_time.time.return_value = 42
        testcase_name = 'testcase'
        testcase_obj = Mock()
        mock_testcase.get.return_value = testcase_obj
        mock_config.dovetail_config = {'stop': True}
        report_obj.check_tc_result.return_value = {'key': 'value'}

        dt_run.run_test([testcase_name], True, logger)

        mock_time.time.assert_called_once_with()
        logger.info.assert_has_calls([
            call('>>[testcase]: {}'.format(testcase_name)),
            call('Stop because {} failed'.format(testcase_name))])
        logger.error.assert_called_once_with("There is no key 'criteria'.")
        mock_testcase.get.assert_called_once_with(testcase_name)
        testcase_obj.run.assert_called_once_with()
        report_obj.check_tc_result.assert_called_once_with(testcase_obj)

    @patch('dovetail.run.dt_cfg')
    def test_filter_config(self, mock_config):
        mock_config.dovetail_config = {
            'cli': {
                'key_a': {
                    'config': {
                        'config_key': {'path': 'a'},
                        'KEY_UPPER': {'path': 'b'}
                    }
                },
                'key_b': {},
                'key_c': {
                    'config': None
                },
                'key_d': {
                    'invalid': {}
                }
            }
        }
        input_dict = {
            'config_key': 'c',
            'key_upper': 'd'
        }
        expected_dict = {
            'config_key': {'path': 'a', 'value': 'c'},
            'KEY_UPPER': {'path': 'b', 'value': 'd'}
        }

        result = dt_run.filter_config(input_dict, Mock())

        self.assertEquals(expected_dict, result)

    @patch('dovetail.run.dt_cfg')
    def test_filter_config_none(self, mock_config):
        mock_config.dovetail_config = {'cli': {}}
        result = dt_run.filter_config({}, Mock())

        self.assertEquals(None, result)

    @patch('dovetail.run.dt_cfg')
    def test_filter_config_keyerror(self, mock_config):
        mock_config.dovetail_config = {
            'cli': {
                'key_a': {
                    'config': {
                        'config_key': {'invalid': 'a'}
                    }
                }
            }
        }
        input_dict = {'config_key': 'c'}
        logger = Mock()

        with self.assertRaises(SystemExit) as cm:
            dt_run.filter_config(input_dict, logger)

        logger.exception.assert_called_once_with("KeyError 'path'.")
        expected = cm.exception
        self.assertEqual(expected.code, 2)

    @patch('dovetail.run.Container')
    @patch('dovetail.run.Parser')
    @patch('dovetail.run.dt_report')
    @patch('dovetail.run.dt_test_runner')
    @patch('dovetail.run.dt_testcase')
    def test_create_logs(self, mock_testcase, mock_test_runner, mock_report,
                         mock_parser, mock_container):

        dt_run.create_logs()

        mock_container.create_log.assert_called_once_with()
        mock_parser.create_log.assert_called_once_with()
        mock_report.Report.create_log.assert_called_once_with()
        mock_report.FunctestCrawler.create_log.assert_called_once_with()
        mock_report.YardstickCrawler.create_log.assert_called_once_with()
        mock_report.VnftestCrawler.create_log.assert_called_once_with()
        mock_report.BottlenecksCrawler.create_log.assert_called_once_with()
        mock_report.FunctestChecker.create_log.assert_called_once_with()
        mock_report.YardstickChecker.create_log.assert_called_once_with()
        mock_report.VnftestChecker.create_log.assert_called_once_with()
        mock_report.BottlenecksChecker.create_log.assert_called_once_with()
        mock_testcase.Testcase.create_log.assert_called_once_with()
        mock_testcase.Testsuite.create_log.assert_called_once_with()
        mock_test_runner.DockerRunner.create_log.assert_called_once_with()
        mock_test_runner.ShellRunner.create_log.assert_called_once_with()

    @patch('dovetail.run.dt_utils')
    @patch('dovetail.run.dt_cfg')
    @patch('dovetail.run.os')
    def test_clean_results_dir(self, mock_os, mock_config, mock_utils):
        mock_config.dovetail_config = {'result_dir': 'value'}
        mock_os.path.exists.return_value = True
        mock_os.path.isdir.return_value = True

        dt_run.clean_results_dir(Mock())

        mock_os.path.exists.assert_called_once_with('value')
        mock_os.path.isdir.assert_called_once_with('value')
        mock_utils.exec_cmd.assert_called_once_with(
            'sudo rm -rf value/*', exit_on_error=False, exec_msg_on=False)

    @patch('dovetail.run.dt_utils')
    @patch('dovetail.run.dt_cfg')
    @patch('dovetail.run.os')
    def test_clean_results_dir_error(self, mock_os, mock_config, mock_utils):
        mock_config.dovetail_config = {'result_dir': 'value'}
        mock_os.path.exists.return_value = True
        mock_os.path.isdir.return_value = False
        logger = Mock()

        with self.assertRaises(SystemExit) as cm:
            dt_run.clean_results_dir(logger)

        mock_os.path.exists.assert_called_once_with('value')
        mock_os.path.isdir.assert_called_once_with('value')
        logger.error.assert_called_once_with(
            'result_dir in dovetail_config.yml is not a directory.')
        expected = cm.exception
        self.assertEqual(expected.code, 2)

    @patch('dovetail.run.dt_cfg')
    @patch('dovetail.run.os')
    def test_get_result_path(self, mock_os, mock_config):
        dovetail_home = 'dovetail_home'
        mock_os.environ = {'DOVETAIL_HOME': dovetail_home}
        mock_os.path.join.side_effect = [
            'result_path', 'images_dir', 'pre_config_path', 'patch_set_path']
        mock_config.dovetail_config = {}

        result = dt_run.get_result_path(Mock())

        mock_os.path.join.assert_has_calls([
            call(dovetail_home, 'results'),
            call(dovetail_home, 'images'),
            call(dovetail_home, 'pre_config'),
            call(dovetail_home, 'patches')])
        expected_dict = {
            'result_dir': 'result_path',
            'images_dir': 'images_dir',
            'config_dir': 'pre_config_path',
            'patch_dir': 'patch_set_path'}
        self.assertEquals(expected_dict, mock_config.dovetail_config)
        self.assertEquals(dovetail_home, result)

    @patch('dovetail.run.os')
    def test_get_result_path_exception(self, mock_os):
        mock_os.environ = {}
        logger = Mock()

        result = dt_run.get_result_path(logger)

        logger.error.assert_called_once_with(
            "Mandatory env variable 'DOVETAIL_HOME' is not found, "
            "please set in env_config.sh and source this file before "
            "running.")
        self.assertEquals(None, result)

    @patch('dovetail.run.constants')
    @patch('dovetail.run.dt_cfg')
    @patch('dovetail.run.dt_utils')
    @patch('dovetail.run.os')
    def test_copy_userconfig_files(self, mock_os, mock_utils, mock_config,
                                   mock_constants):
        mock_config.dovetail_config = {'config_dir': 'value'}
        mock_os.path.isdir.return_value = False
        mock_constants.USERCONF_PATH = 'value'
        logger = Mock()

        dt_run.copy_userconfig_files(logger)

        mock_os.path.isdir.assert_called_once_with('value')
        mock_os.makedirs.assert_called_once_with('value')
        mock_utils.exec_cmd.assert_called_once_with(
            'sudo cp -r value/* value', logger, exit_on_error=False)

    @patch('dovetail.run.constants')
    @patch('dovetail.run.dt_cfg')
    @patch('dovetail.run.dt_utils')
    @patch('dovetail.run.os')
    def test_copy_patch_files(self, mock_os, mock_utils, mock_config,
                              mock_constants):
        mock_config.dovetail_config = {'patch_dir': 'value'}
        mock_os.path.isdir.return_value = False
        mock_constants.PATCH_PATH = 'value'
        logger = Mock()

        dt_run.copy_patch_files(logger)

        mock_os.path.isdir.assert_called_once_with('value')
        mock_os.makedirs.assert_called_once_with('value')
        mock_utils.exec_cmd.assert_called_once_with(
            'sudo cp -a -r value/* value', logger, exit_on_error=False)

    @patch('dovetail.run.dt_cfg')
    @patch('dovetail.run.dt_utils')
    @patch('dovetail.run.os')
    def test_env_init(self, mock_os, mock_utils, mock_config):
        mock_config.dovetail_config = {'config_dir': 'a', 'env_file': 'b'}
        join_path = 'join_path'
        mock_os.path.join.return_value = join_path
        mock_os.path.isfile.return_value = False
        logger = Mock()

        dt_run.env_init(logger)

        mock_os.path.join.assert_called_once_with('a', 'b')
        mock_os.path.isfile.assert_called_once_with(join_path)
        logger.error.assert_called_once_with(
            "File {} does not exist.".format(join_path))
        mock_utils.source_env.assert_called_once_with(join_path)

    @patch('dovetail.run.os')
    def test_update_deploy_scenario(self, mock_os):
        logger = Mock()
        mock_os.environ = {}

        dt_run.update_deploy_scenario(logger, deploy_scenario='a')

        logger.info.assert_called_once_with('DEPLOY_SCENARIO : %s', 'a')
        self.assertEquals({'DEPLOY_SCENARIO': 'a'}, mock_os.environ)

    @patch('dovetail.run.dt_cfg')
    @patch('dovetail.run.os.path')
    def test_check_hosts_file(self, mock_path, mock_config):
        mock_config.dovetail_config = {'config_dir': 'value'}
        hosts_file = 'h_file'
        mock_path.join.return_value = hosts_file
        mock_path.isfile.return_value = False
        logger = Mock()

        dt_run.check_hosts_file(logger)

        mock_path.join.assert_called_once_with('value', 'hosts.yaml')
        mock_path.isfile.assert_called_once_with(hosts_file)
        logger.warn.assert_called_once_with(
            'There is no hosts file {}, may be some issues with '
            'domain name resolution.'.format(hosts_file))

    @patch('dovetail.run.dt_cfg')
    @patch.object(dt_run, 'filter_config')
    def test_cli_no_validation(self, mock_filter, mock_config):
        mock_config.dovetail_config = {}
        logger = Mock()

        dt_run.parse_cli(logger=logger,
                         offline='a',
                         no_clean='b',
                         stop='c',
                         mandatory='d',
                         optional='e',
                         no_api_validation=True)
        expected_dict = {
            'offline': 'a',
            'noclean': 'b',
            'stop': 'c',
            'mandatory': 'd',
            'optional': 'e',
            'no_api_validation': True
        }

        logger.warning.assert_called_once_with(
            'Strict API response validation DISABLED.')
        self.assertEquals(expected_dict, mock_config.dovetail_config)

    @patch('dovetail.run.dt_cfg')
    @patch.object(dt_run, 'filter_config')
    def test_cli_with_validation(self, mock_filter, mock_config):
        mock_config.dovetail_config = {}

        dt_run.parse_cli(offline='a',
                         no_clean='b',
                         stop='c',
                         mandatory='d',
                         optional='e',
                         no_api_validation=False)
        expected_dict = {
            'offline': 'a',
            'noclean': 'b',
            'stop': 'c',
            'mandatory': 'd',
            'optional': 'e',
            'no_api_validation': False
        }

        self.assertEquals(expected_dict, mock_config.dovetail_config)

    def test_check_testcase_list_not_in_list(self):
        logger = Mock()

        result = dt_run.check_testcase_list(['testcase'], logger)

        logger.error.assert_called_once_with(
            'Test case testcase is not defined.')
        self.assertEquals(None, result)

    def test_check_testcase_list_none(self):
        logger = Mock()
        result = dt_run.check_testcase_list(None, logger)

        logger.error.assert_called_once_with(
            'There is no test case to be executed.')
        self.assertEquals(None, result)

    @patch('dovetail.run.dt_testcase.Testcase')
    def test_check_testcase_list(self, mock_testcase):
        testcase_list = ['testcase']
        mock_testcase.testcase_list = testcase_list

        result = dt_run.check_testcase_list(testcase_list)

        self.assertEquals(testcase_list, result)

    @patch('dovetail.run.dt_testcase.Testcase')
    @patch.object(dt_run, 'check_testcase_list')
    def test_get_testcase_list_check(self, mock_check, mock_testcase):
        testcase_list = ['testcase']
        mock_check.return_value = testcase_list

        result = dt_run.get_testcase_list(testcase=testcase_list)

        mock_check.assert_called_once_with(testcase_list, None)
        mock_testcase.load.assert_called_once_with()
        self.assertEquals(testcase_list, result)

    @patch('dovetail.run.dt_cfg')
    @patch('dovetail.run.dt_testcase.Testcase')
    @patch.object(dt_run, 'check_testcase_list')
    @patch.object(dt_run, 'load_testsuite')
    def test_get_testcase_list(self, mock_load, mock_check, mock_testcase,
                               mock_config):
        mock_config.dovetail_config = {'testsuite_supported': ['suite']}
        testcase_list = ['testcase']
        mock_testcase.check_testarea.return_value = (True, 'area')
        mock_load.return_value = 'testsuite_yaml'
        mock_testcase.get_testcases_for_testsuite.return_value = testcase_list
        mock_check.return_value = testcase_list

        result = dt_run.get_testcase_list(
            testcase=None, testsuite='suite', testarea='area')

        mock_testcase.load.assert_called_once_with()
        mock_testcase.check_testarea.assert_called_once_with('area')
        mock_load.assert_called_once_with('suite')
        mock_testcase.get_testcases_for_testsuite.assert_called_once_with(
            'testsuite_yaml', 'area')
        mock_check.assert_called_once_with(testcase_list, None)
        self.assertEquals(testcase_list, result)

    @patch('dovetail.run.dt_cfg')
    @patch('dovetail.run.dt_testcase.Testcase')
    def test_get_testcase_list_no_testsuite(self, mock_testcase, mock_config):
        logger = Mock()
        mock_config.dovetail_config = {'testsuite_supported': []}
        mock_testcase.check_testarea.return_value = (True, 'area')

        result = dt_run.get_testcase_list(
            logger, testcase=None, testsuite='suite', testarea='area')

        mock_testcase.load.assert_called_once_with()
        mock_testcase.check_testarea.assert_called_once_with('area')
        logger.error.assert_called_once_with(
            'Test suite suite is not defined.')
        self.assertEquals(None, result)

    @patch('dovetail.run.dt_cfg')
    @patch('dovetail.run.dt_testcase.Testcase')
    def test_get_testcase_list_no_testarea(self, mock_testcase, mock_config):
        logger = Mock()
        mock_config.dovetail_config = {'testsuite_supported': ['suite']}
        mock_testcase.check_testarea.return_value = (False, 'area')

        result = dt_run.get_testcase_list(
            logger, testcase=None, testsuite='suite', testarea='area')

        mock_testcase.load.assert_called_once_with()
        mock_testcase.check_testarea.assert_called_once_with('area')
        logger.error.assert_called_once_with(
            'Test area area is not defined.')
        self.assertEquals(None, result)

    @patch('dovetail.run.os')
    @patch('dovetail.run.uuid')
    @patch('dovetail.run.dt_logger')
    @patch('dovetail.run.dt_cfg')
    @patch('dovetail.run.dt_utils')
    @patch.object(dt_run, 'get_result_path')
    @patch.object(dt_run, 'clean_results_dir')
    @patch.object(dt_run, 'parse_cli')
    @patch.object(dt_run, 'update_deploy_scenario')
    @patch.object(dt_run, 'env_init')
    @patch.object(dt_run, 'copy_userconfig_files')
    @patch.object(dt_run, 'copy_patch_files')
    @patch.object(dt_run, 'check_hosts_file')
    @patch.object(dt_run, 'get_testcase_list')
    @patch.object(dt_run, 'run_test')
    @patch.object(dt_run, 'create_logs')
    def test_main(self, mock_create_logs, mock_run, mock_get_list, mock_check,
                  mock_copy_patch, mock_copy_userconf, mock_env_init,
                  mock_update, mock_parse, mock_clean, mock_get_result,
                  mock_utils, mock_config, mock_logger, mock_uuid, mock_os):
        mock_config.dovetail_config = {}
        mock_os.environ = {}
        logger_obj = Mock()
        logger_temp_obj = Mock()
        logger_temp_obj.getLogger.return_value = logger_obj
        mock_logger.Logger.return_value = logger_temp_obj
        mock_uuid.uuid1.return_value = 42
        mock_get_result.return_value = True
        testcase_list = ['testcase']
        mock_get_list.return_value = testcase_list
        kwargs_dict = {
            'debug': True,
            'report': True,
            'testsuite': 'testsuite',
            'docker_tag': '2.0.0'
        }

        with self.assertRaises(SystemExit) as cm:
            dt_run.main([
                '--testsuite=testsuite', '--debug', '--report', '2.0.0'])
        expected = cm.exception

        logger_temp_obj.getLogger.assert_called_once_with()
        mock_logger.Logger.assert_called_once_with('run')
        mock_uuid.uuid1.assert_called_once_with()
        self.assertEquals({'build_tag': 'daily-master-42'},
                          mock_config.dovetail_config)
        mock_get_result.assert_called_once_with(logger_obj)
        mock_clean.assert_called_once_with(logger_obj)
        self.assertEquals({'DEBUG': 'true'}, mock_os.environ)
        mock_create_logs.assert_called_once_with()
        logger_obj.info.assert_has_calls([
            call('================================================'),
            call('Dovetail compliance: testsuite!'),
            call('================================================'),
            call('Build tag: daily-master-42')])
        mock_parse.assert_called_once_with(logger_obj, **kwargs_dict)
        mock_update.assert_called_once_with(logger_obj, **kwargs_dict)
        mock_env_init.assert_called_once_with(logger_obj)
        mock_copy_userconf.assert_called_once_with(logger_obj)
        mock_copy_patch.assert_called_once_with(logger_obj)
        mock_utils.check_docker_version.assert_called_once_with(logger_obj)
        mock_utils.get_openstack_endpoint.assert_called_once_with(logger_obj)
        mock_check.assert_called_once_with(logger_obj)
        mock_utils.get_hardware_info.assert_called_once_with(logger_obj)
        mock_get_list.assert_called_once_with(logger_obj, **kwargs_dict)
        mock_run.assert_called_once_with(
            testcase_list, kwargs_dict['report'], logger_obj)
        self.assertEquals(expected.code, 0)

    @patch('dovetail.run.uuid')
    @patch('dovetail.run.dt_logger')
    @patch('dovetail.run.dt_cfg')
    @patch.object(dt_run, 'get_result_path')
    def test_main_no_results_path(self, mock_get_result, mock_config,
                                  mock_logger, mock_uuid):
        mock_config.dovetail_config = {}
        logger_obj = Mock()
        logger_temp_obj = Mock()
        logger_temp_obj.getLogger.return_value = logger_obj
        mock_logger.Logger.return_value = logger_temp_obj
        mock_uuid.uuid1.return_value = 42
        mock_get_result.return_value = False

        with self.assertRaises(SystemExit) as cm:
            dt_run.main(['2.0.0'])
        expected = cm.exception

        logger_temp_obj.getLogger.assert_called_once_with()
        mock_logger.Logger.assert_called_once_with('run')
        mock_uuid.uuid1.assert_called_once_with()
        self.assertEquals({'build_tag': 'daily-master-42'},
                          mock_config.dovetail_config)
        mock_get_result.assert_called_once_with(logger_obj)
        self.assertEquals(expected.code, 0)

    @patch('dovetail.run.os')
    @patch('dovetail.run.uuid')
    @patch('dovetail.run.dt_logger')
    @patch('dovetail.run.dt_cfg')
    @patch('dovetail.run.dt_utils')
    @patch.object(dt_run, 'get_result_path')
    @patch.object(dt_run, 'clean_results_dir')
    @patch.object(dt_run, 'parse_cli')
    @patch.object(dt_run, 'update_deploy_scenario')
    @patch.object(dt_run, 'env_init')
    @patch.object(dt_run, 'copy_userconfig_files')
    @patch.object(dt_run, 'copy_patch_files')
    @patch.object(dt_run, 'check_hosts_file')
    @patch.object(dt_run, 'get_testcase_list')
    @patch.object(dt_run, 'run_test')
    @patch.object(dt_run, 'create_logs')
    def test_main_no_testcaselist(self, mock_create_logs, mock_run,
                                  mock_get_list, mock_check, mock_copy_patch,
                                  mock_copy_userconf, mock_env_init,
                                  mock_update, mock_parse, mock_clean,
                                  mock_get_result, mock_utils, mock_config,
                                  mock_logger, mock_uuid, mock_os):
        mock_config.dovetail_config = {}
        mock_os.environ = {}
        logger_obj = Mock()
        logger_temp_obj = Mock()
        logger_temp_obj.getLogger.return_value = logger_obj
        mock_logger.Logger.return_value = logger_temp_obj
        mock_uuid.uuid1.return_value = 42
        mock_get_result.return_value = True
        mock_get_list.return_value = None
        kwargs_dict = {
            'debug': True,
            'report': True,
            'testsuite': 'testsuite',
            'docker_tag': '2.0.0'
        }

        with self.assertRaises(SystemExit) as cm:
            dt_run.main([
                '--testsuite=testsuite', '--debug', '--report', '2.0.0'])
        expected = cm.exception
        self.assertEquals(expected.code, 2)

        logger_temp_obj.getLogger.assert_called_once_with()
        mock_logger.Logger.assert_called_once_with('run')
        mock_uuid.uuid1.assert_called_once_with()
        self.assertEquals({'build_tag': 'daily-master-42'},
                          mock_config.dovetail_config)
        mock_get_result.assert_called_once_with(logger_obj)
        mock_clean.assert_called_once_with(logger_obj)
        self.assertEquals({'DEBUG': 'true'}, mock_os.environ)
        mock_create_logs.assert_called_once_with()
        logger_obj.info.assert_has_calls([
            call('================================================'),
            call('Dovetail compliance: testsuite!'),
            call('================================================'),
            call('Build tag: daily-master-42')])
        mock_parse.assert_called_once_with(logger_obj, **kwargs_dict)
        mock_update.assert_called_once_with(logger_obj, **kwargs_dict)
        mock_env_init.assert_called_once_with(logger_obj)
        mock_copy_userconf.assert_called_once_with(logger_obj)
        mock_copy_patch.assert_called_once_with(logger_obj)
        mock_utils.check_docker_version.assert_called_once_with(logger_obj)
        mock_utils.get_openstack_endpoint.assert_called_once_with(logger_obj)
        mock_check.assert_called_once_with(logger_obj)
        mock_utils.get_hardware_info.assert_called_once_with(logger_obj)
        mock_get_list.assert_called_once_with(logger_obj, **kwargs_dict)
