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


source_url = 'http://116.66.187.136:9999/api/v1'


def get(url):
    try:
        ret = requests.get(url)
        return ret.json()
    except:
        return None


def pod():
    source = '{}/pods'.format(source_url)
    try:
        pods = get(source)['pods']
        with open("pods.json", "w") as f:
            f.write(json.dumps(pods, indent=4))
    except:
        return


def project():
    source = '{}/projects'.format(source_url)

    try:
        projects = get(source)['projects']
        with open("projects.json", "w") as f:
            f.write(json.dumps(projects, indent=4))
    except:
        return

    for p in projects:
        source = '{}/projects/{}/cases'.format(source_url, p['name'])
        print(p['name'])
        print(source)
        try:
            cases = get(source)
            with open("cases.json", "a+") as f:
                f.write(json.dumps(cases))
                f.write('\n')
                f.close()
        except:
            print("useless data")


if __name__ == '__main__':
    pod()
    project()
