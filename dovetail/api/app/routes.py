#!flask/bin/python

from flask import Flask, jsonify
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
