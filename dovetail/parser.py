#!/usr/bin/env python
#
# grakiss.wanglei@huawei.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

import jinja2


import utils.dovetail_logger as dt_logger
import utils.dovetail_utils as dt_utils
from conf.dovetail_config import dovetail_config


class Parser:
    '''preprocess configuration files'''

    logger = dt_logger.Logger('parser.py').getLogger()

    @classmethod
    def parse_cmd(cls, cmd, testcase):
        cmd_lines = None
        try:
            template = jinja2.Template(cmd, undefined=jinja2.StrictUndefined)
            kwargs = {}
            for arg in dovetail_config['parameters']:
                path = eval(arg['path'])
                cls.logger.debug('name: %s, eval path: %s ' %
                                 (arg['name'], path))
                kwargs[arg['name']] = \
                    dt_utils.get_obj_by_path(testcase.testcase, path)

            cls.logger.debug('kwargs: %s' % kwargs)
            cmd_lines = template.render(**kwargs)
        except Exception as e:
            cls.logger.error('failed to parse cmd %s, exception:%s' % (cmd, e))
            return None

        return cmd_lines
