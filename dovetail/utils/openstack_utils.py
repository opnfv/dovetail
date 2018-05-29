import json
import os_client_config
import shade
from shade import exc


class OS_Utils(object):

    def __init__(self, **kwargs):
        self.cloud = shade.OperatorCloud(os_client_config.get_config(**kwargs))
        self.images = []
        self.flavors = []

    def list_endpoints(self):
        try:
            res = self.cloud.search_endpoints()
            endpoints = json.dumps(res)
            return True, endpoints
        except exc.OpenStackCloudException as o_exc:
            return False, o_exc.orig_message
