#!/usr/bin/env python
#
# Copyright (c) 2018 mokats@intracom-telecom.com and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##

import unittest
from mock import patch

from click.testing import CliRunner
from dovetail.cli import cli_base

__author__ = 'Stamatis Katsaounis <mokats@intracom-telecom.com>'


@patch.object(cli_base, '_testcase')
class CliBaseTesting(unittest.TestCase):

    def test_cli(self, mock_testcase):
        runner = CliRunner()
        result = runner.invoke(cli_base.cli, [])

        self.assertEquals(result.exit_code, 0)

    def test_testcase_list(self, mock_testcase):
        testsuite = 'suite'

        runner = CliRunner()
        result = runner.invoke(cli_base.testcase_list, [testsuite])

        mock_testcase.list_testsuites.assert_called_once_with(testsuite)
        self.assertEquals(result.exit_code, 0)

    def test_testcase_show(self, mock_testcase):
        testcase = 'case'

        runner = CliRunner()
        result = runner.invoke(cli_base.testcase_show, [testcase])

        mock_testcase.show_testcase.assert_called_once_with(testcase)
        self.assertEquals(result.exit_code, 0)

    def test_testcase_run(self, mock_testcase):
        run_args = ('arga', 'argb')

        runner = CliRunner()
        result = runner.invoke(cli_base.testcase_run, run_args)

        expected = ' '.join(run_args)
        mock_testcase.run.assert_called_once_with(expected)
        self.assertEquals(result.exit_code, 0)
