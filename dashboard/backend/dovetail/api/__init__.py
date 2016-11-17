##############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import datetime
import logging

from flask import Flask

from dovetail.utils import util

logging.info('flask app: begin to init')

app = Flask(__name__)
app.debug = True
logging.info('flask app config:%s', app.config)

app.config['REMEMBER_COOKIE_DURATION'] = (
    datetime.timedelta(
        seconds=util.parse_time_interval('2h')
    )
)

logging.info('flask app: finish init')
