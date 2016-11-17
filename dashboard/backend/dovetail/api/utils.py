##############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import json
from flask import make_response


def make_json_response(status_code, data):
    """Wrap json format to the reponse object."""

    result = json.dumps(data, indent=4, default=lambda x: None) + '\r\n'
    resp = make_response(result, status_code)
    resp.headers['Content-type'] = 'application/json'
    return resp
