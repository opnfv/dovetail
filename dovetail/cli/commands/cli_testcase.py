##############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
import os
import yaml
import click

import dovetail.utils.dovetail_utils as dt_utils
import dovetail.utils.dovetail_logger as dt_logger
from dovetail.utils.dovetail_config import DovetailConfig as dt_cfg
from dovetail.testcase import Testsuite


class CliTestcase:

    def list_testcase(self, testsuite):
        dt_cfg.load_config_files()
        testsuite_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__),
                         os.pardir, os.pardir))
        testsuite_path = dt_cfg.dovetail_config['COMPLIANCE_PATH']
        abs_testsuite_path = os.path.join(testsuite_dir, testsuite_path)

        if testsuite is None:
            Testsuite.load()
            testsuite_json = Testsuite.get_all()
            for key, value in testsuite_json.items():
                click.echo("- %s" % key)
                testsuite_stream = Testsuite.get(key)
                if testsuite_stream['testcases_list']:
                    for testcase in testsuite_stream['testcases_list']:
                        click.echo("    %s" % testcase)
                else:
                    click.echo("No testcase in testsuite %s" % key)
        else:
            testsuite_yml = testsuite + '.yml'
            for root, dirs, files in os.walk(abs_testsuite_path):
                if testsuite_yml in files:
                    Testsuite.load()
                    testsuite_stream = Testsuite.get(testsuite)
                    testcase_list = []
                    for value in testsuite_stream['testcases_list']:
                        if value is not None:
                            testcase_list.append(value)
                    testarea_list = []
                    for testcase in testcase_list:
                        testarea = testcase.split('.')[1]
                        if testarea not in testarea_list:
                            testarea_list.append(testarea)
                    for testarea in testarea_list:
                        click.echo("- %s" % testarea)
                        for testcase in testcase_list:
                            if testarea in testcase:
                                click.echo("    %s" % testcase)
                else:
                    click.echo("testsuite %s does not exist or not supported"
                               % testsuite)

    def show_testcase(self, testcase):
        dt_cfg.load_config_files()
        testcase_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__),
                         os.pardir, os.pardir))
        testcase_path = dt_cfg.dovetail_config['TESTCASE_PATH']
        abs_testcase_path = os.path.join(testcase_dir, testcase_path)

        testcase_yml = testcase + '.yml'
        for root, dirs, files in os.walk(abs_testcase_path):
            if testcase_yml in files:
                testcase_path = abs_testcase_path + testcase_yml
                with open(testcase_path, 'r') as stream:
                    try:
                        click.echo(stream.read())
                    except yaml.YAMLError as exc:
                        click.echo(exc)
            else:
                click.echo("testcase %s does not exist or not supported"
                           % testcase)

    def run(self, args_str):
        options = ''
        if args_str is not None:
            options = options + args_str

        dt_cfg.load_config_files()
        repo_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__),
                         os.pardir, os.pardir))
        cli_logger = dt_logger.Logger('dovetail').getLogger()

        cmd = ("python %s/run.py"
               " %s" % (repo_dir, options))
        dt_utils.exec_cmd(cmd, cli_logger, exit_on_error=False, info=True)
