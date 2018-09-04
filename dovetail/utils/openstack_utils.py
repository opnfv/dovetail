#!/usr/bin/env python
#
# Copyright (c) 2018 xudan16@huawei.com and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

import os_client_config
import shade
from shade import exc


class OS_Utils(object):

    def __init__(self, **kwargs):
        self.cloud = shade.OperatorCloud(os_client_config.get_config(**kwargs))
        self.images = []
        self.flavors = []

    def search_endpoints(self, interface='public'):
        try:
            res = self.cloud.search_endpoints(filters={'interface': interface})
            return True, res
        except exc.OpenStackCloudException as o_exc:
            return False, o_exc.orig_message

    def search_services(self, service_id=None):
        try:
            res = self.cloud.search_services(name_or_id=service_id)
            return True, res
        except exc.OpenStackCloudException as o_exc:
            return False, o_exc.orig_message
