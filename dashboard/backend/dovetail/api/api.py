##############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import logging

from dovetail.api import utils
from dovetail.api import exception_handler
from dovetail.db import api as db_api

from flask import Flask
from flask import request

import json

app = Flask(__name__)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add(
        'Access-Control-Allow-Headers',
        'Content-Type, Authorization')
    response.headers.add('Aceess-Control-Allow-Methods', 'GET,PUT,DELETE,POST')
    return response

# test


@app.route("/test", methods=['GET'])
def test():
    """backend api test"""
    logging.info('test functest')
    resp = utils.make_json_response(
        200, {'test': 20}
    )
    return resp


# settings
@app.route("/clear", methods=['POST'])
def clear_settings():
    """ clear all settings data on backend server """
    logging.info('clear all settings')

    return utils.make_json_response(
        200, {}
    )


@app.route("/settings", methods=['GET'])
def list_settings():
    """list settings"""
    logging.info('list settings')
    global settings
    return utils.make_json_response(200, settings)


@app.route("/settings", methods=['POST'])
def add_settings():
    pass


@app.route("/settings", methods=['POST'])
def remove_settings():
    pass


@app.route("/testcases", methods=['GET'])
def get_testcases():
    pass


@app.route("/results/<test_id>", methods=['GET'])
def show_result(test_id):
    data = _get_request_args()
    return utils.make_json_response(
        200,
        db_api.get_result(
            test_id, **data
        )
    )


@app.route("/results", methods=['GET'])
def list_results():
    data = _get_request_args()
    return utils.make_json_response(
        200,
        db_api.list_results(
            **data
        )
    )


@app.route("/results", methods=['POST'])
def add_result():
    data = _get_request_data()
    ret_code = 200
    json_object = json.loads(data)
    logging.debug('json_object:%s' % (json_object))
    if not db_api.store_result(**json_object):
        ret_code = 500
    resp = utils.make_json_response(
        ret_code, data
    )
    return resp


@app.route("/results/<test_id>", methods=['DELETE'])
def remove_results(test_id):
    data = _get_request_data()
    logging.debug('data:%s' % data)
    response = db_api.del_result(
        test_id, **data
    )
    return utils.make_json_response(
        200, response
    )


def _get_request_data():
    """Convert reqeust data from string to python dict.

    If the request data is not json formatted, raises
    exception_handler.BadRequest.
    If the request data is not json formatted dict, raises
    exception_handler.BadRequest
    If the request data is empty, return default as empty dict.

    Usage: It is used to add or update a single resource.
    """
    if request.data:
        try:
            data = json.loads(request.data)
        except Exception:
            raise exception_handler.BadRequest(
                'request data is not json formatted: %s' % request.data
            )
        if not isinstance(data, dict):
            raise exception_handler.BadRequest(
                'request data is not json formatted dict: %s' % request.data
            )

        return request.data
    else:
        return {}


def _get_request_args(**kwargs):
    """Get request args as dict.

    The value in the dict is converted to expected type.

    Args:
       kwargs: for each key, the value is the type converter.
    """
    args = dict(request.args)
    for key, value in args.items():
        if key in kwargs:
            converter = kwargs[key]
            if isinstance(value, list):
                args[key] = [converter(item) for item in value]
            else:
                args[key] = converter(value)
    return args

'''
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
'''
# user login/logout

if __name__ == '__main__':
    app.run(host='127.0.0.1')
