#!/usr/bin/env python
#
# lingui.zeng@huawei.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#
"""
Test 'parser' module

"""

import logging
import os
import unittest

import yaml

import parser as dovetail_parser


class TestParser(unittest.TestCase):

    test_path = os.path.dirname(os.path.realpath(__file__))

    def setUp(self):
        """Test case setup"""
        logging.disable(logging.CRITICAL)
        dovetail_parser.Parser.create_log()

    def test_parser_cmd(self):
        """Test whether the command is correctly parsed."""
        mock_cmd = "python /functest/ci/run_tests.py -t {{script_testcase}} -r"
        with open(os.path.join(self.test_path, 'test_testcase.yaml')) as f:
            mock_testcase_yaml = yaml.safe_load(f)
        MockTestcase = type('Testcase', (object,), {})
        mock_testcase = MockTestcase()
        mock_testcase.testcase = mock_testcase_yaml.values()[0]
        output = dovetail_parser.Parser.parse_cmd(mock_cmd, mock_testcase)
        expected_output = ("python /functest/ci/run_tests.py -t "
                           "tempest_smoke_serial -r")
        self.assertEqual(expected_output, output)

    def test_parser_cmd_fail(self):
        """Test whether the command is correctly parsed."""
        mock_cmd = "python /functest/ci/run_tests.py -t {{script_testcase}} -r"
        mock_testcase_yaml = {}
        MockTestcase = type('Testcase', (object,), {})
        mock_testcase = MockTestcase()
        mock_testcase.testcase = mock_testcase_yaml.values()
        output = dovetail_parser.Parser.parse_cmd(mock_cmd, mock_testcase)
        expected_output = ("python /functest/ci/run_tests.py -t "
                           "None -r")
        self.assertEqual(expected_output, output)

if __name__ == '__main__':
    unittest.main()
