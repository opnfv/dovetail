##############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


DEFAULT_LOGLEVEL = 'debug'
DEFAULT_LOGDIR = '/var/log/dovetail/'
DEFAULT_LOGINTERVAL = 30
DEFAULT_LOGINTERVAL_UNIT = 'M'
DEFAULT_LOGFORMAT = (
    '%(asctime)s - %(filename)s - %(lineno)d - %(levelname)s - %(message)s')
DEFAULT_LOGBACKUPCOUNT = 10
WEB_LOGFILE = 'dovetail_web.log'
