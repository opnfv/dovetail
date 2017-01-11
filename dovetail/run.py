#!/usr/bin/env python
#
# grakiss.wanglei@huawei.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#


import click
import os
import copy
import time

import utils.dovetail_logger as dt_logger
import utils.dovetail_utils as dt_utils

from parser import Parser
from container import Container
from testcase import Testcase
from testcase import Testsuite
from report import Report
from report import FunctestCrawler, YardstickCrawler
from report import FunctestChecker, YardstickChecker
from utils.dovetail_config import DovetailConfig as dt_cfg
from test_runner import DockerRunner, ShellRunner


def load_testsuite(testsuite):
    Testsuite.load()
    return Testsuite.get(testsuite)


def load_testcase():
    Testcase.load()


def run_test(testsuite, testarea, logger):
    testarea_list = []
    for value in testsuite['testcases_list']:
        if value is not None and (testarea == 'full' or testarea in value):
            testarea_list.append(value)

    duration = 0
    for testcase_name in testarea_list:
        logger.info('>>[testcase]: %s', (testcase_name))
        testcase = Testcase.get(testcase_name)
        if testcase is None:
            logger.error('test case %s is not defined in testcase folder, \
                         skipping', (testcase_name))
            continue
        run_testcase = True

        if testcase.exceed_max_retry_times():
            run_testcase = False

        if testcase.script_result_acquired():
            run_testcase = False

        if run_testcase:
            start_time = time.time()
            testcase.run()
            end_time = time.time()
            duration = end_time - start_time

        result = Report.get_result(testcase)
        Report.check_result(testcase, result)

    return duration


def validate_input(input_dict, check_dict, logger):
    # for 'func_tag' and 'yard_tag' options
    func_tag = input_dict['func_tag']
    yard_tag = input_dict['yard_tag']
    valid_tag = check_dict['valid_docker_tag']
    if func_tag is not None and func_tag not in valid_tag:
        logger.error("func_tag can't be %s, valid in %s", func_tag, valid_tag)
        raise SystemExit(1)
    if yard_tag is not None and yard_tag not in valid_tag:
        logger.error("yard_tag can't be %s, valid in %s", yard_tag, valid_tag)
        raise SystemExit(1)

    # for 'SUT_TYPE' option
    sut_type = input_dict['sut_type']
    valid_type = check_dict['valid_sut_type']
    if sut_type is not None and sut_type not in valid_type:
        logger.error("SUT_TYPE can't be %s, valid in %s", sut_type, valid_type)
        raise SystemExit(1)


def filter_config(input_dict, logger):
    cli_dict = dt_cfg.dovetail_config['cli']
    configs = {}
    for key in cli_dict:
        if not cli_dict[key]:
            continue
        try:
            cli_config = cli_dict[key]['config']
            if cli_config is None:
                continue
        except KeyError:
            continue
        for key, value in input_dict.items():
            for config_key, config_value in cli_config.items():
                value_dict = {}
                value_dict['value'] = value
                try:
                    value_dict['path'] = config_value['path']
                    if key == config_key:
                        configs[key] = value_dict
                        break
                    if key.upper() == config_key:
                        configs[key.upper()] = value_dict
                        break
                except KeyError as e:
                    logger.exception('%s lacks subsection %s', config_key, e)
                    raise SystemExit(1)
    if not configs:
        return None
    return configs


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
            raise SystemExit(1)


def main(*args, **kwargs):
    """Dovetail compliance test entry!"""
    clean_results_dir()
    if kwargs['debug']:
        os.environ['DEBUG'] = kwargs['debug']
    create_logs()
    logger = dt_logger.Logger('run').getLogger()
    logger.info('================================================')
    logger.info('Dovetail compliance: %s!', (kwargs['testsuite']))
    logger.info('================================================')
    validate_input(kwargs, dt_cfg.dovetail_config['validate_input'], logger)
    configs = filter_config(kwargs, logger)

    if configs is not None:
        dt_cfg.update_config(configs)
    logger.info('Your new envs for functest: %s',
                dt_cfg.dovetail_config['functest']['envs'])
    logger.info('Your new envs for yardstick: %s',
                dt_cfg.dovetail_config['yardstick']['envs'])

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
        logger.error('invalid input commands, testsuite %s testarea %s',
                     (kwargs['testsuite'], testarea))


dt_cfg.load_config_files()
dovetail_config = copy.deepcopy(dt_cfg.dovetail_config)
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
if dovetail_config['cli']['options'] is not None:
    for key, value in dovetail_config['cli']['options'].items():
        if value is not None:
            for k, v in value.items():
                flags = v['flags']
                v.pop('flags')
                v.pop('path', None)
                main = click.option(*flags, **v)(main)
if dovetail_config['cli']['arguments'] is not None:
    for key, value in dovetail_config['cli']['arguments'].items():
        if value is not None:
            for k, v in value.items():
                flags = v['flags']
                v.pop('flags')
                v.pop('path', None)
                main = click.argument(flags, **v)(main)
main = click.command(context_settings=CONTEXT_SETTINGS)(main)


if __name__ == '__main__':
    main()
