##############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
from dovetail.utils import flags
from dovetail.utils import logsetting
from dovetail.utils import setting_wrapper as setting

from dovetail.api.api import app

import os
import logging

gunicorn_error_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.DEBUG)

# flags.init()
# logdir = setting.DEFAULT_LOGDIR
curr_path = os.path.dirname(os.path.abspath(__file__))
logdir = os.path.join(curr_path, 'log')
if not os.path.exists(logdir):
    os.makedirs(logdir)

flags.OPTIONS.logdir = logdir
flags.OPTIONS.logfile = setting.WEB_LOGFILE
logsetting.init()


if __name__ == "__main__":
    app.run()
