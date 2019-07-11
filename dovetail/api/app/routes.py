#!flask/bin/python

import json
import os
import subprocess
import time
import uuid

from flask import Flask, jsonify, request
from flask_cors import CORS

import server

app = Flask(__name__)
CORS(app)


@app.route('/api/v1/scenario/nfvi/testsuites', methods=['GET'])
def get_all_testsuites():
    testsuites = server.list_testsuites()
    return jsonify({'testsuites': testsuites}), 200


@app.route('/api/v1/scenario/nfvi/testcases', methods=['GET'])
def get_testcases():
    testcases = server.list_testcases()
    return jsonify({'testcases': testcases}), 200


@app.route('/api/v1/scenario/nfvi/execution', methods=['POST'])
def run_testcases():
    requestId = request.args.get('requestId')
    if not requestId:
        requestId = uuid.uuid1()
    if os.getenv('DOVETAIL_HOME'):
        dovetail_home = os.getenv('DOVETAIL_HOME')
    else:
        return 'No DOVETAIL_HOME found in env.\n', 500

    msg, ret = server.set_conf_files(request.json, dovetail_home, requestId)
    if not ret:
        return msg, 500

    msg, ret = server.set_vm_images(dovetail_home, requestId)
    if not ret:
        return msg, 500

    input_str = server.parse_request(request.json)

    repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                               os.pardir, os.pardir))
    run_script = os.path.join(repo_dir, 'run.py')

    cmd = 'python {} {}'.format(run_script, input_str)
    api_home = os.path.join(dovetail_home, str(requestId))
    subprocess.Popen(cmd, shell=True, env={'DOVETAIL_HOME': api_home})

    testcases_file = os.path.join(dovetail_home, str(requestId),
                                  'results', 'testcases.json')
    for loop in range(60):
        if not os.path.isfile(testcases_file):
            time.sleep(1)
        else:
            break
    else:
        return 'Can not get file testcases.json.\n', 500

    with open(testcases_file, "r") as f:
        for jsonfile in f:
            data = json.loads(jsonfile)
        testcases = data['testcases']
        testsuite = data['testsuite']

    result = server.get_execution_status(dovetail_home, testsuite,
                                         testcases, requestId)

    return jsonify({'result': result}), 200


@app.route('/api/v1/scenario/nfvi/execution/status/<exec_id>',
           methods=['POST'])
def get_testcases_status(exec_id):
    if 'testcases' not in request.json:
        return 'Need testcases list as input.\n', 400

    testcases = request.json['testcases']
    dovetail_home = os.getenv('DOVETAIL_HOME')

    testcases_file = os.path.join(dovetail_home, str(exec_id),
                                  'results', 'testcases.json')
    with open(testcases_file, "r") as f:
        for jsonfile in f:
            data = json.loads(jsonfile)
        testsuite = data['testsuite']

    result = server.get_execution_status(dovetail_home, testsuite,
                                         testcases, exec_id)
    return jsonify({'result': result}), 200
