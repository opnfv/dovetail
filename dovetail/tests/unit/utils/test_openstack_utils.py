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
import munch
import os_client_config
import shade

import dovetail.utils.openstack_utils as os_dovetail_utils

__author__ = 'Stamatis Katsaounis <mokats@intracom-telecom.com>'


class OpenStackUtilsTesting(unittest.TestCase):

    def setUp(self):
        self.patcher1 = patch.object(shade,
                                     'OperatorCloud', autospec=True)
        self.patcher2 = patch.object(os_client_config,
                                     'get_config', autospec=True)
        self.cloud = self.patcher1.start().return_value
        self.os_client_config = self.patcher2.start().return_value
        self.os_dovetail = os_dovetail_utils.OS_Utils()

    def tearDown(self):
        self.patcher1.stop()
        self.patcher2.stop()

    def test_search_endpoints(self):
        endpoint = munch.Munch({u'region_id': u'RegionOne',
                                u'url': u'http://127.0.0.1:8977/',
                                u'region': u'RegionOne',
                                u'enabled': True,
                                u'interface': u'public',
                                u'service_id': u'123456',
                                u'id': u'123456'})
        endpoints = [endpoint]
        self.cloud.search_endpoints.return_value = endpoints

        expected = (True, endpoints)
        result = self.os_dovetail.search_endpoints()

        self.assertEqual(expected, result)

    def test_search_endpoints_raised_exception(self):
        errorMSG = 'Exception was raised'
        exception = shade.exc.OpenStackCloudException(errorMSG)
        self.cloud.search_endpoints.side_effect = exception

        expected = (False, errorMSG)
        result = self.os_dovetail.search_endpoints()

        self.assertEqual(expected, result)

    def test_search_services(self):
        service = munch.Munch({'description': u'OpenStack Identity Service',
                               'service_type': u'identity',
                               'type': u'identity',
                               'enabled': True,
                               'id': u'1bd26028c8714f3bb726126dc1ea62fc',
                               'name': u'keystone'})
        services = [service]
        self.cloud.search_services.return_value = services

        expected = (True, services)
        result = self.os_dovetail.search_services()

        self.assertEqual(expected, result)

    def test_search_services_raised_exception(self):
        errorMSG = 'Exception was raised'
        exception = shade.exc.OpenStackCloudException(errorMSG)
        self.cloud.search_services.side_effect = exception

        expected = (False, errorMSG)
        result = self.os_dovetail.search_services()

        self.assertEqual(expected, result)
