#!/usr/bin/env python
#
# Copyright (c) 2018 grakiss.wanglei@huawei.com and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

import jinja2


import utils.dovetail_logger as dt_logger
import utils.dovetail_utils as dt_utils
from utils.dovetail_config import DovetailConfig as dt_cfg


class Parser(object):
    """preprocess configuration files"""

    logger = None

    @classmethod
    def create_log(cls):
        cls.logger = dt_logger.Logger(__name__ + '.Parser').getLogger()

    @classmethod
    def parse_cmd(cls, cmd, testcase):
        cmd_lines = None
        try:
            template = jinja2.Template(cmd, undefined=jinja2.StrictUndefined)
            kwargs = {}
            for arg in dt_cfg.dovetail_config['parameters']:
                path = eval(arg['path'])
                cls.logger.debug(
                    'name: {}, eval path: {}'.format(arg['name'], path))
                kwargs[arg['name']] = \
                    dt_utils.get_obj_by_path(testcase.testcase, path)

            cls.logger.debug('kwargs: {}'.format(kwargs))
            cmd_lines = template.render(**kwargs)
        except Exception as e:
            cls.logger.exception(
                'Failed to parse cmd {}, exception: {}'.format(cmd, e))
            return None

        return cmd_lines
