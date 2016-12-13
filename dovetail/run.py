#!/usr/bin/env python
#
# grakiss.wanglei@huawei.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#


import click
import sys
import os

import utils.dovetail_logger as dt_logger
import utils.dovetail_utils as dt_utils

from parser import Parser
from container import Container
from testcase import Testcase
from testcase import Testsuite
from report import Report
from report import FunctestCrawler, YardstickCrawler
from report import FunctestChecker, YardstickChecker
from conf.dovetail_config import DovetailConfig as dt_cfg
from test_runner import DockerRunner, ShellRunner


def load_testsuite(testsuite):
    Testsuite.load()
    return Testsuite.get(testsuite)


def set_container_tags(option_str):
    for script_tag_opt in option_str.split(','):
        option_str = script_tag_opt.split(':')
        validate_type = option_str[0].strip()
        script_tag = option_str[1].strip()
        dt_cfg.dovetail_config[validate_type]['docker_tag'] = script_tag


def load_testcase():
    Testcase.load()


def run_test(testsuite, testarea, logger):
    testarea_list = []
    for value in testsuite['testcases_list']:
        if value is not None and (testarea == 'full' or testarea in value):
            testarea_list.append(value)

    duration = 0
    for testcase_name in testarea_list:
        logger.info('>>[testcase]: %s' % (testcase_name))
        testcase = Testcase.get(testcase_name)
        if testcase is None:
            logger.error('test case %s is not defined in testcase folder, \
                         skipping' % (testcase_name))
            continue
        run_testcase = True

        if testcase.exceed_max_retry_times():
            run_testcase = False

        if testcase.script_result_acquired():
            run_testcase = False

        if run_testcase:
            testcase.run()

        db_result = Report.get_result(testcase)
        Report.check_result(testcase, db_result)

    return duration


def validate_options(input_dict, logger):
    # for 'tag' option
    for key, value in input_dict.items():
        if key == 'tag' and value is not None:
            for tag in value.split(','):
                if len(tag.split(':')) != 2:
                    logger.error('TAGS option must be "<image>:<tag>,..."')
                    sys.exit(1)


def filter_env_options(input_dict):
    envs_options = {}
    for key, value in input_dict.items():
        key = key.upper()
        if key in dt_cfg.dovetail_config['cli']['options']['envs']:
            envs_options[key] = value
    return envs_options


def create_logs():
    Container.create_log()
    Parser.create_log()
    Report.create_log()
    FunctestCrawler.create_log()
    YardstickCrawler.create_log()
    FunctestChecker.create_log()
    YardstickChecker.create_log()
    Testcase.create_log()
    Testsuite.create_log()
    DockerRunner.create_log()
    ShellRunner.create_log()


def clean_results_dir():
    result_path = dt_cfg.dovetail_config['result_dir']
    if os.path.exists(result_path):
        if os.path.isdir(result_path):
            cmd = 'sudo rm -rf %s/*' % (result_path)
            dt_utils.exec_cmd(cmd, exit_on_error=False)
        else:
            print "result_dir in dovetail_config.yml is not a directory."
            sys.exit(-1)


def main(*args, **kwargs):
    """Dovetail compliance test entry!"""
    clean_results_dir()
    if kwargs['debug']:
        os.environ['DEBUG'] = kwargs['debug']
    create_logs()
    logger = dt_logger.Logger('run').getLogger()
    logger.info('================================================')
    logger.info('Dovetail compliance: %s!' % (kwargs['testsuite']))
    logger.info('================================================')
    validate_options(kwargs, logger)
    envs_options = filter_env_options(kwargs)
    dt_cfg.update_envs(envs_options)
    logger.info('Your new envs for functest: %s' %
                dt_cfg.dovetail_config['functest']['envs'])
    logger.info('Your new envs for yardstick: %s' %
                dt_cfg.dovetail_config['yardstick']['envs'])

    if 'tag' in kwargs and kwargs['tag'] is not None:
        set_container_tags(kwargs['tag'])

    testarea = kwargs['testarea']
    testsuite_validation = False
    testarea_validation = False
    if (testarea == 'full') or \
       (testarea in dt_cfg.dovetail_config['testarea_supported']):
        testarea_validation = True
    if kwargs['testsuite'] in dt_cfg.dovetail_config['testsuite_supported']:
        testsuite_validation = True
    if testsuite_validation and testarea_validation:
        testsuite_yaml = load_testsuite(kwargs['testsuite'])
        load_testcase()
        duration = run_test(testsuite_yaml, testarea, logger)
        Report.generate(testsuite_yaml, testarea, duration)
    else:
        logger.error('invalid input commands, testsuite %s testarea %s' %
                     (kwargs['testsuite'], testarea))


dt_cfg.load_config_files()

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
if dt_cfg.dovetail_config['cli']['options'] is not None:
    for key, value in dt_cfg.dovetail_config['cli']['options'].items():
        if value is not None:
            for k, v in value.items():
                flags = v['flags']
                del v['flags']
                main = click.option(*flags, **v)(main)
if dt_cfg.dovetail_config['cli']['arguments'] is not None:
    for key, value in dt_cfg.dovetail_config['cli']['arguments'].items():
        if value is not None:
            for k, v in value.items():
                flags = v['flags']
                del v['flags']
                main = click.argument(flags, **v)(main)
main = click.command(context_settings=CONTEXT_SETTINGS)(main)


if __name__ == '__main__':
    main()
