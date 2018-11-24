#!/usr/bin/env python

##############################################################################
# Copyright (c) 2017 grakiss.wanglei@huawei.com and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


import copy
import os
import time
import uuid

import click

from container import Container
from dovetail import constants
from parser import Parser
import report as dt_report
import test_runner as dt_test_runner
import testcase as dt_testcase
from utils.dovetail_config import DovetailConfig as dt_cfg
import utils.dovetail_logger as dt_logger
import utils.dovetail_utils as dt_utils

EXIT_RUN_FAILED = 2


def load_testsuite(testsuite):
    dt_testcase.Testsuite.load()
    return dt_testcase.Testsuite.get(testsuite)


def run_test(testcase_list, report_flag, logger):
    report = dt_report.Report()
    duration = 0
    if not testcase_list:
        logger.warning('No test case will be executed.')
        return

    start_time = time.time()
    for testcase_name in testcase_list:
        logger.info('>>[testcase]: {}'.format(testcase_name))
        testcase = dt_testcase.Testcase.get(testcase_name)
        run_testcase = True

        if run_testcase:
            testcase.run()

        result = report.check_tc_result(testcase)
        if dt_cfg.dovetail_config['stop']:
            try:
                if (not result or result['criteria'] == 'FAIL'):
                    logger.info('Stop because {} failed'.format(testcase_name))
                    return
            except KeyError as e:
                logger.error('There is no key {}.'.format(e))
                logger.info('Stop because {} failed'.format(testcase_name))
                return

    end_time = time.time()
    duration = end_time - start_time
    report.generate(testcase_list, duration)
    if report_flag:
        report.save_logs()
    return


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
                    logger.exception('KeyError {}.'.format(e))
                    raise SystemExit(EXIT_RUN_FAILED)
    if not configs:
        return None
    return configs


def create_logs():
    Container.create_log()
    Parser.create_log()
    dt_report.Report.create_log()
    dt_report.FunctestCrawler.create_log()
    dt_report.FunctestK8sCrawler.create_log()
    dt_report.YardstickCrawler.create_log()
    dt_report.VnftestCrawler.create_log()
    dt_report.BottlenecksCrawler.create_log()
    dt_report.OnapVtpCrawler.create_log()
    dt_report.FunctestChecker.create_log()
    dt_report.FunctestK8sChecker.create_log()
    dt_report.YardstickChecker.create_log()
    dt_report.VnftestChecker.create_log()
    dt_report.BottlenecksChecker.create_log()
    dt_report.OnapVtpChecker.create_log()
    dt_testcase.Testcase.create_log()
    dt_testcase.Testsuite.create_log()
    dt_test_runner.DockerRunner.create_log()
    dt_test_runner.ShellRunner.create_log()


def clean_results_dir():
    result_path = dt_cfg.dovetail_config['result_dir']
    if os.path.exists(result_path):
        if os.path.isdir(result_path):
            cmd = 'sudo rm -rf %s/*' % (result_path)
            dt_utils.exec_cmd(cmd, exit_on_error=False, exec_msg_on=False)
        else:
            print('result_dir in dovetail_config.yml is not a directory.')
            raise SystemExit(EXIT_RUN_FAILED)


def get_result_path():
    try:
        dovetail_home = os.environ['DOVETAIL_HOME']
    except Exception:
        print("ERROR: mandatory env variable 'DOVETAIL_HOME' is not found, "
              "please set in env_config.sh and source this file before "
              "running.")
        return None
    dt_cfg.dovetail_config['result_dir'] = os.path.join(dovetail_home,
                                                        'results')
    dt_cfg.dovetail_config['images_dir'] = os.path.join(dovetail_home,
                                                        'images')
    dt_cfg.dovetail_config['config_dir'] = os.path.join(dovetail_home,
                                                        'pre_config')
    dt_cfg.dovetail_config['patch_dir'] = os.path.join(dovetail_home,
                                                       'patches')
    return dovetail_home


def copy_userconfig_files(logger):
    pre_config_path = dt_cfg.dovetail_config['config_dir']
    if not os.path.isdir(pre_config_path):
        os.makedirs(pre_config_path)
    cmd = 'sudo cp -r %s/* %s' % (constants.USERCONF_PATH, pre_config_path)
    dt_utils.exec_cmd(cmd, logger, exit_on_error=False)


def copy_patch_files(logger):
    patch_set_path = dt_cfg.dovetail_config['patch_dir']
    if not os.path.isdir(patch_set_path):
        os.makedirs(patch_set_path)
    cmd = 'sudo cp -a -r %s/* %s' % (constants.PATCH_PATH, patch_set_path)
    dt_utils.exec_cmd(cmd, logger, exit_on_error=False)


def update_deploy_scenario(logger, **kwargs):
    if 'deploy_scenario' in kwargs and kwargs['deploy_scenario'] is not None:
        os.environ['DEPLOY_SCENARIO'] = kwargs['deploy_scenario']
        logger.info('DEPLOY_SCENARIO : %s', os.environ['DEPLOY_SCENARIO'])


def parse_cli(logger=None, **kwargs):
    configs = filter_config(kwargs, logger)
    if configs is not None:
        dt_cfg.update_config(configs)
    dt_cfg.dovetail_config['offline'] = kwargs['offline']
    dt_cfg.dovetail_config['noclean'] = kwargs['no_clean']
    dt_cfg.dovetail_config['stop'] = kwargs['stop']
    dt_cfg.dovetail_config['mandatory'] = kwargs['mandatory']
    dt_cfg.dovetail_config['optional'] = kwargs['optional']
    if kwargs['no_api_validation']:
        dt_cfg.dovetail_config['no_api_validation'] = True
        logger.warning('Strict API response validation DISABLED.')
    else:
        dt_cfg.dovetail_config['no_api_validation'] = False


def check_testcase_list(testcase_list, logger=None):
    if testcase_list:
        for tc in testcase_list:
            if tc not in dt_testcase.Testcase.testcase_list:
                logger.error('Test case {} is not defined.'.format(tc))
                return None
        return testcase_list
    logger.error('There is no test case to be executed.')
    return None


def get_testcase_list(logger=None, **kwargs):
    dt_testcase.Testcase.load()
    testcase_list = kwargs['testcase']

    # If specify 'testcase' on the CLI, ignore 'testsuite' and 'testarea'. In
    # this case, all test cases are marked as mandatory=false in the result
    # file because there is no testsuite to relate to.
    # If 'testcase' is not specified on the CLI, check the combination of
    # 'testsuite' and 'testarea'
    if testcase_list:
        return check_testcase_list(testcase_list, logger)

    testsuite_validation = False
    testsuite = kwargs['testsuite']
    if testsuite in dt_cfg.dovetail_config['testsuite_supported']:
        testsuite_validation = True
    origin_testarea = kwargs['testarea']
    testarea_validation, testarea = dt_testcase.Testcase.check_testarea(
        origin_testarea)

    if testsuite_validation and testarea_validation:
        testsuite_yaml = load_testsuite(testsuite)
        testcase_list = dt_testcase.Testcase.get_testcases_for_testsuite(
            testsuite_yaml, testarea)
        return check_testcase_list(testcase_list, logger)
    elif not testsuite_validation:
        logger.error('Test suite {} is not defined.'.format(testsuite))
    else:
        logger.error('Test area {} is not defined.'.format(origin_testarea))
    return None


def main(*args, **kwargs):
    """Dovetail compliance test entry!"""
    build_tag = 'daily-master-%s' % str(uuid.uuid1())
    dt_cfg.dovetail_config['build_tag'] = build_tag
    if not get_result_path():
        return
    clean_results_dir()
    if kwargs['debug']:
        os.environ['DEBUG'] = 'true'
    create_logs()
    logger = dt_logger.Logger('run').getLogger()

    logger.info('================================================')
    logger.info('Dovetail compliance: {}!'.format(kwargs['testsuite']))
    logger.info('================================================')
    logger.info('Build tag: {}'.format(dt_cfg.dovetail_config['build_tag']))
    parse_cli(logger, **kwargs)
    update_deploy_scenario(logger, **kwargs)
    copy_userconfig_files(logger)
    copy_patch_files(logger)
    dt_utils.check_docker_version(logger)

    testcase_list = get_testcase_list(logger, **kwargs)
    if not testcase_list:
        raise SystemExit(EXIT_RUN_FAILED)

    run_test(testcase_list, kwargs['report'], logger)


dt_cfg.load_config_files(constants.CONF_PATH)
dovetail_config = copy.deepcopy(dt_cfg.dovetail_config)
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
if dovetail_config['cli']['options'] is not None:
    for key, value in dovetail_config['cli']['options'].items():
        if value is not None:
            for _, v in value.items():
                flags = v['flags']
                v.pop('flags')
                v.pop('path', None)
                main = click.option(*flags, **v)(main)
if dovetail_config['cli']['arguments'] is not None:
    for key, value in dovetail_config['cli']['arguments'].items():
        if value is not None:
            for _, v in value.items():
                flags = v['flags']
                v.pop('flags')
                v.pop('path', None)
                main = click.argument(flags, **v)(main)
main = click.command(context_settings=CONTEXT_SETTINGS)(main)


if __name__ == '__main__':
    main()
