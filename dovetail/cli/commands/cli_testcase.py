##############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
import os

import click
import yaml

from dovetail import constants
from dovetail.testcase import Testsuite
from dovetail.utils.dovetail_config import DovetailConfig as dt_cfg
import dovetail.utils.dovetail_utils as dt_utils


class CliTestcase(object):

    @classmethod
    def testsuite_load(cls):
        dt_cfg.load_config_files(constants.CONF_PATH)
        Testsuite.load()

    def list_one_testsuite(self, testsuite):
        testsuite_stream = Testsuite.get(testsuite)
        if testsuite_stream:
            testcase_list = []
            mandatory = dt_utils.get_value_from_dict(
                'testcases_list.mandatory', testsuite_stream)
            optional = dt_utils.get_value_from_dict(
                'testcases_list.optional', testsuite_stream)
            if mandatory:
                click.echo("- mandatory")
                for testcase in mandatory:
                    click.echo("    {}".format(testcase))
            if optional:
                click.echo("- optional")
                for testcase in optional:
                    click.echo("    {}".format(testcase))
            if not (mandatory or optional):
                click.echo("No testcase in testsuite {}".format(testsuite))
        else:
            click.echo("testsuite {} does not exist".format(testsuite))

    def list_testsuites(self, testsuite):
        self.testsuite_load()
        if testsuite:
            self.list_one_testsuite(testsuite)
        else:
            testsuite_json = Testsuite.get_all()
            if testsuite_json:
                for key, value in testsuite_json.items():
                    click.echo("--------------------------")
                    click.echo("Test Suite {}".format(key))
                    click.echo("--------------------------")
                    self.list_one_testsuite(key)
            else:
                click.echo("No testsuite defined yet in dovetail!!!")

    def show_testcase(self, name):
        tc_path = os.path.join(
            constants.TESTCASE_PATH,
            "%s.yml" % (name[9:] if name.startswith('dovetail.') else name))
        if os.path.isfile(tc_path):
            with open(tc_path, 'r') as stream:
                try:
                    click.echo(stream.read())
                except yaml.YAMLError as exc:
                    click.echo(exc)
        else:
            click.echo("testcase %s not exist or not supported" % name)

    def run(self, args_str):
        options = ''
        if args_str:
            options = options + args_str

        repo_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__),
                         os.pardir, os.pardir))

        cmd = ("python %s/run.py"
               " %s" % (repo_dir, options))
        dt_utils.exec_cmd(cmd, exit_on_error=True,
                          exec_msg_on=False, info=True)
