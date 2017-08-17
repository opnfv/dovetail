##############################################################################
# Copyright (c) 2016 HUAWEI TECHNOLOGIES CO.,LTD and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


import requests
import datetime
import json
import yaml
import sys

base_url = sys.argv[1]
headers = {'Content-Type': 'application/json'}


def create_project():

    name = 'dovetail'
    s = '2015-10-14 06:56:09'
    time = datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S')

    data = {
        'name': name,
        'creation_date': str(time),
        'description': ''
    }

    url = '{}/projects'.format(base_url)
    requests.post(url, data=json.dumps(data), headers=headers)


def dovetail():
    with open('../../compliance/proposed_tests.yml') as f:
        data = yaml.safe_load(f)['proposed_tests']['testcases_list']

    url = '{}/projects/dovetail/cases'.format(base_url)
    for case in data:
        c = {
            'ci_loop': 'daily',
            'description': 'dovetail',
            'name': case,
            'project_name': 'dovetail',
            'trust': 'gold',
            'url': '',
            'version': 'master',
            'domains': 'master',
            'tags': 'dovetail'
        }
        requests.post(url, data=json.dumps(c), headers=headers)


if __name__ == '__main__':
    create_project()
    dovetail()
