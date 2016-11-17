##############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

"""Utilities for database."""


import functools
import inspect
import logging

from sqlalchemy import and_
from sqlalchemy import or_

from dovetail.db import exception
from dovetail.db import models


def add_db_object(session, table, exception_when_existing=True,
                  *args, **kwargs):
    """Create db object.

    If not exception_when_existing and the db object exists,
    Instead of raising exception, updating the existing db object.
    """
    if not session:
        raise exception.DatabaseException('session param is None')
    with session.begin(subtransactions=True):
        logging.debug(
            'session %s add object %s atributes %s to table %s',
            id(session), args, kwargs, table.__name__)
        argspec = inspect.getargspec(table.__init__)
        arg_names = argspec.args[1:]
        arg_defaults = argspec.defaults
        if not arg_defaults:
            arg_defaults = []
        if not (
            len(arg_names) - len(arg_defaults) <= len(args) <= len(arg_names)
        ):
            raise exception.InvalidParameter(
                'arg names %s does not match arg values %s' % (
                    arg_names, args)
            )
        db_keys = dict(zip(arg_names, args))
        logging.debug('db_keys:%s' % db_keys)
        if db_keys:
            db_object = session.query(table).filter_by(**db_keys).first()
        else:
            logging.debug('db object is None')
            db_object = None

        new_object = False
        if db_object:
            logging.debug(
                'got db object %s: %s', db_keys, db_object
            )
            if exception_when_existing:
                raise exception.DuplicatedRecord(
                    '%s exists in table %s' % (db_keys, table.__name__)
                )
        else:
            db_object = table(**db_keys)
            new_object = True

        for key, value in kwargs.items():
            setattr(db_object, key, value)

        logging.debug('db_object:%s' % db_object)
        if new_object:
            session.add(db_object)
        session.flush()
        db_object.initialize()
        db_object.validate()
        logging.debug(
            'session %s db object %s added', id(session), db_object
        )
        return db_object


def list_db_objects(session, table, order_by=[], **filters):
    """List db objects.

    If order by given, the db objects should be sorted by the ordered keys.
    """
    if not session:
        raise exception.DatabaseException('session param is None')
    with session.begin(subtransactions=True):
        logging.debug(
            'session %s list db objects by filters %s in table %s',
            id(session), filters, table.__name__
        )
        db_objects = model_order_by(
            model_filter(
                model_query(session, table),
                table,
                **filters
            ),
            table,
            order_by
        ).all()
        logging.debug(
            'session %s got listed db objects: %s',
            id(session), db_objects
        )
        return db_objects


def get_db_object(session, table, exception_when_missing=True, **kwargs):
    """Get db object.

    If not exception_when_missing and the db object can not be found,
    return None instead of raising exception.
    """
    if not session:
        raise exception.DatabaseException('session param is None')
    with session.begin(subtransactions=True):
        logging.debug(
            'session %s get db object %s from table %s',
            id(session), kwargs, table.__name__)
        db_object = model_filter(
            model_query(session, table), table, **kwargs
        ).first()
        logging.debug(
            'session %s got db object %s', id(session), db_object
        )
        if db_object:
            return db_object

        if not exception_when_missing:
            return None

        raise exception.RecordNotExists(
            'Cannot find the record in table %s: %s' % (
                table.__name__, kwargs
            )
        )


def del_db_objects(session, table, **filters):
    """delete db objects."""
    if not session:
        raise exception.DatabaseException('session param is None')
    with session.begin(subtransactions=True):
        logging.debug(
            'session %s delete db objects by filters %s in table %s',
            id(session), filters, table.__name__
        )
        query = model_filter(
            model_query(session, table), table, **filters
        )
        db_objects = query.all()
        query.delete(synchronize_session=False)
        logging.debug(
            'session %s db objects %s deleted', id(session), db_objects
        )
        return db_objects


def model_order_by(query, model, order_by):
    """append order by into sql query model."""
    if not order_by:
        return query
    order_by_cols = []
    for key in order_by:
        if isinstance(key, tuple):
            key, is_desc = key
        else:
            is_desc = False
        if isinstance(key, basestring):
            if hasattr(model, key):
                col_attr = getattr(model, key)
            else:
                continue
        else:
            col_attr = key
        if is_desc:
            order_by_cols.append(col_attr.desc())
        else:
            order_by_cols.append(col_attr)
    return query.order_by(*order_by_cols)


def _model_condition(col_attr, value):
    """Generate condition for one column.

    Example for col_attr is name:
        value is 'a': name == 'a'
        value is ['a']: name == 'a'
        value is ['a', 'b']: name == 'a' or name == 'b'
        value is {'eq': 'a'}: name == 'a'
        value is {'lt': 'a'}: name < 'a'
        value is {'le': 'a'}: name <= 'a'
        value is {'gt': 'a'}: name > 'a'
        value is {'ge': 'a'}: name >= 'a'
        value is {'ne': 'a'}: name != 'a'
        value is {'in': ['a', 'b']}: name in ['a', 'b']
        value is {'notin': ['a', 'b']}: name not in ['a', 'b']
        value is {'startswith': 'abc'}: name like 'abc%'
        value is {'endswith': 'abc'}: name like '%abc'
        value is {'like': 'abc'}: name like '%abc%'
        value is {'between': ('a', 'c')}: name >= 'a' and name <= 'c'
        value is [{'lt': 'a'}]: name < 'a'
        value is [{'lt': 'a'}, {'gt': c'}]: name < 'a' or name > 'c'
        value is {'lt': 'c', 'gt': 'a'}: name > 'a' and name < 'c'

    If value is a list, the condition is the or relationship among
    conditions of each item.
    If value is dict and there are multi keys in the dict, the relationship
    is and conditions of each key.
    Otherwise the condition is to compare the column with the value.
    """
    if isinstance(value, list):
        basetype_values = []
        composite_values = []
        for item in value:
            if isinstance(item, (list, dict)):
                composite_values.append(item)
            else:
                basetype_values.append(item)
        conditions = []
        if basetype_values:
            if len(basetype_values) == 1:
                condition = (col_attr == basetype_values[0])
            else:
                condition = col_attr.in_(basetype_values)
            conditions.append(condition)
        for composite_value in composite_values:
            condition = _model_condition(col_attr, composite_value)
            if condition is not None:
                conditions.append(condition)
        if not conditions:
            return None
        if len(conditions) == 1:
            return conditions[0]
        return or_(*conditions)
    elif isinstance(value, dict):
        conditions = []
        if 'eq' in value:
            conditions.append(_model_condition_func(
                col_attr, value['eq'],
                lambda attr, data: attr == data,
                lambda attr, data, item_condition_func: attr.in_(data)
            ))
        if 'lt' in value:
            conditions.append(_model_condition_func(
                col_attr, value['lt'],
                lambda attr, data: attr < data,
                _one_item_list_condition_func
            ))
        if 'gt' in value:
            conditions.append(_model_condition_func(
                col_attr, value['gt'],
                lambda attr, data: attr > data,
                _one_item_list_condition_func
            ))
        if 'le' in value:
            conditions.append(_model_condition_func(
                col_attr, value['le'],
                lambda attr, data: attr <= data,
                _one_item_list_condition_func
            ))
        if 'ge' in value:
            conditions.append(_model_condition_func(
                col_attr, value['ge'],
                lambda attr, data: attr >= data,
                _one_item_list_condition_func
            ))
        if 'ne' in value:
            conditions.append(_model_condition_func(
                col_attr, value['ne'],
                lambda attr, data: attr != data,
                lambda attr, data, item_condition_func: attr.notin_(data)
            ))
        if 'in' in value:
            conditions.append(col_attr.in_(value['in']))
        if 'notin' in value:
            conditions.append(col_attr.notin_(value['notin']))
        if 'startswith' in value:
            conditions.append(_model_condition_func(
                col_attr, value['startswith'],
                lambda attr, data: attr.like('%s%%' % data)
            ))
        if 'endswith' in value:
            conditions.append(_model_condition_func(
                col_attr, value['endswith'],
                lambda attr, data: attr.like('%%%s' % data)
            ))
        if 'like' in value:
            conditions.append(_model_condition_func(
                col_attr, value['like'],
                lambda attr, data: attr.like('%%%s%%' % data)
            ))
        conditions = [
            condition
            for condition in conditions
            if condition is not None
        ]
        if not conditions:
            return None
        if len(conditions) == 1:
            return conditions[0]
        return and_(conditions)
    else:
        condition = (col_attr == value)
        return condition


def _default_list_condition_func(col_attr, value, condition_func):
    """The default condition func for a list of data.

    Given the condition func for single item of data, this function
    wrap the condition_func and return another condition func using
    or_ to merge the conditions of each single item to deal with a
    list of data item.

    Args:
       col_attr: the colomn name
       value: the column value need to be compared.
       condition_func: the sqlalchemy condition object like ==

    Examples:
       col_attr is name, value is ['a', 'b', 'c'] and
       condition_func is ==, the returned condition is
       name == 'a' or name == 'b' or name == 'c'
    """
    conditions = []
    for sub_value in value:
        condition = condition_func(col_attr, sub_value)
        if condition is not None:
            conditions.append(condition)
    if conditions:
        return or_(*conditions)
    else:
        return None


def _one_item_list_condition_func(col_attr, value, condition_func):
    """The wrapper condition func to deal with one item data list.

    For simplification, it is used to reduce generating too complex
    sql conditions.
    """
    if value:
        return condition_func(col_attr, value[0])
    else:
        return None


def _model_condition_func(
    col_attr, value,
    item_condition_func,
    list_condition_func=_default_list_condition_func
):
    """Return sql condition based on value type."""
    if isinstance(value, list):
        if not value:
            return None
        if len(value) == 1:
            return item_condition_func(col_attr, value)
        return list_condition_func(
            col_attr, value, item_condition_func
        )
    else:
        return item_condition_func(col_attr, value)


def model_filter(query, model, **filters):
    """Append conditons to query for each possible column."""
    for key, value in filters.items():
        if isinstance(key, basestring):
            if hasattr(model, key):
                col_attr = getattr(model, key)
            else:
                continue
        else:
            col_attr = key

        condition = _model_condition(col_attr, value)
        if condition is not None:
            query = query.filter(condition)
    return query


def model_query(session, model):
    """model query.

    Return sqlalchemy query object.
    """
    if not issubclass(model, models.BASE):
        raise exception.DatabaseException("model should be sublass of BASE!")

    return session.query(model)


def wrap_to_dict(support_keys=[], **filters):
    """Decrator to convert returned object to dict.

    The details is decribed in _wrapper_dict.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return _wrapper_dict(
                func(*args, **kwargs), support_keys, **filters
            )
        return wrapper
    return decorator


def _wrapper_dict(data, support_keys, **filters):
    """Helper for warpping db object into dictionary.

    If data is list, convert it to a list of dict
    If data is Base model, convert it to dict
    for the data as a dict, filter it with the supported keys.
    For each filter_key, filter_value  in filters, also filter
    data[filter_key] by filter_value recursively if it exists.

    Example:
       data is models.Switch, it will be converted to
       {
           'id': 1, 'ip': '10.0.0.1', 'ip_int': 123456,
           'credentials': {'version': 2, 'password': 'abc'}
       }
       Then if support_keys are ['id', 'ip', 'credentials'],
       it will be filtered to {
           'id': 1, 'ip': '10.0.0.1',
           'credentials': {'version': 2, 'password': 'abc'}
       }
       Then if filters is {'credentials': ['version']},
       it will be filtered to {
           'id': 1, 'ip': '10.0.0.1',
           'credentials': {'version': 2}
       }
    """
    logging.debug(
        'wrap dict %s by support_keys=%s filters=%s',
        data, support_keys, filters
    )
    if isinstance(data, list):
        return [
            _wrapper_dict(item, support_keys, **filters)
            for item in data
        ]
    if isinstance(data, models.ModelHandler):
        data = data.to_dict()
    if not isinstance(data, dict):
        raise exception.InvalidResponse(
            'response %s type is not dict' % data
        )
    info = {}
    try:
        if len(support_keys) == 0:
            support_keys = data.keys()
        for key in support_keys:
            if key in data and data[key] is not None:
                if key in filters:
                    filter_keys = filters[key]
                    if isinstance(filter_keys, dict):
                        info[key] = _wrapper_dict(
                            data[key], filter_keys.keys(),
                            **filter_keys
                        )
                    else:
                        info[key] = _wrapper_dict(
                            data[key], filter_keys
                        )
                else:
                    info[key] = data[key]
        return info
    except Exception as error:
        logging.exception(error)
        raise error
