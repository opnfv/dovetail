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

import dovetail.testcase as tcase

__author__ = 'Stamatis Katsaounis <mokats@intracom-telecom.com>'


class TestcaseTesting(unittest.TestCase):

    def setUp(self):
        test_path = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(test_path, 'test_testcase.yaml')) as f:
            self.testcase_yaml = yaml.safe_load(f)

    def tearDown(self):
        pass

    def teardown_method(self, method):
        tcase.Testcase.logger = None
        tcase.Testcase.validate_testcase_list = {}
        tcase.Testcase.testcase_list = {}
        tcase.Testsuite.testsuite_list = {}

    @patch('dovetail.testcase.dt_logger')
    def test_create_log(self, mock_logger):
        getlogger_obj = Mock()
        logger_obj = Mock()
        logger_obj.getLogger.return_value = getlogger_obj
        mock_logger.Logger.return_value = logger_obj

        tcase.Testcase.create_log()

        self.assertEquals(getlogger_obj, tcase.Testcase.logger)

    @patch('dovetail.testcase.Parser')
    def test_parse_cmd_no_lines(self, mock_parser):
        testcase = tcase.YardstickTestcase(self.testcase_yaml)
        cmds_list = ['cmd']
        mock_parser.parse_cmd.return_value = None

        result = testcase.parse_cmd(cmds_list)

        mock_parser.parse_cmd.assert_called_once_with(
            'cmd', testcase)
        self.assertEquals(False, result)

    @patch('dovetail.testcase.Parser')
    def test_parse_cmd(self, mock_parser):
        testcase = tcase.BottlenecksTestcase(self.testcase_yaml)
        logger_obj = Mock()
        testcase.logger = logger_obj
        cmds_list = ['cmd']
        mock_parser.parse_cmd.return_value = 'cmd_lines'

        result = testcase.parse_cmd(cmds_list)

        mock_parser.parse_cmd.assert_called_once_with(
            'cmd', testcase)
        logger_obj.debug.assert_called_once_with("cmds: ['cmd_lines']")
        self.assertEquals(['cmd_lines'], testcase.cmds)
        self.assertEquals(True, result)

    @patch('dovetail.testcase.dt_cfg')
    def test_prepare_cmd_no_cmds(self, mock_config):
        testcase = tcase.ShellTestcase(self.testcase_yaml)
        logger_obj = Mock()
        testcase.logger = logger_obj
        mock_config.dovetail_config = {}

        result = testcase.prepare_cmd('type')

        logger_obj.error.assert_called_once_with(
            'Test case {} has no cmds.'.format(testcase.name()))
        self.assertEquals(False, result)

    @patch('dovetail.testcase.dt_cfg')
    @patch.object(tcase.Testcase, 'parse_cmd')
    def test_prepare_cmd_testcase_cmd(self, mock_parse, mock_config):
        testcase = tcase.VnftestTestcase(self.testcase_yaml)
        testcase.testcase['validate']['cmds'] = ['cmd']
        mock_config.dovetail_config = {}
        mock_parse.return_value = True

        result = testcase.prepare_cmd('type')

        mock_parse.assert_called_once_with(['cmd'])
        self.assertEquals(True, result)

    @patch('dovetail.testcase.dt_cfg')
    @patch.object(tcase.Testcase, 'parse_cmd')
    def test_prepare_cmd_config_cmd(self, mock_parse, mock_config):
        testcase = tcase.TestcaseFactory.create('yardstick',
                                                self.testcase_yaml)
        mock_config.dovetail_config = {'type': {'cmds': ['cmd']}}
        mock_parse.return_value = True

        result = testcase.prepare_cmd('type')

        mock_parse.assert_called_once_with(['cmd'])
        self.assertEquals(True, result)

    def test_str(self):
        testcase = tcase.Testcase(self.testcase_yaml)

        result = testcase.__str__()

        self.assertEquals(testcase.testcase, result)

    def test_objective(self):
        testcase = tcase.Testcase(self.testcase_yaml)
        testcase.testcase['objective'] = 'objective'

        result = testcase.objective()

        self.assertEquals('objective', result)

    @patch('dovetail.testcase.dt_utils')
    def test_sub_testcase(self, mock_utils):
        testcase = tcase.Testcase(self.testcase_yaml)
        mock_utils.get_value_from_dict.return_value = 'value'

        result = testcase.sub_testcase()

        mock_utils.get_value_from_dict.assert_called_once_with(
            'report.sub_testcase_list', testcase.testcase)
        self.assertEquals('value', result)

    def test_sub_testcase_passed(self):
        testcase = tcase.Testcase(self.testcase_yaml)
        logger_obj = Mock()
        testcase.logger = logger_obj

        result = testcase.sub_testcase_passed('name', 'passed')

        logger_obj.debug.assert_called_once_with(
            'sub_testcase_passed: name passed')
        self.assertEquals('passed', result)

    def test_validate_type(self):
        testcase = tcase.Testcase(self.testcase_yaml)

        result = testcase.validate_type()

        self.assertEquals('functest', result)

    def test_validate_testcase(self):
        testcase = tcase.Testcase(self.testcase_yaml)

        result = testcase.validate_testcase()

        self.assertEquals('tempest_smoke_serial', result)

    def test_passed(self):
        testcase = tcase.Testcase(self.testcase_yaml)

        result = testcase.passed('passed')

        self.assertEquals('passed', result)

    def test_set_get_results(self):
        testcase = tcase.Testcase(self.testcase_yaml)

        testcase.set_results('results')

        self.assertEquals('results', testcase.get_results())

    def test_pre_condition_exists(self):
        testcase = tcase.Testcase(self.testcase_yaml)
        testcase.testcase['validate']['pre_condition'] = 'pre_condition'

        result = testcase.pre_condition()

        self.assertEquals('pre_condition', result)

    @patch.object(tcase.Testcase, 'pre_condition_cls')
    def test_pre_condition_not_exists(self, mock_pre_condition):
        testcase = tcase.Testcase(self.testcase_yaml)
        logger_obj = Mock()
        testcase.logger = logger_obj
        mock_pre_condition.return_value = False

        result = testcase.pre_condition()

        mock_pre_condition.assert_called_once_with('functest')
        logger_obj.debug.assert_called_once_with(
            'Test case: {} pre_condition is empty.'.format(testcase.name()))
        self.assertEquals(False, result)

    def test_pre_copy_path(self):
        testcase = tcase.Testcase(self.testcase_yaml)
        testcase.testcase['validate']['pre_copy'] = {'key': 'value'}

        result = testcase.pre_copy_path('key')

        self.assertEquals('value', result)

    def test_pre_copy_path_error(self):
        testcase = tcase.Testcase(self.testcase_yaml)

        result = testcase.pre_copy_path('key')

        self.assertEquals(None, result)

    def test_post_condition_exists(self):
        testcase = tcase.Testcase(self.testcase_yaml)
        testcase.testcase['validate']['post_condition'] = 'post_condition'

        result = testcase.post_condition()

        self.assertEquals('post_condition', result)

    @patch.object(tcase.Testcase, 'post_condition_cls')
    def test_post_condition_not_exists(self, mock_post_condition):
        testcase = tcase.Testcase(self.testcase_yaml)
        logger_obj = Mock()
        testcase.logger = logger_obj
        mock_post_condition.return_value = False

        result = testcase.post_condition()

        mock_post_condition.assert_called_once_with('functest')
        logger_obj.debug.assert_called_once_with(
            'Test case: {} post_condition is empty.'.format(testcase.name()))
        self.assertEquals(False, result)

    @patch('__builtin__.open')
    @patch('dovetail.testcase.os.path')
    @patch('dovetail.testcase.dt_cfg')
    @patch.object(tcase.Testcase, 'sub_testcase')
    def test_mk_src_file(self, mock_sub_testcase, mock_config,
                         mock_path, mock_open):
        testcase = tcase.Testcase(self.testcase_yaml)
        logger_obj = Mock()
        testcase.logger = logger_obj
        mock_config.dovetail_config = {'result_dir': 'value'}
        sub_test = 'sub_test'
        file_path = 'file_path'
        mock_path.join.return_value = file_path
        mock_sub_testcase.return_value = [sub_test]
        file_obj = Mock()
        mock_open.return_value.__enter__.return_value = file_obj

        result = testcase.mk_src_file()

        mock_path.join.assert_called_once_with('value', 'tempest_custom.txt')
        mock_open.assert_called_once_with(file_path, 'w+')
        file_obj.write.assert_called_once_with(sub_test + '\n')
        logger_obj.debug.assert_has_calls([
            call('Save test cases {}'.format(sub_test)),
            call('Save test cases to {}'.format(file_path))])
        self.assertEquals(file_path, result)

    @patch('__builtin__.open')
    @patch('dovetail.testcase.os.path')
    @patch('dovetail.testcase.dt_cfg')
    @patch.object(tcase.Testcase, 'sub_testcase')
    def test_mk_src_file_exception(self, mock_sub_testcase,
                                   mock_config, mock_path, mock_open):
        testcase = tcase.Testcase(self.testcase_yaml)
        logger_obj = Mock()
        testcase.logger = logger_obj
        mock_config.dovetail_config = {'result_dir': 'value'}
        sub_test = 'sub_test'
        file_path = 'file_path'
        mock_path.join.return_value = file_path
        mock_sub_testcase.return_value = [sub_test]
        mock_open.return_value.__enter__.side_effect = Exception()

        result = testcase.mk_src_file()

        mock_path.join.assert_called_once_with('value', 'tempest_custom.txt')
        mock_open.assert_called_once_with(file_path, 'w+')
        logger_obj.exception('Failed to save: {}'.format(file_path))
        self.assertEquals(None, result)

    @patch('dovetail.testcase.TestRunnerFactory')
    def test_run(self, mock_factory):
        testcase = tcase.Testcase(self.testcase_yaml)
        logger_obj = Mock()
        testcase.logger = logger_obj
        runner_obj = Mock()
        mock_factory.create.return_value = runner_obj
        error_msg = 'An error happened!'
        runner_obj.archive_logs.side_effect = AttributeError(error_msg)

        testcase.run()

        runner_obj.run.assert_called_once_with()
        runner_obj.archive_logs.assert_called_once_with()
        logger_obj.exception.assert_called_once_with(
            'Test case: {} Exception: {}'.format(testcase.name, error_msg))

    @patch('dovetail.testcase.dt_cfg')
    def test_pre_condition_cls(self, mock_config):
        mock_config.dovetail_config = {'type': {'pre_condition': 'value'}}

        result = tcase.Testcase.pre_condition_cls('type')
        self.assertEquals('value', result)

    @patch('dovetail.testcase.dt_cfg')
    def test_pre_condition_cls_key_error(self, mock_config):
        mock_config.dovetail_config = {}

        result = tcase.Testcase.pre_condition_cls('type')
        self.assertEquals(None, result)

    @patch('dovetail.testcase.dt_cfg')
    def test_post_condition_cls(self, mock_config):
        mock_config.dovetail_config = {'type': {'post_condition': 'value'}}

        result = tcase.Testcase.post_condition_cls('type')
        self.assertEquals('value', result)

    @patch('dovetail.testcase.dt_cfg')
    def test_post_condition_cls_key_error(self, mock_config):
        mock_config.dovetail_config = {}

        result = tcase.Testcase.post_condition_cls('type')
        self.assertEquals(None, result)

    def test_increase_retry(self):
        testcase = tcase.Testcase(self.testcase_yaml)
        tcase.Testcase.validate_testcase_list[
            'tempest_smoke_serial'] = {'retry': 0}

        for _ in range(0, 42):
            result = testcase.increase_retry()
        self.assertEquals(42, result)

    @patch('__builtin__.open')
    @patch('dovetail.testcase.yaml')
    @patch('dovetail.testcase.os')
    @patch('dovetail.testcase.TestcaseFactory')
    @patch('dovetail.testcase.constants')
    def test_load(self, mock_constants, mock_factory, mock_os, mock_yaml,
                  mock_open):
        testcase = tcase.Testcase(self.testcase_yaml)
        mock_constants.TESTCASE_PATH = 'abs_path'
        mock_os.walk.return_value = [('root', ['dir'], ['file'])]
        mock_os.path.join.return_value = 'testcase_path'
        file_obj = Mock()
        mock_open.return_value.__enter__.return_value = file_obj
        yaml_dict = {'key': {'validate': {'type': 'value'}}}
        mock_yaml.safe_load.return_value = yaml_dict
        runner_obj = Mock()
        mock_factory.create.return_value = runner_obj

        testcase.load()

        mock_os.walk.assert_called_once_with('abs_path')
        mock_os.path.join.assert_called_with('root', 'file')
        mock_open.assert_called_once_with('testcase_path')
        mock_yaml.safe_load.assert_called_once_with(file_obj)
        mock_factory.create.assert_called_once_with('value', yaml_dict)
        self.assertEquals(runner_obj, tcase.Testcase.get('key'))

    @patch('__builtin__.open')
    @patch('dovetail.testcase.yaml')
    @patch('dovetail.testcase.os')
    @patch('dovetail.testcase.TestcaseFactory')
    @patch('dovetail.testcase.constants')
    def test_load_no_testcase(self, mock_constants, mock_factory, mock_os,
                              mock_yaml, mock_open):
        logger_obj = Mock()
        tcase.Testcase.logger = logger_obj
        mock_constants.TESTCASE_PATH = 'abs_path'
        mock_os.walk.return_value = [('root', ['dir'], ['file'])]
        mock_os.path.join.return_value = 'testcase_path'
        file_obj = Mock()
        mock_open.return_value.__enter__.return_value = file_obj
        yaml_dict = {'key': {'validate': {'type': 'value'}}}
        mock_yaml.safe_load.return_value = yaml_dict
        mock_factory.create.return_value = None

        tcase.Testcase.load()

        mock_os.walk.assert_called_once_with('abs_path')
        mock_os.path.join.assert_called_with('root', 'file')
        mock_open.assert_called_once_with('testcase_path')
        mock_yaml.safe_load.assert_called_once_with(file_obj)
        mock_factory.create.assert_called_once_with('value', yaml_dict)
        logger_obj.error.assert_called_once_with(
            'Failed to create test case: file')

    def test_get_none(self):
        self.assertEquals(None, tcase.Testcase.get('unknown'))

    def test_check_testarea_none(self):
        self.assertEquals((True, ['full']),
                          tcase.Testcase.check_testarea(None))

    @patch('dovetail.testcase.dt_cfg')
    def test_check_testarea_full(self, mock_config):
        self.assertEquals((True, ['full']),
                          tcase.Testcase.check_testarea(['full']))

    @patch('dovetail.testcase.dt_cfg')
    def test_check_testarea(self, mock_config):
        self.assertEquals((True, ['area']),
                          tcase.Testcase.check_testarea(['area']))

    def test_check_testcase_area(self):
        self.assertEquals(False,
                          tcase.Testcase.check_testcase_area(None, None))

    def test_check_testcase_area_full_or_in_testcase(self):
        self.assertEquals(True,
                          tcase.Testcase.check_testcase_area(['full'], 'full'))

    def test_check_testcase_area_not_in_testcase_or_full(self):
        self.assertEquals(False,
                          tcase.Testcase.check_testcase_area(['full'], 'half'))

    @patch('dovetail.testcase.dt_utils')
    def test_get_testcases_for_testsuite_no_testcases(self, mock_utils):
        mock_utils.get_value_from_dict.return_value = None

        result = tcase.Testcase.get_testcases_for_testsuite('suite', 'area')

        mock_utils.get_value_from_dict.assert_has_calls([
            call('testcases_list', 'suite'),
            call('mandatory', None),
            call('optional', None)])
        self.assertEquals([], result)

    @patch('dovetail.testcase.dt_cfg')
    @patch('dovetail.testcase.dt_utils')
    def test_get_testcases_for_testsuite_no_selected_testcases(self,
                                                               mock_utils,
                                                               mock_config):
        logger_obj = Mock()
        tcase.Testcase.logger = logger_obj
        testcases_obj = Mock()
        mock_utils.get_value_from_dict.side_effect = [
            testcases_obj, None, None]
        mock_config.dovetail_config = {
            'mandatory': True,
            'optional': True
        }
        testsuite = {'name': 'test_name'}

        result = tcase.Testcase.get_testcases_for_testsuite(testsuite, 'area')

        mock_utils.get_value_from_dict.assert_has_calls([
            call('testcases_list', testsuite),
            call('mandatory', testcases_obj),
            call('optional', testcases_obj)])
        logger_obj.error.assert_has_calls([
            call('There is no mandatory test case in test suite {}'
                 .format(testsuite['name'])),
            call('There is no optional test case in test suite {}'
                 .format(testsuite['name']))])
        self.assertEquals(None, result)

    @patch('dovetail.testcase.dt_cfg')
    @patch('dovetail.testcase.dt_utils')
    @patch.object(tcase.Testcase, 'check_testcase_area')
    def test_get_testcases_for_testsuite(self, mock_check, mock_utils,
                                         mock_config):
        logger_obj = Mock()
        tcase.Testcase.logger = logger_obj
        testcases_obj = Mock()
        mock_utils.get_value_from_dict.side_effect = [
            testcases_obj, ['mandatory'], ['optional']]
        mock_config.dovetail_config = {
            'mandatory': True,
            'optional': True
        }
        mock_check.return_value = True
        testsuite = {'name': 'test_name'}
        testarea = ['area']

        mandatory_obj = Mock()
        tcase.Testcase.testcase_list['mandatory'] = mandatory_obj
        optional_obj = Mock()
        tcase.Testcase.testcase_list['optional'] = optional_obj
        result = tcase.Testcase.get_testcases_for_testsuite(
            testsuite, testarea)

        mock_utils.get_value_from_dict.assert_has_calls([
            call('testcases_list', testsuite),
            call('mandatory', testcases_obj),
            call('optional', testcases_obj)])
        mock_check.assert_has_calls([
            call('mandatory', 'area'),
            call('optional', 'area')])
        self.assertEquals(['mandatory', 'optional'], result)
        self.assertEquals(
            True, tcase.Testcase.testcase_list['mandatory'].is_mandatory)
        self.assertEquals(
            False, tcase.Testcase.testcase_list['optional'].is_mandatory)

    @patch('dovetail.testcase.dt_cfg')
    @patch('dovetail.testcase.dt_utils')
    @patch.object(tcase.Testcase, 'check_testcase_area')
    def test_get_testcases_for_testsuite_no_conf(self, mock_check, mock_utils,
                                                 mock_config):
        logger_obj = Mock()
        tcase.Testcase.logger = logger_obj
        testcases_obj = Mock()
        mock_utils.get_value_from_dict.side_effect = [
            testcases_obj, ['mandatory'], ['optional']]
        mock_config.dovetail_config = {
            'mandatory': False,
            'optional': False
        }
        mock_check.return_value = True
        testsuite = {'name': 'test_name'}
        testarea = ['area']

        mandatory_obj = Mock()
        tcase.Testcase.testcase_list['mandatory'] = mandatory_obj
        optional_obj = Mock()
        tcase.Testcase.testcase_list['optional'] = optional_obj
        result = tcase.Testcase.get_testcases_for_testsuite(testsuite,
                                                            testarea)

        mock_utils.get_value_from_dict.assert_has_calls([
            call('testcases_list', testsuite),
            call('mandatory', testcases_obj),
            call('optional', testcases_obj)])
        mock_check.assert_has_calls([
            call('mandatory', 'area'),
            call('optional', 'area')])
        self.assertEquals(['mandatory', 'optional'], result)
        self.assertEquals(True,
                          tcase.Testcase.testcase_list['mandatory']
                          .is_mandatory)
        self.assertEquals(False,
                          tcase.Testcase.testcase_list['optional']
                          .is_mandatory)

    @patch.object(tcase.Testcase, 'prepare_cmd')
    def test_functest_case_prepare_cmd_false(self, mock_prepare):
        testcase = tcase.FunctestTestcase(self.testcase_yaml)
        mock_prepare.return_value = False

        result = testcase.prepare_cmd('type')

        mock_prepare.assert_called_once_with('type')
        self.assertEquals(False, result)

    @patch('dovetail.testcase.os.path')
    @patch('dovetail.testcase.dt_cfg')
    @patch.object(tcase.Testcase, 'prepare_cmd')
    def test_functest_case_prepare_cmd(self, mock_prepare, mock_config,
                                       mock_path):
        testcase = tcase.FunctestTestcase(self.testcase_yaml)
        logger_obj = Mock()
        testcase.logger = logger_obj
        mock_prepare.return_value = True
        mock_config.dovetail_config = {
            'no_api_validation': True,
            'functest': {'patches_dir': 'value'}}
        mock_path.join.return_value = 'patch_cmd'

        result = testcase.prepare_cmd('type')

        mock_path.join.assert_called_once_with(
            'value', 'functest', 'disable-api-validation', 'apply.sh')
        logger_obj.debug.assert_called_once_with(
            'Updated list of commands for test run with '
            'disabled API response validation: {}'
            .format(testcase.cmds))
        self.assertEquals(['patch_cmd'], testcase.cmds)
        self.assertEquals(True, result)

    def test_testfactory_error(self):
        self.assertEquals(None,
                          tcase.TestcaseFactory.create('unknown',
                                                       self.testcase_yaml))

    def test_testfactory_k8s(self):
        k8s_testcase = tcase.TestcaseFactory.create('functest-k8s',
                                                    self.testcase_yaml)
        self.assertEquals('functest-k8s', k8s_testcase.type)

    @patch('dovetail.testcase.dt_logger')
    def test_testsuite_create_log(self, mock_logger):
        getlogger_obj = Mock()
        logger_obj = Mock()
        logger_obj.getLogger.return_value = getlogger_obj
        mock_logger.Logger.return_value = logger_obj

        tcase.Testsuite.create_log()

        self.assertEquals(getlogger_obj, tcase.Testsuite.logger)

    def test_testsuite_get_test(self):
        suite = tcase.Testsuite('suite')
        suite.testcase_list['testcase'] = 'value'

        result = suite.get_test('testcase')

        self.assertEquals('value', result)

    def test_testsuite_get_test_not_exists(self):
        suite = tcase.Testsuite('suite')

        result = suite.get_test('testcase')

        self.assertEquals(None, result)

    @patch('__builtin__.open')
    @patch('dovetail.testcase.yaml')
    @patch('dovetail.testcase.os')
    @patch('dovetail.testcase.constants')
    def test_testsuite_load(self, mock_constants, mock_os, mock_yaml,
                            mock_open):
        mock_constants.COMPLIANCE_PATH = 'abs_path'
        mock_os.walk.return_value = [('root', ['dir'], ['file'])]
        mock_os.path.join.return_value = 'file_path'
        mock_yaml.safe_load.return_value = {'testsuite': 'value'}
        file_obj = Mock()
        mock_open.return_value.__enter__.return_value = file_obj

        tcase.Testsuite.load()

        mock_os.walk.assert_called_once_with('abs_path')
        mock_os.path.join.assert_called_with('root', 'file')
        mock_open.assert_called_once_with('file_path')
        mock_yaml.safe_load.assert_called_once_with(file_obj)
        self.assertEquals({'testsuite': 'value'},
                          tcase.Testsuite.testsuite_list)

    def test_testsuite_get_none(self):
        self.assertEquals(None, tcase.Testsuite.get('unknown'))

    def test_testsuite_get(self):
        tcase.Testsuite.testsuite_list.update({'key': 'value'})
        self.assertEquals('value', tcase.Testsuite.get('key'))

    def test_testsuite_get_all(self):
        tcase.Testsuite.testsuite_list.update({'key': 'value'})
        self.assertEquals({'key': 'value'}, tcase.Testsuite.get_all())
