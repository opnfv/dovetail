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
import copy

import utils.dovetail_logger as dt_logger
import utils.dovetail_utils as dt_utils

from parser import Parser
from container import Container
from testcase import Testcase
from testcase import Testsuite
from report import Report
from report import FunctestCrawler, YardstickCrawler
from report import FunctestChecker, YardstickChecker
from conf.dovetail_config import DovetailConfig as dt_config


def load_testsuite(testsuite):
    Testsuite.load()
    return Testsuite.get(testsuite)


def set_container_tags(option_str):
    for script_tag_opt in option_str.split(','):
        option_str = script_tag_opt.split(':')
        script_type = option_str[0].strip()
        script_tag = option_str[1].strip()
        dt_config.dovetail_config[script_type]['docker_tag'] = script_tag


def load_testcase():
    Testcase.load()


def run_test(testsuite, testarea, logger):
    testarea_list = []
    for value in testsuite['testcases_list']:
        if value is not None and (testarea == 'full' or testarea in value):
            testarea_list.append(value)

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
            Container.pull_image(testcase.script_type())
            container_id = Container.create(testcase.script_type())
            logger.debug('container id:%s' % container_id)

            if not Testcase.prepared(testcase.script_type()):
                cmds = testcase.pre_condition()['cmds']
                if cmds:
                    for cmd in cmds:
                        Container.exec_cmd(container_id, cmd)
                Testcase.prepared(testcase.script_type(), True)

            if not testcase.prepare_cmd():
                logger.error('failed to prepare testcase:%s' % testcase.name())
            else:
                for cmd in testcase.cmds:
                    Container.exec_cmd(container_id, cmd)

            # testcase.post_condition()

            Container.clean(container_id)

        db_result = Report.get_result(testcase)
        Report.check_result(testcase, db_result)


def validate_input(input_dict, check_dict, logger):
    # for 'func_tag' option
    func_tag = input_dict['func_tag']
    valid_tag = check_dict['valid_docker_tag']
    if func_tag is not None and func_tag not in valid_tag:
        logger.error("func_tag can't be %s, valid in %s", func_tag, valid_tag)
        exit(-1)

    # for 'SUT_TYPE' option
    sut_type = input_dict['sut_type']
    valid_type = check_dict['valid_sut_type']
    if sut_type is not None and sut_type not in valid_type:
        logger.error("SUT_TYPE can't be %s, valid in %s", sut_type, valid_type)
        exit(-1)


def filter_config(input_dict, logger):
    cli_dict = dt_config.dovetail_config['cli']
    configs = {}
    for key in cli_dict:
        if cli_dict[key] is None or 'config' not in cli_dict[key]:
            continue
        cli_config = cli_dict[key]['config']
        if cli_config is None:
            continue
        for key, value in input_dict.items():
            for config_key, config_value in cli_config.items():
                value_dict = {}
                value_dict['value'] = value
                if 'path' in config_value:
                    value_dict['path'] = config_value['path']
                else:
                    logger.error('%s must have subsection path', config_key)
                    exit(-1)
                if key == config_key:
                    configs[key] = value_dict
                    break
                if key.upper() == config_key:
                    configs[key.upper()] = value_dict
                    break
    if len(configs) == 0:
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


def clean_results_dir():
    result_path = dt_config.dovetail_config['result_dir']
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
    create_logs()
    logger = dt_logger.Logger('run').getLogger()
    logger.info('================================================')
    logger.info('Dovetail compliance: %s!' % (kwargs['testsuite']))
    logger.info('================================================')
    validate_input(kwargs, dt_config.dovetail_config['validate'], logger)
    configs = filter_config(kwargs, logger)

    if configs is not None:
        dt_config.update_config(configs)
    logger.info('Your new envs for functest: %s' %
                dt_config.dovetail_config['functest']['envs'])
    logger.info('Your new envs for yardstick: %s' %
                dt_config.dovetail_config['yardstick']['envs'])

    testarea = kwargs['testarea']
    testsuite_validation = False
    testarea_validation = False
    if (testarea == 'full') or (testarea in dt_config.testarea_supported):
        testarea_validation = True
    if kwargs['testsuite'] in dt_config.testsuite_supported:
        testsuite_validation = True
    if testsuite_validation and testarea_validation:
        testsuite_yaml = load_testsuite(kwargs['testsuite'])
        load_testcase()
        run_test(testsuite_yaml, testarea, logger)
        Report.generate(testsuite_yaml, testarea)
    else:
        logger.error('invalid input commands, testsuite %s testarea %s' %
                     (kwargs['testsuite'], testarea))


dovetail_config = copy.deepcopy(dt_config.dovetail_config)
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
if dovetail_config['cli']['options'] is not None:
    for key, value in dovetail_config['cli']['options'].items():
        if value is not None:
            for k, v in value.items():
                flags = v['flags']
                del v['flags']
                if 'path' in v:
                    del v['path']
                main = click.option(*flags, **v)(main)
if dovetail_config['cli']['arguments'] is not None:
    for key, value in dovetail_config['cli']['arguments'].items():
        if value is not None:
            for k, v in value.items():
                flags = v['flags']
                del v['flags']
                if 'path' in v:
                    del v['path']
                main = click.argument(flags, **v)(main)
main = click.command(context_settings=CONTEXT_SETTINGS)(main)


if __name__ == '__main__':
    main()
