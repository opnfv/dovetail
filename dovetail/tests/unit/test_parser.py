#!/usr/bin/env python
#
##############################################################################
# Copyright (c) 2016 lingui.zeng@huawei.com and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
#
"""
Test 'parser' module

"""

import logging
import os
import unittest
import yaml
import mock

from dovetail import parser
from dovetail.utils.dovetail_config import DovetailConfig as dt_cfg


@mock.patch('dovetail.parser.Parser.logger')
class TestParser(unittest.TestCase):

    test_path = os.path.dirname(os.path.realpath(__file__))

    def setUp(self):
        """Test case setup"""
        conf_path = os.path.join(self.test_path,
                                 os.pardir, os.pardir, os.pardir,
                                 'etc/conf')
        dt_cfg.load_config_files(conf_path)
        logging.disable(logging.CRITICAL)

    def test_parser_cmd(self, mock_logger):
        """Test whether the command is correctly parsed."""
        mock_cmd = "python /functest/ci/run_tests.py "\
                   "-t {{validate_testcase}} -r"
        with open(os.path.join(self.test_path, 'test_testcase.yaml')) as f:
            mock_testcase_yaml = yaml.safe_load(f)
        MockTestcase = type('Testcase', (object,), {})
        mock_testcase = MockTestcase()
        mock_testcase.testcase = mock_testcase_yaml.values()[0]
        output = parser.Parser.parse_cmd(mock_cmd, mock_testcase)
        expected_output = ("python /functest/ci/run_tests.py -t "
                           "tempest_smoke_serial -r")
        self.assertEqual(expected_output, output)

    def test_parser_cmd_fail(self, mock_logger):
        """Test whether the command is correctly parsed."""
        mock_cmd = "python /functest/ci/run_tests.py "\
                   "-t {{validate_testcase}} -r"
        mock_testcase_yaml = {}
        MockTestcase = type('Testcase', (object,), {})
        mock_testcase = MockTestcase()
        mock_testcase.testcase = mock_testcase_yaml.values()
        output = parser.Parser.parse_cmd(mock_cmd, mock_testcase)
        expected_output = ("python /functest/ci/run_tests.py -t "
                           "None -r")
        self.assertEqual(expected_output, output)

    @mock.patch('dovetail.parser.jinja2')
    def test_parse_cmd_exception(self, mock_jinja, mock_logger):
        errorMSG = 'Exception was raised'
        exception = Exception(errorMSG)
        command = 'cmd'
        undefined_obj = mock.Mock()
        mock_jinja.StrictUndefined = undefined_obj
        mock_jinja.Template.side_effect = exception

        expected = None
        dovetail_parser = parser.Parser()
        exception_obj = mock.Mock()
        dovetail_parser.logger.exception = exception_obj
        result = dovetail_parser.parse_cmd(command, 'testcase')

        mock_jinja.Template.assert_called_once_with(command,
                                                    undefined=undefined_obj)
        exception_obj.assert_called_once_with(
            'Failed to parse cmd {}, exception: {}'.format(command, errorMSG))
        self.assertEqual(expected, result)

    @mock.patch('dovetail.parser.dt_logger.Logger')
    def test_create_log(self, mock_dt_logger, mock_logger):
        mock_dt_logger_obj = mock.Mock()
        logger_obj = mock.Mock()
        mock_dt_logger_obj.getLogger.return_value = logger_obj
        mock_dt_logger.return_value = mock_dt_logger_obj

        dovetail_parser = parser.Parser()
        dovetail_parser.create_log()

        mock_dt_logger.assert_called_once_with('dovetail.parser.Parser')
        mock_dt_logger_obj.getLogger.assert_called_once_with()
        self.assertEqual(dovetail_parser.logger, logger_obj)
