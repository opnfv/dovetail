import json
import os_client_config
import shade
from shade import exc


class OS_Utils(object):

    def __init__(self):
        self.cloud = shade.OperatorCloud(os_client_config.get_config())
        self.images = []
        self.flavors = []

    def list_admin_endpoints(self):
        try:
            res = self.cloud.search_endpoints(filters={"interface": 'admin'})
            endpoints = json.dumps(res)
            return True, endpoints
        except exc.OpenStackCloudException as o_exc:
            return False, o_exc.orig_message
