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
        all_info = self._read_sut_info(id)
        LOG.debug('All SUT info: %s', all_info)

        hardware_info = {k: self._get_single_host_info(v)
                         for k, v in all_info.items()}
        LOG.debug('SUT info: %s', hardware_info)

        self.write({'hardware_info': hardware_info})

    def _read_sut_info(self, id):
        path = '/home/testapi/logs/{}/results/all_hosts_info.json'.format(id)
        with open(path) as f:
            all_info = json.load(f)
        return all_info

    def _get_single_host_info(self, single_info):
        info = []
        facts = single_info.get('ansible_facts', {})

        info.append(['product_name', facts.get('ansible_product_name')])
        info.append(['product_version', facts.get('ansible_product_version')])

        processors = facts.get('ansible_processor', {})
        try:
            processor_type = '{} {}'.format(processors[0], processors[1])
        except IndexError:
            LOG.exception('No Processor in SUT data')
            processor_type = None
        info.append(['processor_type', processor_type])
        info.append(['architecture', facts.get('ansible_architecture')])
        info.append(['processor_cores', facts.get('ansible_processor_cores')])
        info.append(['processor_vcpus', facts.get('ansible_processor_vcpus')])

        info.append(['memorysize', facts.get('facter_memorysize')])

        devices = facts.get('ansible_devices', {})
        info.extend([['disk_{}'.format(k), v['size']]
                    for k, v in devices.items()])

        info.append(['system', facts.get('facter_lsbdistdescription')])

        return info
