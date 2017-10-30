##############################################################################
# Copyright (c) 2017
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
import logging
import json

from opnfv_testapi.resources import handlers
from opnfv_testapi.resources import sut_models
from opnfv_testapi.tornado_swagger import swagger

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)


class GenericSutHandler(handlers.GenericApiHandler):
    def __init__(self, application, request, **kwargs):
        super(GenericSutHandler, self).__init__(application,
                                                request,
                                                **kwargs)
        self.table = "suts"
        self.table_cls = sut_models.Sut


class HardwareHandler(GenericSutHandler):
    @swagger.operation(nickname="getHardwareById")
    def get(self, id):
        path = '/home/testapi/logs/{}/results/all_hosts_info.json'.format(id)
        with open(path) as f:
            data = json.load(f)
        hardware_info = {}
        for k, v in data.items():
            facts = v.get('ansible_facts', {})
            processors = facts.get('ansible_processor', {})

            try:
                processor_type = '{} {}'.format(processors[0], processors[1])
            except IndexError:
                LOG.exception('No Processor in SUT data')
                processor_type = None

            hardware_info[k] = {
                'processor_type': processor_type,
                'processor_cores': facts.get('ansible_processor_cores'),
                'processor_vcpus': facts.get('ansible_processor_vcpus'),
                'product_name': facts.get('ansible_product_name'),
                'product_version': facts.get('ansible_product_version')
            }

        self.write({'hardware_info': hardware_info})
