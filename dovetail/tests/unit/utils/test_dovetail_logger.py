#!/usr/bin/env python
#
# Copyright (c) 2018 mokats@intracom-telecom.com and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##

import unittest
from mock import patch, call, Mock

from dovetail.utils import dovetail_utils
from dovetail.utils.dovetail_logger import Logger

__author__ = 'Stamatis Katsaounis <mokats@intracom-telecom.com>'


class DovetailLoggerTesting(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch('sys.stdout')
    @patch('dovetail.utils.dovetail_logger.os')
    @patch('dovetail.utils.dovetail_logger.logging')
    def test_logger_info(self, mock_logging, mock_os, mock_stdout):
        file_path = 'file_path'
        level_const_info = 'INFO'
        level_const_debug = 'DEBUG'
        logger = Mock()
        mock_os.getenv.return_value = 'False'
        mock_logging.INFO = level_const_info
        mock_logging.DEBUG = level_const_debug
        mock_logging.getLogger.return_value = logger
        dovetail_utils.dt_cfg.dovetail_config = {'result_dir': file_path}
        mock_os.path.exists.return_value = False
        stream_handler_obj = Mock()
        formatter_obj = Mock()
        file_handler_obj = Mock()
        mock_logging.StreamHandler.return_value = stream_handler_obj
        mock_logging.Formatter.return_value = formatter_obj
        mock_logging.FileHandler.return_value = file_handler_obj

        logger_name = 'name'
        dovetail_logger = Logger(logger_name)
        mock_logging.getLogger.assert_called_once_with(logger_name)
        self.assertEquals(dovetail_logger.logger.propagate, 0)
        logger.setLevel.assert_called_once_with(level_const_debug)
        mock_os.path.exists.assert_called_once_with(file_path)
        # mock_os.makedirs.assert_called_once_with(file_path)
        mock_logging.Formatter.assert_called_once_with(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        stream_handler_obj.setFormatter.assert_called_once_with(formatter_obj)
        stream_handler_obj.setLevel.assert_called_once_with(level_const_info)
        file_handler_obj.setLevel.assert_called_once_with(level_const_info)
        logger.addHandler.assert_has_calls([
            call(stream_handler_obj), call(file_handler_obj)])
        self.assertEquals(dovetail_logger.getLogger(), logger)

    @patch('sys.stdout')
    @patch('dovetail.utils.dovetail_logger.os')
    @patch('dovetail.utils.dovetail_logger.logging')
    def test_logger_debug(self, mock_logging, mock_os, mock_stdout):
        file_path = 'file_path'
        level_const_debug = 'DEBUG'
        logger = Mock()
        mock_os.getenv.return_value = 'True'
        mock_logging.DEBUG = level_const_debug
        mock_logging.getLogger.return_value = logger
        dovetail_utils.dt_cfg.dovetail_config = {'result_dir': file_path}
        mock_os.path.exists.return_value = False
        stream_handler_obj = Mock()
        formatter_obj = Mock()
        file_handler_obj = Mock()
        mock_logging.StreamHandler.return_value = stream_handler_obj
        mock_logging.Formatter.return_value = formatter_obj
        mock_logging.FileHandler.return_value = file_handler_obj

        logger_name = 'name'
        dovetail_logger = Logger(logger_name)
        mock_logging.getLogger.assert_called_once_with(logger_name)
        self.assertEquals(dovetail_logger.logger.propagate, 0)
        logger.setLevel.assert_called_once_with(level_const_debug)
        mock_os.path.exists.assert_called_once_with(file_path)
        # mock_os.makedirs.assert_called_once_with(file_path)
        mock_logging.Formatter.assert_called_once_with(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        stream_handler_obj.setFormatter.assert_called_once_with(formatter_obj)
        stream_handler_obj.setLevel.assert_called_once_with(level_const_debug)
        file_handler_obj.setLevel.assert_called_once_with(level_const_debug)
        logger.addHandler.assert_has_calls([
            call(stream_handler_obj), call(file_handler_obj)])
        self.assertEquals(dovetail_logger.getLogger(), logger)
