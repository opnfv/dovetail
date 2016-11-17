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
def store_report(
        test_id, data,
        exception_when_existing=True,
        name=None, session=None, **kwargs):
    """Storing results into database.

    :param results: Dict describes test results.
    """
    report = utils.add_db_object(
        session, models.Report, exception_when_existing,
        test_id, data, name,
        **kwargs
    )

    return report


@database.run_in_session()
@utils.wrap_to_dict()
def list_reports(session=None, **filters):
    logging.debug('session:%s' % session)
    reports = utils.list_db_objects(
        session, models.Report, **filters
    )
    return reports


@database.run_in_session()
@utils.wrap_to_dict()
def get_report(test_id, exception_when_missing=True,
               session=None, **kwargs):

    return _get_report(test_id, session,
                       exception_when_missing=exception_when_missing, **kwargs)


def _get_report(test_id, session=None, **kwargs):
    return utils.get_db_object(
        session, models.Report, test_id=test_id, **kwargs)


@database.run_in_session()
def del_report(test_id, session=None, **kwargs):

    return utils.del_db_objects(session, models.Report,
                                test_id=test_id, **kwargs)
