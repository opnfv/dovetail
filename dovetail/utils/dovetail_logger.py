#!/usr/bin/env python
#
# Copyright (c) 2018 jose.lausuch@ericsson.com and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Logging levels:
#  Level     Numeric value
#  CRITICAL  50
#  ERROR     40
#  WARNING   30
#  INFO      20
#  DEBUG     10
#  NOTSET    0
#
# Usage:
#  import dovetail_logger as dl
#  logger = dl.Logger("script_name").getLogger()
#  logger.info("message to be shown with - INFO - ")
#  logger.debug("message to be shown with - DEBUG -")

import logging
import os
import sys

from dovetail_config import DovetailConfig as dt_cfg


class Logger(object):
    def __init__(self, logger_name):

        DEBUG = os.getenv('DEBUG')

        self.logger = logging.getLogger(logger_name)
        self.logger.propagate = 0
        self.logger.setLevel(logging.DEBUG)

        result_path = dt_cfg.dovetail_config['result_dir']
        if not os.path.exists(result_path):
            os.makedirs(result_path)

        ch = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s - %(name)s - '
                                      '%(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        hdlr = logging.FileHandler(os.path.join(result_path, 'dovetail.log'))
        hdlr.setFormatter(formatter)
        if DEBUG is not None and DEBUG.lower() == "true":
            ch.setLevel(logging.DEBUG)
            hdlr.setLevel(logging.DEBUG)
        else:
            ch.setLevel(logging.INFO)
            hdlr.setLevel(logging.INFO)
        self.logger.addHandler(ch)
        self.logger.addHandler(hdlr)

    def getLogger(self):
        return self.logger
