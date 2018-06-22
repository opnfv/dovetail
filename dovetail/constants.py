#!/usr/bin/env python
#
# Copyright (c) 2018 feng.xiaowei@zte.com.cn and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#
import os.path


DOVETAIL_CONF_PATH = '/etc/dovetail'
USERCONF_PATH = os.path.join(DOVETAIL_CONF_PATH, 'userconfig')
PATCH_PATH = os.path.join(DOVETAIL_CONF_PATH, 'patches')
CONF_PATH = os.path.join(DOVETAIL_CONF_PATH, 'conf')
TESTCASE_PATH = os.path.join(DOVETAIL_CONF_PATH, 'testcase')
COMPLIANCE_PATH = os.path.join(DOVETAIL_CONF_PATH, 'compliance')
