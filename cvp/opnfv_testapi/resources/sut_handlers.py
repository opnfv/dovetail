##############################################################################
# Copyright (c) 2017
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
import logging
import json
import os

from opnfv_testapi.resources import handlers
from opnfv_testapi.resources import sut_models
from opnfv_testapi.tornado_swagger import swagger

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)

RESULT_PATH = '/home/testapi/logs/{}/results'


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
        endpoint_info = self._read_endpoint_info(id)
        LOG.debug('Endpoint info: %s', endpoint_info)

        all_info = self._read_sut_info(id)
        LOG.debug('All SUT info: %s', all_info)

        hardware_info = {k: self._get_single_host_info(v)
                         for k, v in all_info.items()}
        LOG.debug('SUT info: %s', hardware_info)

        data = {
            'endpoint_info': endpoint_info,
            'hardware_info': hardware_info
        }

        self.write(data)

    def _read_endpoint_info(self, id):
        path = os.path.join(RESULT_PATH.format(id), 'endpoint_info.json')
        try:
            with open(path) as f:
                endpoint_info = json.load(f)
        except Exception:
            endpoint_info = []

        return endpoint_info

    def _read_sut_info(self, id):
        path = os.path.join(RESULT_PATH.format(id), 'all_hosts_info.json')
        try:
            with open(path) as f:
                all_info = json.load(f)
        except Exception:
            all_info = {}
        return all_info

    def _get_single_host_info(self, single_info):
        info = []
        facts = single_info.get('ansible_facts', {})

        info.append(['hostname', facts.get('ansible_hostname')])

        info.append(['product_name', facts.get('ansible_product_name')])
        info.append(['product_version', facts.get('ansible_product_version')])

        processors = facts.get('ansible_processor', [])
        try:
            processor_type = '{} {}'.format(processors[0], processors[1])
        except IndexError:
            LOG.exception('No Processor in SUT data')
            processor_type = None
        info.append(['processor_type', processor_type])
        info.append(['architecture', facts.get('ansible_architecture')])
        info.append(['processor_cores', facts.get('ansible_processor_cores')])
        info.append(['processor_vcpus', facts.get('ansible_processor_vcpus')])

        memory = facts.get('ansible_memtotal_mb')
        memory = round(memory * 1.0 / 1024, 2) if memory else None
        info.append(['memory', '{} GB'.format(memory)])

        devices = facts.get('ansible_devices', {})
        info.extend([self._get_device_info(k, v) for k, v in devices.items()])

        lsb_description = facts.get('ansible_lsb', {}).get('description')
        info.append(['OS', lsb_description])

        interfaces = facts.get('ansible_interfaces')
        info.append(['interfaces', interfaces])
        info.extend([self._get_interface_info(facts, i) for i in interfaces])
        info = [i for i in info if i]

        return info

    def _get_interface_info(self, facts, name):
        mac = facts.get('ansible_{}'.format(name), {}).get('macaddress')
        return [name, mac] if mac else []

    def _get_device_info(self, name, info):
        return ['disk_{}'.format(name), info.get('size')]
