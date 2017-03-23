import requests
import json
import sys

db_host_ip = sys.argv[1]
testapi_port = sys.argv[2]

source_url = 'http://testresults.opnfv.org/test/api/v1'
target_url = 'http://{}:{}/api/v1'.format(db_host_ip, testapi_port)
print(target_url)


def get(url):
    return requests.get(url).json()


def post(url, data):
    headers = {'Content-Type': 'application/json'}
    res = requests.post(url, data=json.dumps(data), headers=headers)
    print(res.text)


def pod():
    source = '{}/pods'.format(source_url)
    target = '{}/pods'.format(target_url)

    pods = get(source)['pods']
    for p in pods:
        post(target, p)

    add_pod('master', 'metal')
    add_pod('virtual_136_2', 'virtual')


def project():
    source = '{}/projects'.format(source_url)
    target = '{}/projects'.format(target_url)

    projects = get(source)['projects']
    for p in projects:
        post(target, p)


def cases():
    project_list = ['yardstick', 'functest', 'dovetail']

    for p in project_list:
        source = '{}/projects/{}/cases'.format(source_url, p)
        target = '{}/projects/{}/cases'.format(target_url, p)

        cases = get(source)['testcases']
        for c in cases:
            post(target, c)


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


if __name__ == '__main__':
    pod()
    project()
    cases()




