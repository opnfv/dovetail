#!/usr/bin/env python
#
# Copyright (c) 2018 mokats@intracom-telecom.com and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##

import io
import unittest
from mock import patch, call, Mock
import yaml

from dovetail import constants
from dovetail.cli.commands.cli_testcase import CliTestcase

__author__ = 'Stamatis Katsaounis <mokats@intracom-telecom.com>'


class CliTestcaseTesting(unittest.TestCase):

    @patch('os.path')
    @patch('os.pardir')
    @patch('dovetail.cli.commands.cli_testcase.dt_utils')
    def test_run(self, mock_utils, mock_pardir, mock_path):
        run_args = ('arga', 'argb')
        options = ' '.join(run_args)
        repo_dir = 'repo_dir'
        mock_path.abspath.return_value = repo_dir

        testcase = CliTestcase()
        testcase.run(options)

        mock_path.dirname.assert_called_once()
        cmd = 'python %s/run.py %s' % (repo_dir, options)
        mock_utils.exec_cmd.assert_called_once_with(
            cmd, exit_on_error=True, exec_msg_on=False, info=True)

    @patch('dovetail.cli.commands.cli_testcase.constants')
    @patch('os.path')
    @patch('dovetail.cli.commands.cli_testcase.click')
    def test_show_testcase_not_exist(self, mock_click, mock_path,
                                     mock_constants):
        testcase_name = 'name'
        testcase_path = 'path'
        mock_constants.TESTCASE_PATH = 'path'
        testcase_whole_path = '{}/{}.yaml'.format(testcase_name,
                                                  testcase_path)
        mock_path.join.return_value = testcase_whole_path
        mock_path.isfile.return_value = False

        testcase = CliTestcase()
        testcase.show_testcase(testcase_name)

        mock_path.join.assert_called_once_with(
            testcase_path, '{}.yml'.format(testcase_name))
        mock_path.isfile.assert_called_once_with(testcase_whole_path)
        mock_click.echo.assert_called_once_with(
            'testcase %s not exist or not supported' % testcase_name)

    @patch('__builtin__.open')
    @patch('dovetail.cli.commands.cli_testcase.constants')
    @patch('os.path')
    @patch('dovetail.cli.commands.cli_testcase.click')
    def test_show_testcase(self, mock_click, mock_path, mock_constants,
                           mock_open):
        testcase_name = 'name'
        testcase_path = 'path'
        mock_constants.TESTCASE_PATH = 'path'
        testcase_whole_path = '{}/{}.yaml'.format(testcase_name,
                                                  testcase_path)
        mock_path.join.return_value = testcase_whole_path
        mock_path.isfile.return_value = True
        file_data = u'file data'
        mock_open.return_value.__enter__.return_value = io.StringIO(file_data)

        testcase = CliTestcase()
        testcase.show_testcase(testcase_name)

        mock_open.assert_called_once_with(testcase_whole_path, 'r')
        mock_path.join.assert_called_once_with(
            testcase_path, '{}.yml'.format(testcase_name))
        mock_path.isfile.assert_called_once_with(testcase_whole_path)
        mock_click.echo.assert_called_once_with(file_data)

    @patch('__builtin__.open')
    @patch('dovetail.cli.commands.cli_testcase.constants')
    @patch('os.path')
    @patch('dovetail.cli.commands.cli_testcase.click')
    def test_show_testcase_exception(self, mock_click, mock_path,
                                     mock_constants, mock_open):
        testcase_name = 'name'
        testcase_path = 'path'
        mock_constants.TESTCASE_PATH = 'path'
        testcase_whole_path = '{}/{}.yaml'.format(testcase_name,
                                                  testcase_path)
        mock_path.join.return_value = testcase_whole_path
        mock_path.isfile.return_value = True
        file_obj = Mock()
        mock_open.return_value.__enter__.return_value = file_obj
        exception = yaml.YAMLError()
        file_obj.read.side_effect = exception

        testcase = CliTestcase()
        testcase.show_testcase(testcase_name)

        mock_open.assert_called_once_with(testcase_whole_path, 'r')
        mock_path.join.assert_called_once_with(
            testcase_path, '{}.yml'.format(testcase_name))
        mock_path.isfile.assert_called_once_with(testcase_whole_path)
        mock_click.echo.assert_called_once_with(exception)

    @patch.object(CliTestcase, 'testsuite_load')
    @patch.object(CliTestcase, 'list_one_testsuite')
    def test_list_suites_single(self, mock_list_one, mock_load):
        testsuite = 'suite'

        testcase = CliTestcase()
        testcase.list_testsuites(testsuite)

        mock_load.assert_called_once_with()
        mock_list_one.assert_called_once_with(testsuite)

    @patch.object(CliTestcase, 'testsuite_load')
    @patch('dovetail.cli.commands.cli_testcase.click')
    @patch('dovetail.testcase.Testsuite.get_all')
    def test_list_suites_no_suites(self, mock_get_all, mock_click, mock_load):
        testsuite = None
        mock_get_all.return_value = None

        testcase = CliTestcase()
        testcase.list_testsuites(testsuite)

        mock_load.assert_called_once_with()
        mock_get_all.assert_called_once_with()
        mock_click.echo.assert_called_once_with(
            'No testsuite defined yet in dovetail!!!')

    @patch.object(CliTestcase, 'testsuite_load')
    @patch.object(CliTestcase, 'list_one_testsuite')
    @patch('dovetail.cli.commands.cli_testcase.click')
    @patch('dovetail.testcase.Testsuite.get_all')
    def test_list_suites_many(self, mock_get_all, mock_click, mock_list_one,
                              mock_load):
        testsuite = None
        suite_name = 'suite'
        mock_get_all.return_value = {suite_name: 'A'}

        testcase = CliTestcase()
        testcase.list_testsuites(testsuite)

        mock_load.assert_called_once_with()
        mock_get_all.assert_called_once_with()
        mock_click.echo.assert_has_calls([
            call('--------------------------'),
            call('Test Suite {}'.format(suite_name)),
            call('--------------------------')])
        mock_list_one.assert_called_once_with(suite_name)

    @patch('dovetail.cli.commands.cli_testcase.click')
    @patch('dovetail.testcase.Testsuite.get')
    def test_list_one_testsuite_not_exist(self, mock_get, mock_click):
        testsuite = 'suite'
        mock_get.return_value = None

        testcase = CliTestcase()
        testcase.list_one_testsuite(testsuite)

        mock_get.assert_called_once_with(testsuite)
        mock_click.echo.assert_called_once_with(
            'testsuite {} does not exist'.format(testsuite))

    @patch('dovetail.cli.commands.cli_testcase.click')
    @patch('dovetail.testcase.Testsuite.get')
    @patch('dovetail.cli.commands.cli_testcase.dt_utils')
    def test_list_one_testsuite(self, mock_utils, mock_get, mock_click):
        testsuite = 'suite'
        testsuite_obj = Mock()
        mock_get.return_value = testsuite_obj
        testcase_a = 'testcaseA'
        testcase_b = 'testcaseB'
        mock_utils.get_value_from_dict.side_effect = [
            [testcase_a], [testcase_b]]

        testcase = CliTestcase()
        testcase.list_one_testsuite(testsuite)

        mock_get.assert_called_once_with(testsuite)
        mock_utils.get_value_from_dict.assert_has_calls([
            call('testcases_list.mandatory', testsuite_obj),
            call('testcases_list.optional', testsuite_obj)])
        mock_click.echo.assert_has_calls([
            call('- mandatory'),
            call('    {}'.format(testcase_a)),
            call('- optional'),
            call('    {}'.format(testcase_b))])

    @patch('dovetail.cli.commands.cli_testcase.click')
    @patch('dovetail.testcase.Testsuite.get')
    @patch('dovetail.cli.commands.cli_testcase.dt_utils')
    def test_list_one_testsuite_no_testcases(self, mock_utils, mock_get,
                                             mock_click):
        testsuite = 'suite'
        testsuite_obj = Mock()
        mock_get.return_value = testsuite_obj
        mock_utils.get_value_from_dict.return_value = []

        testcase = CliTestcase()
        testcase.list_one_testsuite(testsuite)

        mock_get.assert_called_once_with(testsuite)
        mock_utils.get_value_from_dict.assert_has_calls([
            call('testcases_list.mandatory', testsuite_obj),
            call('testcases_list.optional', testsuite_obj)])
        mock_click.echo.assert_called_once_with(
            'No testcase in testsuite {}'.format(testsuite))

    @patch('dovetail.cli.commands.cli_testcase.dt_cfg')
    @patch('dovetail.testcase.Testsuite.load')
    @patch.object(constants, 'CONF_PATH')
    def test_testsuite_load(self, mock_path, mock_load, mock_config):
        testcase = CliTestcase()
        testcase.testsuite_load()

        mock_config.load_config_files.assert_called_once_with(mock_path)
        mock_load.assert_called_once_with()
