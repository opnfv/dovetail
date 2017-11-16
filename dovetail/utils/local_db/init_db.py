##############################################################################
# Copyright (c) 2016 HUAWEI TECHNOLOGIES CO.,LTD and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import requests
import json
import sys
import os

db_host_ip = sys.argv[1]
testapi_port = sys.argv[2]

target_url = 'http://{}:{}/api/v1'.format(db_host_ip, testapi_port)
dir_path = os.path.dirname(os.path.realpath(__file__))


def get(url):
    return requests.get(url).json()


def post(url, data):
    headers = {'Content-Type': 'application/json'}
    res = requests.post(url, data=json.dumps(data), headers=headers)
    try:
        status_code = vars(res)["status_code"]
        if (status_code == 403 and "Already Exists" in vars(res)["_content"]) \
            or status_code == 200:
            return
        else:
            print(res.text)
    except Exception as e:
        print("Error: exception {}.".format(e))


def pod():
    target = '{}/pods'.format(target_url)

    with open(os.path.join(dir_path, 'pods.json'), 'r') as f:
        pods = json.load(f)
    for p in pods:
        post(target, p)


def project():
    target = '{}/projects'.format(target_url)
    with open(os.path.join(dir_path, 'projects.json'), 'r') as f:
        projects = json.load(f)
    for p in projects:
        post(target, p)


def cases():
    with open(os.path.join(dir_path, 'cases.json'), 'r') as f:
        for line in f:
            try:
                cases = json.loads(line)
                for c in cases["testcases"]:
                    target = '{}/projects/{}/cases'.format(target_url,
                                                           c['project_name'])
                    post(target, c)
            except:
                print("useless data")
    add_case("functest", "tempest_custom")
    add_case("sdnvpn", "functest_testcase_4")
    add_case("sdnvpn", "functest_testcase_8")


def add_pod(name, mode):
    data = {
        "role": "",
        "name": name,
        "details": '',
        "mode": mode,
        "creation_date": "2017-2-23 11:23:03.765581"
    }
    pod_url = '{}/pods'.format(target_url)
    post(pod_url, data)


def add_case(project, case):
    data = {
        "project_name": project,
        "name": case,
    }
    case_url = '{}/projects/{}/cases'.format(target_url, project)
    post(case_url, data)


if __name__ == '__main__':
    pod()
    project()
    cases()
