##############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

from dovetail.utils import util
from dovetail.db import exception

BASE = declarative_base()


class MarkTimestamp(object):
    created = Column(DateTime, default=lambda: datetime.datetime.now())
    updated = Column(DateTime, default=lambda: datetime.datetime.now(),
                     onupdate=lambda: datetime.datetime.now())


class ModelHandler(object):

    def initialize(self):
        self.update()

    def update(self):
        pass

    @staticmethod
    def type_check(value, column_type):
        if value is None:
            return True
        if not hasattr(column_type, 'python_type'):
            return True
        column_python_type = column_type.python_type
        if isinstance(value, column_python_type):
            return True
        if issubclass(column_python_type, basestring):
            return isinstance(value, basestring)
        if column_python_type in [int, long]:
            return type(value) in [int, long]
        if column_python_type in [float]:
            return type(value) in [float]
        if column_python_type in [bool]:
            return type(value) in [bool]
        return False

    def validate(self):
        columns = self.__mapper__.columns
        for key, column in columns.items():
            value = getattr(self, key)
            if not self.type_check(value, column.type):
                raise exception.InvalidParameter(
                    'column %s value %r type is unexpected: %s' % (
                        key, value, column.type
                    )
                )

    def to_dict(self):
        """General function to convert record to dict.

        Convert all columns not starting with '_' to
        {<column_name>: <column_value>}
        """
        keys = self.__mapper__.columns.keys()
        dict_info = {}
        for key in keys:
            if key.startswith('_'):
                continue
            value = getattr(self, key)
            if value is not None:
                if isinstance(value, datetime.datetime):
                    value = util.format_datetime(value)
                dict_info[key] = value
        return dict_info


class Report(BASE, MarkTimestamp, ModelHandler):
    __tablename__ = 'report'
    id = Column(Integer, primary_key=True)
    test_id = Column(String(120), unique=True)
    name = Column(String(120))
    data = Column(String(64000))

    def __init__(self, test_id, data, name=None, **kwargs):
        self.name = name
        self.test_id = test_id
        self.data = data
        super(Report, self).__init__(**kwargs)

    def __repr__(self):
        return '<Report %r>' % (self.name)

    def __str__(self):
        return 'Report[%s:%s]' % (self.name, self.test_id)

    def to_dict(self):
        dict_info = super(Report, self).to_dict()
        dict_info['name'] = self.name
        dict_info['test_id'] = self.test_id
        dict_info['data'] = self.data
        return dict_info
