#!/usr/bin/env python
#
# grakiss.wanglei@huawei.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

CERT_PATH = './cert/'
TESTCASE_PATH = './testcase/'
SCENARIO_NAMING_FMT = 'certification_%s'

import yaml
import os

with open(os.path.join(os.getcwd(),'conf','dovetail_config.yml')) as f:
    dovetail_config = yaml.safe_load(f)

for extra_config_file in dovetail_config['include_config']:
    with open(os.path.join(os.getcwd(),'conf',extra_config_file)) as f:
        extra_config = yaml.safe_load(f)
        dovetail_config.update(extra_config)

container_config = {}

container_config['functest'] = dovetail_config['functest']
container_config['yardstick'] = dovetail_config['yardstick']
