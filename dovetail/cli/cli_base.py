##############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
import click
from pbr import version
from dovetail.cli.commands.cli_testcase import CliTestcase


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
cli_version = version.VersionInfo('dovetail').version_string()


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=cli_version)
def cli():
    pass


_testcase = CliTestcase()


@cli.command('list',
             help='list the testsuite details')
@click.argument('testsuite', type=click.STRING, required=False)
def testcase_list(testsuite):
    _testcase.list_testsuites(testsuite)


@cli.command('show',
             help='show the testcases details')
@click.argument('testcase', type=click.STRING, required=True)
def testcase_show(testcase):
    _testcase.show_testcase(testcase)


@cli.command('run',
             context_settings=dict(
                 ignore_unknown_options=True, help_option_names=[]),
             help='run the testcases')
@click.argument('run_args', nargs=-1, type=click.UNPROCESSED)
def testcase_run(run_args):
    args_list = [] + list(run_args)
    args_str = ' '.join(args_list)
    _testcase.run(args_str)


# @cli.command('report', help='testcases running result report')
# @click.option('--encrypt', default=True,
#               help='report the test result with encryption')
# def run(**kwargs):
#     CliReport.execute(**kwargs)
