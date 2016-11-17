##############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

"""Exceptions for RESTful API."""
import traceback

from dovetail.api import app
from dovetail.api import utils


class HTTPException(Exception):

    def __init__(self, message, status_code):
        super(HTTPException, self).__init__(message)
        self.traceback = traceback.format_exc()
        self.status_code = status_code

    def to_dict(self):
        return {'message': str(self)}


class ItemNotFound(HTTPException):
    """Define the exception for referring non-existing object."""

    def __init__(self, message):
        super(ItemNotFound, self).__init__(message, 410)


class BadRequest(HTTPException):
    """Define the exception for invalid/missing parameters.

    User making a request in invalid state cannot be processed.
    """

    def __init__(self, message):
        super(BadRequest, self).__init__(message, 400)


class Unauthorized(HTTPException):
    """Define the exception for invalid user login."""

    def __init__(self, message):
        super(Unauthorized, self).__init__(message, 401)


class UserDisabled(HTTPException):
    """Define the exception for disabled users."""

    def __init__(self, message):
        super(UserDisabled, self).__init__(message, 403)


class Forbidden(HTTPException):
    """Define the exception for invalid permissions."""

    def __init__(self, message):
        super(Forbidden, self).__init__(message, 403)


class BadMethod(HTTPException):
    """Define the exception for invoking unsupported methods."""

    def __init__(self, message):
        super(BadMethod, self).__init__(message, 405)


class ConflictObject(HTTPException):
    """Define the exception for creating an existing object."""

    def __init__(self, message):
        super(ConflictObject, self).__init__(message, 409)


@app.errorhandler(Exception)
def handle_exception(error):
    if hasattr(error, 'to_dict'):
        response = error.to_dict()
    else:
        response = {'message': str(error)}
    if app.debug and hasattr(error, 'traceback'):
        response['traceback'] = error.traceback

    status_code = 400
    if hasattr(error, 'status_code'):
        status_code = error.status_code

        return utils.make_json_response(status_code, response)
