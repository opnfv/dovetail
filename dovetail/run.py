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
import uuid

import utils.dovetail_logger as dt_logger
import utils.dovetail_utils as dt_utils

from parser import Parser
from container import Container
from testcase import Testcase
from testcase import Testsuite
from report import Report
from report import FunctestCrawler, YardstickCrawler, BottlenecksCrawler
from report import FunctestChecker, YardstickChecker, BottlenecksChecker
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
    start_time = time.time()
    for testcase_name in testarea_list:
        logger.info('>>[testcase]: {}'.format(testcase_name))
        testcase = Testcase.get(testcase_name)
        if testcase is None:
            logger.error('Test case {} is not defined in testcase folder, '
                         'skipping.'.format(testcase_name))
            continue
        run_testcase = True

        # if testcase.exceed_max_retry_times():
        #    run_testcase = False

        # if testcase.script_result_acquired():
        #    run_testcase = False

        if run_testcase:
            testcase.run()

        check_tc_result(testcase, logger)

    end_time = time.time()
    duration = end_time - start_time
    return duration


def check_tc_result(testcase, logger):
    result_dir = dt_cfg.dovetail_config['result_dir']
    validate_type = testcase.validate_type()
    functest_result = dt_cfg.dovetail_config['functest']['result']['file_path']
    dovetail_result = os.path.join(result_dir,
                                   dt_cfg.dovetail_config['result_file'])
    if dt_cfg.dovetail_config['report_dest'].startswith("http"):
        if dt_utils.store_db_results(dt_cfg.dovetail_config['report_dest'],
                                     dt_cfg.dovetail_config['build_tag'],
                                     testcase.name(), dovetail_result,
                                     logger):
            logger.info("Results have been pushed to database and stored "
                        "with local file {}.".format(dovetail_result))
        else:
            logger.error("Failed to push results to database.")
    if dt_cfg.dovetail_config['report_dest'] == "file":
        if validate_type.lower() == 'yardstick':
            result_file = os.path.join(result_dir, testcase.name() + '.out')
        elif validate_type.lower() == 'functest':
            result_file = os.path.join(result_dir, functest_result)
        elif validate_type.lower() == 'bottlenecks':
            result_file = os.path.join(result_dir, testcase.name() + '.out')
        else:
            logger.error("Don't support {} now.".format(validate_type))
            return
        if os.path.isfile(result_file):
            logger.info(
                "Results have been stored with file {}.".format(result_file))
        else:
            logger.error(
                "Failed to store results with file {}.".format(result_file))
        result = Report.get_result(testcase)
        Report.check_result(testcase, result)


def validate_input(input_dict, check_dict, logger):
    # for 'func_tag' and 'yard_tag' options
    func_tag = input_dict['func_tag']
    yard_tag = input_dict['yard_tag']
    bott_tag = input_dict['bott_tag']
    valid_tag = check_dict['valid_docker_tag']
    if func_tag is not None and func_tag not in valid_tag:
        logger.error("The input option 'func_tag' can't be {}, "
                     "valid values are {}.".format(func_tag, valid_tag))
        raise SystemExit(1)
    if yard_tag is not None and yard_tag not in valid_tag:
        logger.error("The input option 'yard_tag' can't be {}, "
                     "valid values are {}.".format(yard_tag, valid_tag))
        raise SystemExit(1)
    if bott_tag is not None and bott_tag not in valid_tag:
        logger.error("The input option 'bott_tag' can't be {}, "
                     "valid values are {}.".format(bott_tag, valid_tag))
        raise SystemExit(1)

    # for 'report' option
    report = input_dict['report']
    if report:
        if not (report.startswith("http") or report == "file"):
            logger.error("Report type can't be {}, valid types are 'file' "
                         "and 'http'.".format(input_dict['report']))
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
                    logger.exception('KeyError {}.'.format(e))
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
    BottlenecksCrawler.create_log()
    FunctestChecker.create_log()
    YardstickChecker.create_log()
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
            print "result_dir in dovetail_config.yml is not a directory."
            raise SystemExit(1)


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
    pre_config_path = os.path.join(dovetail_home, 'pre_config')
    patch_set_path = os.path.join(dovetail_home, 'patch')
    dt_cfg.dovetail_config['config_dir'] = pre_config_path
    dt_cfg.dovetail_config['patch_dir'] = patch_set_path
    return dovetail_home


def copy_userconfig_files(logger):
    dovetail_home = os.path.dirname(os.path.abspath(__file__))
    userconfig_path = os.path.join(dovetail_home, 'userconfig')
    pre_config_path = dt_cfg.dovetail_config['config_dir']
    if not os.path.isdir(pre_config_path):
        os.makedirs(pre_config_path)
    cmd = 'sudo cp -r %s/* %s' % (userconfig_path, pre_config_path)
    dt_utils.exec_cmd(cmd, logger, exit_on_error=False)


def copy_patch_files(logger):
    dovetail_home = os.path.dirname(os.path.abspath(__file__))
    patch_path = os.path.join(dovetail_home, 'patch')
    patch_set_path = dt_cfg.dovetail_config['patch_dir']
    if not os.path.isdir(patch_set_path):
        os.makedirs(patch_set_path)
    cmd = 'sudo cp -r %s/* %s' % (patch_path, patch_set_path)
    dt_utils.exec_cmd(cmd, logger, exit_on_error=False)


# env_init can source some env variable used in dovetail, such as
# when https+credential used, OS_CACERT
def env_init(logger):
    openrc = os.path.join(dt_cfg.dovetail_config['config_dir'],
                          dt_cfg.dovetail_config['env_file'])
    if not os.path.isfile(openrc):
        logger.error("File {} does not exist.".format(openrc))
    dt_utils.source_env(openrc)


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
    env_init(logger)
    copy_userconfig_files(logger)
    copy_patch_files(logger)
    dt_utils.check_docker_version(logger)
    validate_input(kwargs, dt_cfg.dovetail_config['validate_input'], logger)
    configs = filter_config(kwargs, logger)

    if configs is not None:
        dt_cfg.update_config(configs)

    if kwargs['report']:
        if(kwargs['report'].endswith('/')):
            kwargs['report'] = kwargs['report'][0:kwargs['report'].rfind('/')]
        dt_cfg.dovetail_config['report_dest'] = kwargs['report']
        dt_cfg.update_cmds()

    if kwargs['offline']:
        dt_cfg.dovetail_config['offline'] = True
    else:
        dt_cfg.dovetail_config['offline'] = False

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
        if dt_cfg.dovetail_config['report_dest'] == "file":
            Report.generate(testsuite_yaml, testarea, duration)
        Report.save_logs()
    else:
        logger.error('Invalid input commands, testsuite {} testarea {}'
                     .format(kwargs['testsuite'], testarea))


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
