#!/usr/bin/env python
#
# grakiss.wanglei@huawei.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#


import click

import utils.dovetail_logger as dt_logger


from container import Container
from testcase import Testcase
from testcase import Scenario
from report import Report
from conf.dovetail_config import SCENARIO_NAMING_FMT

logger = dt_logger.Logger('run.py').getLogger()


def load_scenario(scenario):
    Scenario.load()
    return Scenario.get(SCENARIO_NAMING_FMT % scenario)


def load_testcase():
    Testcase.load()


def run_test(scenario):
    for testcase_name in scenario['testcase_list']:
        logger.info('>>[testcase]: %s' % (testcase_name))
        testcase = Testcase.get(testcase_name)
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


@click.command()
@click.option('--scenario', default='basic', help='certification scenario')
def main(scenario):
    """Dovetail certification test entry!"""
    logger.info('=======================================')
    logger.info('Dovetail certification: %s!' % scenario)
    logger.info('=======================================')
    load_testcase()
    scenario_yaml = load_scenario(scenario)
    run_test(scenario_yaml)
    Report.generate(scenario_yaml)

if __name__ == '__main__':
    main()
