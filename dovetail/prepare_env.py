#!/usr/bin/env python
#
# grakiss.wanglei@huawei.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

import os

import utils.dovetail_logger as dt_logger
import utils.dovetail_utils as dt_utils


logger = dt_logger.Logger('prepare_env.py').getLogger()

cmd = "sudo apt-get -y install docker.io python-pip"
dt_utils.exec_cmd(cmd, logger)

cmd = "sudo pip install click pyyaml jinja2"
dt_utils.exec_cmd(cmd, logger)

