#!flask/bin/python

import os
import subprocess
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

    return jsonify({'result': 'ok'}), 200
