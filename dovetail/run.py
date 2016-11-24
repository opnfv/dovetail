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

import utils.dovetail_logger as dt_logger


from container import Container
from testcase import Testcase
from testcase import Testsuite
from report import Report
from conf.dovetail_config import dovetail_config
from conf.dovetail_config import update_envs

logger = dt_logger.Logger('run.py').getLogger()


def load_testsuite(testsuite):
    Testsuite.load()
    return Testsuite.get(testsuite)


def set_container_tags(option_str):
    for script_tag_opt in option_str.split(','):
        option_str = script_tag_opt.split(':')
        script_type = option_str[0].strip()
        script_tag = option_str[1].strip()
        dovetail_config[script_type]['docker_tag'] = script_tag


def load_testcase():
    Testcase.load()


def run_test(testsuite, testarea):
    testarea_list = []
    for value in testsuite['testcases_list']:
        if value is not None and (testarea == 'full' or testarea in value):
            testarea_list.append(value)
    
    for testcase_name in testarea_list:
        logger.info('>>[testcase]: %s' % (testcase_name))
        testcase = Testcase.get(testcase_name)
        if testcase is None:
            logger.error('testcase %s is not defined in testcase folder, \
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


def validate_options(input_dict):
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
        if key in dovetail_config['cli']['options']['envs']:
            envs_options[key] = value
    return envs_options


def main(*args, **kwargs):
    """Dovetail compliance test entry!"""
    logger.info('================================================')
    logger.info('Dovetail compliance: %s!' % (kwargs['testsuite']))
    logger.info('================================================')
    validate_options(kwargs)
    envs_options = filter_env_options(kwargs)
    update_envs(envs_options)
    logger.info('Your new envs for functest: %s' %
                dovetail_config['functest']['envs'])
    logger.info('Your new envs for yardstick: %s' %
                dovetail_config['yardstick']['envs'])
    load_testcase()
    testsuite_yaml = load_testsuite(kwargs['testsuite'])
    testarea = kwargs['testarea']
    if 'tag' in kwargs and kwargs['tag'] is not None:
        set_container_tags(kwargs['tag'])
    
    run_test(testsuite_yaml, testarea)
    Report.generate(testsuite_yaml, testarea)


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
if dovetail_config['cli']['options'] is not None:
    for key, value in dovetail_config['cli']['options'].items():
        if value is not None:
            for k, v in value.items():
                flags = v['flags']
                del v['flags']
                main = click.option(*flags, **v)(main)
if dovetail_config['cli']['arguments'] is not None:
    for key, value in dovetail_config['cli']['arguments'].items():
        if value is not None:
            for k, v in value.items():
                flags = v['flags']
                del v['flags']
                main = click.argument(flags, **v)(main)
main = click.command(context_settings=CONTEXT_SETTINGS)(main)


if __name__ == '__main__':
    main()
