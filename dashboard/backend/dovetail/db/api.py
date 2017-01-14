##############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

"""
Defines interface for DB access.
"""

import logging

from dovetail.db import database
from dovetail.db import utils
from dovetail.db import models


@database.run_in_session()
def store_result(exception_when_existing=True,
                 session=None, **kwargs):
    """Storing results into database.

    :param data: Dict describes test results.
    """
    logging.debug('store_result:%s', kwargs)
    result = utils.add_db_object(
        session, models.Result, exception_when_existing,
        **kwargs)

    return result


@database.run_in_session()
@utils.wrap_to_dict()
def list_results(session=None, **filters):
    """Get all results
    """
    logging.debug('session:%s', session)
    results = utils.list_db_objects(
        session, models.Result, **filters
    )
    return results


@database.run_in_session()
@utils.wrap_to_dict()
def get_result(test_id, exception_when_missing=True,
               session=None, **kwargs):
    """Get specific result with the test_id

    :param test_id: the unique serial number for the test
    """
    return _get_result(test_id, session,
                       exception_when_missing=exception_when_missing, **kwargs)


def _get_result(test_id, session=None, **kwargs):
    return utils.get_db_object(
        session, models.Result, test_id=test_id, **kwargs)


@database.run_in_session()
def del_result(test_id, session=None, **kwargs):
    """Delete a results from database

    :param test_id: the unique serial number for the test
    """
    return utils.del_db_objects(session, models.Result,
                                test_id=test_id, **kwargs)
