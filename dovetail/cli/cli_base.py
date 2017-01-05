##############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
import click

from dovetail.cli.commands.cli_testcase import CliTestcase


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass


_testcase = CliTestcase()


@cli.command('list',
             help='list the testsuite details')
@click.argument('testsuite', type=click.STRING, required=False)
def testcase_list(testsuite):
    _testcase.list_testcase(testsuite)


@cli.command('show',
             help='show the testcases details')
@click.argument('testcase', type=click.STRING, required=True)
def testcase_show(testcase):
    _testcase.show_testcase(testcase)


@cli.command('run', help='run testcases')
@click.option('--SUT_TYPE', default=None,
              help='Installer type of the system under test (SUT).')
@click.option('--SUT_IP', default=None,
              help='IP of the system under test (SUT).')
@click.option('--debug', default=None,
              help='True for showing debug log on screen.')
@click.option('--functest_tag', default=None,
              help='Overwrite tag for functest docker container')
@click.option('--yardstick_tag', default=None,
              help='Overwrite tag for yardstick docker container')
@click.option('--creds', default=None,
              help='Openstack Credential file location')
@click.option('--testsuite', default=None,
              help='run compliance testsuite')
@click.option('--testarea', default=None,
              help='compliance testarea within testsuite')
def testcase_run(sut_type,
                 sut_ip,
                 debug,
                 functest_tag,
                 yardstick_tag,
                 creds,
                 testsuite,
                 testarea):
    _testcase.run(sut_type,
                  sut_ip,
                  debug,
                  functest_tag,
                  yardstick_tag,
                  creds,
                  testsuite,
                  testarea)


# @cli.command('report', help='testcases running result report')
# @click.option('--encrypt', default=True,
#               help='report the test result with encryption')
# def run(**kwargs):
#     CliReport.execute(**kwargs)
