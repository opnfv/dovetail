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
from mock import patch

from dovetail.utils.dovetail_config import DovetailConfig

__author__ = 'Stamatis Katsaounis <mokats@intracom-telecom.com>'


class DovetailConfigTesting(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch.object(DovetailConfig, 'update_non_envs')
    def test_update_config(self, mock_non_envs):
        config_dict = {'key': {'path': ['aa / bb/ cc'], 'value': 'val'}}
        dovetail_cfg = DovetailConfig()

        dovetail_cfg.update_config(config_dict)

        mock_non_envs.assert_called_once_with(['aa', 'bb', 'cc'], 'val')

    def test_set_leaf_dict(self):
        dict_to_test = {}
        dovetail_cfg = DovetailConfig()

        dovetail_cfg.set_leaf_dict(dict_to_test, ['aa', 'bb', 'cc'], 'val')

        self.assertEquals({'aa': {'bb': {'cc': 'val'}}}, dict_to_test)

    @patch.object(DovetailConfig, 'set_leaf_dict')
    @patch.object(DovetailConfig, 'dovetail_config')
    def test_update_non_envs(self, mock_cfg, mock_set_leaf):
        path = ['aa', 'bb', 'cc']
        value = 'val'
        dovetail_cfg = DovetailConfig()

        dovetail_cfg.update_non_envs(path, value)

        mock_set_leaf.assert_called_once_with(mock_cfg, path, value)
