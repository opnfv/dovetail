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
from report import BottlenecksChecker, FunctestChecker, YardstickChecker
from report import VnftestChecker
from report import BottlenecksCrawler, FunctestCrawler, YardstickCrawler
from report import VnftestCrawler
from report import Report
from test_runner import DockerRunner, ShellRunner
from testcase import Testcase
from testcase import Testsuite
from utils.dovetail_config import DovetailConfig as dt_cfg
import utils.dovetail_logger as dt_logger
import utils.dovetail_utils as dt_utils


EXIT_RUN_FAILED = 2


def load_testsuite(testsuite):
    Testsuite.load()
    return Testsuite.get(testsuite)


def run_test(testcase_list, logger):
    duration = 0
    if not testcase_list:
        logger.warning("No test case will be executed.")
        return duration

    start_time = time.time()
    for testcase_name in testcase_list:
        logger.info('>>[testcase]: {}'.format(testcase_name))
        testcase = Testcase.get(testcase_name)
        run_testcase = True

        # if testcase.exceed_max_retry_times():
        #    run_testcase = False

        # if testcase.script_result_acquired():
        #    run_testcase = False

        if run_testcase:
            testcase.run()

        stop_on_fail = Report.check_tc_result(testcase)
        try:
            if (not stop_on_fail or stop_on_fail['criteria'] == "FAIL") \
                and dt_cfg.dovetail_config['stop']:
                return "stop_on_fail"
        except KeyError as e:
            logger.error("There is no key {}.".format(e))

    end_time = time.time()
    duration = end_time - start_time
    return duration


def validate_input(input_dict, check_dict, logger):
    func_tag = input_dict['functest_tag']
    yard_tag = input_dict['yardstick_tag']
    # bott_tag = input_dict['bott_tag']
    valid_functest_tags = check_dict['valid_functest_tags']
    valid_yardstick_tags = check_dict['valid_yardstick_tags']
    if func_tag is not None and func_tag not in valid_functest_tags:
        logger.error("The input option 'functest_tag' can't be '{}', "
                     "valid values are {}.".format(func_tag,
                                                   valid_functest_tags))
        raise SystemExit(EXIT_RUN_FAILED)
    if yard_tag is not None and yard_tag not in valid_yardstick_tags:
        logger.error("The input option 'yardstick_tag' can't be '{}', "
                     "valid values are {}.".format(yard_tag,
                                                   valid_yardstick_tags))
        raise SystemExit(EXIT_RUN_FAILED)
    # if bott_tag is not None and bott_tag not in valid_tag:
    #     logger.error("The input option 'bott_tag' can't be {}, "
    #                  "valid values are {}.".format(bott_tag, valid_tag))
    #     raise SystemExit(1)


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
    Report.create_log()
    FunctestCrawler.create_log()
    YardstickCrawler.create_log()
    VnftestCrawler.create_log()
    BottlenecksCrawler.create_log()
    FunctestChecker.create_log()
    YardstickChecker.create_log()
    VnftestChecker.create_log()
    BottlenecksChecker.create_log()
    Testcase.create_log()
    Testsuite.create_log()
    DockerRunner.create_log()
    ShellRunner.create_log()


def clean_results_dir():
    result_path = dt_cfg.dovetail_config['result_dir']
    if os.path.exists(result_path):
        if os.path.isdir(result_path):
            cmd = 'sudo rm -rf %s/*' % (result_path)
            dt_utils.exec_cmd(cmd, exit_on_error=False, exec_msg_on=False)
        else:
            print("result_dir in dovetail_config.yml is not a directory.")
            raise SystemExit(EXIT_RUN_FAILED)


def get_result_path():
    try:
        dovetail_home = os.environ["DOVETAIL_HOME"]
    except Exception:
        print("ERROR: mandatory env variable 'DOVETAIL_HOME' is not found, "
              "please set in env_config.sh and source this file before "
              "running.")
        return None
    result_path = os.path.join(dovetail_home, 'results')
    dt_cfg.dovetail_config['result_dir'] = result_path
    dt_cfg.dovetail_config['images_dir'] = os.path.join(dovetail_home,
                                                        'images')
    pre_config_path = os.path.join(dovetail_home, 'pre_config')
    patch_set_path = os.path.join(dovetail_home, 'patches')
    dt_cfg.dovetail_config['config_dir'] = pre_config_path
    dt_cfg.dovetail_config['patch_dir'] = patch_set_path
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


# env_init can source some env variable used in dovetail, such as
# when https+credential used, OS_CACERT
def env_init(logger):
    openrc = os.path.join(dt_cfg.dovetail_config['config_dir'],
                          dt_cfg.dovetail_config['env_file'])
    if not os.path.isfile(openrc):
        logger.error("File {} does not exist.".format(openrc))
    dt_utils.source_env(openrc)


def check_hosts_file(logger):
    hosts_file = os.path.join(dt_cfg.dovetail_config['config_dir'],
                              'hosts.yaml')
    if not os.path.isfile(hosts_file):
        logger.warn("There is no hosts file {}, may be some issues with "
                    "domain name resolution.".format(hosts_file))


def parse_cli(logger=None, **kwargs):
    validate_input(kwargs, dt_cfg.dovetail_config['validate_input'], logger)
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
            if tc not in Testcase.testcase_list:
                logger.error('Test case {} is not defined.'.format(tc))
                return None
        return testcase_list
    return None


# If specify 'testcase' with CLI, ignore 'testsuite' and 'testarea'
# If not specify 'testcase', check combination of 'testsuite' and 'testarea'
def get_testcase_list(logger=None, **kwargs):
    Testcase.load()
    testcase_list = kwargs['testcase']
    if testcase_list:
        return check_testcase_list(testcase_list, logger)

    testsuite_validation = False
    testsuite = kwargs['testsuite']
    if testsuite in dt_cfg.dovetail_config['testsuite_supported']:
        testsuite_validation = True
    origin_testarea = kwargs['testarea']
    testarea_validation, testarea = Testcase.check_testarea(origin_testarea)

    if testsuite_validation and testarea_validation:
        testsuite_yaml = load_testsuite(testsuite)
        testcase_list = Testcase.get_testcase_list(testsuite_yaml, testarea)
        return check_testcase_list(testcase_list, logger)
    elif not testsuite_validation:
        logger.error('Test suite {} is not defined.'.format(testsuite))
    else:
        logger.error('Test area {} is not defined.'.format(origin_testarea))
    return None


def main(*args, **kwargs):
    """Dovetail compliance test entry!"""
    build_tag = "daily-master-%s" % str(uuid.uuid1())
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
    env_init(logger)
    copy_userconfig_files(logger)
    copy_patch_files(logger)
    dt_utils.check_docker_version(logger)
    dt_utils.get_openstack_endpoint(logger)
    check_hosts_file(logger)
    dt_utils.get_hardware_info(logger)

    testcase_list = get_testcase_list(logger, **kwargs)
    if not testcase_list:
        raise SystemExit(EXIT_RUN_FAILED)

    duration = run_test(testcase_list, logger)
    if (duration != "stop_on_fail"):
        Report.generate(testcase_list, duration)
        if (kwargs['report']):
            Report.save_logs()


dt_cfg.load_config_files(constants.CONF_PATH)
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
